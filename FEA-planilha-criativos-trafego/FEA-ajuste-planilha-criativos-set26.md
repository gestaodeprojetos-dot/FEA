# FEA · Ajuste da planilha "Criativos para Tráfego" (set/26)

Reorganização das abas por **mês de início da captação**, não mais por mês do evento.

Arquivo de origem no Drive: `Criativos para Tráfego.xlsx`
(ID `1Uj9doFiSNDTOn9z3weT83NdQHvEB-y3e`, pasta `4. TRÁFEGO`).
Arquivo gerado: `FEA-Criativos-para-Trafego-v2.xlsx`.

## O que mudou

| Aba | Antes | Depois |
|-----|-------|--------|
| Setembro26 | IFF+10 (14, 15 e 23/09) | Elite Injector Congress 11/26 sob o dia 01/09, MTI sob o dia 07/09, IFF+10 mantido nos dias originais |
| Novembro26 | Elite Injector Congress + um dia solto de 31/10 | Só o calendário de 01/11 a 30/11, sem campanha |

### Elite Injector Congress 11/26
Bloco inteiro movido para Setembro26 porque a captação começou em 01/09/2026.
Fases mantidas: Captação, Lembrete, Antecipação, Vendas, RMKT, com os mesmos
links de legenda e de criativos que já existiam. A linha sem fase preenchida
(status e campanha apenas) foi descartada.

### MTI · Masterclass em Intercorrências
Bloco novo em Setembro26 sob o dia 07/09/2026, mesma estrutura de colunas, com
os links já existentes no Drive:

| Fase | Legenda | Criativos |
|------|---------|-----------|
| Captação | 1. COPY > 1. CRIATIVOS | 4. TRÁFEGO > CRIATIVOS PRONTOS > 1. CAPTAÇÃO > CAPTAÇÃO |
| Lembrete | idem | ... > LEMBRETE |
| Antecipação | idem | ... > ANTECIPAÇÃO |
| Vendas | idem | pasta ainda não existe no Drive |
| RMKT | idem | ... > REMARKETING |

Links úteis da coluna H: IFF+10 (já existia), Elite Injector Congress (veio junto
de Novembro) e Masterclass em Intercorrências (adicionado).

## Premissas a confirmar

1. **Deadline dos dois blocos** ficou igual à data de início da captação
   (01/09 para o Elite, 07/09 para a MTI). No original, todas as linhas do Elite
   tinham 31/10, que era só o ponto onde o bloco estava estacionado na aba de
   novembro. Se cada fase tem deadline próprio, é ajuste de uma coluna.
2. **Pasta de criativos de Vendas da MTI** não existe no Drive, a célula ficou
   com o rótulo "VENDAS (pasta a criar)" e sem link.

## Como aplicar no Drive

Manter o mesmo ID do arquivo (o atalho na pasta `4. TRÁFEGO` e os links já
distribuídos continuam funcionando): clicar com o botão direito no arquivo no
Drive, `Gerenciar versões` > `Fazer upload de nova versão`, e subir o
`FEA-Criativos-para-Trafego-v2.xlsx`.

## Como reproduzir

```bash
pip install openpyxl
python3 fea_ajusta_planilha.py   # espera orig.xlsx na mesma pasta
```
