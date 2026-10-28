# FEA: mapa do Drive de lançamentos (28/10/2026)

Drive compartilhado da FEA (raiz `0AHC_vBmb5PAsUk9PVA`).

## Onde ficam os lançamentos

| O quê | Caminho | ID |
|---|---|---|
| Lançamentos Brasil (hub) | 2. Produtos > FEP > 2. Lançamentos | `1JdU4O5Fuor6iwZV7fXUp78paOl61SXRD` |
| Brasil 2026 | ... > 2. Lançamentos > 2026 | `18ZDI9-zJwkiO7eCPyjJ-Og6gv5hLCFYH` |
| Brasil 2027 | ... > 2. Lançamentos > 2027 | `1QyO4YNjCBG67QxOErAHe1Tk7hLN7k509` |
| Lançamentos Latam | 8. Internacionalização > Lançamentos Latam | `1IE0KTDvQZzNlp6AYP0hegpQiAl80G-YA` |
| Latam 2026 | ... > Lançamentos Latam > 2026 | `1Z_9U4e8NMKsXCuKB7j_flfdGXJJULoZV` |
| Latam 2027 | ... > Lançamentos Latam > 2027 | `1UExMATSr81NrCGPqfuPRFqYsqcGxi3cS` |
| Planejamento anual | 1. Gestão FEA > 11. Planejamento Anual | `1EkcnPCNQUcY_PaFFcA2IH9YvQVIb0NgP` |
| Planilhas de links úteis | 1. Gestão FEA > 12. Planilhas de Links úteis lançamentos | `1AaK-Gmyntd1p4cABBbhJYNfE74yMmTeS` |
| Templates para lançamento | 1. Gestão FEA > 1. Gestão > Templates para lançamento | `10ZTHrgb4DjvDgm_2nMjsvVhLcQ0xnA4_` |

## Padrão de cada pasta de lançamento

Nome: `NN. NOME DO LANÇAMENTO MM/AA`, numerado pela ordem do ano (ex.: `01. MASTERCLASS TOXINA 01/27`).

Subpastas (modelo do FEA-MTB 11/26): `0. PLANEJAMENTO` · `1. COPY` · `2. ARTES` · `3. PESQUISA` · `4. TRÁFEGO` · `5. LOGO` · `6. PÁGINA DE VENDAS` · `7. URA + SMS` · `8. AUTOMAÇÃO`.

As subpastas são criadas quando o lançamento entra em produção (junto com a pasta do ClickUp, cerca de 45 dias antes da captação). Em 28/10/2026 já estão prontas: Masterclass Anatomia 12/26, Masterclass Toxina 01/27, Masterclass Preenchimento Labial 01/27 e Desafio Full Face Na Prática 02/27.

## Como mover pastas e arquivos

O conector do Google Drive do Claude cria e renomeia, mas **não move** dentro do Drive compartilhado (erro "The caller does not have permission", mesmo com papel de Administrador de conteúdo). Para mover, usar a API do Drive com o acesso do ambiente (`FEA_GDRIVE_CLIENT_ID`, `FEA_GDRIVE_CLIENT_SECRET`, `FEA_GDRIVE_REFRESH_TOKEN`), pelo `token()` e `chamar()` de `FEA-edicao-videos/fea_drive.py`: `PATCH files/{id}?supportsAllDrives=true&addParents={destino}&removeParents={origem}`. Mover não muda o ID nem quebra link.

Movidos em 28/10/2026:
- `Planejamento Anual FEA 2027` para 1. Gestão FEA > 11. Planejamento Anual.
- `Black Friday Total - Latam`, `IFF-5ML LATAM`, `FEBio Latam`, `FEB Latam` e `MBC Latam` para Lançamentos Latam > 2026.
- `Masterclass em Anatomia - 06/26` e `1. Masterclass em Biostimulador de Colágeno` para Lançamentos Brasil > 2026.
