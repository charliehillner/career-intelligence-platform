# Skill Matching Model

This document develops the skill-specific component of the Job-Person Matching Model.

The overall matching model is defined conceptually as

$$
M(P,J) = E(P,J)\cdot A\left(Q(P,J),R(P,J)\right),
$$

where:

- $E(P,J)$ represents eligibility,
- $Q(P,J)$ represents qualification fit,
- $R(P,J)$ represents preference fit.

This document focuses exclusively on the **Skill Fit** component of Qualification Fit.

Other qualification dimensions such as education, seniority, certifications, and general professional experience are outside the current scope.

---

# V1 Modelling Philosophy

The quantities developed in this document represent human concepts such as skill compatibility, proficiency fit, and experience fit.

For these concepts, there is generally no uniquely correct mathematical function.

The purpose of the initial model is therefore not to claim that a particular functional form represents the true structure of job-person compatibility.

Instead, V1 follows a **simple-baseline-first approach**.

## Principles

For the initial implementation, matching functions should preferably be:

- parameter-free,
- deterministic,
- transparent,
- interpretable,
- bounded where appropriate,
- easy to implement,
- and based on explicitly documented assumptions.

Additional parameters should only be introduced when there is a defensible reason for estimating or selecting them.

For example, a function

$$
m(x;\alpha,\beta,\gamma)
$$

may provide substantially greater flexibility than a parameter-free baseline.

However, without empirical data or defensible domain knowledge for choosing

$$
\alpha,\beta,\gamma,
$$

this flexibility may create artificial precision rather than improve the model.

---

## Baseline Models as Hypotheses

The V1 matching functions should therefore be interpreted as **baseline modelling hypotheses**.

For example, the initial experience match

$$
m_{\text{exp},s}(P,J) =
\min\left(
1,
\frac{e_P(s)}{e_J(s)}
\right)
$$

implicitly assumes proportionality between experience fulfilment and experience match up to the required threshold.

This assumption is simple and interpretable, but it is not considered a statement about the true relationship between experience and employability.

Likewise, the initial proficiency model introduces simplifying assumptions about distances between ordinal proficiency ranks.

These assumptions are accepted temporarily because they provide reproducible baseline behaviour without requiring unsupported parameter estimates.

---

## Iterative Model Development

Matching functions should evolve through experimentation and evidence.

The intended development cycle is:

```text
Define desired properties
          |
          v
Choose simple baseline
          |
          v
Implement
          |
          v
Inspect real-world results
          |
          v
Identify systematic weaknesses
          |
          v
Formulate alternative model
          |
          v
Compare
          |
          v
Refine
```

A more complex model should therefore be introduced in response to an identified limitation rather than complexity being added pre-emptively.

---

## Model Evaluation

Because job-person compatibility is not directly observable as a uniquely defined numerical quantity, model evaluation cannot rely exclusively on comparison against a single objective ground truth.

Evaluation may instead involve several forms of evidence:

### Face Validity

Do individual match scores behave in a way that appears reasonable?

### Ranking Validity

Does the model rank obviously stronger matches above obviously weaker matches?

### Sensitivity Analysis

How strongly do recommendations change when individual inputs or modelling assumptions are modified?

### Expert Evaluation

Do recruiters, hiring managers, domain experts, or experienced job seekers consider the resulting rankings plausible?

### Outcome-Based Validation

If sufficient historical data becomes available, model outputs may be compared against outcomes such as:

- interview invitations,
- application success,
- recruiter responses,
- or hiring decisions.

Such outcomes are themselves noisy and potentially biased and should therefore not automatically be interpreted as perfect ground truth.

---

## Guiding Principle

The V1 model follows the principle:

> **Prefer the simplest model whose assumptions are explicit and whose behaviour is useful. Add complexity only when evidence demonstrates why it is needed.**

The goal is not mathematical complexity.

The goal is an explainable model that can be inspected, criticised, tested, and improved.

---

# 1. Scope

Let

$$
S_J=\lbrace s_1,\ldots,s_n\rbrace
$$

denote the set of skills required by job $J$.

For each required skill $s\in S_J$, the model first determines an individual skill match

$$
m_s(P,J).
$$

These individual matches are subsequently aggregated into an overall Skill Fit

$$
m_{\mathrm{Skills}}(P,J) = A_S\left({m_s(P,J):s\in S_J}\right).
$$

The Skill Matching Problem therefore contains two distinct aggregation levels:

```text
Proficiency Match ──┐
                    ├──> Individual Skill Match
Experience Match ───┘           m_s(P,J)
                                      |
                                      |
                         +------------+------------+
                         |            |            |
                      Python         SQL        Power BI
                         |            |            |
                         +------------+------------+
                                      |
                                      v
                              Overall Skill Fit
                             m_Skills(P,J)
```

The current modelling process starts at the lowest level.

---

# 2. V1 Assumptions

The first version deliberately restricts the skill matching problem.

The following assumptions apply:

- Skills are represented by normalised identifiers.
- A required skill is matched only against the same normalised skill.
- No skill substitution is performed.
- No skills are inferred from other skills.
- No ontology-based skill similarity is considered.
- Skill relationships such as `MySQL → SQL` or `PyTorch → Python` are outside the initial scope.

Thus, if job (J) requires skill (s), the model initially considers only the person's capability regarding the same skill (s).

Skill similarity may be introduced as a future extension through a function such as

$$
\text{sim}(s_1,s_2).
$$

---

# 3. Individual Skill Match

For a particular skill $s$, the job and person may provide several relevant characteristics.

On the personal side:

$$
P_s =\left(
\text{Prof}(P,s),
\text{Exp}(P,s),
\text{Evidence}(P,s)
\right).
$$

On the job side:

$$
J_s = \left(
\text{ReqProf}(J,s),
\text{ReqExp}(J,s),
\text{Importance}(J,s)
\right).
$$

The individual skill match is therefore conceptually defined as

$$
m_s(P,J) = f_s(P_s,J_s).
$$

The first component investigated is proficiency.

---

# 4. How should $m_{\mathrm{prof},s}(P,J)$ be defined?

## 4.1 Problem Definition

Assume that proficiency is represented by an ordered set

$$
\mathcal P = \lbrace
\text{Beginner},
\text{Intermediate},
\text{Advanced},
\text{Expert}
\rbrace.
$$

The ordering

$$
\text{Beginner}
<
\text{Intermediate}
<
\text{Advanced}
<
\text{Expert}
$$

means that proficiency is **ordinally scaled**.

The distances between adjacent categories are not intrinsically defined.

Therefore,

$$
\text{distance}(\text{Beginner},\text{Intermediate})
$$

is not automatically equivalent to

$$
\text{distance}(\text{Advanced},\text{Expert}).
$$

Any model using numerical differences between proficiency ranks therefore introduces an additional modelling assumption.

Two initial approaches are considered:

1. rank-based distance,
2. explicit lookup table.

---

## 4.2 Approach A – Rank-Based Distance

Define an ordinal rank function

$$
r:\mathcal P\rightarrow \lbrace 1,\ldots,R \rbrace.
$$

For example:

| Proficiency  | Rank |
| ------------ | ---: |
| Beginner     |    1 |
| Intermediate |    2 |
| Advanced     |    3 |
| Expert       |    4 |

A normalised squared rank distance can then be defined as

$$
\ell_{\mathrm{prof}}(p_1,p_2) = \left(
\frac{r(p_1)-r(p_2)}
{R_{\max}-R_{\min}}
\right)^2.
$$

For the four-level scale,

$$
R_{\max}-R_{\min}=3.
$$

This produces

$$
\ell_{\mathrm{prof}}\in[0,1],
$$

where

$$
\ell_{\mathrm{prof}}=0
$$

represents equal proficiency and

$$
\ell_{\mathrm{prof}}=1
$$

represents the maximum possible rank difference.

Since this quantity represents disagreement rather than compatibility, it is more naturally interpreted as a **proficiency loss**.

A corresponding match could be defined as

$$
m_{\mathrm{prof}} =
1-\ell_{\mathrm{prof}}.
$$

### Advantages

- simple,
- normalised,
- symmetric,
- easy to explain,
- easy to implement,
- automatically extends to additional proficiency levels.

### Limitations

The approach implicitly assumes that rank differences contain meaningful distance information.

For example, it treats every one-rank difference identically before applying the squared transformation.

Thus,

$$
|r(\text{Beginner})-r(\text{Intermediate})| =
|r(\text{Advanced})-r(\text{Expert})|.
$$

This assumption is not implied by ordinal measurement alone.

The squared loss additionally introduces a particular penalty structure: larger rank differences increase disproportionately.

Both choices are modelling assumptions rather than consequences of the data scale.

---

## 4.3 Symmetry of the Rank-Based Model

The proposed distance is symmetric:

$$
\ell_{\mathrm{prof}}(p_1,p_2) =
\ell_{\mathrm{prof}}(p_2,p_1).
$$

For job-person matching, this property may be undesirable.

Consider a job requiring `Intermediate` proficiency.

### Person A

```text
Required: Intermediate
Personal: Beginner
```

### Person B

```text
Required: Intermediate
Personal: Advanced
```

The symmetric distance assigns the same loss to both:

$$
\ell(\text{Beginner},\text{Intermediate}) =
\ell(\text{Advanced},\text{Intermediate}).
$$

Semantically, however, these situations are very different.

- Person A falls below the requirement.
- Person B exceeds it.

If proficiency requirements are interpreted primarily as **minimum requirements**, exceeding the required proficiency should generally not reduce the match.

This suggests an asymmetric alternative.

Define

$$
\ell_{\mathrm{prof}}(P,J) = \left(\frac{\max\left(0, r(\text{ReqProf}(Js)) - r(\text{Prof}(P,s))\right)}{R_{\max}-R_{\min}}\right)^2.
$$

Then:

$$
r(\text{Prof}(P,s)) \geq r(\text{ReqProf}(J,s))
$$

implies

$$
\ell_{\mathrm{prof}}(P,J)=0.
$$

The corresponding match is again

$$
m_{\mathrm{prof},s}(P,J) =
1-\ell_{\mathrm{prof}}(P,J).
$$

This model interprets proficiency requirements as thresholds rather than target values.

Whether this interpretation is appropriate must be decided from the semantics of job requirements.

---

## 4.4 Approach B – Lookup Table

Instead of deriving match values from numerical ranks, compatibility can be specified explicitly.

For example:

| Personal \ Required | Beginner | Intermediate | Advanced | Expert |
| ------------------- | -------: | -----------: | -------: | -----: |
| Beginner            |     1.00 |         0.70 |     0.30 |   0.10 |
| Intermediate        |     1.00 |         1.00 |     0.70 |   0.30 |
| Advanced            |     1.00 |         1.00 |     1.00 |   0.70 |
| Expert              |     1.00 |         1.00 |     1.00 |   1.00 |

These values are illustrative only.

The lookup table directly defines

$$
m_{\mathrm{prof}}:
\mathcal P\times\mathcal P
\rightarrow[0,1].
$$

No assumption of equal distances between ordinal categories is required.

The table can also naturally represent asymmetry.

For example,

$$
m(\text{Advanced},\text{Intermediate})=1
$$

while

$$
m(\text{Intermediate},\text{Advanced})<1.
$$

### Advantages

- respects the ordinal nature of proficiency,
- allows asymmetric matching,
- highly flexible,
- easy to inspect,
- domain assumptions are explicit.

### Limitations

The flexibility creates a new problem:

> Where do the lookup values come from?

Values such as

$$
0.7,\quad0.3,\quad0.1
$$

cannot be justified merely from the ordering of proficiency categories.

They must come from:

- domain knowledge,
- empirical calibration,
- expert judgement,
- observed hiring outcomes,
- or explicitly documented modelling assumptions.

A lookup table therefore avoids unjustified metric assumptions but introduces parameters that themselves require justification.

---

## 4.5 Comparison of Both Approaches

| Property                | Rank-Based             | Lookup Table   |
| ----------------------- | ---------------------- | -------------- |
| Respects ordering       | Yes                    | Yes            |
| Assumes rank distances  | Yes                    | No             |
| Can be asymmetric       | Yes, with modification | Yes            |
| Number of parameters    | Low                    | Higher         |
| Easy to extend          | High                   | Moderate       |
| Flexibility             | Moderate               | High           |
| Parameter justification | Relatively simple      | More difficult |
| Interpretability        | High                   | High           |

Neither approach is automatically correct.

The choice depends on which assumptions are considered more defensible for the application.

---

## 4.6 Desired Properties

Before choosing a final function, the proficiency match should satisfy several properties.

### Identity

If personal and required proficiency are equal,

$$
m_{\mathrm{prof},s}(P,J)=1.
$$

### Monotonicity

Holding the job requirement fixed, increasing personal proficiency should not decrease the match.

If

$$
p_1\leq p_2,
$$

then

$$
m_{\mathrm{prof}}(p_1,r)
\leq
m_{\mathrm{prof}}(p_2,r).
$$

### Requirement Satisfaction

If proficiency requirements are interpreted as minimum requirements, then

$$
p\geq r
$$

should imply

$$
m_{\mathrm{prof}}(p,r)=1.
$$

### Boundedness

For interpretability,

$$
m_{\mathrm{prof}}\in[0,1]
$$

can be interpreted as a percentage-based score.

### Ordinal Awareness

The model should not implicitly claim metric information about proficiency categories without explicitly documenting this as a modelling assumption.

---

## 4.7 Current Status

No final proficiency matching function is selected yet.

The two primary candidates are:

$$
\boxed{
\text{asymmetric normalised rank loss}
}
$$

and

$$
\boxed{
\text{explicit proficiency lookup table}
}
$$

The rank-based model provides a parsimonious baseline.

The lookup-table model provides greater semantic flexibility but requires substantially more parameter justification.

The final choice should be based on the desired properties of the matching model and the availability of defensible information for calibrating proficiency differences.

# 5. How Should $m_{\text{exp},s}(P,J)$ Be Defined?

## 5.1 Problem Definition

For a particular skill (s), let

$$
e_P(s)
$$

denote the amount of experience person (P) has with skill (s), and let

$$
e_J(s)
$$

denote the amount of experience required by job (J).

Experience is assumed to be measured in years and therefore has a meaningful metric scale.

Unlike ordinal proficiency levels, numerical differences and ratios between experience values are interpretable.

However, this does not imply that a simple numerical distance provides a meaningful matching function.

The objective is to define

$$
m_{\text{exp},s}(P,J) \in [0,1],
$$

where larger values indicate a better match between personal and required experience regarding skill (s).

---

## 5.2 Symmetric Distance

A simple candidate would be based on absolute distance:

$$
d_{\text{exp},s}(P,J) = \left|e_J(s)-e_P(s)\right|.
$$

This approach is mathematically straightforward but semantically problematic.

Suppose a job requires five years of experience.

A person with two years and a person with eight years would both have distance

$$
|5-2| = |5-8| = 3.
$$

This treats underqualification and exceeding the requirement identically.

If job experience requirements are interpreted as minimum requirements, this behaviour is undesirable.

---

## 5.3 One-Sided Experience Loss

A more appropriate baseline is therefore an asymmetric loss:

$$
\ell_{\text{exp},s}(P,J) =
\max\left(0,e_J(s)-e_P(s)\right).
$$

If personal experience meets or exceeds the requirement,

$$
e_P(s)\geq e_J(s),
$$

then

$$
\ell_{\text{exp},s}(P,J)=0.
$$

This reflects the interpretation that additional experience does not reduce qualification fit.

However, the raw loss is unbounded and depends strongly on the magnitude of the requirement.

A deficit of one year may have a different interpretation when the requirement is two years than when the requirement is ten years.

---

## 5.4 Relative Experience Loss

The deficit can therefore be normalised by the required experience:

$$
\ell_{\text{exp},s}^{\text{rel}}(P,J) =
\frac{
\max\left(0,e_J(s)-e_P(s)\right)
}{
e_J(s)
}
$$

for

$$
e_J(s)>0.
$$

A corresponding experience match is

$$
m_{\text{exp},s}(P,J) =
1-\ell_{\text{exp},s}^{\text{rel}}(P,J).
$$

For

$$
e_P(s)\geq0
$$

and

$$
e_J(s)>0,
$$

this simplifies to

$$
m_{\text{exp},s}(P,J) =
\min\left(1,\frac{e_P(s)}{e_J(s)}\right).
$$

This produces an intuitive interpretation.

For a requirement of four years:

| Personal Experience | Required Experience | Match |
| ------------------: | ------------------: | ----: |
|                   0 |                   4 |  0.00 |
|                   1 |                   4 |  0.25 |
|                   2 |                   4 |  0.50 |
|                   3 |                   4 |  0.75 |
|                   4 |                   4 |  1.00 |
|                   6 |                   4 |  1.00 |

---

## 5.5 Assumption of Proportionality

The relative model introduces an important assumption:

> Experience match increases linearly with the proportion of required experience already obtained.

For example,

$$
m_{\text{exp},s}(2,4)=0.5
$$

and

$$
m_{\text{exp},s}(5,10)=0.5.
$$

The model therefore treats both candidates as having achieved half of the required experience.

Whether this is semantically appropriate is not obvious.

It assumes that experience has constant marginal value up to the required threshold.

In reality, the relationship between time and professional capability may be nonlinear.

For example, the difference between zero and one year of experience may be more substantial than the difference between nine and ten years.

Thus, while experience itself is metrically scaled, **experience match does not necessarily have to be linear in experience**.

---

## 5.6 Nonlinear Alternatives

A more flexible model could transform the experience ratio.

Define

$$
q_s(P,J) =
\min\left(1,\frac{e_P(s)}{e_J(s)}\right).
$$

The experience match could then be defined as

$$
m_{\text{exp},s}(P,J) =
g\left(q_s(P,J)\right),
$$

where

$$
g:[0,1]\rightarrow[0,1]
$$

is a monotone transformation satisfying

$$
g(0)=0
$$

and

$$
g(1)=1.
$$

For example, a power function could be used:

$$
g(q)=q^\alpha.
$$

Different choices of (\alpha) imply different assumptions about how experience deficits should be penalised.

However, introducing such parameters creates the same calibration problem encountered in proficiency matching:

> What empirical or domain knowledge justifies the chosen shape?

Without appropriate data, additional mathematical flexibility may create artificial precision rather than improve the model.

---

## 5.7 Special Case: No Explicit Experience Requirement

If a job mentions skill (s) but does not specify a required number of years, then

$$
e_J(s)
$$

is unknown rather than necessarily equal to zero.

This distinction is important.

```text
No experience required
```

and

```text
No experience requirement stated
```

represent different information.

Therefore, missing required experience should not automatically be encoded as

$$
e_J(s)=0.
$$

Instead, the experience component may need to be excluded from the individual skill match when no explicit requirement can be identified.

The aggregation model must later define how missing components are handled.

---

## 5.8 Desired Properties

A baseline experience matching function should satisfy the following properties.

### Boundedness

$$
0\leq m_{\text{exp},s}(P,J)\leq1.
$$

### Requirement Satisfaction

If

$$
e_P(s)\geq e_J(s),
$$

then

$$
m_{\text{exp},s}(P,J)=1.
$$

### Monotonicity

For a fixed job requirement, additional relevant experience should not decrease the match.

If

$$
e_{P_1}(s)\leq e_{P_2}(s),
$$

then

$$
m_{\text{exp},s}(P_1,J)
\leq
m_{\text{exp},s}(P_2,J).
$$

### Zero Experience

For a positive experience requirement,

$$
e_P(s)=0
$$

should result in the minimum experience match.

### Asymmetry

Experience below the requirement may reduce the match, while experience exceeding the requirement should not automatically be penalised.

---

## 5.9 V1 Baseline

For the initial model, the relative experience match provides a simple and transparent baseline:

$$
\boxed{
m_{\text{exp},s}(P,J) =
\min\left(
1,
\frac{e_P(s)}{e_J(s)}
\right)
}
$$

for explicitly stated requirements

$$
e_J(s)>0.
$$

This model is selected because it is:

- transparent,
- deterministic,
- parameter-free,
- normalised,
- asymmetric,
- and easy to explain.

Its primary limitation is the assumption that experience match increases proportionally with experience up to the required threshold.

Future versions may replace the linear relationship with an empirically calibrated nonlinear function if sufficient data becomes available.

# 6. How should $m_{Evidence, s}(P, J)$ be modelled?

Evidence is available in the data model but is not yet included numerically in the Skill Match. It is initially used for explainability and confidence assessment.
