# Decision Support

The Decision Support layer combines labour market information from Level 1 with personal profile information from Level 2.

Its central analytical problem is:

> **How well does a person $P$ match a job $J$?**

The answer to this question provides the foundation for subsequent decision-support functionality, including skill-gap prioritisation, learning recommendations, regional and company fit, salary benchmarking, and career-path analysis.

The matching problem is therefore treated as a separate mathematical modelling problem rather than as a simple BI measure.

---

# 1. The Job–Person Matching Problem

Let

$$
M(P,J)
$$

denote the overall match between person $P$ and job $J$.

The goal is to construct a function $M(P,J)$ that maps information about a person's capabilities and preferences together with the requirements of a job posting to an interpretable measure of compatibility.

Conceptually:

```text
Personal Profile P
        +
Job Requirements J
        |
        v
Matching Model
        |
        v
     M(P,J)
```

A naive approach could calculate the proportion of job requirements fulfilled by a person. Such a model, however, discards substantial information.

For example, it would fail to distinguish adequately between:

- different levels of proficiency,
- different amounts of experience,
- required and optional skills,
- weak and strong evidence for personal capabilities,
- compensable and non-compensable requirements,
- and different types of variables and measurement scales.

The matching problem therefore requires an **explicit mathematical model**.

Three fundamental modelling problems must be addressed.

---

# 2. Problem A – Local Matching Functions

For every relevant matching dimension $k$, a local matching function

$$
m_k(P,J)
$$

must describe how well the personal characteristic corresponds to the respective job requirement.

Alternatively, the same problem may be formulated using a local loss or distance

$$
\ell_k(P,J),
$$

where larger values indicate stronger disagreement.

The appropriate function depends on both the **measurement scale** and the **semantic meaning** of the characteristic.

There is therefore no reason to assume that one universal distance measure is appropriate for all dimensions.

## 2.1 Metric Characteristics

Some characteristics have a meaningful numerical scale.

An example is required professional experience in years.

If a job requires $r$ years and a person has $s$ years of relevant experience, the absolute distance

$$
|r-s|
$$

is mathematically well-defined but may be semantically inappropriate.

If the requirement represents a minimum, having more experience than required should not necessarily reduce the match.

A one-sided loss may therefore be more appropriate:

$$
\ell_{\mathrm{experience}}(s,r)
=
\max(0,r-s).
$$

This yields zero loss whenever the requirement is met or exceeded.

Possible normalisations and nonlinear alternatives should be investigated before implementation.

---

## 2.2 Ordinal Characteristics

Other characteristics are ordinal.

An example is proficiency:

```text
Beginner < Intermediate < Advanced < Expert
```

The ordering is meaningful, but the distances between adjacent categories are not defined.

Encoding these categories as

$$
1,2,3,4
$$

does not justify treating the numerical differences as metric distances.

In particular, it cannot automatically be assumed that the difference between Beginner and Intermediate is equivalent to the difference between Advanced and Expert.

Possible approaches include:

- explicitly defined matching matrices,
- threshold-based rules,
- monotone scoring functions,
- or other models that preserve ordering without assuming equal distances.

The chosen approach should reflect the semantics of the characteristic rather than numerical convenience.

---

## 2.3 Nominal and Preference-Based Characteristics

Some dimensions may have no natural numerical ordering at all.

Examples may include:

- location,
- employment type,
- industry,
- or particular working arrangements.

Their matching functions may therefore depend on explicit compatibility or preference rules rather than numerical distance.

For example, location fit may depend on:

- remote availability,
- willingness to relocate,
- commuting constraints,
- or preferred regions.

---

## 2.4 Evidence and Reliability

Not every characteristic necessarily contributes directly to the match.

Project evidence, for example, may instead influence the **reliability** of an estimated personal skill level.

Conceptually, the model may distinguish between:

```text
Capability
    |
    v
Local Skill Match

Evidence
    |
    v
Confidence / Reliability
```

The precise role of evidence remains an open modelling question.

It may become:

- an independent matching component,
- a modifier of personal proficiency,
- a confidence measure,
- or an explanatory quantity shown alongside the match score.

---

# 3. Problem B – Weighting

Even after suitable local matching functions have been defined, the relative importance of the different components remains unknown.

Let $$w_k$$ denote the importance assigned to matching dimension $k$.

A possible model may eventually take a form such as

$$
M(P,J)
=
\sum_{k=1}^{K} w_k m_k(P,J),
$$

subject, for example, to

$$
w_k \geq 0,
\qquad
\sum_{k=1}^{K} w_k = 1.
$$

However, the values of these weights cannot be chosen arbitrarily.

## 3.1 Job-Specific Importance

Different jobs may assign different importance to the same skill.

For example:

```text
Job A
Python        → Core Requirement
Git           → Nice to Have

Job B
Python        → Nice to Have
Git           → Core Requirement
```

Therefore, weights may need to depend on the job:

$$
w_{k}(J).
$$

This allows the same skill to contribute differently depending on the requirements of job $J$.

---

## 3.2 Possible Sources of Weights

Several approaches may be considered.

### Rule-based weighting

Weights are specified through transparent domain rules.

### Requirement-based weighting

Explicit distinctions in job postings such as

- required,
- preferred,
- optional,

determine relative importance.

### Market-based weighting

Information from the labour market may influence weights.

### User-dependent weighting

Personal preferences may affect the importance of criteria such as location, salary, or remote work.

### Data-driven weighting

Future versions may estimate weights from observed outcomes such as applications, interviews, or hiring decisions.

For the initial version, transparent and explainable weighting rules may be preferable to a complex model whose parameters cannot be justified.

---

# 4. Problem C – Aggregation and Non-Compensable Requirements

Even if all local matching functions $m_k$ and their weights $w_k$ are known, the overall aggregation function remains a separate modelling decision.

A weighted sum is a natural candidate, but it implies **compensability**.

A poor match on one dimension can be offset by sufficiently strong matches on other dimensions.

This assumption is not always appropriate.

## 4.1 Hard Requirements

Some requirements may represent eligibility conditions rather than gradual preferences.

Examples may include:

- mandatory certifications,
- required work authorisation,
- mandatory language requirements,
- required security clearance eligibility,
- or strict location constraints.

Failure to satisfy such a requirement may invalidate the job match regardless of performance on other dimensions.

The matching architecture may therefore require two stages:

```text
Person P + Job J
       |
       v
Hard-Constraint Check
       |
       +---- Failed ----> Not Eligible
       |
     Passed
       |
       v
Soft Matching Model
       |
       v
     M(P,J)
```

Mathematically, an eligibility function could be introduced:

$$
E(P,J)\in{0,1}.
$$

The final match could then conceptually take a form such as

$$
M(P,J)
=
E(P,J)\cdot S(P,J),
$$

where $S(P,J)$ represents the match across compensable criteria.

If

$$
E(P,J)=0,
$$

the overall match becomes zero regardless of the soft matching score.

---

## 4.2 Discontinuities Are Permissible

The resulting matching function is not required to be continuous.

A small change in an input may lead to a discrete change in eligibility if a hard requirement crosses a threshold.

For example, satisfying a mandatory certification requirement may change a person from

```text
Not Eligible
```

to

```text
Eligible
```

without any gradual transition.

Such discontinuities are not necessarily undesirable behaviour. They may correctly represent the semantics of the underlying decision problem.

Mathematical convenience should therefore not override domain meaning.

---

## 4.3 Partial Compensability

Between fully compensable criteria and absolute hard constraints, intermediate cases may also exist.

For example, a severe deficit in a core skill might not make a candidate strictly ineligible but should perhaps not be completely compensated by several minor strengths.

Possible aggregation approaches may therefore include:

- weighted additive models,
- multiplicative components,
- minimum thresholds,
- penalties,
- hierarchical aggregation,
- or combinations of these methods.

The appropriate aggregation structure remains an open modelling problem.

---

# 5. Matching Model Architecture

The current conceptual architecture can therefore be represented as:

```text
                Person P
                   +
                 Job J
                   |
                   v
        +---------------------+
        | A. Local Matching   |
        |                     |
        | m_skill             |
        | m_experience        |
        | m_proficiency       |
        | m_location          |
        | ...                 |
        +----------+----------+
                   |
                   v
        +---------------------+
        | B. Weighting        |
        |                     |
        | w_1, ..., w_K       |
        +----------+----------+
                   |
                   v
        +---------------------+
        | C. Aggregation      |
        |                     |
        | Hard Constraints    |
        | Soft Aggregation    |
        +----------+----------+
                   |
                   v
                M(P,J)
```

Problems A, B and C are logically distinct.

A valid matching model therefore requires explicit answers to all three:

1. **Local Matching:** How is compatibility measured within each dimension?
2. **Weighting:** How important is each dimension?
3. **Aggregation:** How are the dimensions combined, and which deficits may or may not be compensated?

---

# 6. Design Principles

Before choosing a concrete mathematical specification, the matching model should satisfy a set of desired properties.

Potential principles include:

### Interpretability

A user should be able to understand why a job received a particular match assessment.

### Monotonicity

Improving a personal characteristic relevant to a job should, all else being equal, not reduce the match unless the domain provides a specific reason.

### Requirement Sensitivity

More important job requirements should have a greater influence on the result than minor or optional requirements.

### Scale Awareness

Matching functions should respect the measurement scale of the underlying variables.

Ordinal variables must not automatically be treated as metric variables.

### Non-Compensability Where Appropriate

Failure to satisfy genuine hard requirements should not be hidden by strong performance on unrelated criteria.

### Transparency

Weights, thresholds and transformations should be documented and justifiable.

### Extensibility

The model should allow additional matching dimensions and alternative matching functions to be introduced later.

---

# 7. Open Modelling Questions

The following questions must be answered before implementing the first matching model:

- Which dimensions should contribute to $M(P,J)$?
- Which requirements should be treated as hard constraints?
- Which local matching function is appropriate for each dimension?
- How should ordinal proficiency levels be compared?
- How should experience deficits be normalised?
- How should missing information be treated?
- How should evidence influence skill assessments?
- How should requirement importance be extracted from job postings?
- How should weights be determined?
- Which criteria may compensate for one another?
- How should the final score be normalised and interpreted?

These questions define the next stage of the Decision Support modelling process.
