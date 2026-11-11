# Lecture 6: Comparing two treatments I

**Date:** 29 Oct 2026 (onsite) · **Lecturer:** Lukas Schmid · [Exercises](exercises.md) · [Notebook](exercises.ipynb)

## Contents

1. [Motivation](#1-motivation)
2. [Causal estimands](#2-causal-estimands)
3. [Characteristics of experiments](#3-characteristics-of-experiments)
4. [Key terms](#key-terms)

The slides give the definitions and examples 6.1 to 6.6. The Salk trial figures in section 1.4 and the worked answers to the open questions in examples 6.3 and 6.6 are my additions, sources at the end.

Lecture 5 set up the potential outcome framework. This lecture turns it into something you can compute, and gives the two assumptions that make randomization work.

---

## 1. Motivation

#### Example 6.1: Salk vaccine field trial

Polio caused hundreds of thousands of victims in the first half of the 20th century. Laboratory tests of the Salk vaccine looked promising, and in 1954 the US Public Health Service was ready to try it outside the lab. The question was how to measure its effectiveness in the real world.

The slides walk through three designs. The first two are the wrong answers, and they are wrong for reasons from lectures 3 and 4.

### 1.1 Proposal 1: vaccinate many children and compare this year to last year

**What is problematic?** Polio is an epidemic disease, and the incidence rate swings enormously from year to year for reasons that have nothing to do with any vaccine. The slide's own figure (Meier 1957, polio cases in the US 1930–56) makes the point: cases climb through the 1940s, peak around 1952 at roughly 58,000, and are already falling in 1953.

A before/after comparison confounds the vaccine with the epidemic cycle. If 1954 happened to be a mild year, the vaccine would look like a triumph whether or not it worked. If 1954 happened to be severe, a working vaccine could look useless.

This is the beriberi design from lecture 5 (Ryujo versus Tsukuba) with the same flaw: **no simultaneous control group**, so anything that changed between the two periods is part of the estimate.

### 1.2 Proposal 2: let parents decide, and use the non-consenting children as controls

Parents must give permission for a vaccination, so the obvious shortcut is to vaccinate the children whose parents agree and treat the rest as the control group.

**What is problematic?** Consent is a choice, so the two groups differ in everything that drives the choice. In the lecture 5 language, selection bias is not zero: E[Y(0) | D = 1] ≠ E[Y(0) | D = 0].

Meier reports that volunteering families "tend to be better educated and, generally, more well-to-do". The direction of the resulting bias was **not predictable in advance**, because polio was linked to better hygiene: children in cleaner homes met the virus later, missed the mild infant infection that confers immunity, and were therefore more likely to be paralysed if they caught it as schoolchildren. Better-off children were plausibly at **higher** risk, which would bias against the vaccine.

The trial itself ended up measuring this. See 1.4.

### 1.3 Proposal 3: randomize, with a placebo

> The solution was to give every child a 50% chance to get the vaccine. All other children received a placebo that looked exactly like the vaccine.

| Group | Group size | Polio rate (per 100,000) |
| --- | --- | --- |
| Treatment | 200,000 | 28 |
| Control | 200,000 | 71 |

The difference is highly statistically significant (lecture 7 covers how that is established).

Three design choices are doing work here, and each one closes a specific hole:

| Choice | What it closes |
| --- | --- |
| **Randomized** assignment | selection bias, all of it, measured and unmeasured |
| **Simultaneous** control group | the epidemic cycle from proposal 1 |
| **Placebo** that looks identical | the placebo and John Henry effects, and, because diagnosis is a judgement call, the doctor's expectation. The trial was **double blind** |

Blinding deserves the emphasis. Polio diagnosis in borderline cases depends on a physician's judgement, and a physician who knows the child was vaccinated will read the symptoms differently. In the randomized areas nobody knew who got what until the code was broken.

### 1.4 What the trial measured about consent

The 1954 programme actually ran **two designs at once**, which is why it is such a useful teaching case. Some districts ran the randomized placebo-controlled trial. Others ran the "observed control" design that the National Foundation for Infantile Paralysis preferred: vaccinate second-graders whose parents consented, use first- and third-graders as controls.

Paralytic polio rates per 100,000 (Meier 1957):

| | Randomized areas | | NFIP observed-control areas | |
| --- | --- | --- | --- | --- |
| | Group | Rate | Group | Rate |
| Vaccinated | consenters, randomized in | **16** | grade 2 consenters | **17** |
| Control | consenters, randomized out (placebo) | **57** | grades 1 and 3, everyone | **46** |
| Not inoculated | non-consenters | **36** | grade 2 non-consenters | **35** |

Read the third row against the second:

- In the randomized areas, the children whose parents **consented** and got the placebo had a polio rate of 57. The children whose parents **refused** had a rate of 36. Consent is strongly related to the outcome, exactly as proposal 2 feared.
- So the NFIP comparison, 17 against 46, mixes a consenter treatment group with a control group that contains both types. Because non-consenters are lower risk, the control group's 46 is pulled below what the treated children would have had, and the design **understates** the vaccine.
- The randomized estimate is 57 − 16 = 41 per 100,000. The NFIP estimate is 46 − 17 = 29. The observed-control design loses nearly a third of the effect.

The slide's 28 and 71 are rates for **all** polio cases. Meier's 16 and 57 are for **paralytic** polio only. Both are correct for their own definition, so do not try to reconcile them.

---

## 2. Causal estimands

### 2.1 Manipulation

- Yᵢ(d) is the value Yᵢ would take under Dᵢ set to d.
- For this to be a theoretically meaningful concept, Dᵢ should be **manipulable at least in principle**. This is Holland's (1986) slogan: **"no causation without manipulation"**.
- Difficult causal problems:
  - effect of gender, race, schooling
  - effect of macroeconomic variables (negative interest rates before 2008, effect of good institutions)

Why these are difficult: Yᵢ(1) has to mean something. "What would this person's wage be if she were a man" is not a well-posed question until you say what exactly changes, since you cannot intervene on gender without also intervening on everything attached to it. Researchers usually reformulate into something manipulable: audit studies change the **name on a CV**, which is an intervention you can actually make, and which answers a narrower question.

Note what this does to SUTVA part 2 from lecture 5. A treatment that cannot be manipulated has no single version either, so the two problems are the same problem seen from different sides.

### 2.2 The estimands

**Average treatment effect (ATE):**

> τ = E[τᵢ] = (1/N) Σᵢ [Yᵢ(1) − Yᵢ(0)]

**Average treatment effect on the treated (ATT):**

> τ_ATT = E[τᵢ | Dᵢ = 1] = (1/N_t) Σ_{i:Dᵢ=1} [Yᵢ(1) − Yᵢ(0)],  where N_t = Σᵢ Dᵢ

Both are averages of the same individual effects. They differ only in who is averaged over.

#### Example 6.2 and 6.3: the seven students again

| Student i | Dᵢ | Yᵢ(0) | Yᵢ(1) | τᵢ |
| --- | --- | --- | --- | --- |
| 1 | 1 | 145 | 155 | 10 |
| 2 | 0 | 100 | 100 | 0 |
| 3 | 0 | 120 | 130 | 10 |
| 4 | 0 | 110 | 100 | −10 |
| 5 | 0 | 50 | 55 | 5 |
| 6 | 1 | 120 | 130 | 10 |
| 7 | 1 | 125 | 135 | 10 |
| **Average** | | **110** | **115** | **5** |

Example 6.3 on the slides is an empty box, to be filled in during the lecture. The answers:

> **ATE** = (10 + 0 + 10 − 10 + 5 + 10 + 10) / 7 = 35 / 7 = **5**
>
> **ATT** = (10 + 10 + 10) / 3 = 30 / 3 = **10**, over students 1, 6 and 7
>
> **ATU** = (0 + 10 − 10 + 5) / 4 = 5 / 4 = **1.25**, over students 2 to 5

ATE is the weighted average of the two: (3 × 10 + 4 × 1.25) / 7 = 5.

They differ here because the treated students are not a random subset. All three treated students happen to have τᵢ = 10, while the untreated ones are all over the place. Under randomization the three numbers coincide in expectation, which is the entire point of section 3.

### 2.3 The naive estimator

> E[Yᵢ | Dᵢ = 1] − E[Yᵢ | Dᵢ = 0] = **ATT + selection bias**

- **ATT:** E[Yᵢ(1) − Yᵢ(0) | Dᵢ = 1]
- **Selection bias:** how different the treated and control groups are in terms of their potential outcome under the control condition, E[Yᵢ(0) | Dᵢ = 1] − E[Yᵢ(0) | Dᵢ = 0]
- Both terms are **unobserved**. The ATT is therefore unidentified unless the selection bias equals 0.

That last sentence is the exam-relevant one. You never get to see the split. You can only argue that the second term is zero by pointing at the **design**, which is why randomization is a claim about how the data were produced, not a property you can test in the data.

#### Example 6.4: naive estimate and selection bias

| Student i | Dᵢ | Yᵢ (observed) | Yᵢ(0) | Yᵢ(1) |
| --- | --- | --- | --- | --- |
| 1 | 1 | 155 | 145 | 155 |
| 2 | 0 | 100 | 100 | 100 |
| 3 | 0 | 120 | 120 | 130 |
| 4 | 0 | 110 | 110 | 100 |
| 5 | 0 | 50 | 50 | 55 |
| 6 | 1 | 130 | 120 | 130 |
| 7 | 1 | 135 | 125 | 135 |

> E[Y | D = 1] = (155 + 130 + 135) / 3 = **140**
> E[Y | D = 0] = (100 + 120 + 110 + 50) / 4 = **95**
> naive = **45**
>
> ATT = **10**
> selection bias = E[Y(0)|D=1] − E[Y(0)|D=0] = (145 + 120 + 125)/3 − 95 = 130 − 95 = **35**
>
> 45 = 10 + 35 ✓

The naive comparison overstates the effect by a factor of nine, and four fifths of what it reports is the gap between the groups before anyone was treated.

## 3. Characteristics of experiments

A randomized experiment is a study where the researcher controls the assignment to the treatment. It has two defining properties.

### 3.1 Positivity

**Definition 6.1.** The treatment assignment is probabilistic and not deterministic:

> 0 < pᵢ = P[Dᵢ = 1] < 1

Every unit must have a real chance of landing in either arm. If some group gets the treatment with probability 1 or 0, there is nothing to compare it with, and no amount of data fixes that.

This is violated more often than it looks. If a programme is offered only to people above an income threshold, everyone below it has p = 0 and the effect is simply not identified for them. It is also what makes a conditional analysis fail: once you slice the sample finely enough, some cells contain only treated or only control units.

### 3.2 Unconfoundedness

**Definition 6.2.** The treatment assignment does not depend on any potential outcomes Y(1) and Y(0):

> P[Dᵢ = 1 | Y(1), Y(0)] = P[Dᵢ = 1]

The assignment may not be related to how the unit would respond. Note it is stated in terms of the **potential** outcomes, not the observed ones, so it is an assumption about the design, not something you can check in the data.

A randomized coin flip satisfies it by construction, since the coin knows nothing. The Salk proposal 2 violates it, because a parent's consent is related to the child's underlying risk.

### 3.3 Why randomization works

- Randomization addresses the **missing data problem** by creating two groups that are, in expectation, identical before the treatment and differ only in the treatment.
- The treatment group is a random sample from the population, and so is the control group.
- So the potential outcomes of the treated are comparable to those of the controls.
- Therefore the sample control mean is an unbiased estimator of the population control mean:

> E[Yᵢ | Dᵢ = 0] = E[Yᵢ(0) | Dᵢ = 0] = E[Yᵢ(0)] = E[Yᵢ(0) | Dᵢ = 1]

Read that chain from left to right, because each equality uses a different fact:

| Step | Why it holds |
| --- | --- |
| E[Y \| D=0] = E[Y(0) \| D=0] | **SUTVA.** For an untreated unit the observed outcome *is* Y(0) |
| E[Y(0) \| D=0] = E[Y(0)] | **unconfoundedness.** The controls are a random sample, so their Y(0) average equals the population's |
| E[Y(0)] = E[Y(0) \| D=1] | same reason, applied to the treated group |

The last term is the counterfactual you wanted and can never see. The chain says the control group's observed average stands in for it, and selection bias is zero.

In expectation is doing real work in that sentence. One randomization can still be unlucky, which is exactly what section 3.4 is for, and the lecture 5 notebook showed how wide the spread is in a small sample.

### 3.4 Causation versus association

The slide reproduces the diamond figure from Hernán and Robins (2025).

- The **population of interest** is one diamond, half white and half grey.
- **Causation** compares two full diamonds: E[Y^{a=1}] against E[Y^{a=0}]. The whole population under treatment against the whole population under control.
- **Association** compares two half-diamonds: E[Y | A = 1] against E[Y | A = 0]. The treated half against the untreated half.

Causation asks one question of everybody. Association asks two different groups one question each. Randomization is what makes the second a good stand-in for the first.

### 3.5 Balance of covariates

- Comparability between treatment and control groups can be assessed by checking how similar they are in their average **covariates**.
- This is called assessing the **balance of covariates**.
- For each covariate, calculate the mean in both groups and test whether they are equal.

What is actually going on: unconfoundedness is untestable, because it is about potential outcomes. What *is* testable is whether the groups look alike on things measured **before** the treatment. If randomization worked, they should. A balance table is therefore an indirect check on the design, not a test of the assumption itself.

Two rules that follow:

- Only **pre-treatment** variables belong in a balance table. A variable measured after the treatment could have been changed by it, so an imbalance there is a result, not a problem.
- Balance on observed covariates is **evidence** that the randomization ran correctly, not proof that unobservables are balanced. It is reassurance, not identification.

#### Example 6.5: balance table

The table from the exercise-and-grades paper lists Age, Female, Year of study, UIB, Self-control, Lifestyle, Study hours, Happiness and Registered study points, with p-values from 0.249 to 0.955 and N = 778 (380 control, 398 treatment).

**What do you conclude?** Nothing is significant at any conventional level, the group sizes are close to even, and the means line up to within a fraction of a standard deviation. The randomization looks like it worked. The table is also the standard first table of an experimental paper, and its real audience is a reader deciding whether to believe the rest.

### 3.6 Rejection rates

- As the number of variables increases, the likelihood of detecting significant effects increases.
- This is addressed by looking at **rejection rates**: the share of significant coefficients at a given significance level.
- Example from the slide: 2 significant coefficients out of 20 variables at the 5% level is a rejection rate of 10%, which is an **overrejection**.

The logic: if the groups really are balanced, every p-value is uniform on [0, 1], so a share α of the tests comes out significant at level α **by construction**. Twenty tests at 5% produce one significant result on average. Finding one is not evidence of a problem. Finding six is.

#### Example 6.6: the 20-variable table, worked

Going through all 20 p-values:

| Significance level | Variables below it | Rejection rate | Expected |
| --- | --- | --- | --- |
| **5%** | Math score (0.002) | **1/20 = 5%** | 5% |
| **10%** | Math score (0.002), English score (0.076), French score (0.088) | **3/20 = 15%** | 10% |

- At 5% the rejection rate is **exactly** what the null predicts. No overrejection.
- At 10% it is 15% against an expected 10%, a mild overrejection. With 20 tests, though, 3 rejections instead of 2 is well inside what chance produces. Nobody should reject the design over this.
- The one result that deserves a second look is **Math score, p = 0.002**, which is not a typical near-miss. The other two sit just under the threshold, where ordinary noise lives.
- A sensible response is to control for the imbalanced covariates in the main regression and check whether the estimate moves, not to throw the experiment away.

**The limit of the method, which the exercise makes concrete.** A rejection rate is a count, and counting throws away how extreme each p-value is. In exercise 6.2 the rejection rate is 4% at the 5% level, apparently fine, while two of the variables have p-values of 3×10⁻¹⁴ and 5×10⁻¹². Those are not unlucky draws, they are a broken randomization. Always look at the individual p-values as well as the rate.

---

## Key terms

| Term | Meaning |
| --- | --- |
| No causation without manipulation | a treatment must be manipulable at least in principle for Y(d) to mean anything (Holland 1986) |
| ATE | E[τᵢ], average over everybody |
| ATT | E[τᵢ \| Dᵢ = 1], average over the treated |
| ATU | E[τᵢ \| Dᵢ = 0], average over the untreated |
| Naive estimator | E[Y\|D=1] − E[Y\|D=0] = ATT + selection bias |
| Selection bias | E[Y(0)\|D=1] − E[Y(0)\|D=0] |
| Identified | the quantity can be recovered from observable data under the stated assumptions |
| Positivity | 0 < P[Dᵢ = 1] < 1 for every unit |
| Unconfoundedness | assignment does not depend on the potential outcomes |
| Covariate | a characteristic measured before the treatment |
| Balance table | means of covariates by group, with a test of equality |
| Rejection rate | share of balance tests significant at a given level |
| Overrejection | more rejections than the significance level predicts |
| Observed control design | controls chosen by who did not volunteer, not by randomization |

## References

From the slides:

- Hernán, M. A. and Robins, J. M. (2025). _Causal Inference: What If_. Chapman and Hall / CRC.
- Holland, P. W. (1986). Statistics and Causal Inference. _Journal of the American Statistical Association_ 81(396): 945–960.

My additions:

- Meier, P. (1957). [The Biggest Public Health Experiment Ever: The 1954 Field Trial of the Salk Poliomyelitis Vaccine](https://www.biostat.wisc.edu/~chappell/641/papers/paper2.htm). In _Statistics: A Guide to the Unknown_. (the two designs, the paralytic polio rates by group, and the volunteer effect)
- Francis, T. et al. (1955). An Evaluation of the 1954 Poliomyelitis Vaccine Trials. _American Journal of Public Health_ 45(5 Pt 2): 1–63. (the original evaluation report)
