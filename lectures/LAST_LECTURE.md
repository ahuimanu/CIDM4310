# BI, Data Analytics & Decision Science, ML, and AirlineOps — 70-Minute Last Lecture + Case

> BI = Business Intelligence  
> Data Analytics & Decision Science = Data Analytics & Decision Science  
> ML = Machine Learning  

---

## 0. Opening Frame (0–5 min)

**Purpose:** Connect the whole course into one loop and one concrete case.

Key points:

- "Tonight I want to show you that **Business Intelligence**,  
  **Data Analytics & Decision Science**, and  
  **Machine Learning (ML)** are **not three silos**."
- “They are three angles on one continuous loop:  
  **Data → Information → Knowledge → Decision → Action → (back to Data)**.”
- “We’ll walk that loop twice:
  1. In the abstract, with a diagram.
  2. In a concrete airline planning case using **DB28**, **DB1B**, **ASQP**, plus **ARIMA** and **XGBoost**.”

---

## 1. The Data → Information → Knowledge → Decision → Action Loop (5–15 min)

### 1.1 The outer loop

    DATA → INFORMATION → KNOWLEDGE → DECISION → ACTION → (back to DATA)

Draw or show this on the board/slide:

    ┌─────────────────────────────────────────────┐
    │                                             │
    │                 KNOWLEDGE                   │
    │                                             │
    └───────────────▲───────────────▲─────────────┘
                    │               │
                    │  interpret    │ apply to
                    │  & integrate  │ a situation
                    │               │
             ┌──────┴──────┐   ┌────┴─────┐
             │ INFORMATION │   │ DECISION │
             └──────▲──────┘   └────▲─────┘
                    │               │
                    │ organize      │ implement
                    │ & contextual. │
                    │               │
                 ┌──┴───┐       ┌───┴───┐
                 │ DATA │◄─────┤ ACTION│
                 └──▲───┘  records of… └───────┐
                    │                          │
                    └─────────observations─────┘

Explain:

- **Data** — recordings of actions and events (bookings, flights, clicks, payments).
- **Information** — data organized and contextualized (tables, metrics, dashboards).
- **Knowledge** — information integrated into a mental model  
  (“this is a seasonal route,” “this is business-heavy,” etc.).
- **Decision** — choosing among options with trade-offs  
  (“increase frequency?” “raise price?” “enter or exit this market?”).
- **Action** — implementing the decision (change schedule, price, marketing),  
  which creates new **data**.

Key line:

> "Your entire BI / Data Analytics & Decision Science / ML career will live somewhere on this loop."

### 1.2 Inner core: what we’re really trying to get from data

Draw the inner triangle/cycle:

    ┌───────────────┐
    │   MEANING     │
    └──────▲────────┘
           │
    ┌──────┴───────┐
    │    VALUE     │
    └──────▲───────┘
           │
    ┌──────┴───────┐
    │     DATA     │
    └──────────────┘

Interpretation:

- We start with **data**, but what we actually care about is:
  - **Meaning** — do we understand what is going on in the system?
  - **Value** — can we change something in a way that matters?
    (profit, safety, service quality, fairness, resilience).

---

## 2. Where BI, Data Analytics & Decision Science, and ML Live on the Loop (15–25 min)

Show or say this mapping:

    DATA → INFORMATION → KNOWLEDGE → DECISION → ACTION → (back to DATA)
     |         |              |          |
     |         |              |          └─ Data Analytics & Decision Science & ML
     |         |              └──────────── Data Analytics & Decision Science
     |         └─────────────────────────── BI & Data Analytics & Decision Science
     └───────────────────────────────────── BI

### 2.1 Business Intelligence (BI)

- Primarily **Data → Information → early Knowledge**.
- Work:
  - Data pipelines and warehouses  
    (e.g., turning raw DB28/DB1B/ASQP into consistent aviation_core tables).
  - Metric definitions (“What exactly is ‘load factor’ here?”).
  - Dashboards and reports that decision-makers actually use.
- Without BI:
  - Decision meetings become “whose numbers are right?” instead of  
    “what should we do?”.

### 2.2 Data Analytics & Decision Science — Data Analytics & Decision Science

- Lives mostly in **Information → Knowledge → Decision**.
- Work:
  - Ask *why* questions, not just *what*:
    - "Why is this route underperforming?"
    - "What happens if we add a frequency or change price?"
  - Statistical modeling, causal inference, experiments, optimization.
  - Structuring trade-offs and scenarios.
- Without Data Analytics & Decision Science:
  - Lots of charts, but decisions revert to anecdotes, politics, and habit.

### 2.3 Machine Learning (ML)

- Operates across **Data ↔ Decision ↔ Action** at scale.
- Work:
  - Learn patterns from historical data.
  - Predict outcomes (demand, churn, delay risk, etc.).
  - Embed models into systems so thousands of micro-decisions happen automatically.
- Without ML:
  - All decisions remain manual; you can’t scale fine-grained personalization,  
    pricing, or routing decisions.

Transition line:

> "BI keeps the loop **honest**, Data Analytics & Decision Science keeps it **thoughtful**, and ML lets it run at **scale**."

---

## 3. Historical Arc: How We Got Here (25–35 min)

High-level, compressed overview:

1. **PCs and relational databases (’70s–’90s)**  
   - Relational databases, SQL, OLTP systems.  
   - Early reporting and OLAP cubes. Classic BI roots.

2. **Internet & Web era (mid ’90s–2000s)**  
   - Web traffic, clickstreams, e-commerce logs.  
   - Web analytics tools; faster, more interactive dashboards.

3. **“Big Data” & Cloud (2010s)**  
   - Cheap compute and storage; data lakes; NoSQL; streaming.  
   - Emergence of the “data scientist” role.

4. **AI / ML & LLM era (late 2010s–now)**  
   - Deep learning for search, ads, recommendations, pricing, routing.  
   - Time-series models, gradient boosting, transformers.  
   - Now LLMs: text, code, planning.

Connect back to the loop:

> “The tech stack changed dramatically, but the loop didn’t.  
> We just got better at collecting more **data**, turning it into **information** faster,  
> and pushing more **decisions** closer to real time.”

---

## 4. AirlineOps / aviation_core in the Loop + ARIMA & XGBoost (35–50 min)

Anchor the concepts in your own project.

### 4.1 Where aviation_core lives on the loop

Map AirlineOps / aviation_core stages:

- **Action**  
  Real or simulated airline behavior:
  - Flights flown, tickets sold, delays, cancellations, fares, schedules.

- **Data (aviation_core resolve / download / normalize)**  
  - BTS DB28 (segment & market), DB1B (tickets/coupons), ASQP (on-time), T100, NASR, etc.
  - aviation_core’s job:
    > “Turn messy DOT files into consistent tables with strong keys and invariants.”

- **Information (stage / curated + BI)**  
  - Aggregations and pivots:
    - pax per route per quarter,
    - yields and load factors,
    - delay distributions by route and carrier.
  - This is your BI layer: dashboards on markets, routes, seasonality, reliability.

- **Knowledge (models & doctrine)**  
  - Recognized patterns:
    - “These are cruise-driven routes.”
    - “These are ski markets.”
    - “These are thin, business-heavy routes.”
  - Captured in analytics, documentation, and your mental model of the network.

- **Decision (network & schedule planning)**  
  - Example questions:
    - “Should we launch AMA–SAT?”
    - “What frequencies and timings?”
    - “Seasonal or year-round?”

- **Action (schedule + pricing + simulation)**  
  - Update planned schedule, run simulations, eventually operate flights (real or sim).  
  - New performance data flows back into aviation_core → the loop restarts.

### 4.2 ARIMA in this context (univariate TS baseline)

Explain ARIMA in airline language:

- **AR (AutoRegressive)**  
  Today’s demand depends on **past** demand.

- **I (Integrated)**  
  Differencing to remove trend/seasonality so the series is roughly stationary.

- **MA (Moving Average)**  
  Today’s value depends partly on past **shocks/errors**.

For a route like AMA–SAT (or a corridor AMA–SAT via hubs):

1. Build a **quarterly pax series** from DB28 or your curated tables.  
   (Passengers per quarter on AMA–SAT, maybe including connections if no nonstop exists yet.)
2. Plot it: look for trend, seasonal peaks, structural breaks.
3. Difference appropriately (e.g., 1st difference + seasonal difference at lag 4 for quarterly).
4. Fit a SARIMA model.
5. Forecast next 8 quarters as a **baseline**.

Framing:

> “ARIMA gives us a **transparent baseline forecast** for each series:  
> ‘If nothing dramatic changes, here’s how this corridor behaves over time.’”

### 4.3 XGBoost in this context (feature-rich ML model)

Explain XGBoost conceptually:

- Gradient-boosted decision trees for tabular data.
- Can learn complex nonlinear interactions among many features.

For AirlineOps / aviation_core:

- Build a feature table across many routes and periods:
  - Route-level:
    - Origin, destination, distance, region, fleet type.
  - Time-level:
    - Year, quarter, month, holiday and school-break flags.
  - Market structure:
    - Competitor count, total seats, LCC presence.
  - Reliability:
    - Avg delay, cancellation rates (from ASQP).
  - Exogenous:
    - Road drivable indicator (drive vs fly), maybe cruise or snow indices for other markets.
  - Time-series lags:
    - pax last quarter, pax last year, etc.

- Train XGBoost to predict:
  - Pax per route per period, or
  - Load factor, or
  - Revenue per flight.

Framing:

> “XGBoost gives us a **feature-driven, cross-route forecast** that:
>
> - Learns from many routes at once,
> - Uses multiple signals (price, competition, reliability, etc.),
> - Can predict for new or lightly-served routes like AMA–SAT.”

Contrast:

- ARIMA: **per-series, interpretable, history-driven** baseline.  
- XGBoost: **cross-sectional + temporal, nonlinear, feature-driven** model.

Transition:

> “Now let’s spend the last 20 minutes walking a single planning problem —  
> **AMA–SAT** — through the entire loop with DB28, DB1B, ASQP, ARIMA, and XGBoost.”

---

## 5. Case (50–70 min): Should Caprock Launch AMA–SAT?

We’ll use **five planning questions** to show how all the data and techniques fit together.

### Case Setup (50–52 min)

Caprock Connect is considering a **year-round (or strong seasonal) AMA ↔ SAT** service:

- Mix of **business** (state government, military, medical) and **leisure**  
  (River Walk, Alamo, I-35 corridor).
- Realistic competition:
  - Drive vs fly pressure (Panhandle → San Antonio by car),
  - Connections via DFW/DAL/AUS/IAH on incumbents.

Available data via aviation_core:

- **DB28** — segment & market volumes, seats, load factors on real routes.
- **DB1B** — 10% ticket sample with O&D and fares.
- **ASQP** — flight-level on-time and delay statistics.

Available tools:

- **BI** — curated tables, dashboards, basic comparisons.
- **DADS** — economic and statistical reasoning.
- **ARIMA** — route-level time-series baselines.
- **XGBoost** — feature-rich demand prediction across many routes.

Five questions:

1. Is there enough underlying O&D demand in the AMA–SAT corridor?  
2. What kind of operational reliability environment are we walking into?  
3. Is there a plausible profit envelope at realistic prices and load factors?  
4. What is the “business-as-usual” demand baseline over time?  
5. Under different scenarios, what happens if we actually launch AMA–SAT?

---

### Q1 — Is There Enough O&D Demand in the Corridor? (52–56 min)

**Question:**  
> “How many people already travel between the Amarillo area and the San Antonio area, and when?”

**Data & BI:**

- **DB28 (market)**:
  - O&D passengers and seats between **AMA ↔ SAT** (if any historical nonstops existed).
  - Proxy flows:
    - AMA–DFW–SAT, AMA–DAL–SAT, AMA–IAH–SAT, etc.
  - Seasonal pattern by quarter or month.
- **DB1B (tickets + coupons)**:
  - O&D tickets with origin AMA and destination SAT (including connections).
  - Fare distribution (what people actually pay now).
  - Route choices: which hubs they go through most often.

**BI outputs:**

- Time series: AMA–SAT O&D pax per quarter.
- Fare distribution: mean, median, quartiles for AMA–SAT round trips.
- Routing split: % via DFW, DAL, IAH, etc.

**Loop mapping:**

- **Data → Information**:
  - Raw DB28/DB1B → grouped and aggregated tables.
- **Information → Knowledge**:
  - “There are ~X AMA–SAT O&D passengers per quarter with [weak/moderate/strong] seasonality.”
  - “The typical round-trip fare is about \$Y, with most traffic routed via DFW and DAL.”

Now we know whether there is **latent AMA–SAT demand** worth considering.

---

### Q2 — What Is the Operational Quality of the Existing Service? (56–59 min)

**Question:**  
> “If we compete in this corridor (offering a nonstop vs connections),  
> what delay and reliability environment are we stepping into?”

**Data & BI + Data Analytics & Decision Science:**

- **ASQP**:
  - On-time performance, delays, and cancellations for:
    - AMA–DFW, AMA–DAL, AMA–IAH,
    - DFW–SAT, DAL–SAT, IAH–SAT, AUS–SAT, etc.
  - Statistics by carrier, time of day, month/season.

**BI outputs:**

- On-time % by route and by month.
- Delay distributions (0–15, 15–60, 60+ minutes).
- Cancellation rates across the relevant legs.

**Data Analytics & Decision Science reasoning:**

- Estimate connection risk for typical AMA–SAT itineraries:
  - Probability that a two-leg AMA–hub–SAT itinerary has a misconnect or ≥60-minute delay.
- Compare to a hypothetical **AMA–SAT nonstop**:
  - Nonstop offers:
    - Shorter elapsed time,
    - Lower connection risk,
    - Potentially more predictable arrival.

**Loop mapping:**

- **Data → Information**:
  - Individual flight records → reliability metrics by route and carrier.
- **Information → Knowledge**:
  - “DFW in summer has higher thunderstorm delays; DAL may be more stable;  
    IAH is more weather-sensitive in certain seasons.”

This informs schedule design, time-of-day choice, and how much **reliability premium** you might claim for a nonstop.

---

### Q3 — Can We Make Money at Realistic Prices? (59–63 min)

**Question:**  
> “Given what people currently pay to go AMA–SAT, and realistic Q400/RJ economics,  
> can this route be profitable?”

**Data & Data Analytics & Decision Science:**

- **DB1B**:
  - Fare distribution for AMA–SAT O&D:
    - Mean, median, quartiles, business vs leisure proxies.
  - Advance purchase patterns, day-of-week patterns.
- **DB28**:
  - Load factors and yields on similar Texas small-city ↔ large-city routes.
  - Identify analogs (e.g., LBB–SAT, MAF–SAT, AMA–AUS analogs).

**Data Analytics & Decision Science calculation:**

- Assume:
  - Aircraft: Q400 or ERJ-145,
  - Seats,
  - Cost per block hour,
  - Stage length ≈ AMA–SAT.
- Scenario grid:
  - Load factor: 55%, 65%, 75%.
  - Average one-way fare: P25, median, P75 from DB1B.
- Compute:
  - Revenue per flight vs cost per flight,
  - Rough break-even load factor and fare.

**Loop mapping:**

- **Information → Knowledge**:
  - “At current market fares, we need about L% load factor to break even.”
  - “With a slight convenience premium for nonstop, we might push fares slightly above hub-connection levels.”

Now we have a **financial feasibility envelope** for AMA–SAT.

---

### Q4 — What Does the Baseline Demand Pattern Look Like Over Time? (63–66 min)

**Question:**  
> “If we just extrapolate historical AMA–SAT behavior, what demand do we expect over time?”

**Data & ARIMA (Data Analytics & Decision Science + simple ML):**

- Construct a **quarterly AMA–SAT O&D pax series**:
  - From DB28/DB1B, count how many AMA–SAT O&D pax per quarter (mostly connections).
- Visualize:
  - Trend: flat, growing, or declining?
  - Seasonality: summer or holiday peaks?
  - Structural breaks (e.g., COVID, airline exits).

**ARIMA/SARIMA:**

1. Difference the series to remove trend and seasonal pattern (e.g., lag 4).
2. Fit a SARIMA model (SARIMA(p,d,q)(P,D,Q)\_4 for quarterly).
3. Forecast the next 8 quarters of AMA–SAT demand under “business as usual”.

**Use:**

- Treat this as the **baseline** if no Caprock nonstop appears:
  - Incumbents continue via hubs, similar capacity and competition.
- Any Caprock scenario is compared to this baseline:
  - Uplift vs that business-as-usual curve.

**Loop mapping:**

- **Information → Knowledge → Decision**:
  - ARIMA turns the historical AMA–SAT pattern into a concrete forecast trajectory to plan against.

---

### Q5 — Under Different Scenarios, What Happens If We Launch AMA–SAT? (66–70 min)

**Question:**  
> “Given fares, competition, reliability, seasonality, and network patterns,  
> what demand do we expect if Caprock launches AMA–SAT?”

**Data, XGBoost, and full loop:**

1. **Feature engineering (aviation_core → ML table)**  
   Build a table where each row is (route, time period) with:

   - Route features:
     - Origin, destination, distance, region, fleet.
   - Time features:
     - Year, quarter, month, holiday, school-break flags.
   - Market structure:
     - Competitor count, total seats, presence of LCC.
   - Reliability (from ASQP):
     - Avg delay, cancellation rate for that route.
   - Road/drivability proxy:
     - Indicator for “drivable within X hours” to capture drive vs fly.
   - Time-series lags:
     - Pax in t–1, t–4, etc.
   - Target:
     - pax per route per period.

2. **Train XGBoost regressor**

   - Learn relationships like:
     - “Small-city ↔ big-city with short drive alternative behaves differently than pure air-only pairs.”
     - “Business-heavy routes maintain demand even at higher fares; leisure-heavy routes are more elastic.”

3. **Construct AMA–SAT scenarios**

   For each scenario, create feature rows for hypothetical **Caprock AMA–SAT nonstop**:

   - Inputs:
     - Nonstop AMA–SAT with Q400,
     - Frequency:
       - e.g., 2x daily weekdays, 1x weekends, or seasonal only.
     - Pricing:
       - At parity with existing connection fares,
       - Slight premium for convenience,
       - Or promotional discount for entry.
     - Expected reliability:
       - Assume better on-time performance vs two-leg connections.
   - Feed these rows into XGBoost to get predicted pax per quarter under each scenario.

4. **Compare and choose**

   - Compare XGBoost scenario forecasts to:
     - ARIMA baseline (Q4, business-as-usual via connections),
     - Economic envelope (Q3: load factor vs fare vs cost),
     - Reliability and operational constraints (Q2).
   - Use Data Analytics & Decision Science thinking to evaluate:
     - Risk vs return,
     - Seasonality (maybe start as peak-season service),
     - Impact on fleet utilization and network.

**Full loop recap:**

- **Data** — DB28, DB1B, ASQP, plus any exogenous indicators (road, macro).
- **Information** — cleaned and aggregated AMA–SAT views (BI).
- **Knowledge** — demand patterns, reliability profiles, economic thresholds, ARIMA baseline, XGBoost scenarios.
- **Decision** — e.g., “Launch AMA–SAT with 2x daily Q400 on weekdays and 1x on weekends,  
  price near-parity with connection fares but sell convenience and reliability.”
- **Action** — implement schedule and pricing; later observe realized data, feed back into aviation_core, and restart the loop.

---

## Final Wrap (last 60–90 seconds)

Tie it together explicitly:

- "In 70 minutes we:
  - Built a **conceptual loop**: Data → Information → Knowledge → Decision → Action.
  - Mapped **BI**, **Data Analytics & Decision Science**, and **ML** onto that loop.
  - Anchored the whole thing in **aviation_core / AirlineOps**.
  - Ran an actual **AMA–SAT planning case** using DB28, DB1B, ASQP, plus ARIMA and XGBoost.”

Closing line:

> "Data work is decision work.  
> BI helps us **see** clearly,  
> Data Analytics & Decision Science helps us **reason** clearly,  
> and ML helps us **scale** those decisions —  
> whether we're talking about dashboards in a bank, or a Q400 between Amarillo and San Antonio."

Optional 1-minute reflection prompt:

- "Write down:
  1. One place in this loop where you already feel strong (BI, Data Analytics & Decision Science, or ML), and
  2. One place you want to grow over the next 5 years.”

  ## Final Requirement: Texas New Air Service Planning Mini-Case (5-Page Cap)

### Purpose

To close the course, you will **apply the full BI → Data Analytics & Decision Science → ML lifecycle** to a self-chosen **new air service concept within Texas**. You will design and narrate how an airline (real or fictional) could use **DB28**, **DB1B**, **ASQP**, plus **synthetic / external signals** to evaluate and forecast a set of **Texas city-pair routes**.

The goal is **not** to build a perfect model or full network plan, but to demonstrate that you can:

- Ask **good questions** of each dataset,  
- Connect those questions to the **Data → Information → Knowledge → Decision → Action** loop,  
- Show how forecasting (e.g., ARIMA / XGBoost or similar) would fit into that loop, even if only conceptually.

You will capture this work in a **single narrative report (Markdown, ≤ 5 pages)** plus any supporting notebooks/code you wish to attach.

---

### Scenario

You are advising a new or expanding airline that wants to develop **new intra-Texas air service**. Examples (you can pick any you like, including but not limited to):

- AMA–SAT, AMA–AUS, AMA–HOU, AMA–DAL, AMA–DFW  
- LBB–SAT, LBB–AUS, LBB–HOU  
- MAF–SAT, MAF–AUS, MAF–HOU  
- Any other Texas city-pairs that interest you (small city ↔ large city, regional ↔ major hub, etc.).

The airline wants to:

- Identify **promising candidate routes** among Texas city pairs,  
- Understand **current travel behavior** (drive vs fly, connect vs nonstop),  
- Assess **operational reliability environments**,  
- Build at least **baseline demand expectations** and see how ML-style forecasting might improve those expectations.

---

### Question Design Requirements

You must formulate and use a total of **20 questions**, structured as:

- **5 questions using DB28** (segment/market volume, seats, load factors, yields, etc.)  
- **5 questions using DB1B** (O&D, fares, itineraries, drive-vs-fly behavior, etc.)  
- **5 questions using ASQP** (delays, cancellations, on-time performance, carrier and route reliability, etc.)  
- **5 synthetic questions** that:
  - Combine signals (e.g., DB28 + DB1B + ASQP), and/or  
  - Bring in plausible external or derived indicators (e.g., drive time, population, economic profile, event calendars).

Each question should be written in **plain language**, and each should connect to at least one layer of the loop:

- DATA → INFORMATION  
- INFORMATION → KNOWLEDGE  
- KNOWLEDGE → DECISION  
- DECISION → ACTION

You do **not** need to fully “solve” every question, but you should be able to explain:

- **What** you would compute or visualize,  
- **Why** the question matters to the airline’s planning problem,  
- **How** the answer would inform subsequent decisions.

---

### Report Deliverable (Markdown, ≤ 5 Pages)

Your primary deliverable is a **Markdown report** (not to exceed 5 pages if printed) that includes:

1. **Introduction (½–1 page)**  
   - Briefly describe:
     - Your chosen Texas city-pairs,  
     - The airline’s strategic interest (business, leisure, connectivity, etc.),  
     - The overall planning question (e.g., “Should we launch AMA–SAT and AMA–AUS, and under what conditions?”).

2. **BI / Data Landscape Overview (½–1 page)**  
   - Summarize:
     - What DB28, DB1B, and ASQP each contribute to your case,  
     - How you conceptually move from **raw data → information** (tables, dashboards, summary stats),  
     - Any notable data limitations (sampled data, missing fields, coarse granularity).

3. **Question Sets by Dataset (≈ 2 pages total)**  
   Organize by dataset:

   - **DB28 Section**  
     - List your 5 DB28-driven questions.  
     - For each question:
       - Explain what you would compute (e.g., pax per quarter, load factors, comparable market analogs),  
       - Show or describe the kind of chart/table you would use,  
       - State what kind of **knowledge** the airline gains (e.g., size, seasonality, competitive pressure).

   - **DB1B Section**  
     - List your 5 DB1B-driven questions.  
     - Emphasize:
       - O&D behavior (routes, hubs, frequencies),  
       - Fare distributions,  
       - Drive-vs-fly patterns.  
     - Connect these to **pricing, product, and target-market decisions**.

   - **ASQP Section**  
     - List your 5 ASQP-driven questions.  
     - Focus on:
       - Delay profiles, cancellation rates, carrier differences, time-of-day and seasonal risk.  
     - Explain how this informs:
       - Schedule design,  
       - Nonstop vs connect value proposition,  
       - Risk/uncertainty in delivering the proposed product.

   - **Synthetic / Integrated Questions Section**  
     - List your 5 synthetic questions that **combine**:
       - Multiple DOT datasets, and/or  
       - External proxies (drive times, population, event calendars, etc.).  
     - Show how these questions:
       - Tie together economics, reliability, and customer behavior,  
       - Lead toward ***network-level*** or ***portfolio-level*** thinking.

4. **Forecasting and Planning Concept (½–1 page)**  
   - Based on your questions and insights, sketch how you would:
     - Build a **baseline time-series forecast** (e.g., ARIMA/SARIMA) for one or more routes, and  
     - Extend to a **feature-based ML model** (e.g., XGBoost-style) using:
       - Route characteristics (distance, city sizes),  
       - Market structure (competitors, seats),  
       - Temporal features (seasonality, holidays),  
       - Reliability metrics (average delay, cancellations).
   - You do **not** need to fully implement the models, but you should:
     - Clearly distinguish what ARIMA would do vs what a boosted-tree model would add,  
     - Explain how forecasts would influence **frequency**, **seasonality**, and **pricing** decisions.

5. **Conclusion (½ page)**  
   - Reflect on:
     - Which questions were most powerful or surprising,  
     - Where the data is strong vs weak,  
     - How this BI/DADS/ML lens changes your thinking about launching new Texas routes.

Remember: the Markdown report is narrative-first. Use bullet points, numbered lists, and small tables or figures as needed, but keep the story **coherent** and **decision-focused**.

---

### Supporting Artifacts (Optional but Encouraged)

You may submit **supporting notebooks or scripts** (Python, R, SQL, etc.) that:

- Demonstrate how you would:
  - Extract basic DB28/DB1B/ASQP subsets,  
  - Produce simple descriptive charts or tables,  
  - Sketch an ARIMA baseline or a simple ML model (even on toy data).

These supporting artifacts are **not graded for production quality**; they are evidence that you can move from:

- **Questions → Queries → Simple Models → Interpretations.**

The primary grading focus remains on the **clarity, structure, and depth** of your Markdown narrative.

---

### Evaluation Focus

Your work will be evaluated on:

- **Question quality**  
  - Are your 20 questions meaningful, non-trivial, and clearly aligned with the airline planning problem?

- **Lifecycle reasoning**  
  - Do you explicitly and coherently move through:
    - Data → Information → Knowledge → Decision → (proposed) Action?

- **Integration across datasets**  
  - Do you show how DB28, DB1B, ASQP, and synthetic signals  
    complement one another, rather than acting as isolated silos?

- **Forecasting awareness**  
  - Do you give a sensible, technically plausible picture of how ARIMA-like and ML-like approaches would be used,  
    even if you do not fully implement them?

- **Communication**  
  - Is your Markdown report well-structured, readable, and ≤ 5 pages if printed?
  - Does it read like something a data-literate manager or planner could actually act on?

The intent is that, by the time you complete this, you can **look at any pair (or small set) of Texas cities** and say:

- "Here is what we know from DOT data,"  
- "Here is what we still don't know,"  
- "Here is how we would build forecasts and plan a route launch,"  
- "And here's how BI, Data Analytics & Decision Science, and ML all showed up in that reasoning."
