
# BTS Time Series Lecture — ARIMA Demo + FastAI N-BEATS Demo

This Markdown matches the full notebook content, with two runnable demos:

1. **ARIMA-only demo** using `statsmodels`
2. **FastAI N-BEATS neural-network demo** using `darts`

Replace the sample CSV paths with your DB28/DB1B/ASQP extracts.

---

# 1. ARIMA-Only Demo (Statsmodels)

## Install Dependencies
```python
!pip install pandas numpy matplotlib statsmodels --quiet
```

## Load DB28 Sample
```python
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.api as tsa

df = pd.read_csv("/content/db28_sample.csv")
df['Date'] = pd.to_datetime(df[['Year','Month']].assign(Day=1))
df = df.sort_values("Date")
df = df.set_index('Date')

ts = df['Passengers']
ts.plot(title="DB28 Monthly Passengers")
plt.show()
```

## Check Stationarity (ADF Test)
```python
from statsmodels.tsa.stattools import adfuller

adf = adfuller(ts)
print("ADF p-value:", adf[1])
```

## Fit SARIMA Model
Monthly data → period s = 12

```python
model = tsa.SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12))
fit = model.fit()
print(fit.summary())
```

## Forecast 12 Months
```python
forecast = fit.forecast(12)
ts.plot(label="Actual")
forecast.plot(label="Forecast")
plt.legend()
plt.show()
```

---

# 2. FastAI N-BEATS Demo (Darts Library)

## Install Dependencies
```python
!pip install pandas numpy matplotlib darts[u] --quiet
```

## Load DB28 Sample
```python
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import NBEATSModel

df = pd.read_csv("/content/db28_sample.csv")
df['Date'] = pd.to_datetime(df[['Year','Month']].assign(Day=1))
df = df.sort_values("Date")

series = TimeSeries.from_dataframe(df, 'Date', 'Passengers')
scaler = Scaler()
series_scaled = scaler.fit_transform(series)

train, test = series_scaled[:-12], series_scaled[-12:]
```

## Train N-BEATS
```python
model = NBEATSModel(
    input_chunk_length=24,
    output_chunk_length=12,
    n_epochs=200,
    random_state=42
)

model.fit(train)
forecast = model.predict(12)
```

## Plot Forecast
```python
series_scaled.plot(label="Actual")
forecast.plot(label="N-BEATS Forecast")
plt.legend()
plt.show()
```

---

# End of Matching Markdown File
