
# 90-Minute Lecture: Time-Series Analytics and ML for BTS Datasets  
### *With Techniques + Code Examples for Every Question (DB28, DB1B, ASQP + Cross-Dataset)*

This lecture includes:
- DB28 / DB1B / ASQP analytics foundations  
- Descriptive → Diagnostic → Predictive → Prescriptive workflows  
- ARIMA / SARIMA / ARIMAX  
- N-BEATS neural network model  
- Google Colab–ready examples  
- **20 questions** with **techniques + code blocks** for each

---

# 1. Foundations of Data Analytics (DA) and Machine Learning (ML)

## 1.1 What is Data Analytics?
Data Analytics (DA) is the systematic exploration of data to identify trends, relationships, and actionable insights.

## 1.2 Four Types of Analytics  
1. **Descriptive** – Summarize past behavior  
2. **Diagnostic** – Explain why it happened  
3. **Predictive** – Forecast what comes next  
4. **Prescriptive** – Recommend what to do  

## 1.3 ARIMA & Neural Techniques

### ARIMA/SARIMA/ARIMAX
- Good for stability, interpretability, forecasting, exogenous features  

### N-BEATS (Neural)
- Excellent for automatic trend/seasonality learning  
- Simple feed‑forward architecture (no RNNs)  
- Great for DB28, DB1B, ASQP

---

# 2. BTS Datasets Overview
- **DB28** — Monthly passengers  
- **DB1B** — Quarterly fares  
- **ASQP** — Monthly on-time performance  

---

# 3. Google Colab Setup

```python
!pip install pandas numpy matplotlib darts[u] statsmodels --quiet
```

---

# 4. Techniques & Code for Dataset Questions  
Below are **15 questions** (5 per dataset) with **techniques** + **code templates**.

==============================================================  
# DB28 — Air Carrier Traffic Statistics  
==============================================================  

## **Q1 — Descriptive:**  
### *How have monthly passenger counts changed over 5 years?*

**Technique:** Line plot + rolling mean.

```python
plt.plot(df["Date"], df["Passengers"])
df["Passengers"].rolling(12).mean().plot(label="12-month trend")
```

---

## **Q2 — Descriptive:**  
### *Which months show highest/lowest demand?*

**Technique:** Monthly seasonality plot.

```python
df["Month"] = df["Date"].dt.month
df.groupby("Month")["Passengers"].mean().plot(kind="bar")
```

---

## **Q3 — Diagnostic:**  
### *How did competitor entry affect demand?*

**Technique:** Difference-of-means + regression.

```python
df["PostEntry"] = df["Date"] >= "2022-01-01"
import statsmodels.formula.api as smf
smf.ols("Passengers ~ PostEntry", data=df).fit().summary()
```

---

## **Q4 — Predictive:**  
### *Forecast next 12 months of demand.*

**Technique:** N-BEATS.

```python
series = TimeSeries.from_dataframe(df, "Date", "Passengers")
model = NBEATSModel(input_chunk_length=24, output_chunk_length=12)
model.fit(series[:-12])
forecast = model.predict(12)
```

---

## **Q5 — Prescriptive:**  
### *Which routes need capacity increases?*

**Technique:** Forecast vs. seats.

```python
df["LoadFactorForecast"] = forecast.values() / df["Seats"].iloc[-12:]
routes_to_expand = df[df["LoadFactorForecast"] > 0.9]
```

==============================================================  
# DB1B — Origin & Destination Survey  
==============================================================  

## **Q1 — Descriptive:**  
### *How have fares changed over 10 years?*

**Technique:** Trend + smoothing.

```python
plt.plot(df["Date"], df["AvgFare"])
df["roll"] = df["AvgFare"].rolling(4).mean()
df["roll"].plot()
```

---

## **Q2 — Diagnostic:**  
### *How does competition impact fare?*

**Technique:** Regression with competition count.

```python
smf.ols("AvgFare ~ Competitors", data=df).fit().summary()
```

---

## **Q3 — Diagnostic:**  
### *How do fares differ by distance band?*

**Technique:** Distance bucket aggregation.

```python
df["Band"] = pd.cut(df["Distance"], bins=[0,500,1500,3000])
df.groupby("Band")["AvgFare"].mean()
```

---

## **Q4 — Predictive:**  
### *Quarterly fare forecasting (N-BEATS).*

```python
model = NBEATSModel(input_chunk_length=8, output_chunk_length=4)
model.fit(series[:-4])
forecast = model.predict(4)
```

---

## **Q5 — Prescriptive:**  
### *Which markets respond most to fare reductions?*

**Technique:** Elasticity regression.

```python
smf.ols("Passengers ~ AvgFare", data=df).fit().params
```

==============================================================  
# ASQP — Airline Service Quality Performance  
==============================================================  

## **Q1 — Descriptive:**  
### *Trend in monthly OTP?*

```python
plt.plot(df["Date"], df["OTP"])
```

---

## **Q2 — Diagnostic:**  
### *Which delay causes dominate?*

```python
df[["Weather","Carrier","NAS","Security","LateAircraft"]].sum().plot(kind="bar")
```

---

## **Q3 — Diagnostic:**  
### *How does schedule density affect delay?*

```python
smf.ols("ArrDelay ~ FlightsPerHour", data=df).fit().summary()
```

---

## **Q4 — Predictive:**  
### *Forecast OTP for next 12 months.*

```python
model = NBEATSModel(24, 12)
model.fit(series[:-12])
forecast = model.predict(12)
```

---

## **Q5 — Prescriptive:**  
### *Where to add buffers to protect OTP?*

**Technique:** Threshold-based identification.

```python
problem_months = forecast[forecast.values() < 0.80]
```

==============================================================  
# 5 Cross-Dataset Questions  
==============================================================  

## **Q1:** *How do fares (DB1B) drive demand (DB28)?*  
Technique: Merge & elasticity model.
```python
merged = db28.merge(db1b, on=["Origin","Dest","Quarter"])
smf.ols("Passengers ~ AvgFare", merged).fit().summary()
```

## **Q2:** *How does reliability (ASQP) impact demand (DB28)?*
```python
merged = db28.merge(asqp, on=["Date"])
smf.ols("Passengers ~ OTP", merged).fit().summary()
```

## **Q3:** *Capacity, fare, demand alignment?*
```python
df["Rev"] = df["Passengers"] * df["AvgFare"]
```

## **Q4:** *Which new routes to prioritize?*
Cluster markets by demand + fare + OTP.

```python
from sklearn.cluster import KMeans
KMeans(4).fit(df[["Passengers","AvgFare","OTP"]])
```

## **Q5:** *Scenario analysis with fuel ↑ and OTP ↓*
Simulate multiple regression.

```python
smf.ols("Rev ~ FuelPrice + OTP + AvgFare", df).fit().summary()
```

---

# END OF LECTURE

