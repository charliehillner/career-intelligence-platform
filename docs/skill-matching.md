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

# 4.2 Approach A – Rank-Based Distance

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

# 4.4 Approach B – Lookup Table

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

# 4.5 Comparison of Both Approaches

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

# 4.6 Desired Properties

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

# 4.7 Current Status

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
