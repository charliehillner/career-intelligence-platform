# Job–Person Matching Model

This document develops the mathematical model used to quantify the compatibility between a person (P) and a job posting (J).

The central quantity is

$$
M(P,J),
$$

which represents the overall match between person $P$ and job $J$.

The matching model is developed independently from the Power BI implementation. Its purpose is to provide a mathematically justified analytical foundation for the Decision Support layer.

---

# 1. Overall Decomposition

Job-person compatibility consists of three conceptually distinct components:

1. **Eligibility**
2. **Qualification Fit**
3. **Preference Fit**

These components answer different questions.

| Component         | Question                                     |
| ----------------- | -------------------------------------------- |
| Eligibility       | Can the person take this job?                |
| Qualification Fit | Can the person perform this job?             |
| Preference Fit    | Does the job match the person's preferences? |

Evidence is initially treated separately as information about the reliability of personal skill assessments rather than as an independent fit dimension.

---

# 2. Eligibility

Eligibility represents requirements that cannot meaningfully be compensated by strengths in unrelated dimensions.

Let

$$
E(P,J)\in{0,1}
$$

denote whether person $P$ satisfies all mandatory eligibility requirements of job $J$.

Examples may include:

- mandatory work authorisation,
- mandatory certifications,
- mandatory security requirements,
- legally required qualifications,
- other genuine hard constraints.

If any mandatory requirement is violated,

$$
E(P,J)=0.
$$

Otherwise,

$$
E(P,J)=1.
$$

Eligibility therefore acts as a gate rather than as an ordinary matching component.

Conceptually, the overall model may eventually have the structure

$$
M(P,J)
=
E(P,J)\cdot S(P,J),
$$

where $S(P,J)$ represents compatibility across compensable dimensions.

This formulation explicitly permits discontinuities in $M(P,J)$.

---

# 3. Soft Matching

Conditional on eligibility, the remaining match is divided into two major components:

$$
Q(P,J)
$$

for **Qualification Fit**, and

$$
R(P,J)
$$

for **Preference Fit**.

The soft matching component can conceptually be written as

$$
S(P,J)
=
A\left(Q(P,J), R(P,J)\right),
$$

where $A$ denotes an aggregation function.

A weighted additive model is a natural initial candidate:

$$
S(P,J)
=

w_Q(J)Q(P,J)

- w_R(P,J)R(P,J),
$$

with

$$
w_Q(J),w_R(P,J)\geq0.
$$

The exact weighting and normalisation scheme remains an open modelling question.

The notation emphasises that qualification importance may depend on the job, while preference importance may additionally depend on the person.

---

# 4. Qualification Fit

Qualification Fit measures how well the professional capabilities of person $P$ correspond to the requirements of job $J$.

Potential components include:

- required skills,
- skill-specific proficiency,
- skill-specific experience,
- overall professional experience,
- seniority,
- domain knowledge.

However, these components do not necessarily form a flat collection of independent criteria.

In particular, skill-related matching has an internal hierarchical structure.

---

# 5. Skill Matching

A job generally requires multiple skills.

Let

$$
S_J=\lbrace s_1,\ldots,s_n \rbrace
$$

denote the set of skills required by job $J$.

The quantity

$$
m_{\mathrm{Skills}}(P,J)
$$

therefore cannot represent a single direct comparison.

Instead, it must aggregate individual skill-specific matches

$$
m_s(P,J),
\qquad s\in S_J.
$$

Conceptually,

$$
m_{\mathrm{Skills}}(P,J)
=
A_S
\left(
{m_s(P,J):s\in S_J}
\right),
$$

where $A_S$ denotes a skill aggregation function.

A simple weighted candidate would be

$$
m_{\mathrm{Skills}}(P,J)
=
\sum_{s\in S_J}
w_s(J)m_s(P,J),
$$

subject to an appropriate normalisation such as

$$
\sum_{s\in S_J}w_s(J)=1.
$$

Here,

$$
w_s(J)
$$

represents the importance of skill $s$ for job $J$.

For example, a core requirement should generally receive greater importance than an optional or supporting skill.

The exact determination of $w_s(J)$ is a separate modelling problem.

---

# 6. Internal Structure of a Skill Match

Even the individual skill match

$$
m_s(P,J)
$$

may itself consist of multiple components.

For a particular skill $s$, relevant information may include:

### Proficiency

$$
\operatorname{Prof}(P,s)
$$

versus

$$
\operatorname{ReqProf}(J,s).
$$

### Experience

$$
\operatorname{Exp}(P,s)
$$

versus

$$
\operatorname{ReqExp}(J,s).
$$

### Evidence

The person's claimed capability may additionally be supported by evidence such as projects.

Evidence is initially interpreted as a reliability or confidence component rather than as a direct measure of compatibility.

Thus, the conceptual structure is:

```text
Skill s
   |
   +------ Personal Side
   |          |
   |          +-- Proficiency(P,s)
   |          +-- Experience(P,s)
   |          +-- Evidence(P,s)
   |
   +------ Job Side
              |
              +-- RequiredProficiency(J,s)
              +-- RequiredExperience(J,s)
              +-- Importance(J,s)
```

A skill-specific matching function therefore has the general form

$$
m_s(P,J)
=
f_s\left(P_s,J_s\right),
$$

where $P_s$ and $J_s$ represent the personal and job-specific information associated with skill $s$.

The precise definition of $f_s$ remains an open modelling question.

---

# 7. Hierarchical Matching Structure

The resulting qualification model is hierarchical rather than flat.

Conceptually:

```text
Qualification Fit Q(P,J)
│
├── Skill Fit
│   │
│   ├── Python Match
│   │   ├── Proficiency Match
│   │   └── Experience Match
│   │
│   ├── SQL Match
│   │   ├── Proficiency Match
│   │   └── Experience Match
│   │
│   └── Power BI Match
│       ├── Proficiency Match
│       └── Experience Match
│
├── Overall Experience Fit
├── Seniority Fit
└── Domain Knowledge Fit
```

This structure implies multiple levels of aggregation.

For example:

$$
m_{\mathrm{proficiency},s} \text{, }
m_{\mathrm{experience},s}
$$

may first be combined into

$$
m_s(P,J).
$$

The individual skill matches may then be combined into

$$
m_{\mathrm{Skills}}(P,J).
$$

Finally, Skill Fit and other qualification components may be combined into

$$
Q(P,J).
$$

Therefore, aggregation is not a single operation performed at the end of the model. It occurs at multiple hierarchical levels.

---

# 8. Preference Fit

Preference Fit measures compatibility between job characteristics and personal preferences.

Potential dimensions include:

- location,
- remote-work arrangement,
- salary,
- employment type,
- industry.

Conceptually,

$$
R(P,J)
=
A_R
\left(
m_{\mathrm{location}},
m_{\mathrm{remote}},
m_{\mathrm{salary}},
m_{\mathrm{employment}},
m_{\mathrm{industry}},
\ldots
\right).
$$

Unlike qualification requirements, preference matching is primarily determined by compatibility between job characteristics and personal preferences.

Preference weights may therefore depend on the person as well as the job.

For example, remote work may be highly important to one person but irrelevant to another.

---

# 9. Current Matching Architecture

The current conceptual model can be summarised as:

```text
                         Person P + Job J
                                |
                                v
                         Eligibility E(P,J)
                                |
                      +---------+---------+
                      |                   |
                   E = 0                E = 1
                      |                   |
                      v                   v
                  No Match          Soft Matching
                                          |
                         +----------------+----------------+
                         |                                 |
                         v                                 v
                Qualification Fit Q(P,J)         Preference Fit R(P,J)
                         |
            +------------+-------------+
            |                          |
            v                          v
       Skill Fit                 Other Qualification
            |
      +-----+-----+-----+
      |           |     |
      v           v     v
   Skill 1     Skill 2 ... Skill n
      |
   +--+--+
   |     |
   v     v
 Prof.  Exp.
 Match  Match
```

The overall matching function may therefore eventually take the general form

$$
M(P,J)
=
E(P,J)
\cdot
A
\left(
Q(P,J),
R(P,J)
\right).
$$

The exact definitions of the local matching functions, weighting functions and aggregation operators remain subjects of further modelling.

---

# 10. Key Modelling Consequence

The Job-Person Matching Model should not be interpreted as one large weighted sum over unrelated variables.

Instead, it is a **hierarchical matching model**.

Local comparisons are performed at the lowest meaningful level and subsequently aggregated into increasingly broader concepts:

$$
\text{local attribute matches}
\rightarrow
\text{skill matches}
\rightarrow
\text{qualification/preference matches}
\rightarrow
\text{overall job-person match}.
$$

This hierarchy preserves the semantic structure of the underlying problem and allows different matching methods to be used for different types of variables.
