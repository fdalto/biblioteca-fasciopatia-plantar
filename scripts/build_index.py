#!/usr/bin/env python3
"""Gera índice navegável com ordenação canônica das modalidades."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [
    ("A1", "Injeção de corticoide", "A1-corticoide/README.md"),
    ("A1.b", "Infiltração ecoguiada dirigida por plano (subtipo de A1)", "A1-corticoide/A1b-infiltracao-por-plano/README.md"),
    ("A2", "Proloterapia com dextrose hipertônica", "A2-proloterapia/README.md"),
    ("A3", "Injeção de ácido hialurônico", "A3-acido-hialuronico/README.md"),
    ("A4", "Injeção de plasma rico em plaquetas (PRP)", "A4-PRP/README.md"),
    ("B1", "Fenestração com agulha", "B1-fenestracao/README.md"),
    ("B2", "Fasciotomia percutânea com agulha", "B2-fasciotomia-agulha/README.md"),
    ("C1", "Fenestração + sangue autólogo", "C1-fenestracao-sangue/README.md"),
    ("C2", "Fasciotomia + PRP", "C2-fasciotomia-PRP/README.md"),
    ("D1", "Bloqueio ecoguiado do nervo tibial", "D1-bloqueio-tibial/README.md"),
]

def main() -> None:
    rows = ["# Índice de procedimentos", "", "| Código | Modalidade | Ficha |", "|---|---|---|"]
    rows += [f"| {code} | {name} | [Abrir]({path}) |" for code, name, path in ITEMS]
    (ROOT / "INDICE_PROCEDIMENTOS.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("INDICE_PROCEDIMENTOS.md atualizado")

if __name__ == "__main__": main()
