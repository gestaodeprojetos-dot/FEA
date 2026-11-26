# FEA · Integração uazapi (WhatsApp)

Cliente Python sem dependências externas para a API da uazapi (contrato 2.6.9, docs.uazapi.com).

## Configuração (uma vez)

1. Copiar `.env.example` para `.env` nesta pasta (o `.env` já está no `.gitignore`).
2. Preencher `FEA_UAZAPI_URL` (Server URL da instância, no painel da uazapi) e `FEA_UAZAPI_TOKEN` (token da instância).
3. Testar: `python3 fea_uazapi.py status`

## Comandos

| Comando | O que faz | Mexe em algo? |
|---|---|---|
| `status` | Estado da instância (conectada, número) | Não |
| `limites` | Limites atuais de novas conversas | Não |
| `grupos [--busca X]` | Lista grupos com JID (ID do grupo, termina em `@g.us`) | Não |
| `verificar 11999990000 ...` | Confere se números têm WhatsApp | Não |
| `texto NUMERO "mensagem"` | Envia texto (`@arquivo.txt` lê de arquivo) | Só com `--enviar` |
| `midia NUMERO image/video/document/ptt ARQUIVO --legenda "..."` | Envia mídia (URL ou arquivo local) | Só com `--enviar` |
| `webhook [--url URL --eventos messages,connection]` | Mostra ou configura o webhook | Só com `--enviar` |
| `conectar [--telefone N]` | Gera QR code ou código de pareamento | Só com `--enviar` |
| `instancias` | Lista instâncias do servidor (exige admintoken) | Não |

## Marcar pessoas

`--mencionar` aceita nomes da agenda `FEA-contatos-equipe.json` (Keila, Gabi, Luca), números ou `all`.
O script coloca o `@número` no texto sozinho, que é o que faz o WhatsApp exibir a marcação.

```bash
python3 fea_uazapi.py texto 120363432442225090@g.us "Keila, o report do funil está encaminhado." --mencionar Keila --enviar
```

## Travas de segurança

- **Simulação por padrão:** envio e configuração só acontecem com `--enviar`; sem a flag, o script mostra o que faria.
- **Regra de escrita FEA:** texto com "pra"/"pro" ou em-dash é bloqueado (liberar só com `--forcar`).
- **Anti-loop no webhook:** mensagens enviadas pela própria API são ignoradas no webhook (`excludeMessages: wasSentByApi`).
- **Retry automático** em limite de requisições (HTTP 429/503), respeitando o `Retry-After` da API.
- Número sem DDI ganha `55` automaticamente; JIDs (`@g.us`, `@lid`, `@newsletter`) passam intactos.

## Uso como biblioteca

```python
from fea_uazapi import Uazapi
api = Uazapi()
api.enviar_texto("120363000000000000@g.us", "Bom dia, equipe.")
```
