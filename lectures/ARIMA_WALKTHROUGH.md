
ARIMA WALKTHROUGH WITH STATSMODELS
Context: AMA–SAT quarterly passengers from aviation_core / AirlineOps

This script shows:
1. Loading and preparing a time series
2. Exploring and checking stationarity
3. Differencing and using ACF/PACF for order hints
4. Fitting a (S)ARIMA model with statsmodels
5. Running diagnostics
6. Forecasting and evaluating forecast accuracy

You can adapt this directly to any route or metric.


# 0. Imports and basic setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from sklearn.metrics import mean_absolute_error, mean_squared_error

# If you prefer inline plots in a notebook:
# %matplotlib inline

# ------------------------------------------------------------
# 1. LOAD AND PREPARE THE SERIES
# ------------------------------------------------------------

# Replace this with your actual CSV or data source
# Expecting columns: period (string or date), pax (numeric)
df = pd.read_csv("ama_sat_quarterly_pax.csv")

# Parse period as datetime (end of quarter) and set as index
df["period"] = pd.to_datetime(df["period"])
df = df.set_index("period").sort_index()

# Tell pandas the frequency is quarterly (Q for quarter-end; adjust if needed)
# If your data is exactly quarterly with no gaps, you can set freq explicitly:
df = df.asfreq("Q")

# Inspect the head
print("Head of data:")
print(df.head())

# Quick plot of the series
fig, ax = plt.subplots()
df["pax"].plot(ax=ax)
ax.set_title("AMA–SAT Quarterly Passengers")
ax.set_ylabel("Passengers per Quarter")
plt.show()

# ------------------------------------------------------------
# 2. TRAIN–TEST SPLIT FOR FORECAST EVALUATION
# ------------------------------------------------------------

# We'll use the last N quarters as a test set, e.g., last 8 quarters
test_horizon = 8

train = df.iloc[:-test_horizon]
test = df.iloc[-test_horizon:]

print(f"Train period: {train.index[0].date()} to {train.index[-1].date()}")
print(f"Test  period: {test.index[0].date()} to {test.index[-1].date()}")

# Plot train vs test
fig, ax = plt.subplots()
train["pax"].plot(ax=ax, label="Train")
test["pax"].plot(ax=ax, label="Test", color="orange")
ax.set_title("Train / Test Split — AMA–SAT Pax")
ax.legend()
plt.show()

# ------------------------------------------------------------
# 3. STATIONARITY CHECK (ADF TEST) AND DIFFERENCING
# ------------------------------------------------------------

def adf_report(series, title=""):
    """Run Augmented Dickey–Fuller test and print a short report."""
    print("\n" + "-" * 60)
    print(f"ADF TEST FOR: {title}")
    print("-" * 60)
    result = adfuller(series.dropna())
    labels = ["ADF statistic", "p-value", "# lags used", "# observations used"]
    out = dict(zip(labels, result[:4]))
    for k, v in out.items():
        print(f"{k}: {v}")
    for key, value in result[4].items():
        print(f"Critical value ({key}): {value}")
    if result[1] < 0.05:
        print("=> Reject H0: Series looks STATIONARY at 5% level.")
    else:
        print("=> Fail to reject H0: Series looks NON-STATIONARY at 5% level.")

# Check stationarity of the original series
adf_report(train["pax"], title="Original pax")

# If non-stationary, try differencing
train["pax_diff1"] = train["pax"].diff(1)
adf_report(train["pax_diff1"], title="1st difference (pax_diff1)")

# For quarterly data, we might also check a seasonal difference (lag 4)
train["pax_diff_seasonal"] = train["pax"].diff(4)
adf_report(train["pax_diff_seasonal"], title="Seasonal difference (lag 4)")

# Or combine both:
train["pax_diff1_seasonal"] = train["pax"].diff(1).diff(4)
adf_report(train["pax_diff1_seasonal"], title="1st + seasonal difference")

# Choose differencing orders based on:
# - visual plots
# - ADF results
# For example, suppose:
#   d = 1  (non-seasonal difference)
#   D = 1  (seasonal difference with period s = 4)
# and we will treat s = 4 for quarterly data.

# ------------------------------------------------------------
# 4. ACF/PACF TO GET HINTS FOR p, q, P, Q
# ------------------------------------------------------------

# Use the combined differenced series as a working stationary candidate
stationary_series = train["pax_diff1_seasonal"].dropna()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(stationary_series, lags=20, ax=axes[0])
plot_pacf(stationary_series, lags=20, ax=axes[1])
axes[0].set_title("ACF — Differenced Series")
axes[1].set_title("PACF — Differenced Series")
plt.tight_layout()
plt.show()

"""
Interpretation hints (high-level, not rigid rules):

- If PACF cuts off sharply after lag p, that suggests AR(p).
- If ACF cuts off sharply after lag q, that suggests MA(q).
- For quarterly seasonality (s = 4), look at lags 4, 8, 12, ...

In practice you will:
- eyeball ACF/PACF,
- try a small grid of (p, q) and (P, Q),
- pick based on AIC/BIC and diagnostics.
"""

# For this example, let's pick:
#   p = 1, d = 1, q = 1
#   P = 1, D = 1, Q = 1, s = 4

order = (1, 1, 1)
seasonal_order = (1, 1, 1, 4)

# ------------------------------------------------------------
# 5. FIT A SARIMA MODEL (STATESPACE / SARIMAX)
# ------------------------------------------------------------

# We'll use statsmodels' SARIMAX (which covers ARIMA/SARIMA)
model = sm.tsa.statespace.SARIMAX(
    train["pax"],
    order=order,
    seasonal_order=seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False,
)

results = model.fit()
print(results.summary())

# ------------------------------------------------------------
# 6. MODEL DIAGNOSTICS
# ------------------------------------------------------------

# Quick diagnostic plots: residuals, QQ-plot, etc.
results.plot_diagnostics(figsize=(12, 8))
plt.suptitle("SARIMA Diagnostics — AMA–SAT Pax", y=1.02)
plt.show()

"""
Things to look for:

- Standardized residuals: no obvious remaining structure, roughly zero-mean.
- Histogram + KDE of residuals: roughly normal-ish (doesn't have to be perfect).
- Normal Q-Q: points fall roughly on the straight line.
- Correlogram of residuals: ACF of residuals within confidence bands
  (no strong autocorrelation left).

If diagnostics look bad:
- Try different (p, d, q, P, D, Q) values.
- Check if you over/under-differenced.
"""

# ------------------------------------------------------------
# 7. FORECAST ON THE TEST WINDOW
# ------------------------------------------------------------

# We forecast the same length as the test set
n_test = len(test)

forecast_results = results.get_forecast(steps=n_test)
forecast_mean = forecast_results.predicted_mean
forecast_ci = forecast_results.conf_int()

# Align index with test data
forecast_mean.index = test.index
forecast_ci.index = test.index

# Plot train, test, and forecast
fig, ax = plt.subplots(figsize=(10, 5))
train["pax"].plot(ax=ax, label="Train")
test["pax"].plot(ax=ax, label="Test", color="orange")
forecast_mean.plot(ax=ax, label="Forecast", color="green")

ax.fill_between(
    forecast_ci.index,
    forecast_ci.iloc[:, 0],
    forecast_ci.iloc[:, 1],
    color="green",
    alpha=0.2,
    label="95% conf. interval",
)

ax.set_title("SARIMA Forecast vs Actual — AMA–SAT Quarterly Pax")
ax.set_ylabel("Passengers per Quarter")
ax.legend()
plt.show()

# ------------------------------------------------------------
# 8. FORECAST ACCURACY METRICS
# ------------------------------------------------------------

y_true = test["pax"]
y_pred = forecast_mean

mae = mean_absolute_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
mape = (np.abs((y_true - y_pred) / y_true)).mean() * 100

print("\nFORECAST ACCURACY ON TEST SET:")
print(f"MAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"MAPE : {mape:,.2f}%")

"""
Interpretation:

- MAE: average absolute error in passengers per quarter.
- RMSE: penalizes larger errors more heavily.
- MAPE: average percentage error (be careful if there are zeros or very small values).

For planning:
- Compare different SARIMA specs by AIC/BIC AND out-of-sample metrics.
- Keep at least one simple, interpretable baseline (like SARIMA) to compare
  more complex ML models (XGBoost, transformers, etc.) against.
"""

# ------------------------------------------------------------
# 9. FUTURE (EX-ANTE) FORECAST BEYOND TEST WINDOW
# ------------------------------------------------------------

# Once you're satisfied with diagnostics and test performance, refit the model
# on the FULL data (train + test) to generate ex-ante forecasts.

full_model = sm.tsa.statespace.SARIMAX(
    df["pax"],
    order=order,
    seasonal_order=seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False,
)

full_results = full_model.fit()

# Forecast next 8 quarters (for example)
steps_ahead = 8
future_forecast = full_results.get_forecast(steps=steps_ahead)
future_mean = future_forecast.predicted_mean
future_ci = future_forecast.conf_int()

print("\nFUTURE FORECAST (NEXT 8 QUARTERS):")
print(future_mean)

# Plot full history + future forecast
fig, ax = plt.subplots(figsize=(10, 5))
df["pax"].plot(ax=ax, label="Observed", color="black")
future_mean.index = pd.date_range(
    start=df.index[-1] + pd.offsets.QuarterEnd(),
    periods=steps_ahead,
    freq="Q",
)
future_ci.index = future_mean.index

future_mean.plot(ax=ax, label="Future forecast", color="purple")
ax.fill_between(
    future_ci.index,
    future_ci.iloc[:, 0],
    future_ci.iloc[:, 1],
    color="purple",
    alpha=0.2,
    label="95% conf. interval",
)

ax.set_title("Future SARIMA Forecast — AMA–SAT Quarterly Pax")
ax.set_ylabel("Passengers per Quarter")
ax.legend()
plt.show()

"""
At this point you have:

- A clean time series model for AMA–SAT pax.
- Diagnostics and forecast metrics.
- Ex-ante forecasts for planning capacity and economics.

Next step in the broader AirlineOps stack:
- Use these SARIMA forecasts as a baseline:
  - Compare them to XGBoost or other demand models.
  - Feed them into schedule and fleet planning.
"""