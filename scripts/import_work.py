#!/usr/bin/env python3
"""Importa pacotes Work com associação de modalidades revisável e segura."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "dados" / "modalidades.json").read_text(encoding="utf-8"))["modalidades"]
INBOX = ROOT / "_work" / "inbox"
PROCESSED = ROOT / "_work" / "processed"
REJECTED = ROOT / "_work" / "rejected"
ORDER = ["A1", "A1.b", "A2", "A3", "A4", "B1", "B2", "C1", "C2", "D1"]
SCHEMAS = {
    "artigos.csv": ["id", "doi", "pmid", "titulo", "autores", "ano", "revista", "desenho", "url", "pdf", "pdf_url", "licenca", "modalidades", "status_triagem", "status_texto_completo", "motivo_exclusao"],
    "protocolos.csv": ["id_artigo", "grupo_tratamento", "modalidade", "modalidade_recebida", "pacientes", "tipo_agulha", "calibre", "acesso", "orientacao", "plano", "substancia", "dose", "concentracao", "volume", "sessoes", "intervalo", "origem"],
    "achados.csv": ["id_artigo", "modalidade", "modalidade_recebida", "grupo_tratamento", "desfecho", "valor", "unidade", "momento", "definicao_sucesso", "denominador", "origem", "status_conferencia"],
    "midias.csv": ["id_artigo", "modalidades", "tipo_midia", "identificacao", "pagina", "url_original", "caminho_local", "legenda", "licenca", "status"],
}
ALIASES = {
    "artigos.csv": {"article_id": "id"},
    "protocolos.csv": {"article_id": "id_artigo", "grupo": "grupo_tratamento", "n_pacientes": "pacientes", "agulha_tipo": "tipo_agulha", "agulha_calibre": "calibre", "via_acesso": "acesso", "volume_ml": "volume", "fonte_localizacao": "origem"},
    "achados.csv": {"article_id": "id_artigo", "grupo": "grupo_tratamento", "seguimento": "momento", "fonte_localizacao": "origem", "status_verificacao": "status_conferencia"},
    "midias.csv": {"article_id": "id_artigo", "tipo": "tipo_midia", "identificador": "identificacao", "url_origem": "url_original"},
}

def norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def modality_for(text: str) -> str | None:
    """Resolve por procedimento/substância explícitos, nunca por A2/A3/A4 legado."""
    t = norm(text)
    has_steroid = any(term in t for term in ("corticoide", "corticosteroide", "corticosteroid", "steroid", "betametasona", "methylprednisolone", "metilprednisolona", "dexametasona", "triamcinolona", "cortisona"))
    has_target_plan = any(norm(term) in t for term in ("infiltracao por plano", "infiltracao ecoguiada dirigida", "perifascial", "plano profundo da fascia", "profundo e", "profunda e", "superficial a fascia", "profundo a fascia"))
    if has_steroid and has_target_plan:
        return "A1.b"
    if any(norm(x) in t for x in ("fasciotomia prp", "fasciotomy prp", "fasciotomia percutanea com prp")):
        return "C2"
    if any(norm(x) in t for x in ("fenestracao sangue", "fenestration blood", "sangue autologo")) and any(norm(x) in t for x in ("fenestracao", "fenestration")):
        return "C1"
    rules = [
        ("A4", ("prp", "plasma rico em plaquetas", "platelet rich plasma")),
        ("A3", ("acido hialuronico", "hyaluronic acid")),
        ("A2", ("dextrose", "proloterapia", "prolotherapy")),
        ("A1", ("corticoide", "corticosteroide", "corticosteroid", "steroid")),
        ("B2", ("fasciotomia", "fasciotomy")),
        ("B1", ("fenestracao", "multipunctura", "dry needling", "peppering", "multiple punctures")),
        ("D1", ("bloqueio tibial", "tibial nerve block", "nervo tibial")),
    ]
    for code, terms in rules:
        if any(norm(term) in t for term in terms):
            return code
    # Códigos isolados do formato corrigido são aceitos. A1b é normalizado para A1.b.
    m = re.search(r"(?<![A-Z0-9])(A1\.b|A1b|A[1-4]|B[12]|C[12]|D1)(?![A-Z0-9])", str(text), re.I)
    if m:
        code = m.group(1).upper()
        if code in {"A1.B", "A1B"}: code = "A1.b"
        return code
    return None

def article_modalities(row: dict[str, str]) -> list[str]:
    """Extrai todas as modalidades citadas; artigos podem avaliar mais de uma."""
    text = norm(" ".join(str(row.get(k, "")) for k in ("modalidades", "titulo", "grupo_tratamento")))
    found = []
    if any(norm(term) in text for term in ("fasciotomia prp", "fasciotomy prp", "fasciotomia percutanea com prp")):
        found.append("C2")
    if any(norm(term) in text for term in ("fenestracao sangue", "fenestration blood", "sangue autologo")) and any(norm(term) in text for term in ("fenestracao", "fenestration")):
        found.append("C1")
    steroid_terms = ("corticoide", "corticosteroide", "corticosteroid", "steroid", "betametasona", "methylprednisolone", "metilprednisolona", "dexametasona", "triamcinolona", "cortisona")
    plan_terms = ("perifascial", "infiltracao por plano", "plano profundo da fascia", "infiltracao ecoguiada dirigida", "profundo e", "profunda e", "superficial a fascia", "profundo a fascia")
    has_steroid = any(norm(term) in text for term in steroid_terms)
    if has_steroid and any(norm(term) in text for term in plan_terms): found.append("A1.b")
    for code, terms in (("A1", steroid_terms),
                        ("A2", ("dextrose", "proloterapia", "prolotherapy")),
                        ("A3", ("acido hialuronico", "hyaluronic acid")),
                        ("A4", ("prp", "plasma rico em plaquetas", "platelet rich plasma")),
                        ("B2", ("fasciotomia", "fasciotomy", "needle release", "fascia release", "needle fasciotomy")),
                        ("B1", ("multipunctura", "multiple puncture", "multiple punctures")),
                        ("D1", ("bloqueio tibial", "tibial nerve block", "nervo tibial"))):
        if any(norm(term) in text for term in terms): found.append(code)
    return [code for code in REGISTRY if code in dict.fromkeys(found)]

def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def canonicalize_table(src: Path, name: str, report: list[str]) -> Path:
    """Renomeia cabeçalhos do contrato exportado para o esquema local no diretório temporário."""
    rows = csv_rows(src)
    aliases = ALIASES[name]
    normalized = []
    for line, row in enumerate(rows, 2):
        item = dict(row)
        for old, new in aliases.items():
            if old in item:
                if new in item and item[new] and item[old] and item[new] != item[old]:
                    report.append(f"Conflito de campos em {name}, linha {line}: {old} e {new}; mantido {new}.")
                elif new not in item or not item[new]:
                    item[new] = item[old]
                del item[old]
        if name in {"protocolos.csv", "achados.csv"}:
            item.setdefault("modalidade_recebida", item.get("modalidade", ""))
        if name == "midias.csv": item.setdefault("modalidades", "")
        normalized.append(item)
    headers = list(dict.fromkeys(list(rows[0].keys() if rows else []) + list(aliases.values())))
    headers = [aliases.get(h, h) for h in headers]
    if name == "midias.csv" and "modalidades" not in headers: headers.insert(1, "modalidades")
    if name == "artigos.csv" and "modalidades_recebidas" not in headers: headers.append("modalidades_recebidas")
    # Include current schema fields plus any harmless source-specific columns.
    headers = list(dict.fromkeys(headers + SCHEMAS[name]))
    target = src.parent / f".canonical-{name}"
    write_rows(target, headers, normalized)
    return target

def write_rows(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def merge_table(src: Path, dest: Path, report: list[str]) -> None:
    incoming = csv_rows(src)
    if not incoming:
        return
    header = list(incoming[0])
    if dest.name == "midias.csv" and "modalidades" not in header:
        # Compatibilidade com exports anteriores, que não associavam mídia a modalidades.
        header.insert(1, "modalidades")
    if not header:
        return
    key = next((k for k in ("id", "id_artigo") if k in header), header[0])
    existing = csv_rows(dest) if dest.exists() else []
    seen = {r.get(key, "").strip(): r for r in existing if r.get(key, "").strip()}
    article_codes = {}
    article_table = ROOT / "dados" / "artigos.csv"
    if dest.name == "midias.csv" and article_table.exists():
        article_codes = {r.get("id", "").strip(): r.get("modalidades", "") for r in csv_rows(article_table)}
    # Artigos têm identificador único; protocolos/achados/mídias podem ter várias linhas por ID.
    for i, row in enumerate(incoming, 1):
        if dest.name == "midias.csv":
            row.setdefault("modalidades", article_codes.get(row.get("id_artigo", "").strip(), ""))
        code_field = "modalidades" if "modalidades" in row else "modalidade" if "modalidade" in row else None
        evidence = " ".join(str(row.get(k, "")) for k in ("modalidade", "substancia", "grupo_tratamento", "titulo", "plano", "desfecho"))
        semantic = modality_for(evidence)
        if code_field:
            if dest.name == "artigos.csv":
                resolved = article_modalities(row)
            else:
                tokens = re.split(r"[;,|]+", row.get(code_field, ""))
                resolved = [modality_for(x) for x in tokens if x.strip()]
                resolved = [x for x in resolved if x]
                # A substância/procedimento explícito prevalece sobre código A antigo.
                code_only = row.get(code_field, "").strip().upper()
                if semantic and code_only not in {"C1", "C2", "B1", "B2", "D1"}:
                    if resolved and semantic not in resolved:
                        report.append(f"Divergência em {src.name}, linha {i}: código(s) {row[code_field]!r} conflita(m) com procedimento/substância ({semantic}); associação semântica aplicada.")
                    resolved = [semantic]
            if resolved:
                row[code_field] = ";".join(dict.fromkeys(resolved))
            elif row.get(code_field, "").strip():
                report.append(f"Modalidade não resolvida em {src.name}, linha {i}: {row[code_field]!r}; mantida para revisão.")
        row_key = row.get(key, "").strip()
        if not row_key:
            report.append(f"Sem identificador {key} em {src.name}, linha {i}; linha ignorada."); continue
        if key == "id" and dest.name == "artigos.csv" and row_key in seen:
            # Não sobrescreve ficha já cadastrada; DOI/PMID iguais também geram alerta.
            prior = seen[row_key]
            if (row.get("doi") and prior.get("doi", "").lower() == row["doi"].lower()) or (row.get("pmid") and prior.get("pmid") == row["pmid"]):
                report.append(f"Artigo duplicado ({row_key}) em {src.name}; registro existente preservado.")
            else:
                report.append(f"ID de artigo já existe ({row_key}); registro existente preservado.")
            continue
        if dest.name == "artigos.csv":
            doi = row.get("doi", "").strip().lower()
            pmid = row.get("pmid", "").strip()
            duplicate = next((r for r in existing if (doi and r.get("doi", "").strip().lower() == doi) or (pmid and r.get("pmid", "").strip() == pmid)), None)
            if duplicate:
                report.append(f"Artigo {row_key} duplicado por DOI/PMID; registro canônico {duplicate.get('id', '')} preservado.")
                continue
        if key != "id" or dest.name != "artigos.csv":
            if row in existing:
                continue
        existing.append(row)
        if key == "id": seen[row_key] = row
    write_rows(dest, list(dict.fromkeys(header + (list(existing[0]) if existing else []))), existing)
    if dest.name == "artigos.csv":
        for row in incoming:
            art_id = row.get("id", "").strip()
            if not art_id: continue
            target = ROOT / "biblioteca" / art_id / "metadata.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            incoming_meta = dict(row)
            incoming_meta["classificacao"] = "2.0"
            incoming_meta["modalidades"] = article_modalities(row) or row.get("modalidades", "")
            if target.exists():
                current = json.loads(target.read_text(encoding="utf-8"))
                for k, v in incoming_meta.items():
                    if not current.get(k): current[k] = v
                    elif v and current[k] != v: report.append(f"Conflito JSON em biblioteca/{art_id}/metadata.json, campo {k}; valor existente preservado.")
                prior = current.get("modalidades", [])
                prior = prior if isinstance(prior, list) else re.split(r"[;,|]+", str(prior))
                added = incoming_meta["modalidades"] if isinstance(incoming_meta["modalidades"], list) else re.split(r"[;,|]+", str(incoming_meta["modalidades"]))
                current["modalidades"] = list(dict.fromkeys([x.strip() for x in prior + added if x.strip()]))
            else:
                current = incoming_meta
            target.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def safe_extract(zf: zipfile.ZipFile, target: Path) -> None:
    root = target.resolve()
    for info in zf.infolist():
        name = info.filename.replace("\\", "/")
        p = PurePosixPath(name)
        if p.is_absolute() or ".." in p.parts or (p.parts and ":" in p.parts[0]):
            raise ValueError(f"Caminho inseguro no ZIP: {info.filename}")
        out = (target / Path(*p.parts)).resolve()
        if root not in out.parents and out != root:
            raise ValueError(f"Caminho fora do pacote: {info.filename}")
    zf.extractall(target)

def process(package: Path) -> None:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp = ROOT / "_work" / f"tmp-{stamp}"
    report: list[str] = []
    try:
        with zipfile.ZipFile(package) as zf:
            bad = zf.testzip()
            if bad: raise ValueError(f"ZIP corrompido: {bad}")
            safe_extract(zf, temp)
        bundle = temp / "work_export"
        if not bundle.exists():
            # aceita arquivos diretamente na raiz do ZIP
            bundle = temp
        manifest_path = bundle / "manifest.json"
        if not manifest_path.is_file(): raise ValueError("manifest.json ausente")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if str(manifest.get("versao_classificacao", "")) not in {"", "2.0"}:
            report.append(f"Classificação do pacote é {manifest.get('versao_classificacao')}; associações serão conferidas semanticamente.")
        for entry in manifest.get("arquivos", []):
            rel = PurePosixPath(str(entry.get("caminho", "")))
            if rel.is_absolute() or ".." in rel.parts or not rel.parts:
                raise ValueError(f"Caminho inseguro no manifest: {entry.get('caminho')}")
            file_path = bundle / Path(*rel.parts)
            if not file_path.is_file(): raise ValueError(f"Arquivo do manifest ausente: {entry.get('caminho')}")
            expected_hash = entry.get("sha256")
            if expected_hash:
                digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if digest.lower() != str(expected_hash).lower(): raise ValueError(f"SHA-256 divergente: {entry.get('caminho')}")
        (bundle / "dados").mkdir(exist_ok=True)
        validated = []
        for name, header in SCHEMAS.items():
            src = bundle / "dados" / name
            if src.exists():
                with src.open(encoding="utf-8-sig", newline="") as f:
                    got = next(csv.reader(f), [])
                mapped = {ALIASES[name].get(h, h) for h in got}
                synthesized = {"pdf", "modalidades_recebidas", "modalidade_recebida"}
                if name == "midias.csv": synthesized.add("modalidades")
                required_header = [h for h in header if h not in synthesized]
                missing = [h for h in required_header if h not in mapped]
                if missing: raise ValueError(f"Cabeçalho inválido em {name}: faltam {missing}")
                validated.append((canonicalize_table(src, name, report), ROOT / "dados" / name))
        for src, dest in validated:
            if dest.name == "artigos.csv":
                # Preserve codes as received; derive canonical associations from article and protocol evidence.
                article_rows = csv_rows(src)
                protocol_src = next((s for s, d in validated if d.name == "protocolos.csv"), None)
                protocol_evidence: dict[str, list[str]] = {}
                if protocol_src:
                    for pr in csv_rows(protocol_src):
                        aid = pr.get("id_artigo", "").strip()
                        if aid:
                            group = norm(pr.get("grupo_tratamento", ""))
                            substance = pr.get("substancia", "")
                            after_release = any(norm(term) in norm(substance) for term in ("apos secao", "apos seccao", "depois da secao", "depois da seccao", "after release", "after section"))
                            if after_release and any(term in group for term in ("fasciotomia", "fasciotomy", "release")):
                                report.append(f"{aid}: corticoide/anestésico pós-liberação registrado como cointervenção no protocolo; modalidade principal B2 preservada.")
                                substance = ""
                            protocol_evidence.setdefault(aid, []).append(" ".join([pr.get("grupo_tratamento", ""), pr.get("modalidade", ""), substance, pr.get("plano", "")]))
                for row in article_rows:
                    received = row.get("modalidades", "")
                    row["modalidades_recebidas"] = received
                    evidence = " ".join([row.get("titulo", ""), *protocol_evidence.get(row.get("id", ""), [])])
                    resolved = article_modalities({**row, "titulo": evidence, "modalidades": ""})
                    row["modalidades"] = ";".join(resolved)
                    if received and not resolved:
                        report.append(f"Associação não confirmada para {row.get('id')}: códigos recebidos {received!r}, sem evidência semântica suficiente; modalidade canônica deixada vazia.")
                    elif received:
                        received_codes = [modality_for(c) for c in re.split(r"[;,|]+", received) if c.strip()]
                        received_codes = [c for c in received_codes if c]
                        if any(code not in resolved for code in received_codes):
                            report.append(f"Revisar associação de {row.get('id')}: recebidos {received!r}; semântica encontrada {','.join(resolved)}.")
                if article_rows:
                    write_rows(src, list(dict.fromkeys(list(article_rows[0].keys()) + SCHEMAS["artigos.csv"])), article_rows)
            merge_table(src, dest, report)
        notes_dir = bundle / "notas"
        if notes_dir.is_dir():
            for note in notes_dir.glob("*.md"):
                art_id = note.stem
                target = ROOT / "biblioteca" / art_id / "fontes.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    if target.read_bytes() != note.read_bytes():
                        report.append(f"Nota {art_id} já existe com conteúdo diferente; versão recebida arquivada sem sobrescrever.")
                else:
                    shutil.copy2(note, target)
        # Cria apontadores em cada pasta de modalidade; a nota canônica permanece única na biblioteca.
        folder_by_code = {
            "A1": "A1-corticoide", "A1.b": "A1-corticoide/A1b-infiltracao-por-plano",
            "A2": "A2-proloterapia", "A3": "A3-acido-hialuronico", "A4": "A4-PRP",
            "B1": "B1-fenestracao", "B2": "B2-fasciotomia-agulha", "C1": "C1-fenestracao-sangue",
            "C2": "C2-fasciotomia-PRP", "D1": "D1-bloqueio-tibial",
        }
        article_dest = ROOT / "dados" / "artigos.csv"
        if article_dest.exists():
            for row in csv_rows(article_dest):
                for code in re.split(r"[;,|]+", row.get("modalidades", "")):
                    code = code.strip()
                    if code not in folder_by_code: continue
                    art_id = row.get("id", "").strip()
                    note_target = ROOT / "procedimentos" / folder_by_code[code] / "notas" / f"{art_id}.md"
                    canonical_record = ROOT / "biblioteca" / art_id / "fontes.md"
                    if not canonical_record.exists(): canonical_record = ROOT / "biblioteca" / art_id / "metadata.json"
                    canonical = canonical_record.relative_to(note_target.parent).as_posix()
                    note_target.parent.mkdir(parents=True, exist_ok=True)
                    if not note_target.exists():
                        note_target.write_text(f"# {art_id} — Nota do artigo\n\n[Ver registro canônico]({canonical})\n", encoding="utf-8")
                    article_target = ROOT / "procedimentos" / folder_by_code[code] / "artigos" / f"{art_id}.md"
                    if not article_target.exists():
                        metadata = (ROOT / "biblioteca" / art_id / "metadata.json").relative_to(article_target.parent).as_posix()
                        doi = row.get("doi", "").strip()
                        doi_link = f"\n- DOI: [{doi}](https://doi.org/{doi})" if doi else ""
                        source_url = row.get("url", "").strip()
                        source_link = f"\n- Fonte: [{source_url}]({source_url})" if source_url else ""
                        title = row.get("titulo", "Não informado")
                        article_target.write_text(f"# {art_id} — {title}\n\n- Modalidade: {code}{doi_link}{source_link}\n- PDF local: Não incluído no pacote recebido.\n- [Nota canônica]({canonical}) · [Metadados]({metadata})\n", encoding="utf-8")
        props = bundle / "propostas"
        expected = ["A1.md", "A1b.md", "A2.md", "A3.md", "A4.md"]
        for name in expected:
            if not (props / name).exists(): report.append(f"Proposta opcional ausente: propostas/{name}")
        # Propostas e notas são arquivadas para revisão; não substituem fichas vigentes.
        destination = PROCESSED / f"{package.stem}-{stamp}"
        destination.mkdir(parents=True, exist_ok=False)
        shutil.copytree(bundle, destination / "work_export", dirs_exist_ok=True)
        report.insert(0, f"Pacote: {package.name}\nManifest: {json.dumps(manifest, ensure_ascii=False)}\nImportado em UTC: {datetime.now(timezone.utc).isoformat()}")
        (destination / "RELATORIO_IMPORTACAO.md").write_text("# Relatório de importação\n\n" + "\n".join(f"- {x}" for x in report) + "\n", encoding="utf-8")
        package.unlink()
        print(f"Importado: {destination.relative_to(ROOT)}")
    except Exception as exc:
        destination = REJECTED / f"{package.stem}-{stamp}"
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "RELATORIO_IMPORTACAO.md").write_text(f"# Pacote rejeitado\n\nArquivo: {package.name}\n\nErro: {exc}\n", encoding="utf-8")
        shutil.move(str(package), destination / package.name)
        print(f"Rejeitado: {destination.relative_to(ROOT)} — {exc}", file=sys.stderr)
    finally:
        shutil.rmtree(temp, ignore_errors=True)

def main() -> None:
    INBOX.mkdir(parents=True, exist_ok=True); PROCESSED.mkdir(parents=True, exist_ok=True); REJECTED.mkdir(parents=True, exist_ok=True)
    packages = sorted(INBOX.glob("*.zip"))
    if not packages:
        print(f"Nenhum ZIP encontrado em {INBOX}"); return
    for package in packages: process(package)

if __name__ == "__main__": main()
