# Love Island Australia – Season 7  
## Audience Performance & Sentiment Analysis (Reddit)

This repository contains a quantitative and qualitative audience performance analysis of *Love Island Australia Season 7* using Reddit engagement from **r/LoveIslandAus** as a proxy for live and VOD audience interest. The project was designed to mirror internal **TV ratings and title performance reporting** workflows.

**Prepared by:** Marsya Amanda  
**Season Covered:** Episodes 1–20 (27 Oct 2025 – 27 Nov 2025)  
**Tools:** Python, pandas, matplotlib  

---

## Project Overview

- **Threads analysed:** 74  
- **Comments analysed:** 12,438  
- **Episodes covered:** 20  
- **Peak engagement:** Episode 20 (2,251 total interactions)  
- **Primary drivers of engagement:** Recouplings, eliminations, and production-driven conflicts  

The analysis integrates:
- Episode-level engagement tracking
- Cumulative season engagement
- Sentiment homogeneity as a measure of audience consensus vs polarisation
- Qualitative interpretation of discussion dynamics

---

## Data Source

- Subreddit: **r/LoveIslandAus**
- Collection method: Web scraping with BeautifulSoup
- Filters:
  - Episode identifiers (“Episode”, “Ep”, “E0X”)
  - Season identifiers (“Season 7”, “S7”)
  - Posts from **27 Oct 2025 onward**
- Posts sorted by newest
- All data is publicly available Reddit content

---

## Key Metrics

- **Engagement Volume:** Posts + comments per episode  
- **Attention Intensity:** Total upvotes per episode  
- **Cumulative Engagement:** Running total across episodes  
- **Sentiment Homogeneity:** Standard deviation of sentiment across discussion threads  

---

## Key Outputs

- Episode-level engagement and sentiment metrics  
- Season-wide cumulative engagement trends  
- Sentiment homogeneity by episode  
- Final performance report (`report.pdf`)
- Reproducible Python analysis notebook

---

## Repository Structure

```
data/ # Raw and cleaned Reddit data
plot/ # Generated figures for the report
analysis.ipynb
report.pdf
requirements.txt
README.md
```

---

## Limitations

- Reddit users represent a highly engaged but non-representative subset of total viewers  
- Engagement is used as a **proxy** for audience interest, not official ratings or streaming data  
- Sentiment was inferred via qualitative analysis and engagement-based proxies  

---

## Reproducibility

1. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
2. Run `analysis.ipynb` to reproduce all figures and tables.

--

## Use Case

This project demonstrates a title-level audience performance reporting pipeline aligned with broadcast and streaming analytics roles, including engagement tracking, sentiment analysis, and editorial performance interpretation.