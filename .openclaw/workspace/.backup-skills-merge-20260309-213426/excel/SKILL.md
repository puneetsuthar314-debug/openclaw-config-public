---
name: excel
description: "Complete Excel skill for reading, writing, editing, and generating professional spreadsheets. Covers technical implementation (pandas/openpyxl), financial modeling standards, visual design systems, and cross-platform compatibility. Use for any .xlsx, .xlsm, .csv, or .tsv file operations."
license: Proprietary. See LICENSE files for complete terms
---

# Excel — Complete Spreadsheet Skill

Comprehensive Excel skill combining technical implementation, financial modeling standards, and professional design systems.

---

## Part 1: When to Use

Use this skill whenever the user wants to:
- Open, read, edit, or fix existing .xlsx, .xlsm, .csv, or .tsv files
- Create new spreadsheets from scratch or from other data sources
- Convert between tabular file formats
- Clean or restructure messy tabular data into proper spreadsheets
- Generate professional Excel reports with charts and formatting

**Do NOT use** when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration.

---

## Part 2: Excel Fundamentals (Critical Knowledge)

### 2.1 Dates Are Serial Numbers
Excel stores dates as days since 1900-01-01 (Windows) or 1904-01-01 (Mac legacy). Time is fractional: 0.5 = noon, 0.25 = 6 AM.

### 2.2 The 1900 Leap Year Bug
Excel incorrectly treats 1900 as a leap year. Serial 60 represents Feb 29, 1900 (invalid date). Account for this when calculating dates before March 1, 1900.

### 2.3 15-Digit Precision Limit
Numbers beyond 15 digits silently truncate. Use TEXT format for: phone numbers, IDs, credit cards, any long numeric identifiers. Leading zeros also require TEXT.

### 2.4 Formulas vs Cached Values
Cells may contain both formula and cached result. Some readers return formula string, others return cached value. Force recalculation if cached values might be stale.

### 2.5 Merged Cells Are Traps
Only the top-left cell of a merged range holds the value. Reading other cells in the merge returns empty. Hidden rows/columns still contain data.

### 2.6 Format Limits
| Format | Rows | Columns | Notes |
|--------|------|---------|-------|
| XLSX | 1,048,576 | 16,384 (XFD) | Modern default |
| XLS | 65,536 | 256 | Legacy, avoid |
| CSV | Unlimited | Unlimited | No formatting |

---

## Part 3: Technical Implementation

### 3.1 Library Selection

| Library | Best For |
|---------|----------|
| **pandas** | Data analysis, bulk operations, simple export |
| **openpyxl** | Complex formatting, formulas, Excel-specific features |

### 3.2 Reading Excel Files

```python
import pandas as pd
from openpyxl import load_workbook

# Using pandas (data analysis)
df = pd.read_excel('file.xlsx')  # First sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets

# Using openpyxl (preserve formulas/formatting)
wb = load_workbook('file.xlsx')  # Formulas preserved
wb = load_workbook('file.xlsx', data_only=True)  # Cached values only
```

### 3.3 Creating Excel Files

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active

# Add data
ws['A1'] = 'Hello'
ws['B1'] = 'World'

# Add formula (CRITICAL: use formulas, not hardcoded calculations)
ws['B2'] = '=SUM(A1:A10)'

# Formatting
ws['A1'].font = Font(bold=True, color='FF0000')
ws['A1'].fill = PatternFill('solid', start_color='FFFF00')

# Column width
ws.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 3.4 CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python.** This ensures the spreadsheet remains dynamic.

#### ❌ WRONG - Hardcoding Calculated Values
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15
```

#### ✅ CORRECT - Using Excel Formulas
```python
# Good: Let Excel calculate
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'
```

### 3.5 Formula Recalculation (MANDATORY)

Excel files created/modified by openpyxl contain formulas as strings but not calculated values. Use LibreOffice to recalculate:

```bash
python scripts/recalc.py output.xlsx
```

The script:
- Automatically sets up LibreOffice macro on first run
- Recalculates all formulas in all sheets
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
- Returns JSON with detailed error locations

### 3.6 Formula Verification Checklist

- [ ] Test 2-3 sample references before building full model
- [ ] Verify column mapping (column 64 = BL, not BK)
- [ ] Check row offset (Excel rows are 1-indexed)
- [ ] Handle NaN values with `pd.notna()`
- [ ] Check for division by zero (#DIV/0!)
- [ ] Verify all cell references exist (#REF!)
- [ ] Use correct cross-sheet format (Sheet1!A1)

---

## Part 4: Financial Modeling Standards

### 4.1 Color Coding Standards

| Color | RGB | Use |
|-------|-----|-----|
| **Blue** | 0,0,255 | Hardcoded inputs, scenario variables |
| **Black** | 0,0,0 | ALL formulas and calculations |
| **Green** | 0,128,0 | Links to other worksheets |
| **Red** | 255,0,0 | External links to other files |
| **Yellow BG** | 255,255,0 | Key assumptions needing attention |

### 4.2 Number Formatting Standards

| Data Type | Format Code | Example |
|-----------|-------------|---------|
| Years | Text string | "2024" (not "2,024") |
| Currency | $#,##0 | $1,234 (specify units: "Revenue ($mm)") |
| Zeros | $#,##0;($#,##0);- | Display as "-" |
| Percentages | 0.0% | 12.3% |
| Multiples | 0.0x | 15.2x (EV/EBITDA) |
| Negative | Parentheses | (123) not -123 |

### 4.3 Documentation Requirements

For hardcoded values, add comments:
```
Source: Company 10-K, FY2024, Page 45, [SEC EDGAR URL]
Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity
```

---

## Part 5: Professional Design System

### 5.1 Theme System

Choose ONE theme per workbook. All visual elements derive from the theme color.

| Theme | Primary | Use Case |
|-------|---------|----------|
| **Elegant Black** | 2D2D2D | Luxury, fashion, premium (recommended default) |
| Corporate Blue | 1F4E79 | Finance, corporate |
| Forest Green | 2E5A4C | Sustainability, environmental |
| Navy | 1E3A5F | Government, institutional |
| Slate Gray | 4A5568 | Tech, modern, minimalist |

### 5.2 Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Document title | Serif | 18-22 | Bold, Primary color |
| Section header | Serif | 12-14 | Bold, Primary color |
| Table header | Serif | 10-11 | Bold, White |
| Data cells | Sans-Serif | 11 | Regular, Black |
| Notes | Sans-Serif | 9-10 | Italic, #666666 |

**Recommended fonts:**
- Serif: Source Serif Pro (or Georgia fallback)
- Sans-Serif: Source Sans Pro (or Calibri fallback)

### 5.3 Layout Rules

| Element | Position |
|---------|----------|
| Left margin | Column A empty (width 3) |
| Top margin | Row 1 empty |
| Content start | Cell B2 |
| Section spacing | 1 empty row |
| Table spacing | 2 empty rows |

### 5.4 Border System (Horizontal-Only Style)

Each Data Block must have:
- **Outer frame**: All 4 sides (thin, #D1D1D1)
- **Header bottom**: Medium weight, theme primary color
- **Internal horizontal**: Thin, between all rows
- **Internal vertical**: None (omit for cleaner look)

### 5.5 Row Heights

| Row Type | Height |
|----------|--------|
| Document title | 35 |
| Section header | 25 |
| Table header | 30 |
| Standard data | 18 |
| Wrapped text | lines × 15 + 10 |

### 5.6 Data Visualization

**Data Bars:**
```python
from openpyxl.formatting.rule import DataBarRule
rule = DataBarRule(start_type='min', end_type='max', color=THEME['primary'])
ws.conditional_formatting.add('C5:C50', rule)
```

**Color Scale:**
```python
from openpyxl.formatting.rule import ColorScaleRule
rule = ColorScaleRule(start_type='min', start_color='FFFFFF', end_type='max', end_color=THEME['primary'])
ws.conditional_formatting.add('D5:D50', rule)
```

**Charts:**
```python
from openpyxl.chart import BarChart, Reference
chart = BarChart()
chart.title = "Revenue by Region"
data = Reference(ws, min_col=3, min_row=4, max_row=10)
cats = Reference(ws, min_col=2, min_row=5, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "F5")
```

---

## Part 6: User Experience Features

### 6.1 Navigation
For files with 3+ sheets, include Sheet Index with hyperlinks:
```python
cell.hyperlink = "#'Data'!A1"
cell.font = Font(color=THEME['accent'], underline='single')
```

### 6.2 Freeze Panes
For tables with >10 rows:
```python
ws.freeze_panes = 'B5'  # Freeze below header row
```

### 6.3 Filters
For tables with >20 rows:
```python
ws.auto_filter.ref = f"B4:{get_column_letter(last_col)}{last_row}"
```

### 6.4 Key Insights Section
For analytical reports, add explicit insights:
```python
ws['B20'] = "KEY INSIGHTS"
insights = [
    "• Revenue grew 23% YoY, driven by APAC expansion",
    "• Top 3 customers account for 45% of total revenue"
]
```

---

## Part 7: Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Numbers stored as text | Explicit type conversion needed |
| Column index confusion | A=0 or A=1 varies by library—verify |
| Newlines in cells | Need "wrap text" format to display |
| External references | Break when source file moves |
| Password protection | Trivial to break—encrypt externally |
| Large files (>100K rows) | Use streaming readers |
| Empty rows at end | May be padded by some writers |

---

## Part 8: Best Practices

### 8.1 Before Saving
- [ ] All numeric cells have `number_format` set
- [ ] Same column = same precision
- [ ] Formula cells have explicit formats (no default)
- [ ] Data source and time range documented
- [ ] Generation date in footer
- [ ] Zero formula errors (#REF!, #DIV/0!, etc.)

### 8.2 Code Style
- Write minimal, concise Python code
- Avoid verbose variable names
- Avoid unnecessary print statements
- Add comments to cells with complex formulas
- Document data sources for hardcoded values

### 8.3 Security & Privacy
- All file processing happens locally
- No external services called
- XLSM files contain macros (security risk)
- Password protection is not real security

---

## Quick Reference

| Task | Tool | Command |
|------|------|---------|
| Read data | pandas | `pd.read_excel('file.xlsx')` |
| Read with formulas | openpyxl | `load_workbook('file.xlsx')` |
| Create new | openpyxl | `Workbook()` |
| Add formula | openpyxl | `ws['A1'] = '=SUM(B2:B10)'` |
| Recalculate | LibreOffice | `python scripts/recalc.py file.xlsx` |
| Add chart | openpyxl | `BarChart()`, `ws.add_chart()` |
| Conditional formatting | openpyxl | `DataBarRule()`, `ColorScaleRule()` |

---

*This skill combines xlsx, excel-xlsx, and excel-generator into one comprehensive Excel skill.*
