# Esquemas dos dados

Os códigos canônicos estão em [modalidades.json](modalidades.json). Valores associados a modalidades devem seguir essa classificação. Os campos `modalidade_recebida` e `modalidades_recebidas` preservam os códigos fornecidos pelo pacote de origem quando a associação semântica exige conferência; campo canônico vazio significa que o projeto não assumiu uma modalidade.

## Tabelas

- `artigos.csv`: identidade bibliográfica, DOI/PMID, URLs, estado da triagem e modalidades canônicas e recebidas. `pdf` guarda caminho local; `pdf_url` mantém uma URL de PDF fornecida pela fonte.
- `protocolos.csv`: grupo de tratamento e detalhes técnicos. `origem` registra página, seção ou localização do dado. `modalidade_recebida` preserva o rótulo vindo da exportação.
- `achados.csv`: desfechos, unidade, seguimento, definição de sucesso, denominador, origem e estado de conferência.
- `midias.csv`: modalidade associada, identificação, origem, caminho local, legenda, licença e status. URL sem arquivo local permanece apenas como link.

Todos os CSVs usam UTF-8. Os campos vazios indicam informação não fornecida ou associação ainda não confirmada; não devem ser preenchidos por inferência sem fonte.
