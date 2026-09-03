# Real-World Job Normalization V1

## Purpose

This document defines the V1 normalization strategy for transforming
real-world job postings into the canonical analytical representation of
the Career Intelligence Platform.

The primary goal of V1 is not to extract every potentially useful piece
of information from a job posting. Instead, V1 prioritizes:

- reproducibility,
- explainability,
- conservative information extraction,
- clear separation between observed and inferred information.

The central principle is:

> V1 extracts observable evidence rather than inferring unspecified
> requirements.

Information that cannot be extracted with sufficient confidence remains
unknown.

---

## Normalization Pipeline

Real-world job data passes through three conceptual representations:

```text
Source Representation
        ↓
Extracted Information
        ↓
Canonical Representation
```

For Adzuna:

```text
Adzuna API
    ↓
Raw Job Posting
    ↓
Direct Field Mapping
    +
Explicit Requirement Extraction
    ↓
Canonical Job Representation
    ↓
V1 Matching Engine
```

The Matching Engine operates only on the canonical representation and
does not depend on the original source.

---

## Extraction Levels

### Level 1 — Direct Structured Mapping

Structured source attributes are mapped directly whenever their
semantics correspond sufficiently well to the canonical model.

Examples include:

| Adzuna Source          | Canonical Concept |
| ---------------------- | ----------------- |
| `id`                   | Source Job ID     |
| `title`                | Job Title         |
| `created`              | Publication Date  |
| `company.display_name` | Company           |
| `location`             | Location          |

These transformations require little or no semantic inference.

---

### Level 2 — Explicit Text Extraction

Information contained in unstructured text is extracted only when it can
be identified explicitly.

V1 considers:

- explicit skill mentions,
- explicit proficiency terminology,
- explicit skill-specific experience requirements.

Examples:

```text
"Python"
    → Skill = Python

"advanced Python skills"
    → Skill = Python
    → Required Proficiency = Advanced

"expert knowledge of R"
    → Skill = R
    → Required Proficiency = Expert

"at least 3 years of experience with SAS"
    → Skill = SAS
    → Required Experience = 3 years
```

---

### Level 3 — Semantic Inference

Semantic inference is explicitly outside the scope of V1.

Examples include:

```text
"strong Python skills"
    → NOT automatically interpreted as Advanced

"excellent knowledge of R"
    → NOT automatically interpreted as Expert

"extensive SAS experience"
    → NOT converted into a number of years

"Senior Data Scientist"
    → NOT automatically assigned an expected skill set
```

Such mappings may be introduced in later versions using more advanced
rule systems, NLP methods, language models, or empirically calibrated
mappings.

---

## Skill Normalization

Skills are mapped to the canonical skill vocabulary used by the
platform.

A controlled alias mapping may be used where the semantic equivalence is
sufficiently clear.

Examples:

```text
"PowerBI"     → Power BI
"Power BI"    → Power BI
"R Shiny"     → Shiny
"PostgreSQL"  → PostgreSQL or SQL depending on the canonical taxonomy
```

Alias mappings must be explicitly defined and reproducible.

V1 does not infer unmentioned related skills.

For example:

```text
PostgreSQL
```

does not automatically imply additional database technologies unless
this relationship is explicitly represented by the canonical skill
taxonomy.

---

## Proficiency Extraction

V1 extracts proficiency only from terminology that maps directly to the
canonical proficiency scale.

The canonical scale is:

1. Beginner
2. Intermediate
3. Advanced
4. Expert

Examples of accepted explicit mappings may include:

| Observed Expression       | Canonical Proficiency |
| ------------------------- | --------------------- |
| `beginner`                | Beginner              |
| `intermediate`            | Intermediate          |
| `advanced`                | Advanced              |
| `expert` / `expert-level` | Expert                |

More subjective expressions are not mapped in V1.

Examples:

```text
strong
excellent
solid
good
very good
proficient
deep knowledge
```

These expressions provide qualitative evidence but do not have a
sufficiently direct relationship to the canonical ordinal scale.

The corresponding proficiency requirement therefore remains unknown.

---

## Experience Extraction

Experience requirements are extracted only when a numerical experience
requirement can be explicitly associated with a skill.

Examples:

```text
"3+ years of Python experience"
    → Python
    → Required Experience = 3 years

"at least 5 years working with SAS"
    → SAS
    → Required Experience = 5 years
```

General experience requirements are not assigned to individual skills.

For example:

```text
"5 years of experience in clinical development"
```

does not imply:

```text
R = 5 years
SAS = 5 years
Statistics = 5 years
```

The association between experience and skill must be observable in the
source text.

---

## Requirement Information States

Real-world data introduces several states that were not equally visible
in the synthetic dataset.

For a canonical skill requirement, V1 distinguishes:

### 1. Skill not observed

No evidence for the skill requirement is available in the source data.

This does not prove that the real job does not require the skill,
particularly when only a truncated job description is available.

### 2. Skill observed, requirement details unknown

The skill is explicitly mentioned, but neither proficiency nor
skill-specific experience can be extracted.

Example:

```text
"Experience with SAS required."
```

Canonical representation:

```text
Skill = SAS
Required Proficiency = NULL
Required Experience = NULL
```

### 3. Skill and proficiency observed

Example:

```text
"Advanced Python skills"
```

Canonical representation:

```text
Skill = Python
Required Proficiency = Advanced
Required Experience = NULL
```

### 4. Skill and experience observed

Example:

```text
"3+ years of experience with R"
```

Canonical representation:

```text
Skill = R
Required Proficiency = NULL
Required Experience = 3
```

### 5. Skill, proficiency, and experience observed

Example:

```text
"Advanced Python skills with at least 3 years of experience"
```

Canonical representation:

```text
Skill = Python
Required Proficiency = Advanced
Required Experience = 3
```

---

## Matching Implications

The distinction between a missing skill and missing requirement
information remains fundamental.

If a job explicitly requires a skill and the person does not have that
skill in their profile:

$$
m_s(P,J)=0.
$$

If the person has the required skill but only one matching component is
available, only that component is evaluated.

For example, if only required proficiency is known:

$$
m_s(P,J)=m_{\text{prof},s}(P,J).
$$

If only required experience is known:

$$
m_s(P,J)=m_{\text{exp},s}(P,J).
$$

Real-world data introduces an additional case:

```text
Skill required
+
Person has skill
+
Proficiency unknown
+
Experience unknown
```

For V1, this case should be treated as a binary skill-presence match:

$$
m_s(P,J)=1
$$

if the person possesses the explicitly required skill, and

$$
m_s(P,J)=0
$$

otherwise.

This allows explicitly observed skill requirements to participate in
V1 matching without inventing unavailable proficiency or experience
requirements.

---

## Source Uncertainty

Normalization must preserve the distinction between:

```text
Requirement not observed
```

and

```text
Requirement known not to exist
```

This is particularly important for Adzuna because the explored Search
API responses contain truncated description text.

Therefore, absence of a skill from the available source text must not be
interpreted as evidence that the complete job posting does not require
that skill.

The resulting V1 match score represents compatibility with the
requirements observable from the available source data.

It does not necessarily represent compatibility with every requirement
contained in the complete original vacancy.

---

## Jobs Without Observable Skill Requirements

A real-world job posting may contain no observable skill requirements
in the available source representation.

This is particularly relevant for truncated source descriptions.

Such a job must not receive a V1 qualification score because the absence
of extracted requirements does not imply either poor or perfect
compatibility.

Jobs with zero extracted skill requirements are therefore classified as
`not matchable` under V1 and excluded from the V1 ranking.

This state represents insufficient source information rather than a
matching result.

---

## V1 Scope Boundary

V1 deliberately avoids:

- NLP-based entity extraction,
- language-model-based requirement extraction,
- fuzzy semantic skill matching,
- inferred proficiency levels,
- inferred years of experience,
- skill ontology traversal,
- skill substitution,
- requirements inferred from job titles,
- requirements inferred from seniority,
- requirements inferred from related technologies.

These capabilities may be evaluated in later versions.

The V1 normalization pipeline instead establishes a deterministic,
transparent baseline against which more sophisticated extraction methods
can later be compared.
