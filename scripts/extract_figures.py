#!/usr/bin/env python3
"""Extrai imagens raster embutidas de PDFs usando PyMuPDF; não contorna controles."""
import argparse
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("Instale dependências com: python -m pip install -r requirements.txt") from exc
    args.output.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    count = 0
    for page_no, page in enumerate(doc, 1):
        for index, image in enumerate(page.get_images(full=True), 1):
            xref = image[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3: pix = fitz.Pixmap(fitz.csRGB, pix)
            pix.save(args.output / f"pagina-{page_no:03}-imagem-{index:02}.png")
            count += 1
    print(f"Imagens embutidas extraídas: {count}. Registre artigo, figura, página, legenda, licença e procedência em dados/midias.csv.")

if __name__ == "__main__": main()
