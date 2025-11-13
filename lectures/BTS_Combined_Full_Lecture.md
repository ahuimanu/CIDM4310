
# Combined BTS Time-Series Lecture (Full 90 Minutes)  
## Includes:  
- Lecture Foundations  
- Dataset Overviews  
- ARIMA Demo  
- FastAI / Darts N-BEATS Demo  
- 20 Questions (15 Dataset-Specific + 5 Cross-Dataset)  
- Techniques + Representative Code  

---

# 1. Introduction  
Time-series analytics for DB28 (monthly traffic), DB1B (quarterly fares), and ASQP (monthly OTP) using classical models (ARIMA/SARIMA/ARIMAX) and neural networks (N-BEATS).  

---

# 2. The Four Types of Analytics  
- Descriptive  
- Diagnostic  
- Predictive  
- Prescriptive  

---

# 3. BTS Dataset Landscape  
**DB28:** monthly passengers, seats, load factors  
**DB1B:** quarterly fares, coupons, distance  
**ASQP:** delays, OTP, causes  

---

# 4. ARIMA-Only Demo (Statsmodels)  
```python
!pip install pandas numpy matplotlib statsmodels --quiet

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.api as tsa

df = pd.read_csv("/content/db28_sample.csv")
df['Date'] = pd.to_datetime(df[['Year','Month']].assign(Day=1))
df = df.sort_values("Date").set_index("Date")

ts = df['Passengers']
ts.plot(title="DB28 Monthly Passengers")
plt.show()

from statsmodels.tsa.stattools import adfuller
print("ADF:", adfuller(ts)[1])

model = tsa.SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12))
fit = model.fit()
forecast = fit.forecast(12)

ts.plot(); forecast.plot(); plt.show()
```

---

# 5. FastAI / Darts N-BEATS Demo  
```python
!pip install darts[u] pandas numpy matplotlib --quiet

from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import NBEATSModel

df = pd.read_csv("/content/db28_sample.csv")
df['Date'] = pd.to_datetime(df[['Year','Month']].assign(Day=1))
series = TimeSeries.from_dataframe(df, 'Date', 'Passengers')

scaler = Scaler()
series_scaled = scaler.fit_transform(series)

train, test = series_scaled[:-12], series_scaled[-12:]

model = NBEATSModel(24, 12, n_epochs=150)
model.fit(train)
forecast = model.predict(12)

series_scaled.plot(); forecast.plot(); plt.show()
```

---

# 6. 🚀 20 Questions + Techniques + Code  

## DB28 — 5 Questions  
### 1. Monthly passenger trends  
```python
df.plot(x="Date",y="Passengers")
```

### 2. Identify peak/off-peak months  
```python
df['Month']=df['Date'].dt.month
df.groupby('Month')['Passengers'].mean().plot(kind='bar')
```

### 3. Competition impact  
```python
import statsmodels.formula.api as smf
smf.ols("Passengers ~ Competitors",df).fit().summary()
```

### 4. Forecast DB28 using N-BEATS  
```python
model.predict(12)
```

### 5. Prescriptive: capacity planning  
```python
lf = forecast.values()/df['Seats'].iloc[-12:].values.reshape(-1,1)
```

---

## DB1B — 5 Questions  
### 6. Fare trends  
```python
plt.plot(df['Date'],df['AvgFare'])
```

### 7. Competition vs fare  
```python
smf.ols("AvgFare ~ Competitors",df).fit().summary()
```

### 8. Distance bands  
```python
pd.cut(df['Distance'],[0,500,1500,3000]).value_counts()
```

### 9. Forecast fares (N-BEATS)  
```python
fc = model.predict(4)
```

### 10. Prescriptive fare sensitivity  
```python
smf.ols("Passengers ~ AvgFare",df).fit().params
```

---

## ASQP — 5 Questions  
### 11. OTP trends  
```python
plt.plot(df['Date'],df['OTP'])
```

### 12. Delay causes  
```python
df[['Weather','Carrier','NAS','Security','Late']].sum().plot(kind='bar')
```

### 13. Density vs delays  
```python
smf.ols("ArrDelay ~ FlightsPerHour",df).fit().summary()
```

### 14. Forecast OTP  
```python
fc = model.predict(12)
```

### 15. Prescriptive reliability  
```python
fc[fc.values()<0.80]
```

---

# CROSS-DATASET — 5 Questions  
### 16. Fare ↔ demand (DB1B + DB28)  
```python
df=db28.merge(db1b,on=["Origin","Dest","Quarter"])
```

### 17. OTP ↔ demand (ASQP + DB28)  
```python
df=db28.merge(asqp[['Date','OTP']],on='Date')
```

### 18. Capacity–fare–demand model  
```python
smf.ols("Revenue ~ Seats + AvgFare + Passengers",df).fit()
```

### 19. Route prioritization  
```python
from sklearn.cluster import KMeans
KMeans(4).fit(df[['Passengers','AvgFare','OTP']])
```

### 20. Scenario analysis  
```python
smf.ols("Revenue ~ FuelPrice + OTP + AvgFare",df).fit()
```

---

# END OF COMBINED LECTURE FILE
