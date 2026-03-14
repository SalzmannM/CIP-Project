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
| Saidkosim Abulkosimov | tbd |
| Alina Caspar | tbd |
| Andrin Lehmann | Scraper (overview + detail pages), data pipeline, BFS integration, project structure |
| Maurice Salzmann | tbd |

## Project Structure

```
CIP_FS2026_106/
├── .gitignore
├── .vscode/
│   └── settings.json          # Positron/VS Code Python + Quarto config
├── data/                      # scraped data & BFS reference files (git-ignored)
│   └── .gitkeep
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
