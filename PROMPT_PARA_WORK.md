# Prompt para o Work — revisão e atualização científica

## Objetivo

Atualize a revisão científica da biblioteca sobre procedimentos percutâneos guiados por ultrassonografia para fasciopatia plantar proximal. Consulte os dados, notas e relatório preliminar já versionados neste projeto. Execute as etapas 1 a 5 abaixo e entregue um pacote estruturado para importação. Trate os arquivos existentes como evidência preliminar: confira as fontes originais antes de aceitar resultados ou associações.

## Classificação canônica — versão 2.0

- A1 — Injeção de corticoide.
- A1.b — Infiltração ecoguiada por plano, especialmente perifascial ou profundo à fáscia; subtipo técnico de A1, associado à injeção de corticoide. Registre o plano separadamente da substância. Plano, sem confirmação de corticoide, não basta para classificar como A1.b.
- A2 — Proloterapia com dextrose hipertônica.
- A3 — Injeção de ácido hialurônico.
- A4 — Injeção de plasma rico em plaquetas (PRP).
- B1 — Fenestração com agulha, sem secção fascial contínua intencional.
- B2 — Fasciotomia percutânea com agulha convencional.
- C1 — Fenestração + sangue autólogo.
- C2 — Fasciotomia percutânea + PRP.
- D1 — Bloqueio ecoguiado do nervo tibial.

Apresente A sempre nesta ordem: A1, A1.b, A2, A3, A4. Preserve os significados de B1, B2, C1, C2 e D1. Não crie modalidades novas; registre possibilidades em CANDIDATOS.md.

Associe publicações e achados pelo procedimento e substância descritos, não apenas por código recebido. Se a fonte não permitir decidir, deixe a modalidade canônica vazia, conserve o código original em campo separado e explique a pendência. Não transforme propostas arquivadas em fichas aprovadas.

## 1. Busca reproduzível

Amplie e documente buscas em PubMed/MEDLINE, PMC quando disponível, páginas oficiais de periódicos, Crossref e fontes oficiais de pôsteres/suplementos. Registre para cada fonte a consulta exata, data, limites, resultados, deduplicação, triagem, inclusão/exclusão e razões. Priorize fontes primárias. Busque especialmente evidências para C1, C2, A3 recente e fasciotomia com agulha 14G. Ausência de achados nesta busca não prova inexistência de evidência.

## 2. Identidade e acesso das publicações

Mantenha os IDs ART001–ART009; novos registros começam em ART010 e não podem duplicar DOI/PMID. Confira título, autores, ano, periódico, identificadores e URL oficial.

- ART005 e ART006: procure texto integral acessível; se só o resumo estiver disponível, declare isso.
- ART007: confira texto e suplementos S3, S5 e S6. Não presuma qual substância foi injetada; a associação A1.b exige confirmação de corticoide.
- ART008: confira o pôster ECR e só associe A1 se a injeção de corticoide estiver descrita.
- ART009: tente identificar a publicação candidata de 14G. Se não confirmar identidade, autores e título, mantenha-a pendente e não invente dados.

Não contorne paywalls, DRM, páginas bloqueadas ou outras restrições. Registre tentativas e limitações de acesso.

## 3. Auditoria dos dados

Confira nos textos, tabelas e figuras os protocolos, amostras, desfechos, denominadores, seguimento, efeitos adversos, perdas, cointervenções e datas. Para cada informação técnica ou quantitativa, registre página, seção, tabela ou figura e estado de conferência.

Priorize as inconsistências já sinalizadas: valores de FAOS de ART003 e FADI basal de ART004. Em ART004, corticoide após a liberação é cointervenção do procedimento B2; não o classifique automaticamente como A1 independente. Distinga concentração inicial da concentração final em misturas. Não chame variação média de escala de dor de taxa de sucesso.

Para taxa de sucesso, informe definição dos autores, numerador/denominador, período de acompanhamento e referência. Use “Não informado” se a fonte não trouxer o dado e “Não avaliado no texto completo” se o texto integral não tiver sido consultado. Avalie risco de viés com ferramenta adequada ao desenho, sem inferir causalidade em séries não controladas.

## 4. Propostas de fichas

Produza propostas Markdown para A1.md, A1b.md, A2.md, A3.md, A4.md, B1.md, B2.md, C1.md, C2.md e D1.md. São sugestões para revisão e não devem ser descritas como aprovadas.

Para cada modalidade, inclua, se disponível: princípio, indicações estudadas, agulha/calibre, acesso, orientação, plano, substância, dose/concentração/volume, sessões/intervalo, técnica, resultados quantitativos, critério de sucesso, seguimento, complicações, limitações, risco de viés, referências com DOI/PMID e links, figuras/vídeos com origem e notas dos artigos. Use tabelas quando protocolos variarem. Não invente síntese para modalidade sem estudo confirmado; descreva a lacuna.

## 5. Busca e direitos das mídias

Para cada figura/vídeo, registre artigo, identificação, página, legenda, URL oficial, acesso, licença e restrições. Não baixe mídia sem acesso e uso autorizados, não remova créditos e não suponha que acesso público autorize republicação. Se o acesso falhar, mantenha o link e o motivo; não crie arquivos fictícios.

## Entrega

Entregue `work_export.zip` com:

- `manifest.json`: formato 1.0, classificação 2.0, data real, arquivos incluídos e SHA-256 quando possível;
- `RELATORIO.md`: método, consultas, datas, contagens, síntese, conflitos, limitações e pendências;
- `dados/artigos.csv`, `protocolos.csv`, `achados.csv`, `midias.csv`;
- `propostas/A1.md`, `A1b.md`, `A2.md`, `A3.md`, `A4.md`, `B1.md`, `B2.md`, `C1.md`, `C2.md`, `D1.md`;
- `notas/ART-ID.md` para cada publicação;
- `arquivos/pdfs/`, `figuras/` e `videos/` somente para arquivos que possam ser incluídos legalmente.

Use os cabeçalhos do pacote anterior para compatibilidade; pode acrescentar campos, sem remover os existentes. Em especial, preserve códigos recebidos separadamente das modalidades canônicas quando houver divergência. Use UTF-8. Valide o manifesto e os hashes antes da entrega. Liste claramente tudo que permaneceu sem confirmação.
