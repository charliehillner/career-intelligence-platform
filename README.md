# Career Intelligence Platform

> A Business Intelligence and Decision Support platform for analysing the labour market, understanding personal skill profiles, and identifying career opportunities.

## Overview

Finding a job is not only a search problem.

Job seekers need to understand questions such as:

- Which skills are currently in demand?
- Which technologies are commonly required together?
- How does demand differ between regions and industries?
- How well does my current profile match the market?
- Which skills should I learn next?
- Which jobs, companies, or career paths fit my profile?

The **Career Intelligence Platform** aims to answer these questions by combining labour market analytics with personal profile analytics.

The project is built around three analytical levels:

```text
Level 1                         Level 2
Labour Market                  Personal Profile
"What does the market need?"   "What can I offer?"
       |                              |
       +--------------+---------------+
                      |
                      v
               Matching Model
                      |
                      v
                   Level 3
               Decision Support
              "What should I do?"
```

The long-term goal is not merely to build a reporting dashboard, but an explainable **Decision Support System**.

---

# Analytical Levels

## Level 1 - Understanding the Labour Market

The first level analyses the job market independently of any individual person.

Business questions include:

- What skills are sought after?
- What technologies are often requested together?
- Which regions seek which profiles?
- What industries prefer which profiles?
- How does demand change over time?
- Which experience levels are expected?

Potential analyses include skill demand, technology co-occurrence, regional job density, experience requirements, industry differences, and market trends.

---

## Level 2 - Understanding the Personal Profile

The second level models the capabilities of an individual.

Business questions include:

- What skills do I have?
- How much experience do I have?
- Which projects demonstrate my skills?
- How do my skills develop over time?

A skill is deliberately **not represented as a binary property**.

Instead of merely storing

```text
Python = Yes
```

the model can represent information such as:

```text
Python
|
+-- Proficiency
+-- Years of Experience
+-- Last Used
+-- Project Evidence
```

This allows substantially more nuanced comparisons between a personal profile and labour market requirements.

---

## Level 3 - Decision Support

The third level combines market demand and personal capabilities.

Business questions include:

- Which skill gaps should be prioritised?
- Which additional skills would provide the greatest increase in marketability?
- Which regions best match my current profile?
- Which companies are realistic targets?
- Which technologies should I learn next?
- What salary range is realistic based on my profile?
- Which career paths appear to be the best fit?

These questions require more than traditional BI aggregation.

They depend on a mathematical **Job-Person Matching Model**.

---

# Central Data Concept

The central semantic link between the labour market and the personal profile is `Skill`.

```text
JobPosting ---- requires ---- Skill ---- possessed by ---- Person
                                |
                                |
                         demonstrated by
                                |
                             Project
```

Job postings define **skill demand**.

Persons define **skill supply**.

Projects provide **evidence** for personal capabilities.

Using a shared skill representation allows both sides to be compared analytically.

---

# Data Model

The analytical data model follows dimensional modelling principles and is designed for Power BI.

The core market fact is:

```text
FactJobPosting
```

with dimensions such as:

```text
DimDate
DimCompany
DimLocation
DimIndustry
DimJobProfile
DimExperienceLevel
DimSkill
```

The many-to-many relationship between job postings and skills is represented through a bridge table.

The personal profile introduces additional analytical structures:

```text
FactPersonSkill
FactProjectSkill

DimPerson
DimProject
DimProficiency
DimEvidenceLevel
```

A central design decision is that both the market and personal profile models share the same `DimSkill`.

Conceptually:

```text
                     DimSkill
                    /        \
                   /          \
          Market Side       Personal Side
               |                 |
        BridgeJobSkill     FactPersonSkill
               |                 |
        FactJobPosting        DimPerson
```

This shared dimension provides the foundation for skill-gap and job-fit analyses.

More details are documented in [`docs/data-model.md`](docs/data-model.md).

---

# Job-Person Matching

The central question of the Decision Support layer is:

> **How well does a person P match a job J?**

Let

$$
M(P,J)
$$

represent the overall compatibility between person $P$ and job $J$.

The current conceptual model separates matching into three components:

```text
                     Job-Person Match
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
       Eligibility     Qualification     Preference
            |               |               |
        Can I take       Can I do         Do I want
         this job?       this job?        this job?
```

Eligibility represents non-compensable constraints.

Qualification describes the correspondence between job requirements and professional capabilities.

Preference describes the correspondence between job characteristics and personal preferences.

A general representation is:

$$
M(P,J) = E(P,J) \cdot A\left(Q(P,J),R(P,J)\right)
$$

where:

- $E(P,J)$ represents eligibility,
- $Q(P,J)$ represents qualification fit,
- $R(P,J)$ represents preference fit,
- $A$ represents an aggregation function.

The exact mathematical specification is developed separately from the BI layer.

See [`docs/matching-model.md`](docs/matching-model.md).

---

# Skill Matching

Skill matching is currently the primary focus of the mathematical modelling process.

A job generally requires multiple skills.

Let

$$
S_J = \lbrace s_1,\ldots,s_n \rbrace
$$

denote the skills required by job $J$.

For each required skill $s$, an individual match

$$
m_s(P,J)
$$

is determined.

The individual skill matches are subsequently aggregated into

$$
m_{\text{Skills}}(P,J).
$$

An individual skill match may itself depend on several components:

```text
Individual Skill Match
         |
    +----+----+
    |         |
    v         v
Proficiency  Experience
   Match       Match
```

Project evidence may additionally provide information about the reliability of the personal skill assessment.

This creates a hierarchical matching model:

```text
Local Attribute Matches
          |
          v
Individual Skill Matches
          |
          v
Overall Skill Fit
          |
          v
Qualification Fit
          |
          v
Job-Person Match
```

See [`docs/skill-matching.md`](docs/skill-matching.md).

---

# Proficiency Matching

One of the first investigated modelling problems is the comparison of personal and required proficiency.

Proficiency levels are ordinal, for example:

```text
Beginner < Intermediate < Advanced < Expert
```

Their ordering is meaningful, but the distances between the categories are not inherently defined.

For the initial model, an asymmetric rank-based loss provides a transparent baseline:

$$
\ell_{\text{prof},s}(P,J) =
\left(
\frac{
\max\left(0,r_J(s)-r_P(s)\right)
}{
R_{\max}-R_{\min}
}
\right)^2
$$

with the corresponding match

$$
m_{\text{prof},s}(P,J) = 1-\ell_{\text{prof},s}(P,J).
$$

The asymmetry reflects the interpretation of proficiency requirements as minimum requirements: exceeding the required proficiency does not reduce the match.

This baseline deliberately makes a simplifying assumption by treating ordinal rank differences as comparable distances.

A future alternative is an explicitly calibrated compatibility matrix:

| Personal \ Required | Beginner | Intermediate | Advanced | Expert |
| ------------------- | -------: | -----------: | -------: | -----: |
| Beginner            |        1 |            ? |        ? |      ? |
| Intermediate        |        1 |            1 |        ? |      ? |
| Advanced            |        1 |            1 |        1 |      ? |
| Expert              |        1 |            1 |        1 |      1 |

Such a matrix avoids the equidistance assumption but requires defensible values obtained through expert knowledge or empirical calibration.

---

# Explainability

Explainability is a central design goal.

The system should not only output:

```text
Job Match: 78%
```

Instead, the result should be decomposable into the factors that produced it.

For example:

```text
Overall Match
|
+-- Eligibility
|
+-- Qualification Fit
|   |
|   +-- Skill Fit
|   |   |
|   |   +-- Python
|   |   |   +-- Proficiency
|   |   |   +-- Experience
|   |   |
|   |   +-- SQL
|   |   +-- Power BI
|   |
|   +-- Other Qualifications
|
+-- Preference Fit
```

This makes recommendations inspectable and allows users to understand why a particular job, skill, region, or career path is recommended.

---

# Technology Stack

The planned analytical stack includes:

- **Power BI** - dashboard and analytical frontend
- **Power Query** - ETL and data transformation
- **DAX** - analytical measures
- **Dimensional Modelling** - star-schema-based analytical model

Additional technologies may be introduced for data collection, preprocessing, mathematical modelling, or automation where appropriate.

---

# Project Structure

```text
.
|
+-- docs/
|   |
|   +-- requirements.md
|   +-- data-model.md
|   +-- decision-support.md
|   +-- matching-model.md
|   +-- skill-matching.md
|
+-- README.md
```

The documentation is intentionally developed before the dashboard implementation.

The project follows the general workflow:

```text
Business Questions
        |
        v
Conceptual Model
        |
        v
Dimensional Model
        |
        v
Analytical Models
        |
        v
ETL / Power Query
        |
        v
DAX Measures
        |
        v
Power BI Dashboard
        |
        v
Decision Support
```

---

# Current Status

The project is currently in the **modelling and architecture phase**.

Completed or substantially developed:

- business requirements,
- Level 1 conceptual market model,
- Level 1 dimensional market model,
- Level 2 conceptual personal-profile model,
- Level 2 dimensional personal-profile model,
- Level 3 Decision Support architecture,
- initial Job-Person Matching architecture,
- initial Skill Matching architecture,
- baseline Proficiency Matching model.

Current mathematical modelling focuses on the individual components of Skill Fit.

The next major research question is:

> **How should skill-specific experience match be quantified?**

---

# Roadmap

Planned next steps include:

1. Complete the Skill Matching model.
2. Define experience matching.
3. Investigate skill importance and weighting.
4. Define aggregation across individual skills.
5. Extend Qualification Fit beyond skills.
6. Develop Preference Fit.
7. Define the first complete baseline Job-Person Matching model.
8. Identify and implement initial job-market data sources.
9. Build the ETL pipeline using Power Query.
10. Implement the dimensional model in Power BI.
11. Develop Level 1 market analytics.
12. Develop Level 2 personal-profile analytics.
13. Implement explainable Level 3 Decision Support.
14. Evaluate and calibrate the matching model using real-world data.

---

# Design Philosophy

The project follows several principles:

- **Business questions before visualisations**
- **Conceptual modelling before dimensional modelling**
- **Explicit table grains**
- **Shared semantics between market and personal data**
- **Transparent mathematical assumptions**
- **Explainable scores instead of black-box recommendations**
- **Simple baselines before unnecessary model complexity**
- **Empirical calibration when sufficient data becomes available**

The goal is not to create an arbitrary "AI career score".

The goal is to build a transparent analytical system in which market data, personal capabilities, modelling assumptions, and resulting recommendations can be inspected and understood.
