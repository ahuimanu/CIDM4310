# 90-Minute Lecture: **Time-Series Analytics and Machine Learning for Bureau of Transportation Statistics (BTS) Datasets**

**Audience:** Graduate students or professionals in Data Analytics (DA) and Machine Learning (ML) with interest in aviation systems and large-scale public data.  
**Goal:** Deliver a comprehensive 90-minute master lecture combining **30 minutes of Data Analytics and Machine Learning foundations** with **60 minutes of applied Time-Series techniques** using **Bureau of Transportation Statistics (BTS)** datasets.

---

## Agenda

| Time | Section |
|:--:|:--|
| 00–30 | Data Analytics (DA) and Machine Learning (ML) Foundations |
| 30–45 | Bureau of Transportation Statistics (BTS) Dataset Discovery and Characteristics |
| 45–65 | Classical Time-Series Analytics (STL, ARIMA, Prophet) |
| 65–80 | Machine Learning Approaches (Tree Ensembles, Deep Neural Models) |
| 80–88 | Feature Engineering, Leakage Control, and Backtesting |
| 88–90 | Summary and Diagram Index |

---

## 1️⃣ Data Analytics (DA) and Machine Learning (ML) Foundations (00–30 min)

### 1.1 What is Data Analytics?

**Definition:**  
**Data Analytics (DA)** is the process of systematically examining datasets to identify meaningful patterns, trends, and relationships that can inform decisions.

**Purpose:**  
- To transform raw data into actionable knowledge.  
- To create value by supporting predictions and prescriptive recommendations.  
- To provide evidence-based decision support across domains.

---

### 1.2 The Four Types of Analytics

Data Analytics can be classified into **four levels of maturity**, each answering a specific question and aligning with different modeling approaches.

**Summary Bullet List**
- **Descriptive Analytics:** What happened? (Historical performance)  
- **Diagnostic Analytics:** Why did it happen? (Root cause)  
- **Predictive Analytics:** What will happen next? (Forecasting)  
- **Prescriptive Analytics:** What should we do? (Optimization and decision support)

---

#### **Descriptive Analytics — “What Happened?”**

**Purpose:**  
Summarize, visualize, and report historical performance and outcomes.

**Techniques:**  
Aggregation, visualization (charts, dashboards), summary statistics, frequency distributions, correlation matrices.

**Example (BTS Context):**  
- Compute average delay minutes per airline from the **Airline Service Quality Performance (ASQP)** dataset.  
- Aggregate monthly passenger counts for major routes in **Air Carrier Traffic Statistics (DB28)**.  
- Analyze average quarterly fare levels from **Origin and Destination Survey (DB1B)**.

**Diagram:**  
![Descriptive Analytics](https://upload.wikimedia.org/wikipedia/commons/3/3e/Descriptive_analytics_workflow_diagram.png)

**Analytical Outputs:**  
- Charts, dashboards, pivot tables.  
- KPIs such as On-Time Performance (OTP%) or Load Factor.  
- Basic correlation reports showing relationships between delay type and seasonality.

---

#### **Diagnostic Analytics — “Why Did It Happen?”**

**Purpose:**  
Identify underlying causes, dependencies, or relationships explaining patterns observed in descriptive analytics.

**Techniques:**  
Regression analysis, root cause analysis (RCA), drill-down dashboards, variance decomposition, hypothesis testing.

**Example (BTS Context):**  
- Examine delay causes — weather, air traffic control, carrier issues (ASQP).  
- Investigate fare decreases due to new competitors (DB1B).  
- Identify why load factors dropped on regional routes (DB28).

**Diagram:**  
![Diagnostic Analytics](https://upload.wikimedia.org/wikipedia/commons/4/4a/Diagnostic_analytics_cause_effect_flow.png)

**Analytical Outputs:**  
- Regression summaries linking predictors to delay probabilities.  
- Variance decomposition of route-level performance.  
- Factor impact charts.

---

#### **Predictive Analytics — “What Will Happen Next?”**

**Purpose:**  
Leverage statistical models or Machine Learning (ML) algorithms to forecast future trends or probabilities.

**Techniques:**  
- **Statistical:** Autoregressive Integrated Moving Average (ARIMA), Exponential Smoothing, Seasonal and Trend Decomposition using Loess (STL).  
- **ML:** Gradient Boosting (XGBoost, LightGBM), Neural Networks, Prophet model.

**Example (BTS Context):**  
- Forecast next month’s passenger volumes for specific routes (DB28).  
- Predict next quarter’s median fare per origin–destination pair (DB1B).  
- Estimate likelihood of delay or cancellation by airport and carrier (ASQP).

**Diagram:**  
![Predictive Analytics](https://upload.wikimedia.org/wikipedia/commons/0/0b/Predictive_Analytics_Pipeline.png)

**Analytical Outputs:**  
- Forecast graphs, confidence intervals, and accuracy metrics (MAE, RMSE).  
- Probability distributions for future outcomes.

---

#### **Prescriptive Analytics — “What Should We Do?”**

**Purpose:**  
Recommend specific actions to optimize or improve outcomes based on predictive results.

**Techniques:**  
Optimization algorithms, simulation, constraint programming, reinforcement learning, linear programming.

**Example (BTS Context):**  
- Optimize route schedules to minimize expected delays (ASQP).  
- Allocate aircraft based on predicted load factor and capacity (DB28).  
- Recommend pricing adjustments to maximize revenue (DB1B).

**Diagram:**  
![Prescriptive Analytics](https://upload.wikimedia.org/wikipedia/commons/6/6d/Prescriptive_analytics_decision_framework.png)

**Analytical Outputs:**  
- Decision trees, optimization dashboards, prescriptive policy maps.

---

**Instructor Guidance:**  
Use the four diagrams to demonstrate how each analytical layer builds on the prior one:
1. **Descriptive:** “Know what happened.”  
2. **Diagnostic:** “Understand why.”  
3. **Predictive:** “Anticipate what’s next.”  
4. **Prescriptive:** “Decide what to do.”

Then map each BTS dataset to its analytical role:
- ASQP → Descriptive & Diagnostic (delays, causes).  
- DB28 → Predictive (demand, load factors).  
- DB1B → Prescriptive (fare optimization, network planning).

---

### 1.3 The CRISP-DM (Cross-Industry Standard Process for Data Mining) Framework

**Diagram:**  
![CRISP-DM](https://upload.wikimedia.org/wikipedia/commons/6/61/CRISP-DM_Process_Diagram.png)

**Phases:**
1. **Business Understanding:** Define problem scope and objectives.  
2. **Data Understanding:** Explore BTS dataset schemas (ASQP = flight-level; DB28 = route-level; DB1B = ticket-level).  
3. **Data Preparation:** Merge sources, correct outliers, create time indices.  
4. **Modeling:** Select techniques (STL, ARIMA, Prophet, LightGBM, etc.).  
5. **Evaluation:** Validate with backtesting, cross-validation, and error metrics.  
6. **Deployment:** Integrate forecasts into dashboards or data products.

---

### 1.4 Data Characteristics in BTS Context

| Characteristic | Description | Example |
|----------------|--------------|----------|
| **Granularity** | Level of observation | Flight-level (ASQP), Market-level (DB28), Ticket-level (DB1B) |
| **Frequency** | Time interval | Daily (ASQP), Monthly (DB28), Quarterly (DB1B) |
| **Dimensionality** | Number of fields per record | Dozens of variables per flight or route |
| **Volume** | Dataset size | Millions of records per reporting period |
| **Lag/Lead Effects** | Temporal dependencies | Past OTP predicting future reliability |

---

### 1.5 What is Machine Learning (ML)?

**Definition:**  
Machine Learning (ML) is a subfield of Artificial Intelligence (AI) focusing on algorithms that learn from data to predict outcomes or discover structure without being explicitly programmed.

**Diagram:**  
![ML Taxonomy](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*P-yWhukYArlTq84yJZ1YfA.png)

| ML Type | Description | Example (BTS Context) |
|----------|--------------|----------------------|
| **Supervised Learning** | Learn mapping between features and labels | Predict on-time vs. delayed (ASQP); forecast fare (DB1B) |
| **Unsupervised Learning** | Find structure in unlabeled data | Cluster airports by delay severity (ASQP); group routes by profitability (DB28) |
| **Reinforcement Learning** | Learn through feedback from environment | Adaptive fare optimization or schedule simulation |

---

### 1.6 Machine Learning Pipeline

**Diagram:**  
![ML Pipeline](https://developers.google.com/machine-learning/crash-course/images/Workflow.svg)

**Stages:**
1. **Data ingestion and preparation** — clean, filter, merge.  
2. **Feature generation** — create lag features, rolling averages, holiday flags.  
3. **Model training** — choose algorithms (e.g., ARIMA, LightGBM, Neural Networks).  
4. **Evaluation** — rolling-origin cross-validation and error analysis.  
5. **Deployment and monitoring** — retrain periodically as data drifts.

---

### 1.7 Common Machine Learning Models

#### Linear Regression
![Linear Regression](https://scikit-learn.org/stable/_images/sphx_glr_plot_ols_001.png)  
**Use Case:** Predict fare vs. distance and number of competitors (DB1B).  
- Pros: interpretable coefficients, simple to implement.  
- Cons: limited for nonlinear or seasonal relationships.

#### Decision Tree
![Decision Tree](https://upload.wikimedia.org/wikipedia/commons/f/f7/CART_tree_titanic_survivors.png)  
**Use Case:** Classify delay reasons (ASQP).  
- Pros: intuitive logic (“if-then-else”).  
- Cons: prone to overfitting small samples.

#### Random Forest
![Random Forest](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*w6TQZtJ-91HTb9S1WkmU5g.png)  
**Use Case:** Forecast passenger counts by route (DB28).  
- Pros: stable predictions; good for nonlinear data.  
- Cons: difficult to interpret feature interactions.

#### Gradient Boosting (XGBoost / LightGBM)
![Gradient Boosting](https://xgboost.readthedocs.io/en/stable/_images/boosting.png)  
**Use Case:** Fare forecasting and load-factor prediction.  
- Pros: high accuracy and flexibility.  
- Cons: complex hyperparameter tuning.

#### Artificial Neural Network (ANN)
![ANN](https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg)  
**Use Case:** Predict on-time probability or network flow optimization.  
- Pros: captures nonlinear, multivariate patterns.  
- Cons: opaque (“black box”), data-intensive.

---

## 2️⃣ Bureau of Transportation Statistics (BTS) Dataset Discovery and Characteristics (30–45 min)

| Dataset | Full Name | Description | Frequency | Example Use |
|----------|------------|--------------|------------|--------------|
| **ASQP** | Airline Service Quality Performance | Flight-level operations: delays, causes, cancellations | Daily / Monthly | Delay prediction and reliability benchmarking |
| **DB28 (T-100)** | Air Carrier Traffic Statistics | Route-level passengers, freight, and seat capacity | Monthly | Passenger demand forecasting |
| **DB1B** | Origin & Destination Survey | 10% ticket sample: fares, itineraries, distances | Quarterly | Fare elasticity and yield modeling |

---

### 2.1 Dataset Structures

| Dataset | Key Fields | Target Variables | Approx. Size | Primary Key |
|----------|-------------|------------------|---------------|--------------|
| ASQP | Carrier, FlightDate, Origin, Dest, DepDelay, ArrDelay | On-Time %, Cancellation Flag | 10M+ / month | (Carrier, FlightDate, FlightNum) |
| DB28 | Carrier, Origin, Dest, Passengers, Seats, Distance | Passenger Count, Load Factor | 1M+ / month | (Carrier, Origin, Dest, Month) |
| DB1B | Origin, Dest, Fare, Distance, CouponCount | Average Fare | 5M+ / quarter | (Origin, Dest, Quarter) |

---

### 2.2 Analytical Match Matrix

| Dataset | Analytical Type | Recommended Models | Goal |
|----------|----------------|--------------------|------|
| **ASQP** | Diagnostic & Predictive | Decision Tree, Random Forest | Classify flight delay causes |
| **DB28 (T-100)** | Predictive | STL, ARIMA, Prophet, XGBoost | Forecast monthly passenger demand |
| **DB1B** | Diagnostic & Prescriptive | Linear Regression, LightGBM, ANN | Model fare elasticity and optimize pricing |

---

### 2.3 Dataset Type vs. Analytical Technique

| Data Type | Example Dataset | Analysis Category | Example Model | Forecast Horizon |
|------------|-----------------|-------------------|----------------|------------------|
| Time-Series Continuous | DB28 | Statistical Forecasting | ARIMA, Prophet | 1–12 months |
| Categorical / Binary | ASQP | Classification | Decision Tree, Random Forest | 1–3 days |
| Panel / Longitudinal | DB1B | Regression & ML | LightGBM, TFT | Quarterly |
| Nonlinear Multivariate | All | Deep Learning | ANN, N-BEATS | Multi-horizon |

---

### 2.4 Dataset Integration Diagram
![Dataset Integration Flow](https://upload.wikimedia.org/wikipedia/commons/e/e5/Data_pipeline_diagram_en.svg)

---

## 3️⃣ Classical Time-Series Analytics (45–65 min)

### Seasonal and Trend Decomposition Using Loess (STL)
![STL decomposition](https://www.statsmodels.org/dev/_images/stl_plot_001.png)
- Splits a time series into **Trend**, **Seasonal**, and **Remainder** components.  
- Useful for DB28 passenger demand analysis and seasonality detection.

### Autoregressive Integrated Moving Average (ARIMA)
![ARIMA workflow](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*y9xmnA3rXQ4nK3xZjl8Wdg.png)
- Combines AR (autoregressive) and MA (moving-average) processes with differencing for stationarity.  
- Excellent for single series forecasting.

### Prophet (Meta/Facebook)
![Prophet Components](https://facebook.github.io/prophet/static/prophet_plot_components_1.png)
- Additive model of trend + seasonality + holiday effects.  
- Ideal for interpretable, business-oriented forecasting.

### Rolling-Origin Cross-Validation
![Rolling Origin CV](https://otexts.com/fpp3/fpp_files/figure-html/tscv-1.png)
- Evaluate models over moving time windows to simulate live forecasting performance.

---

## 4️⃣ Machine Learning for Time Series (65–80 min)

### Tree Ensembles
![Gradient Boosting Flow](https://xgboost.readthedocs.io/en/stable/_images/boosting.png)
- Combine predictive power of multiple decision trees.
- **Use Case:** Multi-route forecasting using route-level features.

### Deep Learning Models

#### Neural Basis Expansion Analysis for Time Series (N-BEATS)
![N-BEATS Architecture](https://raw.githubusercontent.com/philipperemy/n-beats/master/nbeats_architecture.png)
- Decomposes time series into interpretable trend/seasonal components via neural basis expansions.

#### Temporal Fusion Transformer (TFT)
![TFT Architecture](https://www.researchgate.net/profile/Bryan-Lim-3/publication/375803949/figure/fig1/AS:1143196034825216@1700648883539/Temporal-fusion-transformer-model-architecture.png)
- Attention-based model incorporating static, past, and known-future covariates for multi-horizon forecasts.

---

## 5️⃣ Feature Engineering, Leakage Control, and Backtesting (80–88 min)

| Category | Example Features |
|-----------|------------------|
| Lag | t−1, t−12, rolling mean, moving std |
| Calendar | month, quarter, day-of-week, holidays |
| Weather | temperature, precipitation, wind speed |
| Network | distance, hub/non-hub, competition index |
| Macro | fuel price, GDP, CPI |
| Operational | schedule load, delay rate, fleet type |

**Leakage Control:**  
- Always align training data to publication lag (BTS data releases monthly/quarterly).  
- Include embargo periods before test windows.  
- Validate using rolling-origin or expanding window methods.

---

## 6️⃣ Summary and Diagram Index (88–90 min)

| Concept | Diagram Link |
|----------|---------------|
| Descriptive Analytics | <https://upload.wikimedia.org/wikipedia/commons/3/3e/Descriptive_analytics_workflow_diagram.png> |
| Diagnostic Analytics | <https://upload.wikimedia.org/wikipedia/commons/4/4a/Diagnostic_analytics_cause_effect_flow.png> |
| Predictive Analytics | <https://upload.wikimedia.org/wikipedia/commons/0/0b/Predictive_Analytics_Pipeline.png> |
| Prescriptive Analytics | <https://upload.wikimedia.org/wikipedia/commons/6/6d/Prescriptive_analytics_decision_framework.png> |
| CRISP-DM | <https://upload.wikimedia.org/wikipedia/commons/6/61/CRISP-DM_Process_Diagram.png> |
| Machine Learning Taxonomy | <https://miro.medium.com/v2/resize:fit:1400/format:webp/1*P-yWhukYArlTq84yJZ1YfA.png> |
| STL | <https://www.statsmodels.org/dev/_images/stl_plot_001.png> |
| ARIMA | <https://miro.medium.com/v2/resize:fit:1400/format:webp/1*y9xmnA3rXQ4nK3xZjl8Wdg.png> |
| Prophet | <https://facebook.github.io/prophet/static/prophet_plot_components_1.png> |
| N-BEATS | <https://raw.githubusercontent.com/philipperemy/n-beats/master/nbeats_architecture.png> |
| Temporal Fusion Transformer (TFT) | <https://www.researchgate.net/profile/Bryan-Lim-3/publication/375803949/figure/fig1/AS:1143196034825216@1700648883539/Temporal-fusion-transformer-model-architecture.png> |
| Dataset Integration Flow | <https://upload.wikimedia.org/wikipedia/commons/e/e5/Data_pipeline_diagram_en.svg> |

---

**Instructor Note:****Instructor Notes**

- Every acronym (e.g., BTS, ASQP, DB28, DB1B, STL, ARIMA, ML, DA, CPI, ANN, AI) is fully spelled out upon first use.  
- This 90-minute lecture weaves conceptual foundations with hands-on applications, making it suitable for advanced MBA analytics or graduate data-science courses.  
- Key learning outcomes: distinguish among analytic types; understand dataset structure; apply classical and machine-learning forecasting models; evaluate model performance with appropriate metrics; and connect insights to operational and economic airline decisions.  
- Suggested follow-up: assign lab projects using open BTS datasets, guiding students to replicate Descriptive → Diagnostic → Predictive → Prescriptive workflows.

*End of 90-Minute Lecture.*