# V1 Matching Model Evaluation

## Purpose

This document evaluates the first baseline version of the qualification
matching model used in the Career Intelligence Platform.

The purpose of this evaluation is not to demonstrate that the V1 model
provides an optimal representation of job-person fit. Instead, the goal
is to verify that the implemented model behaves according to its
specification, produces interpretable results, and provides a useful
baseline for future model development.

The evaluation uses the synthetic person profile and synthetic job
postings defined for MVP 1.

---

## Evaluation Setup

The V1 matching model considers only qualification fit based on required
skills:

$$
M_{\text{V1}}(P,J) =
Q_{\text{V1}}(P,J) =
m_{\text{Skills}}(P,J).
$$

Each required skill is evaluated using up to two components:

- proficiency match,
- experience match.

If both components are available, the individual skill match is their
arithmetic mean.

The overall qualification fit is the arithmetic mean across all required
skills:

$$
Q_{\text{V1}}(P,J) =
\frac{1}{|S_J|}\sum_{s\in S_J}m_s(P,J).
$$

All required skills therefore receive equal weight in V1.

A required skill that is absent from the person's profile receives a
skill match of zero.

Missing requirement information, such as unspecified required years of
experience, is instead excluded from the corresponding skill-level
aggregation.

---

## Synthetic Evaluation Results

The V1 matching engine produced the following ranking for the synthetic
candidate:

| Rank | Job                           | Qualification Fit |
| ---: | ----------------------------- | ----------------: |
|    1 | Statistical Programmer        |            100.0% |
|    2 | Biostatistician               |            100.0% |
|    3 | R/Shiny Developer             |            100.0% |
|    4 | Research Software Engineer    |             92.6% |
|    5 | Data Scientist                |             92.4% |
|    6 | Business Intelligence Analyst |             82.4% |
|    7 | Machine Learning Engineer     |             73.6% |
|    8 | Senior Java Backend Developer |             50.8% |
|    9 | Senior Data Engineer          |             44.6% |
|   10 | Cloud Data Engineer           |             39.2% |

The resulting ranking is broadly consistent with the qualitative
expectations used when constructing the synthetic dataset.

Roles closely related to the candidate's strongest skills in statistics,
R, Shiny, and quantitative analysis appear at the top of the ranking.

Roles requiring stronger software engineering, machine learning, data
engineering, or cloud-specific capabilities receive progressively lower
scores.

This indicates that the V1 model captures the intended broad structure
of qualification fit.

---

## Explainability

An important property of the V1 model is that the final score can be
decomposed into individual skill matches and their underlying
components.

For example, the Data Scientist role receives an overall qualification
fit of approximately 92.4%.

Its individual skill matches are:

| Skill            | Skill Match | Proficiency Match | Experience Match |
| ---------------- | ----------: | ----------------: | ---------------: |
| Machine Learning |       69.4% |             88.9% |            50.0% |
| Python           |      100.0% |            100.0% |           100.0% |
| SQL              |      100.0% |            100.0% |           100.0% |
| Statistics       |      100.0% |            100.0% |           100.0% |

The result therefore does not only indicate that the job is a strong
overall match. It also identifies Machine Learning experience as the
main qualification gap.

This decomposition is important for later decision-support features,
because the platform should explain why a job receives a particular
score rather than only provide a ranking.

---

## Observed Model Properties

### Requirement Satisfaction

V1 effectively behaves as a requirement-satisfaction model.

If the candidate meets or exceeds a proficiency or experience
requirement, the corresponding component match is capped at 1.

Consequently, the model does not distinguish between a requirement that
is exactly satisfied and one that is substantially exceeded.

This is intentional in V1 but limits the model's ability to distinguish
between several highly suitable jobs.

For example, Statistical Programmer, Biostatistician, and R/Shiny
Developer all receive a score of 100%.

---

### Missing Skills

Missing required skills behave as intended.

For the Cloud Data Engineer role, the candidate has no recorded Azure or
Kubernetes skill:

| Skill      | Skill Match |
| ---------- | ----------: |
| Azure      |        0.0% |
| Kubernetes |        0.0% |
| Python     |       87.5% |
| SQL        |       69.4% |

This produces an overall qualification fit of approximately 39.2%.

The model therefore clearly distinguishes between partial deficits in an
existing skill and a required skill that is entirely absent from the
person profile.

---

## Limitations

### Equal Skill Weighting

The most important limitation observed in V1 is the use of equal weights
for all required skills.

The qualification score is calculated as:

$$
Q_{\text{V1}}(P,J) =
\frac{1}{|S_J|}\sum_{s\in S_J}m_s(P,J).
$$

This means that the impact of an individual skill depends directly on
the total number of skills listed for a job.

For example, if a job requires three skills and one is completely
missing while the remaining two are perfect matches, the resulting
score is:

$$
\frac{1+1+0}{3}=0.667.
$$

If another job lists ten required skills and only one is missing, the
result becomes:

$$
\frac{9}{10}=0.9.
$$

The semantic importance of the missing skill is not represented in
either calculation.

As a consequence, the score is sensitive to how many skills happen to
be represented in the job requirements. A larger number of listed
skills can dilute the effect of an important skill gap.

This is particularly problematic when one skill is essential for
performing the job while several others are secondary.

Future versions should therefore investigate skill importance weights,
mandatory-skill mechanisms, alternative aggregation functions, or a
combination of these approaches.

---

### Equal Weighting of Skill Components

Proficiency and experience are also weighted equally whenever both are
available:

$$
m_s(P,J)=\frac{m_{\text{prof},s}(P,J)+m_{\text{exp},s}(P,J)}{2}.
$$

There is currently no empirical justification that both components
should contribute equally to qualification fit.

The equal weighting is therefore a baseline assumption rather than a
claim about their actual importance.

---

### Ordinal Proficiency Distance

The proficiency model treats distances between adjacent proficiency
levels according to their ordinal ranks.

This implicitly imposes a numerical structure on levels such as
Beginner, Intermediate, Advanced, and Expert.

There is currently no empirical evidence that these transitions should
be treated as equally spaced.

A later model could replace this assumption with a calibrated lookup
table or another nonlinear mapping.

---

### Linear Experience Matching

Experience matching uses the ratio:

$$
m_{\text{exp},s}(P,J)=\min\left(1,\frac{e_P}{e_J}\right).
$$

This assumes proportional behaviour below the requirement.

For example, 2 years against a 4-year requirement and 5 years against a
10-year requirement both produce a match of 0.5.

Whether these situations should actually be considered equivalent is
unclear.

A nonlinear experience function may provide a more realistic model in a
future version.

---

### Limited Qualification Dimensions

V1 only evaluates explicitly represented skill requirements.

It does not yet consider:

- overall professional experience,
- seniority,
- domain knowledge,
- project evidence,
- education,
- skill substitutability,
- related skills,
- eligibility constraints,
- personal preferences.

The resulting score must therefore be interpreted specifically as a
baseline skill-based qualification fit and not as a complete measure of
job-person compatibility.

---

## Evaluation Conclusion

The V1 matching model behaves consistently with its mathematical
specification and produces a ranking that is broadly aligned with the
qualitative expectations of the synthetic evaluation dataset.

The model also provides useful explainability by preserving the
contribution of individual skills, proficiency matches, and experience
matches.

At the same time, the evaluation reveals several structural limitations,
most importantly the dependence of the overall score on the number of
required skills and the assumption that all skills are equally
important.

These limitations are not corrected within V1.

Instead, V1 serves as a deliberately simple and reproducible baseline
against which future matching approaches can be compared.

Future versions can therefore be evaluated not only by whether they
produce plausible rankings, but by whether they demonstrably improve
upon the behaviour and limitations documented here.
