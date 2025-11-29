# 📊 Love Island Games (Season 2) — Reddit Analytics Dashboard

> A one-day end-to-end data science project analyzing Reddit engagement and sentiment around *Love Island Games Season 2* using real-time community data.

This project collects, processes, and visualizes Reddit discussion data to explore how audience sentiment and engagement evolve across episodes and major events. It demonstrates a complete **data pipeline**: from data ingestion to NLP analysis to interactive visualization.

---

## 🎯 Project Goals

- Build a complete **data ingestion → analysis → visualization pipeline in one day**
- Quantify:
  - audience engagement over time
  - sentiment trends across episodes
  - key discussion themes
- Combine **quantitative metrics** (post volume, scores, comment counts)
  with **qualitative analysis** (sentiment, keywords, topics)

---

## 🧪 Data Source

- **Platform:** Reddit  
- **Communities:** Relevant Love Island subreddits  
- **Data Collected:**
  - post titles and bodies  
  - comment text  
  - timestamps  
  - upvotes / scores  
  - comment counts  

Data was collected using the Reddit API and stored locally for reproducibility.

---

## 🛠 Tech Stack

- **Language:** Python  
- **Data Collection:** PRAW (Reddit API)  
- **Data Processing:** pandas, numpy  
- **NLP & Text Analysis:** nltk / vader / scikit-learn  
- **Visualization:** matplotlib, seaborn / plotly  
- **Dashboard:** Streamlit

---

## 🔁 Pipeline Overview

Reddit API -> Raw JSON Data -> Data Cleaning & Normalization -> Feature Engineering -> Sentiment -> Analysis & Keyword Extraction -> Time-Series Aggregation -> Interactive Dashboard

---

## 📈 Key Analyses Performed

- **Engagement Over Time**
  - Daily post and comment volume
  - Spike detection around episode drops

- **Sentiment Trends**
  - Compound sentiment by day
  - Rolling sentiment averages
  - Episode-to-episode mood shifts

- **Discussion Themes**
  - Keyword frequency analysis
  - Common phrases and topics
  - High-engagement posts vs. low-engagement posts

- **Performance Indicators**
  - Posts per episode
  - Average sentiment vs upvote score

---

## 📊 Dashboard Features

- Time-series plots of:
  - submission volume
  - average sentiment
- Distribution of post scores
- Top keywords by day / week
- Filters by:
  - subreddit
  - date range
  - sentiment polarity

> Screenshots or demo GIFs can be added here.

---

## 🧠 Technical Challenges & Solutions

### 1. Noisy Social Media Text
**Challenge:** Reddit text contains slang, sarcasm, emojis, and abbreviations.  
**Solution:** Implemented text normalization (lowercasing, punctuation removal, stopword filtering) before sentiment computation.

### 2. Biased Sentiment Readings
**Challenge:** Single-post sentiment is often unstable.  
**Solution:** Aggregated sentiment using rolling averages and daily means to smooth volatility.

### 3. Data Collection Rate Limits
**Challenge:** API rate limits restrict large-scale scraping.  
**Solution:** Batched requests and cached intermediate results locally for fast re-analysis.

### 4. Signal vs. Hype
**Challenge:** Engagement spikes do not always reflect sentiment shifts.  
**Solution:** Visualized sentiment and engagement side-by-side to detect divergence patterns.

---

## 🚀 How the Project Was Built (1-Day Sprint)

- **Hour 1–2:** API setup, subreddit discovery, raw data extraction  
- **Hour 3–4:** Data cleaning, schema design, CSV persistence  
- **Hour 5–6:** Sentiment analysis + keyword extraction  
- **Hour 7–8:** Aggregation + time-series feature engineering  
- **Hour 9–10:** Dashboard construction  
- **Hour 11–12:** Refinement, visualization cleanup, documentation