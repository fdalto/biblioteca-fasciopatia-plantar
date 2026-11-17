# Biblioteca Científica — Intervenções Ecoguiadas na Fasciopatia Plantar

Biblioteca local para organizar evidências sobre intervenções percutâneas guiadas por ultrassonografia na fasciopatia plantar proximal. As fichas contêm propostas científicas para revisão e links para as fontes; algumas lacunas ainda precisam de conferência.

## Procedimentos

### A — Injeções terapêuticas

| Código | Procedimento | Ficha |
|---|---|---|
| A1 | Injeção de corticoide | [A1 — Corticoide](procedimentos/A1-corticoide/README.md) |
| A1.b | Infiltração ecoguiada dirigida por plano, subtipo técnico de A1 | [A1.b — Infiltração por plano](procedimentos/A1-corticoide/A1b-infiltracao-por-plano/README.md) |
| A2 | Proloterapia com dextrose hipertônica | [A2 — Proloterapia](procedimentos/A2-proloterapia/README.md) |
| A3 | Injeção de ácido hialurônico | [A3 — Ácido hialurônico](procedimentos/A3-acido-hialuronico/README.md) |
| A4 | Injeção de plasma rico em plaquetas (PRP) | [A4 — PRP](procedimentos/A4-PRP/README.md) |

### B — Intervenções mecânicas

| Código | Procedimento | Ficha |
|---|---|---|
| B1 | Fenestração com agulha (*dry needling*, *multiple punctures*, *peppering*) | [B1 — Fenestração](procedimentos/B1-fenestracao/README.md) |
| B2 | Fasciotomia percutânea com agulha convencional | [B2 — Fasciotomia](procedimentos/B2-fasciotomia-agulha/README.md) |

### C — Procedimentos combinados

| Código | Procedimento | Ficha |
|---|---|---|
| C1 | Fenestração com agulha + sangue autólogo | [C1 — Fenestração + sangue](procedimentos/C1-fenestracao-sangue/README.md) |
| C2 | Fasciotomia percutânea com agulha + PRP | [C2 — Fasciotomia + PRP](procedimentos/C2-fasciotomia-PRP/README.md) |

### D — Bloqueios nervosos

| Código | Procedimento | Ficha |
|---|---|---|
| D1 | Bloqueio ecoguiado do nervo tibial | [D1 — Bloqueio tibial](procedimentos/D1-bloqueio-tibial/README.md) |

## Pesquisa para revisão médica

- [Técnicas e doses](_work/revisao-20261117/TECNICAS.md) · [Tabela de resultados](_work/revisao-20261117/RESULTADOS.md) · [Figuras e vídeos](_work/revisao-20261117/MIDIAS.md) · [Pendências e candidatos](_work/revisao-20261117/PENDENCIAS_E_CANDIDATOS.md)

## Navegação e dados

- [Referências](REFERENCIAS.md) · [Metodologia](METODOLOGIA.md) · [Candidatos a modalidades](CANDIDATOS.md)
- [Índice completo de procedimentos](INDICE_PROCEDIMENTOS.md)
- [Esquemas CSV e registro de modalidades](dados/README.md) · [Modelos](_modelos/) · [Importador do Work](scripts/import_work.py)
- [Prompt atualizado para o Work](PROMPT_PARA_WORK.md) · [Relatório de importação](_work/processed/work_export-20261116-221523/RELATORIO_IMPORTACAO.md)
- Última atualização da estrutura: 2026-11-16.

Os códigos A1, A1.b, A2, A3 e A4 são fixados por modalidade; o registro canônico está em [dados/modalidades.json](dados/modalidades.json). A1.b é um subtipo técnico de A1 e registra o plano de administração separadamente da substância. A ordem acima deve ser mantida em índices e relatórios.

## Publicação estática futura

Após a revisão e consolidação científica, esta mesma documentação Markdown poderá alimentar um site estático com MkDocs Material, menu lateral, pesquisa, imagens ampliáveis e referências clicáveis. Os arquivos-fonte continuarão sendo a versão principal; não manteremos cópias editoriais paralelas. A configuração de publicação será preparada quando a biblioteca estiver consolidada.

## Convenções de evidência

Não classifique evidência sem avaliação da fonte. Use “Não informado” quando o dado não constar na fonte e “Não avaliado no texto completo” quando o texto completo não tiver sido consultado. Taxas de sucesso devem incluir definição, denominador, acompanhamento e referência. Consulte [METODOLOGIA.md](METODOLOGIA.md) para os critérios.

## Uso rápido

Coloque `work_export.zip` em `_work/inbox/` e execute `python scripts/import_work.py`. Para validar a estrutura e os dados, execute `python scripts/validate_project.py`. Para reconstruir o índice, execute `python scripts/build_index.py`. Instale a dependência de extração com `python -m pip install -r requirements.txt`. Consulte [AGENTS.md](AGENTS.md) para as convenções permanentes.

