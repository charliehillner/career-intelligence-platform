# Architecture

This document describes the technical architecture and data flow of the Career Intelligence Platform.

The architecture is designed around a clear separation of responsibilities:

- data acquisition and preprocessing,
- persistent storage,
- dimensional modelling,
- mathematical matching logic,
- and analytical visualisation.

The primary V1 data flow is:

```text
Data Sources
    |
    v
Python
    |
    v
PostgreSQL
    |
    v
Power Query
    |
    v
Power BI
```

The architecture intentionally keeps the mathematical matching model separate from the reporting layer.

---

# 1. Architectural Goals

The architecture should support the following goals:

- reproducible data processing,
- clear separation of concerns,
- persistence of raw and processed data,
- dimensional modelling using a star schema,
- explainable implementation of the Job-Person Matching Model,
- extensibility for additional job platforms,
- and straightforward consumption by Power BI.

The system should remain simple enough for an initial portfolio implementation while allowing later extensions.

---

# 2. High-Level Architecture

```text
+----------------------+
|     Data Sources     |
|                      |
| Job APIs / CSV /     |
| manual profile data  |
+----------+-----------+
           |
           v
+----------------------+
|        Python        |
|                      |
| Acquisition          |
| Parsing              |
| Normalisation        |
| Matching Logic       |
+----------+-----------+
           |
           v
+----------------------+
|     PostgreSQL       |
|                      |
| Raw Data             |
| Dimensional Model    |
| Match Results        |
+----------+-----------+
           |
           v
+----------------------+
|     Power Query      |
|                      |
| Import               |
| Light Transformation |
| Semantic Preparation |
+----------+-----------+
           |
           v
+----------------------+
|      Power BI        |
|                      |
| DAX Measures         |
| Visualisation        |
| Decision Support     |
+----------------------+
```

---

# 3. Component Responsibilities

## 3.1 Data Sources

Data sources provide the external and personal information used by the platform.

Potential market data sources include:

- job APIs,
- exported job data,
- CSV files,
- or other structured job-platform sources.

Personal information may initially be maintained manually.

Examples include:

- personal skills,
- proficiency levels,
- years of experience,
- and projects.

The first implementation may use synthetic data before connecting to real external sources.

---

## 3.2 Python Layer

Python is responsible for application and modelling logic that would be difficult or inappropriate to express in Power BI.

Responsibilities include:

### Data Acquisition

- retrieving job data,
- reading source files,
- handling APIs,
- and preparing raw records for persistence.

### Parsing

Job postings may contain unstructured or semi-structured information.

Python may therefore extract:

- skills,
- experience requirements,
- proficiency information,
- locations,
- job profiles,
- and other relevant fields.

### Normalisation

Source-specific terminology must be mapped to common analytical concepts.

Examples include:

```text
PowerBI
Microsoft Power BI
Power BI

        ↓

Power BI
```

or:

```text
Entry Level
Junior
Berufseinsteiger

        ↓

Junior
```

### Matching Model

The mathematical Job-Person Matching Model is implemented in Python.

For V1:

$$
M_{\text{V1}}(P,J) = Q_{\text{V1}}(P,J)
$$

and:

$$
Q_{\text{V1}}(P,J) = m_{\text{Skills}}(P,J).
$$

The Python layer therefore implements functions such as:

```text
proficiency_match()
experience_match()
individual_skill_match()
overall_skill_match()
qualification_fit()
```

Keeping this logic outside Power BI provides several advantages:

- easier unit testing,
- clearer mathematical implementation,
- better version control,
- greater flexibility,
- and easier extension of the model.

---

# 4. PostgreSQL Layer

PostgreSQL acts as the persistent analytical data store.

It separates data collection and modelling from visualisation.

The database may contain several logical layers.

## 4.1 Raw Data

Raw source records should be retained before transformation where practical.

For example:

```text
raw_job_posting
```

may contain:

- source identifier,
- retrieval timestamp,
- original title,
- original description,
- original location,
- and optionally the original source payload.

Keeping raw data provides:

- reproducibility,
- easier debugging,
- reduced dependence on repeated API requests,
- and the ability to rerun transformation logic.

---

## 4.2 Dimensional Model

Processed data is transformed into the dimensional model documented in `data-model.md`.

Core Level 1 structures include:

```text
FactJobPosting

DimDate
DimCompany
DimLocation
DimIndustry
DimJobProfile
DimExperienceLevel
DimSkill

BridgeJobSkill
```

Level 2 introduces:

```text
FactPersonSkill
FactProjectSkill

DimPerson
DimProject
DimProficiency
DimEvidenceLevel
```

The shared `DimSkill` connects market demand and personal capabilities.

---

## 4.3 Match Results

Precomputed matching results may optionally be persisted.

For example:

```text
FactJobMatch
```

could have the grain:

> One row represents the match between one person and one job posting for one model version.

Possible fields include:

```text
PersonKey
JobPostingKey
ModelVersion
QualificationFit
OverallMatch
CalculatedAt
```

A more detailed table may later store skill-level explanations.

For V1, match persistence is optional and should only be introduced if it improves performance, reproducibility, or explainability.

---

# 5. Power Query Layer

Power Query is responsible for loading the analytical data into Power BI.

Its role should primarily include:

- establishing database connections,
- selecting required tables,
- defining data types,
- performing light analytical preparation,
- and applying presentation-specific transformations.

Complex domain logic should generally not be duplicated in Power Query if it already exists in Python or PostgreSQL.

This prevents the transformation logic from being distributed unnecessarily across multiple technologies.

Power Query remains an important part of the BI workflow, but its responsibilities should remain clearly defined.

---

# 6. Power BI Layer

Power BI is the analytical and visualisation frontend.

Responsibilities include:

- loading the dimensional model,
- defining relationships,
- implementing analytical DAX measures,
- filtering and aggregation,
- interactive exploration,
- and presentation of Decision Support results.

Typical DAX measures may include:

- Job Count,
- Skill Demand,
- Regional Job Density,
- Average Required Experience,
- Median Salary,
- Match Count,
- High-Fit Job Count,
- and Skill Coverage.

Power BI should primarily consume the mathematical matching results rather than implement the core matching model itself.

This keeps the mathematical logic independently testable and prevents complex scoring logic from becoming hidden inside DAX measures.

---

# 7. Separation of Responsibilities

The architecture follows the principle:

```text
Python
    → domain and mathematical logic

PostgreSQL
    → persistent analytical state

Power Query
    → BI ingestion and light transformation

Power BI / DAX
    → analysis and visualisation
```

This separation avoids unnecessary duplication.

For example, the proficiency matching function should not exist simultaneously in:

- Python,
- SQL,
- Power Query,
- and DAX.

A single implementation should be treated as the source of truth.

For V1, the source of truth for the matching model is Python.

---

# 8. V1 Vertical Slice

Before integrating real job-market data, the platform should first implement a small end-to-end vertical slice.

The initial pipeline should use synthetic data.

```text
Synthetic Jobs
      +
Synthetic / Personal Profile
              |
              v
            Python
              |
        Matching Model
              |
              v
          PostgreSQL
              |
              v
         Power Query
              |
              v
           Power BI
```

The purpose of this vertical slice is to validate:

- the dimensional model,
- the matching implementation,
- the database structure,
- the Power BI connection,
- and the explainability of match results.

The goal is not to build a polished dashboard at this stage.

The goal is to prove that the complete analytical pipeline works.

---

# 9. Initial Synthetic Dataset

The initial test dataset may contain approximately:

- one person,
- 10–20 job postings,
- 5–10 normalised skills,
- several proficiency requirements,
- several experience requirements,
- multiple locations,
- and multiple job profiles.

The dataset should deliberately include:

- strong matches,
- weak matches,
- missing skills,
- overqualified cases,
- underqualified cases,
- and incomplete requirements.

This allows the V1 matching model to be evaluated before introducing noisy real-world data.

---

# 10. Testing Strategy

The mathematical matching model should be tested independently from Power BI.

Unit tests should cover cases such as:

### Proficiency

- equal proficiency,
- personal proficiency above requirement,
- personal proficiency below requirement,
- maximum proficiency deficit.

### Experience

- exact requirement,
- experience above requirement,
- partial experience,
- zero experience,
- missing experience requirement.

### Skill Aggregation

- one required skill,
- multiple equally matched skills,
- one missing skill among strong matches,
- incomplete matching components.

### Overall V1 Match

Since

$$
M_{\text{V1}}(P,J) = Q_{\text{V1}}(P,J),
$$

tests should verify that the full pipeline produces rankings consistent with the underlying skill matches.

Synthetic examples may additionally act as regression tests for later model versions.

---

# 11. Model Versioning

The matching model is expected to evolve.

Results should therefore be associated with a model version.

Example:

```text
V1
Skill-only Qualification Fit

V2
Eligibility
+
Extended Qualification
+
Preferences
```

Model versioning allows results to remain reproducible even when the mathematical specification changes.

A future persisted match table should therefore contain a field such as:

```text
ModelVersion
```

---

# 12. Future Architecture

Later versions may extend the architecture with:

```text
Multiple Job Platforms
        |
        v
Automated Acquisition
        |
        v
Raw Data Storage
        |
        v
Python Parsing / NLP
        |
        v
Normalised Dimensional Model
        |
        v
Versioned Matching Engine
        |
        v
Power BI
        |
        v
Decision Support
```

Possible future additions include:

- scheduled data ingestion,
- multiple job sources,
- automated skill extraction,
- ontology-based skill similarity,
- machine-learning-based parameter calibration,
- historical snapshots,
- and model evaluation using application outcomes.

---

# 13. Architecture Principles

The architecture follows several guiding principles:

- **Model before implementation.**
- **Document assumptions before introducing complexity.**
- **Keep raw data reproducible.**
- **Use one source of truth for business logic.**
- **Keep the dimensional model analytically focused.**
- **Keep mathematical matching logic independently testable.**
- **Prefer simple baselines before complex models.**
- **Use synthetic data before real-world integration.**
- **Add architecture only when a concrete requirement justifies it.**

The initial goal is therefore not maximum automation or model complexity.

The initial goal is a small, explainable, reproducible end-to-end system that connects mathematical modelling, dimensional BI architecture, and Power BI visualisation.
