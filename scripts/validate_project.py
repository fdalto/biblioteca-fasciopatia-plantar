#!/usr/bin/env python3
"""Valida a estrutura mínima, ordem e cabeçalhos CSV da biblioteca."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "A1-corticoide", "A2-proloterapia", "A3-acido-hialuronico", "A4-PRP",
    "B1-fenestracao", "B2-fasciotomia-agulha", "C1-fenestracao-sangue", "C2-fasciotomia-PRP", "D1-bloqueio-tibial",
]
HEADERS = {
    "artigos.csv": ["id", "doi", "pmid", "titulo", "autores", "ano", "revista", "desenho", "url", "pdf", "pdf_url", "licenca", "modalidades", "modalidades_recebidas", "status_triagem", "status_texto_completo", "motivo_exclusao"],
    "protocolos.csv": ["id_artigo", "grupo_tratamento", "modalidade", "modalidade_recebida", "pacientes", "tipo_agulha", "calibre", "acesso", "orientacao", "plano", "substancia", "dose", "concentracao", "volume", "sessoes", "intervalo", "origem"],
    "achados.csv": ["id_artigo", "modalidade", "modalidade_recebida", "grupo_tratamento", "desfecho", "valor", "unidade", "momento", "definicao_sucesso", "denominador", "origem", "status_conferencia"],
    "midias.csv": ["id_artigo", "modalidades", "tipo_midia", "identificacao", "pagina", "url_original", "caminho_local", "legenda", "licenca", "status"],
}

def main() -> int:
    errors = []
    proc = ROOT / "procedimentos"
    for name in EXPECTED:
        p = proc / name
        for component in ("artigos", "figuras", "videos", "notas"):
            if not (p / component).is_dir(): errors.append(f"Pasta ausente: procedimentos/{name}/{component}")
        if not (p / "README.md").is_file(): errors.append(f"README ausente: procedimentos/{name}/README.md")
    a1b = proc / "A1-corticoide" / "A1b-infiltracao-por-plano"
    for component in ("artigos", "figuras", "videos", "notas"):
        if not (a1b / component).is_dir(): errors.append(f"Pasta ausente: {a1b.relative_to(ROOT)}/{component}")
    if not (a1b / "README.md").is_file(): errors.append("README ausente para A1.b")
    for name, required in HEADERS.items():
        path = ROOT / "dados" / name
        try:
            with path.open(encoding="utf-8-sig", newline="") as f: got = next(csv.reader(f), [])
            if not set(required).issubset(got): errors.append(f"Cabeçalhos ausentes em dados/{name}: {sorted(set(required)-set(got))}")
        except OSError: errors.append(f"CSV ausente: dados/{name}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ordered = ["A1", "A1.b", "A2", "A3", "A4"]
    positions = [readme.index(f"| {code} |") if f"| {code} |" in readme else -1 for code in ordered]
    if positions != sorted(positions) or min(positions) < 0: errors.append("Classificação A fora da ordem canônica no README")
    if errors:
        print("\n".join(f"ERRO: {e}" for e in errors)); return 1
    print("Estrutura e cabeçalhos válidos."); return 0

if __name__ == "__main__": sys.exit(main())
