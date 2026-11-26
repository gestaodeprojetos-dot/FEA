# FEA · Backups de páginas WordPress (eb.joaopithon.com.br)

Estado das páginas antes da edição via API REST de 26/11/2026 (task ClickUp 17th71zb1n0).

Rollback: enviar `meta._elementor_data` (e `title.raw`, no caso da 208) do JSON para `POST /wp-json/wp/v2/pages/{id}` e depois `DELETE /wp-json/elementor/v1/cache` (sem esse passo o Elementor continua servindo o HTML antigo do cache).
