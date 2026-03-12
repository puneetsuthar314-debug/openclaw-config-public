---
name: data-analysis-unified
description: "A comprehensive data analysis skill that automatically analyzes structured data (CSV, Excel, JSON), generates statistical summaries, creates relevant visualizations, and provides insights without needing user guidance. Use when the user asks to analyze, summarize, visualize, or process any tabular data file."
allowed-tools: [shell, file]
---

# Unified Data Analysis

This Skill provides a powerful, unified capability to analyze structured data files. It automatically inspects the data, performs relevant statistical analyses, and generates appropriate visualizations without requiring step-by-step instructions from the user.

## ⚠️ CRITICAL BEHAVIOR: Proactive & Comprehensive Analysis

**Your primary directive is to be proactive. When the user provides a data file and asks for analysis, you MUST immediately perform a full, comprehensive analysis. DO NOT ask for clarification or offer options.**

- **DO NOT** ask what the user wants to do with the data.
- **DO NOT** offer a list of possible analyses or charts.
- **DO NOT** wait for user input before starting the analysis.

**IMMEDIATELY AND AUTOMATICALLY:**
1.  Inspect the data to understand its structure (column types, data formats).
2.  Run a comprehensive analysis tailored to the data's content.
3.  Generate ALL relevant visualizations.
4.  Present the complete findings, including summaries, statistics, and charts, in a single, thorough response.

✅ **Correct:** "I will analyze this data file now and provide a complete report." (Then immediately proceed with the analysis).

❌ **Incorrect:** "What would you like me to do with this CSV file?" or "I can create a summary, make a chart, or check for missing data. What would you prefer?"

## Supported Data Formats

This skill is optimized for the following structured data formats. Use the appropriate pandas function to read the data.

| Format | Read Function |
| :--- | :--- |
| CSV | `pd.read_csv('file.csv')` |
| Excel | `pd.read_excel('file.xlsx')` |
| JSON | `pd.read_json('file.json')` |

## Standard Analysis Workflow

Follow these steps to perform the analysis. The core logic should be executed within a single Python script.

1.  **Setup & Load**: Create a Python script. Import pandas, matplotlib, and seaborn. Set matplotlib to 'Agg' mode for a headless environment and configure fonts for broad character support.
2.  **Data Inspection**: Load the data into a pandas DataFrame. Identify column types (numeric, categorical, datetime), and check for missing values.
3.  **Intelligent Analysis**: Based on the column names and data types, infer the data's context (e.g., sales, financial, survey data) and determine the most relevant analyses and visualizations.
    -   **Time-series data**: If a date/timestamp column exists, perform trend analysis.
    -   **Numeric data**: Calculate descriptive statistics (`.describe()`) and create histograms or correlation matrices.
    -   **Categorical data**: Generate frequency counts (`.value_counts()`) and bar charts.
4.  **Generate Outputs**: 
    -   Print a clear, well-structured text summary including data dimensions, summary statistics, and key insights.
    -   Save all generated charts as PNG images to a designated output directory (e.g., `/home/ubuntu/analysis_output/`).
5.  **Present Results**: Display the text summary and embed the generated chart images for the user.

### Example Python Script Structure

Use this template as a starting point. Save it to a file (e.g., `run_analysis.py`) and execute it with `python3.11 run_analysis.py`.

```python
# filename: run_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os

# --- Setup ---
matplotlib.use('Agg') # Use non-interactive backend
plt.rcParams['font.sans-serif'] = ['DejaVu Sans'] # General-purpose font
plt.rcParams['axes.unicode_minus'] = False

# --- Configuration ---
FILE_PATH = '/path/to/your/data.csv' # <-- IMPORTANT: Change this to the actual file path
OUTPUT_DIR = '/home/ubuntu/analysis_output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Data Loading ---
try:
    # Universal loader (add more logic as needed)
    if FILE_PATH.endswith('.csv'):
        df = pd.read_csv(FILE_PATH)
    elif FILE_PATH.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(FILE_PATH)
    elif FILE_PATH.endswith('.json'):
        df = pd.read_json(FILE_PATH)
    else:
        raise ValueError("Unsupported file format.")

    print("--- Data Overview ---")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n--- Column Types ---")
    print(df.dtypes)
    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    # --- Statistical Summary ---
    print("\n--- Descriptive Statistics (Numeric Columns) ---")
    print(df.describe())

    # --- Intelligent Visualization ---
    print("\n--- Generating Visualizations ---")
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    # 1. Histograms for numeric columns
    for col in numeric_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribution of {col}')
        chart_path = os.path.join(OUTPUT_DIR, f'hist_{col}.png')
        plt.savefig(chart_path)
        plt.close()
        print(f"Generated histogram for {col} at {chart_path}")

    # 2. Bar charts for categorical columns (with high cardinality check)
    for col in categorical_cols:
        if df[col].nunique() < 50: # Avoid plotting charts with too many categories
            plt.figure(figsize=(12, 7))
            sns.countplot(y=df[col], order=df[col].value_counts().index)
            plt.title(f'Count of {col}')
            plt.tight_layout()
            chart_path = os.path.join(OUTPUT_DIR, f'bar_{col}.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Generated bar chart for {col} at {chart_path}")

    # 3. Correlation Heatmap for numeric columns
    if len(numeric_cols) > 1:
        plt.figure(figsize=(12, 10))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix')
        chart_path = os.path.join(OUTPUT_DIR, 'correlation_heatmap.png')
        plt.savefig(chart_path)
        plt.close()
        print(f"Generated correlation heatmap at {chart_path}")

    print("\nAnalysis complete. All charts saved in", OUTPUT_DIR)

except Exception as e:
    print(f"An error occurred: {e}")

```
