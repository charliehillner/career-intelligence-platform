# Roadmap

This document describes the implementation roadmap of the Career Intelligence Platform.

The project is developed through small vertical increments rather than as one large implementation effort.

Each milestone has a clearly defined scope and Definition of Done.

The general development strategy is:

```text
Model
  ↓
Document
  ↓
Implement
  ↓
Test
  ↓
Evaluate
  ↓
Extend
```

The first major portfolio release is **MVP 1**.

---

# MVP 1 — Explainable Career Intelligence Baseline

## Goal

MVP 1 demonstrates an end-to-end Career Intelligence pipeline that:

- processes job-market data,
- stores it in a dimensional analytical model,
- represents a personal skill profile,
- calculates explainable Job-Person matches,
- and exposes market and matching information through Power BI.

For MVP 1, Job-Person Matching is deliberately restricted to Qualification Fit based on skills:

$$
M_{\text{V1}}(P,J) = Q_{\text{V1}}(P,J) = m_{\text{Skills}}(P,J).
$$

The purpose of MVP 1 is not to build the complete Career Intelligence Platform.

It is intended to establish a simple, explainable and reproducible baseline that can later be evaluated and extended.

---

# MVP 1A — Data Foundation

## Objective

Create the persistent data foundation required by the platform.

```text
Docker
   ↓
PostgreSQL
   ↓
Database Schema
   ↓
Synthetic Job Postings
   ↓
Synthetic Personal Profile
```

## Tasks

- [x] Define conceptual data model
- [x] Define dimensional data model
- [x] Document architecture
- [x] Create Docker Compose configuration
- [x] Start PostgreSQL container
- [x] Verify database connectivity
- [x] Implement initial SQL schema
- [x] Create dimension tables
- [x] Create fact tables
- [x] Create bridge tables
- [x] Define synthetic job postings
- [x] Define synthetic personal profile
- [x] Load synthetic data into PostgreSQL
- [x] Verify relationships and constraints

## Definition of Done

MVP 1A is complete when a fresh PostgreSQL environment can represent the relevant V1 domain and contains a small synthetic dataset consisting of:

- one personal profile,
- personal skills,
- approximately 10–20 job postings,
- job requirements,
- and normalised skills.

The database must be sufficient to support the V1 Matching Engine without requiring external job data.

---

# MVP 1B — Intelligence Core

## Objective

Translate the mathematical matching specification into executable and testable code.

```text
Person P             Job J
    \                 /
     \               /
      +-------------+
             |
             v
      Matching Engine
             |
             v
        Q_V1(P,J)
             |
             v
        M_V1(P,J)
```

## Mathematical Scope

For MVP 1:

$$
M_{\text{V1}}(P,J) = Q_{\text{V1}}(P,J).
$$

Qualification Fit is restricted to Skill Fit:

$$
Q_{\text{V1}}(P,J) = m_{\text{Skills}}(P,J).
$$

Individual Skill Matches are based on:

- Proficiency Match
- Experience Match

Evidence remains available as descriptive information but is not numerically included in V1.

## Tasks

- [x] Define V1 Matching Model
- [x] Define Skill Matching architecture
- [x] Define Proficiency Matching baseline
- [x] Define Experience Matching baseline
- [x] Define individual Skill Match aggregation
- [x] Define overall Skill Fit aggregation
- [x] Implement Proficiency Match in Python
- [x] Implement Experience Match in Python
- [x] Implement individual Skill Match
- [x] Implement overall Skill Fit
- [x] Implement Qualification Fit
- [x] Add unit tests
- [x] Add end-to-end integration test for one complete job
- [x] Connect Python to PostgreSQL
- [x] Load synthetic person profile from DB
- [x] Load synthetic job requirements from DB
- [x] Calculate M_V1(P,J) for all synthetic jobs
- [x] Produce ranked job results
- [x] Preserve skill-level explanations for each score
- [x] Inspect ranking against qualitative expectations
- [x] Document observed limitations / surprising behaviour

## Definition of Done

MVP 1B is complete when the system can take one person and multiple synthetic job postings and produce reproducible, explainable V1 Match Scores.

The resulting ranking should be inspectable down to individual skills and matching components.

---

# MVP 1C — Real-World Data

## Objective

Replace controlled synthetic job inputs with real labour-market data.

The first planned external source is Adzuna.

```text
Adzuna
   ↓
Python Ingestion
   ↓
Raw Job Data
   ↓
PostgreSQL
   ↓
Extraction
   ↓
Normalisation
   ↓
Dimensional Model
   ↓
Matching Engine
```

## Tasks

- [x] Register / configure Adzuna API access
- [x] Retrieve first real job postings
- [x] Inspect raw API response structure
- [x] Identify available and missing attributes
- [x] Compare Adzuna representation with canonical model
- [ ] Load normalized real jobs through repository
- [ ] Run existing V1 matching engine
- [ ] Rank real job postings
- [ ] Inspect skill-level explanations
- [ ] Compare behaviour with synthetic evaluation

## Definition of Done

MVP 1C is complete when real external job postings can be transformed into the same normalised analytical representation used by the synthetic dataset and processed by the V1 Matching Engine.

The Matching Engine should not depend on whether a normalised job originated from synthetic or real data.

---

# MVP 1D — Analytics

## Objective

Expose market intelligence, personal analytics and explainable matching results through Power BI.

```text
PostgreSQL
     ↓
Power Query
     ↓
Power BI Semantic Model
     ↓
DAX
     ↓
Career Intelligence Dashboard
```

## Dashboard Scope

The first Power BI release should contain four primary analytical areas.

### Market Overview

Example questions:

- How many jobs are available?
- Which job profiles are most common?
- Which locations contain the most opportunities?
- What experience levels are requested?

### Skill Intelligence

Example questions:

- Which skills are most frequently requested?
- Which skills occur together?
- How does skill demand differ by job profile?
- How does skill demand differ by region?

### Personal Profile

Example information:

- personal skills,
- proficiency,
- experience,
- and available evidence.

### Job Fit

The central Decision Support page.

It should allow the user to:

- rank jobs by V1 Match Score,
- select an individual job,
- inspect Qualification Fit,
- inspect individual Skill Matches,
- inspect Proficiency Match,
- inspect Experience Match,
- and understand why a particular score was produced.

## Tasks

- [ ] Connect Power BI to PostgreSQL
- [ ] Implement Power Query ingestion
- [ ] Configure dimensional relationships
- [ ] Create core DAX measures
- [ ] Build Market Overview
- [ ] Build Skill Intelligence
- [ ] Build Personal Profile
- [ ] Build Job Fit page
- [ ] Add interactive filtering
- [ ] Add match explainability
- [ ] Validate dashboard results against source data
- [ ] Prepare portfolio screenshots and documentation

## Definition of Done

MVP 1D is complete when the complete pipeline

```text
Real Job Data
      ↓
Python
      ↓
PostgreSQL
      ↓
Matching Engine
      ↓
Power Query
      ↓
Power BI
```

produces an interactive dashboard that demonstrates both labour-market intelligence and explainable personal Job-Person Matching.

At this point, **MVP 1 is considered portfolio-ready**.

---

# MVP 1 — Explicit Non-Goals

The following features are deliberately excluded from MVP 1:

- Eligibility Fit
- Preference Fit
- advanced Qualification dimensions
- Seniority Fit
- Domain Knowledge Fit
- Evidence Scoring
- skill substitution
- skill ontology
- ontology-based skill similarity
- learned matching weights
- machine-learning-based matching
- application management
- application strategy recommendations
- learning recommendations
- shortest-path-to-job optimisation
- salary recommendations
- CV parsing
- user accounts
- multiple personal profiles
- Web Application frontend
- real-time ingestion

These concepts may be investigated in later versions.

---

# Beyond MVP 1

Potential future development areas include:

## Matching Model

- Eligibility Fit
- Preference Fit
- additional Qualification dimensions
- non-trivial skill weights
- nonlinear matching functions
- empirically calibrated parameters
- skill similarity
- skill ontology

## Decision Support

- skill-gap prioritisation
- learning recommendations
- application strategy
- target-company recommendations
- salary positioning
- career-path analysis
- shortest-path-to-job optimisation

## Data & Analytics

- additional job platforms
- historical market trends
- scheduled ingestion
- improved skill extraction
- geographical analysis
- salary analytics

## Model Evaluation

- application outcomes
- interview outcomes
- ranking evaluation
- sensitivity analysis
- model comparison
- empirical parameter calibration
- machine learning

---

# Current Status

```text
MVP 1
│
├── 1A Data Foundation       ← CURRENT
│
├── 1B Intelligence Core     ← MODEL DEFINED
│
├── 1C Real-World Data
│
└── 1D Analytics
```

The immediate next milestone is:

> **Complete MVP 1A by implementing the PostgreSQL schema and loading the first synthetic dataset.**
