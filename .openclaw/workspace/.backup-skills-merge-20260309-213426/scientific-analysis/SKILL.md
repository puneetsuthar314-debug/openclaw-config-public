---
name: scientific-analysis
description: Perform comprehensive exploratory data analysis and create publication-ready visualizations for scientific data. This skill integrates data analysis across 200+ formats with advanced plotting capabilities for creating journal-quality figures.
license: MIT license
metadata:
    skill-author: Manus AI
---

# Scientific Analysis and Visualization

## Overview

This skill provides a unified workflow for scientific data analysis and visualization. It combines comprehensive exploratory data analysis (EDA) across over 200 scientific file formats with a powerful suite of tools for creating publication-ready figures. From initial data inspection to generating journal-quality plots for manuscripts (Nature, Science, Cell), this skill streamlines the entire process.

**Key Capabilities:**
- **Automated EDA:** Automatic file type detection, format-specific analysis, and data quality assessment.
- **Broad Format Support:** Covers chemistry, bioinformatics, microscopy, spectroscopy, and general scientific data formats.
- **Publication-Ready Plots:** Create multi-panel figures, with error bars, significance markers, and colorblind-safe palettes.
- **Journal-Specific Styling:** Apply formatting for specific journals like Nature, Science, and Cell.
- **High-Resolution Export:** Export figures to vector (PDF, EPS) and raster (TIFF, PNG) formats at the required DPI.

## When to Use This Skill

Use this skill when you need to:
- Analyze a scientific data file to understand its structure, content, and quality.
- Generate a comprehensive report on a dataset before downstream analysis.
- Create plots or visualizations for a scientific manuscript.
- Prepare figures for journal submission that meet specific formatting guidelines.
- Ensure visualizations are clear, accurate, and colorblind-friendly.
- Improve an existing figure to meet publication standards.

## Workflow

The workflow is divided into two main stages: data analysis and visualization.

### Stage 1: Exploratory Data Analysis

This stage focuses on understanding the data. It uses the foundation of the `exploratory-data-analysis` skill.

#### Step 1.1: File Type Detection and Analysis

Use the `scripts/eda_analyzer.py` script to automatically analyze the input file. This script detects the file type, performs format-specific analysis, and generates a detailed markdown report.

```shell
python3.11 scripts/eda_analyzer.py <filepath> [output.md]
```

Alternatively, perform a manual analysis by following the steps in the `references/eda_workflow.md` document. This involves identifying the file type, consulting the relevant format reference file (e.g., `references/bioinformatics_genomics_formats.md`), and then performing analysis using appropriate Python libraries (e.g., pandas, Biopython).

#### Step 1.2: Generate and Review the EDA Report

Whether generated automatically or manually, the EDA report should contain:
- **Basic Information:** File properties, format description, and use cases.
- **Data Analysis:** Structure, dimensions, statistical summaries, and quality assessment.
- **Key Findings:** Notable patterns, potential issues, and quality metrics.
- **Recommendations:** Suggested preprocessing steps and appropriate downstream analyses.

Review this report to inform the visualization strategy.

### Stage 2: Publication-Ready Visualization

Once the data is understood, create publication-quality figures using the principles from the `scientific-visualization` skill.

#### Step 2.1: Choose a Plot Type and Style

Based on the EDA report and the research question, select an appropriate plot type (e.g., line plot, box plot, heatmap, scatter plot). Apply a pre-configured journal style to ensure consistency.

```python
import matplotlib.pyplot as plt
from style_presets import configure_for_journal

# Configure for a specific journal (e.g., Nature, single-column)
configure_for_journal('nature', figure_width='single')

# Now, create your figure and axes
fig, ax = plt.subplots()
```

#### Step 2.2: Create the Visualization

Use libraries like Matplotlib, Seaborn, or Plotly to create the plot. Adhere to best practices for scientific figures:
- **Use Colorblind-Safe Palettes:** Employ palettes like Okabe-Ito or perceptually uniform colormaps (`viridis`, `cividis`). Test figures in grayscale.
- **Clear and Legible Text:** Use sans-serif fonts (Arial, Helvetica) at appropriate sizes (7-9pt for labels).
- **Proper Labeling:** Label all axes with descriptive names and units.
- **Error Bars and Statistics:** If showing comparisons, include error bars (SEM, SD, CI) and significance annotations.

Consult `references/visualization_best_practices.md` for a detailed guide.

#### Step 2.3: Compose Multi-Panel Figures (if needed)

For complex stories, combine multiple plots into a single, cohesive figure using `GridSpec`. Ensure consistent styling and clear panel labels (A, B, C).

```python
from string import ascii_uppercase

fig = plt.figure(figsize=(7, 4)) # Double-column width
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)
ax1 = fig.add_subplot(gs[0, 0])
# ... add other panels

# Add panel labels
for i, ax in enumerate(fig.axes):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

#### Step 2.4: Export the Figure

Save the final figure in the required formats and resolutions for journal submission. The `figure_export.py` script handles this automatically.

```python
from figure_export import save_for_journal

# Saves figure with correct DPI and format for the specified journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

## Resources

This skill relies on a collection of scripts, reference documents, and style assets. Key resources are located in the following directories:

- **/home/ubuntu/skills/scientific-analysis/scripts/**: Contains Python scripts for automated analysis (`eda_analyzer.py`), figure exporting (`figure_export.py`), and styling (`style_presets.py`).
- **/home/ubuntu/skills/scientific-analysis/references/**: Detailed markdown documents covering EDA workflows, visualization best practices, journal guidelines, color palettes, and code examples.
- **/home/ubuntu/skills/scientific-analysis/assets/**: Matplotlib style files (`.mplstyle`) for various journals and a template for EDA reports (`report_template.md`).

Always consult these resources to ensure adherence to best practices and for detailed, format-specific guidance.
