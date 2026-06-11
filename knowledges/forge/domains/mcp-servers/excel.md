---
name: excel
description: Excel file manipulation — read, write, create, and modify .xlsx workbooks without Microsoft Excel.
---
# Excel

- **Status**: installed
- **JSON key**: `excel`
- **Location**: agents/compass.json
- **Wrapper**: none
- **Command**: `uvx excel-mcp-server stdio`
- **Source**: Community (excel-mcp-server, 3.8k stars)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `read_data_from_excel` | Read cells/ranges |
| `write_data_to_excel` | Write cells/ranges |
| `create_workbook` | Create new .xlsx file |
| `list_sheets` | List worksheets |
| `create_chart` | Generate charts |
| `create_pivot_table` | Pivot tables |
| `format_cells` | Cell formatting |

## Auth

- None (local file access)

## Limitations

- .xlsx format only (not .xls)
- Primary file: `/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/Suivi-tresorie-perso/suivi-des-affaires.xlsx`
- No cloud sync — reads/writes local file only
