# 1. Conceptual Data Model

## Purpose

The conceptual data model describes the business domain independently of any technical implementation. It identifies the relevant business entities, their relationships and their properties without considering how they will later be represented in a dimensional model.

## Business Domain (Level 1 – Understanding the Job Market)

### Entities

The following entities are part of the first business domain.

---

**JobPosting**: Represents a published job advertisement.

<ins>Properties</ins>

- title
- description
- publicationDate
- salary
- employmentType
- remoteOption

<ins>Relationships</ins>

- published by → Company
- located in → Location
- belongs to → Industry
- classified as → JobProfile
- requires → Skill
- targets → ExperienceLevel

---

**Skill**: Represents a professional skill required by one or more job postings.

<ins>Properties</ins>

- name
- category

Examples:

- SQL
- Python
- Power BI
- Communication
- Leadership

---

**Company**: Represents the employer.

<ins>Properties</ins>

- name

<ins>Relationships</ins>

- publishes → JobPosting

---

**Industry**: Represents the industry sector.

<ins>Properties</ins>

- name

---

**Location**: Represents the geographical location.

<ins>Properties</ins>

- city
- state
- country

---

**JobProfile**: Represents the primary job category.

Examples:

- BI Analyst
- Data Analyst
- Data Engineer
- Data Scientist

---

**ExperienceLevel**: Represents the seniority targeted by a job posting.

Examples:

- Entry
- Junior
- Mid
- Senior
- Lead

## Level 2 – Understanding Yourself

Level 2 extends the labour market model with a representation of the individual user.

While Level 1 describes **market demand**, Level 2 describes **personal capabilities and evidence**. The central linking concept between both perspectives is `Skill`:

- job postings **require** skills;
- persons **possess** skills;
- projects **demonstrate** skills.

This common representation of skills will later enable comparisons between labour market demand and a person's individual profile.

## Business Questions

Level 2 addresses the following questions:

- What skills do I have?
- How much experience do I have?
- Which projects prove my skills?
- How do my skills develop over time?

---

## Conceptual Data Model

### Person

`Person` represents the individual whose professional profile is analysed.

A person can possess multiple skills and can work on multiple projects.

Possible properties include:

- `PersonID`
- `Name`

The initial version of the system may contain only one person. The conceptual model nevertheless treats `Person` as an independent entity to keep the model extensible.

---

### Skill

`Skill` is shared between the labour market model and the personal profile model.

A skill represents a professional capability that may be required by job postings and possessed by persons.

Possible properties include:

- `SkillID`
- `SkillName`
- `SkillCategory`
- `SkillSubcategory`

Example categories may include:

- Technical Skill
- Methodological Skill
- Domain Knowledge
- Soft Skill

Example subcategories may include:

- Programming Language
- BI Tool
- Database Technology
- Cloud Technology
- Statistics
- Communication
- Leadership

The first version deliberately uses a pragmatic skill taxonomy rather than attempting to construct a complete skill ontology. The taxonomy can be refined as the project evolves.

---

### PersonSkill

The relationship between `Person` and `Skill` must not be modelled as a simple binary property.

Knowing that a person "has" a skill is insufficient for meaningful personal analytics. The system must also be able to describe the extent and recency of that capability.

`PersonSkill` therefore represents the relationship between a person and a particular skill.

Possible properties include:

- `YearsExperience`
- `ProficiencyLevel`
- `LastUsedDate`

For example:

| Person   | Skill    | YearsExperience | ProficiencyLevel | LastUsedDate |
| -------- | -------- | --------------: | ---------------- | ------------ |
| Person A | Python   |               5 | Advanced         | 2026         |
| Person A | Power BI |               1 | Intermediate     | 2026         |
| Person A | Azure    |               0 | Beginner         | 2025         |

This makes it possible to distinguish between merely knowing a technology and having substantial, recent experience with it.

Conceptually:

```text
Person M:N Skill
```

with `PersonSkill` acting as the associative entity describing this relationship.

---

### Project

`Project` represents practical work that can provide evidence for one or more skills.

Possible properties include:

- `ProjectID`
- `ProjectName`
- `Description`
- `StartDate`
- `EndDate`
- `ProjectType`
- `RepositoryURL`

Possible project types include:

- Professional Project
- Portfolio Project
- Research Project
- Academic Project

A person may work on multiple projects.

A project may demonstrate multiple skills, while the same skill may be demonstrated by multiple projects.

Therefore:

```text
Project M:N Skill
```

---

### ProjectSkill

`ProjectSkill` represents the relationship between a project and the skills demonstrated by that project.

The relationship may optionally contain an `EvidenceLevel` describing how strongly a particular project demonstrates a skill.

Possible values could initially be:

- Primary
- Supporting
- Minor

For example:

| Project                      | Skill          | EvidenceLevel |
| ---------------------------- | -------------- | ------------- |
| Career Intelligence Platform | Power BI       | Primary       |
| Career Intelligence Platform | Power Query    | Primary       |
| Career Intelligence Platform | Data Modelling | Primary       |
| Career Intelligence Platform | Git            | Supporting    |

This distinction prevents all project-skill relationships from being treated as equally strong evidence.

`EvidenceLevel` should remain deliberately simple in the first version. The project should avoid introducing artificial precision into the assessment of skill evidence.

---

## Skill Evidence

Skill evidence should not be stored redundantly as aggregated attributes of `PersonSkill`.

For example, properties such as

- Number of Projects
- Number of Professional Projects
- Number of Skills Demonstrated

can be derived from the relationships between `Person`, `Project`, and `Skill`.

The conceptual distinction is therefore:

```text
PersonSkill
    → describes the person's capability

ProjectSkill
    → describes evidence for that capability
```

This separation will later allow the system to distinguish between self-reported capability and observable evidence.

---

## Skill Development over Time

`SkillDevelopment` is not treated as an independent entity.

It is an analytical concept derived from historical observations of a person's skill profile.

To analyse skill development over time, future versions may introduce a historical representation such as `PersonSkillHistory`.

Possible properties include:

- `Person`
- `Skill`
- `ObservationDate`
- `YearsExperience`
- `ProficiencyLevel`

For example:

| ObservationDate | Skill    | YearsExperience | ProficiencyLevel |
| --------------- | -------- | --------------: | ---------------- |
| 2025-01         | Power BI |             0.2 | Beginner         |
| 2025-08         | Power BI |             0.8 | Intermediate     |
| 2026-08         | Power BI |             1.8 | Advanced         |

Skill development can then be derived by comparing observations over time.

Historical skill tracking is considered an extension of the initial model and does not have to be implemented in the first version.

---

## Conceptual ER Diagram

```mermaid
erDiagram

    PERSON ||--o{ PERSON_SKILL : possesses
    SKILL ||--o{ PERSON_SKILL : describes

    PERSON ||--o{ PROJECT : works_on

    PROJECT ||--o{ PROJECT_SKILL : demonstrates
    SKILL ||--o{ PROJECT_SKILL : evidenced_by

    PERSON {
        int PersonID
        string Name
    }

    SKILL {
        int SkillID
        string SkillName
        string SkillCategory
        string SkillSubcategory
    }

    PERSON_SKILL {
        int PersonID
        int SkillID
        decimal YearsExperience
        string ProficiencyLevel
        date LastUsedDate
    }

    PROJECT {
        int ProjectID
        string ProjectName
        string Description
        date StartDate
        date EndDate
        string ProjectType
        string RepositoryURL
    }

    PROJECT_SKILL {
        int ProjectID
        int SkillID
        string EvidenceLevel
    }
```

---

## Connection to the Labour Market Model

The central architectural concept of the Career Intelligence Platform is that `Skill` connects labour market demand with personal capabilities.

Conceptually:

```text
                      Skill
                    /       \
                   /         \
            required by     possessed by
                /               \
        JobPosting             Person
                                  \
                                   \
                                supported by
                                     \
                                    Project
```

More precisely:

```text
JobPosting ── requires ── Skill
                         ▲
                         │
                    PersonSkill
                         │
                       Person
                         │
                     works on
                         │
                      Project
                         │
                    ProjectSkill
                         │
                         └──── demonstrates ────► Skill
```

This shared `Skill` concept creates the foundation for Level 3.

Once both market demand and personal capabilities use the same skill taxonomy, the system can analyse:

- skill matches,
- skill gaps,
- differences in required and personal proficiency,
- evidence supporting personal skills,
- experience gaps,
- and potential learning priorities.

In this sense, `Skill` acts as the central semantic bridge between **the labour market** and **the individual profile**.

## Dimensional Data Model

The dimensional model translates the conceptual Level 2 model into an analytical structure suitable for Power BI.

While the conceptual model focuses on entities and relationships, the dimensional model focuses on:

- measurable business facts,
- dimensions used for filtering and grouping,
- clearly defined table grains,
- and reusable dimensions shared with the labour market model.

A central design principle is that the same `DimSkill` is used for both labour market demand and personal capabilities.

---

## FactPersonSkill

### Grain

> One row represents the current relationship between one person and one skill.

`FactPersonSkill` describes the current state of a person's capability regarding a specific skill.

Possible measures and foreign keys include:

- `PersonKey`
- `SkillKey`
- `ProficiencyKey`
- `LastUsedDateKey`
- `YearsExperience`

Example:

| PersonKey | SkillKey | YearsExperience | ProficiencyKey | LastUsedDateKey |
| --------- | -------- | --------------: | -------------- | --------------- |
| 1         | Python   |             5.0 | Advanced       | 20260820        |
| 1         | Power BI |             1.2 | Intermediate   | 20260820        |

`YearsExperience` is treated as a measurable fact.

`ProficiencyLevel` is represented through a dimension rather than stored as free text, allowing ordered comparisons between personal and required proficiency levels.

---

## FactProjectSkill

### Grain

> One row represents one skill demonstrated by one project.

`FactProjectSkill` models the many-to-many relationship between projects and skills.

It can be interpreted as a factless or bridge-like fact table: the existence of the relationship itself represents an analytically relevant fact.

Possible foreign keys include:

- `ProjectKey`
- `SkillKey`
- `EvidenceLevelKey`

Example:

| ProjectKey                   | SkillKey    | EvidenceLevelKey |
| ---------------------------- | ----------- | ---------------- |
| Career Intelligence Platform | Power BI    | Primary          |
| Career Intelligence Platform | Power Query | Primary          |
| Career Intelligence Platform | Git         | Supporting       |

This structure allows the system to analyse not only whether a project demonstrates a skill, but also how strongly the project supports that skill.

---

## DimPerson

`DimPerson` represents the person whose professional profile is being analysed.

Possible attributes include:

- `PersonKey`
- `PersonName`

The initial version of the platform may contain only one person. The dimension is nevertheless retained to keep the model extensible.

---

## DimSkill

`DimSkill` is shared between the labour market model and the personal profile model.

Possible attributes include:

- `SkillKey`
- `SkillName`
- `SkillCategory`
- `SkillSubcategory`

Example:

| SkillName             | SkillCategory        | SkillSubcategory     |
| --------------------- | -------------------- | -------------------- |
| Python                | Technical Skill      | Programming Language |
| Power BI              | Technical Skill      | BI Tool              |
| Statistical Modelling | Methodological Skill | Statistics           |
| Communication         | Soft Skill           | Interpersonal        |

Using the same `DimSkill` for both job postings and personal capabilities is essential for later skill-gap and fit analyses.

---

## DimProject

`DimProject` describes projects that provide evidence for personal skills.

Possible attributes include:

- `ProjectKey`
- `ProjectName`
- `ProjectType`
- `Description`
- `StartDate`
- `EndDate`
- `RepositoryURL`

Possible project types include:

- Professional Project
- Portfolio Project
- Research Project
- Academic Project

---

## DimProficiency

`DimProficiency` represents an ordered proficiency scale.

Possible attributes include:

- `ProficiencyKey`
- `ProficiencyLabel`
- `ProficiencyRank`

Example:

| ProficiencyLabel | ProficiencyRank |
| ---------------- | --------------: |
| Beginner         |               1 |
| Intermediate     |               2 |
| Advanced         |               3 |
| Expert           |               4 |

The numerical rank enables comparisons between a person's proficiency and the proficiency required by a job posting.

The rank should be interpreted as an ordinal scale rather than as a precise quantitative measurement.

---

## DimEvidenceLevel

`DimEvidenceLevel` describes how strongly a project demonstrates a particular skill.

Possible attributes include:

- `EvidenceLevelKey`
- `EvidenceLabel`
- `EvidenceRank`

Example:

| EvidenceLabel | EvidenceRank |
| ------------- | -----------: |
| Minor         |            1 |
| Supporting    |            2 |
| Primary       |            3 |

As with proficiency, the rank represents an ordered category and should not imply artificial numerical precision.

---

## DimDate

The existing `DimDate` from Level 1 is reused.

Within Level 2 it may support fields such as:

- `LastUsedDateKey`
- project start dates,
- project end dates,
- and later historical skill observations.

This reuse allows personal skill development to be analysed using the same temporal dimension as labour market trends.

---

## Level 2 Dimensional Model

```mermaid
erDiagram

    DIM_PERSON ||--o{ FACT_PERSON_SKILL : has
    DIM_SKILL ||--o{ FACT_PERSON_SKILL : describes
    DIM_PROFICIENCY ||--o{ FACT_PERSON_SKILL : rates
    DIM_DATE ||--o{ FACT_PERSON_SKILL : last_used

    DIM_PROJECT ||--o{ FACT_PROJECT_SKILL : provides
    DIM_SKILL ||--o{ FACT_PROJECT_SKILL : demonstrates
    DIM_EVIDENCE_LEVEL ||--o{ FACT_PROJECT_SKILL : qualifies

    DIM_PERSON {
        int PersonKey
        string PersonName
    }

    DIM_SKILL {
        int SkillKey
        string SkillName
        string SkillCategory
        string SkillSubcategory
    }

    FACT_PERSON_SKILL {
        int PersonKey
        int SkillKey
        int ProficiencyKey
        int LastUsedDateKey
        decimal YearsExperience
    }

    DIM_PROFICIENCY {
        int ProficiencyKey
        string ProficiencyLabel
        int ProficiencyRank
    }

    DIM_PROJECT {
        int ProjectKey
        string ProjectName
        string ProjectType
        string Description
        date StartDate
        date EndDate
        string RepositoryURL
    }

    FACT_PROJECT_SKILL {
        int ProjectKey
        int SkillKey
        int EvidenceLevelKey
    }

    DIM_EVIDENCE_LEVEL {
        int EvidenceLevelKey
        string EvidenceLabel
        int EvidenceRank
    }

    DIM_DATE {
        int DateKey
        date Date
        int Year
        int Quarter
        int Month
        int Week
    }
```

---

## Integration with Level 1

The key architectural decision is that Level 1 and Level 2 share the same `DimSkill`.

Conceptually, the dimensional model connects labour market demand and personal capabilities as follows:

```text
FactJobPosting
      |
BridgeJobSkill
      |
   DimSkill
      |
FactPersonSkill
      |
   DimPerson
```

Project-based evidence extends the personal side:

```text
DimProject
     |
FactProjectSkill
     |
  DimSkill
     |
FactPersonSkill
     |
  DimPerson
```

This shared structure enables later Level 3 analyses such as:

- skill matching,
- skill-gap identification,
- proficiency comparisons,
- evidence-based profile assessment,
- learning prioritisation,
- and personal job-fit scoring.

---

## Historical Skill Development

Historical skill development is not part of the initial dimensional model.

If implemented later, a separate snapshot fact table such as `FactPersonSkillSnapshot` may be introduced.

Its grain could be:

> One row represents the state of one person's relationship to one skill at one observation date.

Possible fields include:

- `PersonKey`
- `SkillKey`
- `DateKey`
- `ProficiencyKey`
- `YearsExperience`

This would make it possible to analyse how personal capabilities evolve over time without overwriting previous states.

# Level 3 – Decision Support

Level 3 builds upon the labour market model from Level 1 and the personal profile model from Level 2.

Unlike the previous levels, Level 3 primarily does not introduce new entities representing the business domain. Instead, it derives analytical quantities by comparing labour market requirements with personal capabilities.

The purpose of this layer is to transform descriptive information into actionable decision support.

---

## From Description to Decision Support

The three analytical levels of the platform can be summarised as:

```text
Level 1 – Labour Market
"What does the market require?"
            |
            v
      Market Profile


Level 2 – Personal Profile
"What can I offer?"
            |
            v
     Personal Profile


Market Profile + Personal Profile
            |
            v
      Matching Model
            |
            v
Level 3 – Decision Support
"What should I do?"
```

The central challenge of Level 3 is therefore the definition of the **matching model**.

---

## The Matching Problem

The shared `Skill` dimension allows job requirements and personal capabilities to be represented in a common space.

Conceptually, a job posting can be represented through its required skills:

```text
JobProfile(J)
=
{
    (Skill_1, Requirement_1),
    (Skill_2, Requirement_2),
    ...
}
```

A person's professional profile can similarly be represented through personal capabilities:

```text
PersonalProfile(P)
=
{
    (Skill_1, Capability_1),
    (Skill_2, Capability_2),
    ...
}
```

The matching problem consists of determining how closely these two profiles correspond.

Conceptually, the platform therefore requires a function

```text
Match(Person, JobPosting)
```

or equivalently a distance or loss function

```text
Distance(Person, JobPosting)
```

where a smaller distance represents a better match.

The exact mathematical definition of this function is deliberately left open at this stage and should be specified separately before implementing the Decision Support layer.

---

## Matching Dimensions

A meaningful match should not necessarily be based on binary skill possession alone.

Potential components include:

### Skill Coverage

How many of the required skills are covered by the personal profile?

### Proficiency Match

How closely does personal proficiency correspond to the proficiency expected by the job?

### Experience Match

How closely does personal experience correspond to the required experience?

### Skill Importance

Not every skill mentioned in a job posting is equally important.

Core requirements may receive greater weight than optional or supporting skills.

### Evidence

Personal capabilities may be supported by different amounts and strengths of evidence, for example through projects.

### Skill Recency

Recently used skills may provide stronger evidence of current capability than skills that have not been used for several years.

These components may later form a multidimensional matching function.

---

## Match as an Analytical Foundation

The matching model is not itself a recommendation.

Instead, it provides the analytical foundation from which recommendations can be derived.

Conceptually:

```text
Market Data
     +
Personal Data
     |
     v
Matching Model
     |
     +------> Job Fit
     |
     +------> Skill Gaps
     |
     +------> Regional Fit
     |
     +------> Company Fit
     |
     +------> Career Path Fit
     |
     v
Decision Support
```

This separation is important because the same matching model can support several different business questions.

---

## Derived Analytical Concepts

### Job Fit

`JobFit` describes how closely a person's profile matches the requirements of an individual job posting.

Conceptually:

```text
JobFit(Person, JobPosting)
```

The measure may combine skill coverage, proficiency, experience and evidence.

---

### Skill Gap

A `SkillGap` describes a mismatch between market requirements and personal capabilities.

A missing skill is not automatically an important skill gap.

The relevance of a gap depends on factors such as:

- frequency of the skill in relevant job postings,
- importance of the skill within those postings,
- current personal proficiency,
- required proficiency,
- and the effect of closing the gap on overall job fit.

Therefore, skill-gap prioritisation should be based on the matching model rather than simple absence or presence.

---

### Marketability Gain

`MarketabilityGain` describes the expected improvement in market coverage resulting from acquiring or improving a skill.

Conceptually, this can be viewed as a counterfactual comparison:

```text
Current Profile
      |
      v
Current Job Coverage

Current Profile + Skill X
      |
      v
New Job Coverage
```

The difference between both states represents the incremental value of Skill X.

This allows the platform to distinguish between:

> "Which skills are popular?"

and the more decision-relevant question:

> "Which skill would improve this person's opportunities the most?"

---

### Regional Fit

`RegionalFit` aggregates personal job fit over geographical locations.

It may combine information such as:

- number of available jobs,
- average or median job fit,
- number of high-fit jobs,
- salary levels,
- and remote opportunities.

This distinguishes general job density from **personal opportunity density**.

---

### Company Fit

`CompanyFit` aggregates job-fit information at company level.

It can be used to identify employers whose current demand aligns particularly well with the personal profile.

---

### Technology Learning Priority

Technology learning recommendations are a specialised form of skill-gap prioritisation.

The analysis can be restricted to technical skill categories and may consider:

- current market demand,
- personal skill gaps,
- marketability gain,
- demand trends,
- and required proficiency.

The resulting ranking should answer:

> Which technology would provide the greatest expected benefit if learned next?

---

### Salary Benchmark

Salary recommendations should not be based on the overall labour market.

Instead, salary ranges should be estimated from a relevant comparison set of job postings.

This comparison set may be determined using:

- job profile,
- personal job fit,
- experience level,
- location,
- skills,
- and other relevant characteristics.

The resulting output should preferably be expressed as a range or distribution, for example using:

- lower quartile,
- median,
- upper quartile.

The system should therefore provide a **salary benchmark**, not claim to determine an individual's exact market value.

---

### Career Path Fit

`CareerPathFit` aggregates matching information by `JobProfile`.

For example:

```text
BI Analyst
Data Scientist
Data Engineer
Statistical Programmer
Software Developer
```

Possible components include:

- current average job fit,
- number of matching vacancies,
- magnitude of remaining skill gaps,
- required learning effort,
- salary potential,
- and market demand.

This can be used to identify career directions that combine strong current fit with attractive market opportunities.

---

## Decision-Support Questions

The Level 3 analytical layer ultimately supports the following business questions:

- Which skill gaps should be prioritised?
- Which additional skills would provide the greatest increase in marketability?
- Which regions best match my current profile?
- Which companies are realistic targets?
- Which technologies should I learn next?
- What salary range is realistic based on my profile?
- Which career paths appear to be the best fit?

These questions are not answered directly by additional domain entities.

Instead, they are answered through derived analytical quantities based on the Level 1 and Level 2 models.

---

## Architectural Principle

Level 3 introduces a clear separation between **data**, **analytics**, and **recommendations**:

```text
Level 1 + Level 2
      |
      v
Observed Data
      |
      v
Matching / Scoring Model
      |
      v
Derived Analytical Measures
      |
      v
Decision Rules
      |
      v
Recommendations
```

This separation allows the matching model and decision rules to evolve independently from the underlying dimensional model.

The exact mathematical definitions of matching scores, distance measures, weighting schemes and recommendation rules are outside the scope of the conceptual data model and should be specified separately before implementation.
