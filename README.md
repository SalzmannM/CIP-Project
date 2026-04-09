# CIP_FS2026_106 — Swiss Public Sector Job Market Analysis

## Project Overview

This project analyzes job advertisements within the Swiss public sector using data scraped from [publicjobs.ch](https://publicjobs.ch). It is submitted as part of the CIP module (Coding in Python) at HSLU — Master in Applied Information and Data Science.

## Research Questions

1. **Geography & Market Demand**: How does current demand for public sector labour distribute across Swiss regions and organization types?
2. **Workload & Flexibility**: Which sectors/regions offer the highest flexibility (part-time vs. full-time), and how do these compare to official BFS employment statistics?
3. **Benefits & Attractiveness**: Which fringe benefits are most frequently offered, and do these vary by canton or workload?

## Team & Code Contributions

| Name | Contribution |
|---|---|
| Alina Caspar | Full analysis pipeline covering all three research questions: canton choropleth & occupation/ISCO breakdowns (RQ1), workload flexibility with BFS chi-square benchmark (RQ2), benefits frequency & canton heatmap (RQ3), plus drafting of the Results & Discussion text |
| Andrin Lehmann | Project setup & structure, dynamic Selenium scraper (overview + detail pages), BFS BESTA / PX-Web integration, ISCO-08 mapping, QMD authoring, integration of teammates' branches, PDF render pipeline |
| Maurice Salzmann | Data validation checks, cleansing pipeline steps (datatype enforcement, range checks, outlier filtering) |

## Project Structure

```
CIP_FS2026_106/
├── .gitignore
├── .vscode/
│   └── settings.json          # Positron/VS Code Python + Quarto config
├── data/                      # scraped data, BFS reference files, GeoJson (git-ignored)
│   └── .gitkeep
├── public_jobs_analysis.html  # html version of documentation including code-chunks
├── public_jobs_analysis.pdf   # clean 6 page pdf-version of documentation
├── public_jobs_analysis.qmd   # main Quarto document (code + documentation)
├── requirements.txt           # Python dependencies
├── style.css                  # custom Quarto styling (optional)
└── README.md                  # this file
```

## Setup & Reproduction

```bash
# 1. Clone the repository
git clone <https://github.com/SalzmannM/CIP-Project.git>
cd CIP_FS2026_106

# 2. Create virtual environment
python -m venv .venv

# 3. Activate (Windows)
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run scraper cells in the QMD (sections 2.3 and 2.4) (ONLY REQUIRED IF data is empty)
#    → produces data/publicjobs_raw.json and data/publicjobs_benefits.json

# 6. Render the Quarto document
quarto render public_jobs_analysis.qmd
```

## Data Sources

- **publicjobs.ch** — Job listings (web scraping, Selenium + BeautifulSoup)
- **BFS BESTA** — Employment statistics by sector and Beschäftigungsgrad (PX-Web API)
- **BFS LSE 2022** — Median salaries by ISCO-08 occupation group (Excel download)

## Tools & Technologies

- Python 3.12+, Selenium, BeautifulSoup, Pandas, Plotly, Seaborn, Matplotlib
- Quarto for reproducible documentation
- Git for version control
