# 90-Minute Lecture: Time-Series Analytics and Machine Learning for Bureau of Transportation Statistics (BTS) Datasets

## Datasets Covered
- **DB28 — Air Carrier Traffic Statistics (monthly)**
- **DB1B — Origin & Destination Survey (quarterly)**
- **ASQP — Airline Service Quality Performance (monthly)**

## Lecture Goals
- Understand the four layers of analytics: Descriptive, Diagnostic, Predictive, Prescriptive.
- Apply ARIMA/SARIMA/ARIMAX models.
- Apply a simple neural network (N-BEATS).
- Run a practical Google Colab demonstration.
- Use BTS datasets for forecasting and prescriptive recommendations.

---

## 1. Data Analytics (DA) and Machine Learning (ML) Foundations

### 1.1 What is Data Analytics?
Data Analytics (DA) is the systematic use of data to identify patterns and support decision‑making.

### 1.2 The Four Types of Analytics
1. **Descriptive:** What happened?
2. **Diagnostic:** Why did it happen?
3. **Predictive:** What will happen next?
4. **Prescriptive:** What should we do?

### 1.3 Time-Series Concepts
- Level, trend, seasonality, noise
- Exogenous variables: population, GDP, fuel price, competition, weather

### 1.4 Machine Learning (ML) Types
- Supervised learning
- Unsupervised learning
- Reinforcement learning

---

## 2. BTS Dataset Landscape

### DB28 — Air Carrier Traffic Statistics
- Monthly passengers, seats, freight
- Used for demand forecasting and capacity planning

### DB1B — Origin & Destination Survey
- Quarterly fares, itineraries
- Used for fare trends and competitive analysis

### ASQP — Airline Service Quality Performance
- Monthly OTP (on‑time performance)
- Used for reliability and delay forecasting

---

## 3. Classical and Neural Forecasting

### 3.1 ARIMA, SARIMA, ARIMAX
- ARIMA(p,d,q)
- SARIMA(P,D,Q,s)
- ARIMAX supports exogenous variables

### 3.2 N‑BEATS Neural Network
- Feed‑forward network specialized for time‑series
- Implemented via `darts`

---

## 4. Google Colab Demo

### Install Dependencies
```python
!pip install pandas numpy matplotlib darts[u] --quiet
```

### DB28 Demo
Load → plot → forecast → prescriptive rules.

### DB1B Demo
Quarterly fare forecasting.

### ASQP Demo
Monthly OTP forecasting.

---

## 7. Fifteen Dataset Questions

### DB28 — Monthly (5)
1. Trend in monthly passenger counts?
2. Peak/off‑peak months?
3. Impact of new competition?
4. Forecast next year’s demand?
5. Should capacity change?

### DB1B — Quarterly (5)
1. Fare trends?
2. Competition vs. fare changes?
3. Distance-band fare differences?
4. Forecast next‑quarter fares?
5. Which markets are most sensitive to fare changes?

### ASQP — Monthly (5)
1. OTP trends?
2. Delay‑cause decomposition?
3. Schedule density vs. delays?
4. Forecast next‑year OTP?
5. Where to add buffers?

---

## 8. Five Cross‑Dataset Questions

1. How do fares (DB1B) drive demand (DB28)?
2. How does reliability (ASQP) change demand (DB28)?
3. How do fare + demand + reliability integrate into network planning?
4. What routes should be expanded based on combined metrics?
5. Scenario analysis: fuel ↑, OTP ↓ → impact across DB28 + DB1B + ASQP?

---

*End of Lecture.*
