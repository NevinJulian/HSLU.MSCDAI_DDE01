# Lecture 7: Comparing two treatments II

**Date:** 05 Nov 2026 (onsite) · **Lecturer:** Lukas Schmid · [Exercises](exercises.md) · [Notebook](exercises.ipynb)

## Contents

1. [Motivation](#1-motivation)
2. [Treatment effect estimation](#2-treatment-effect-estimation)
3. [Statistical inference](#3-statistical-inference)
4. [Key terms](#key-terms)

The slides give the definitions and examples 7.1 to 7.5. The worked answers to the open questions, the note on what a p-value is not, and the link back to the lecture 5 enumeration are my additions, sources at the end.

Lecture 6 established that randomization makes the naive comparison an unbiased estimate. This lecture is about how to compute it and how confident to be in it.

---

## 1. Motivation

#### Example 7.1: Lady tasting tea

"Lady tasting tea" is an experiment designed by the British statistician Ronald Fisher. The phycologist Muriel Bristol claimed she could tell whether milk or tea was poured first when preparing a cup of tea. Fisher was sceptical and designed an experiment in which the subject was presented with **eight cups of tea in random order**. In four of the cups milk was poured first, in the other four tea was poured first. The subject had to correctly identify the method of preparation for all eight cups.

The design is worth pausing on before the statistics arrive.

- **She is told there are four of each.** That is what makes the answer a choice among a known, finite set of possibilities, and it is what makes the p-value exactly computable.
- **The cups are presented in random order.** Without this, she could pick up a pattern that has nothing to do with taste.
- **The threshold is set in advance:** all eight correct. Deciding afterwards what would have counted as success is how you turn any result into a confirmation.

Section 3.8 computes the p-value. The answer comes back in section 3.8 and does not need a normal distribution, a t-table or a large sample, which is what makes the example famous.

## 2. Treatment effect estimation

If the randomization has worked, the ATT can be estimated in two ways.

**1. Mean comparison:**

> τ̂_ATT = (1/N_T) Σ_{i:Dᵢ=1} Yᵢ − (1/N_C) Σ_{i:Dᵢ=0} Yᵢ

**2. Regression:**

> Yᵢ = β₀ + τ_ATT · Dᵢ + uᵢ

where Dᵢ is a dummy that is 1 for the treatment group and 0 otherwise.

These are not two approaches that happen to agree. They are **the same calculation**. With a single binary regressor, OLS fits the group means by construction: β̂₀ is the mean of the control group and β̂₀ + τ̂ the mean of the treated, so τ̂ is the difference. Nothing is assumed about linearity, because a line through two points is exact.

Why bother with the regression form, then:

- it hands you the standard error, the t-statistic and the p-value without extra work
- covariates can be added to soak up residual variance and tighten the estimate
- interactions give subgroup effects and, more importantly, a **test** of whether the subgroups differ (exercise 7.2)

#### Example 7.2: eight students

A sample where the treatment is randomized, with eight students. Different data from the seven observational students in lecture 6.

| Student i | Dᵢ | Yᵢ | Yᵢ(0) | Yᵢ(1) |
| --- | --- | --- | --- | --- |
| A | 0 | 110 | 110 | 120 |
| B | 0 | 95 | 95 | 105 |
| C | 0 | 105 | 105 | 115 |
| D | 0 | 150 | 150 | 160 |
| E | 1 | 160 | 150 | 160 |
| F | 1 | 100 | 90 | 100 |
| G | 1 | 95 | 85 | 95 |
| H | 1 | 145 | 135 | 145 |

**1. Mean comparison**

```r
df_experimental %>%
  group_by(D) %>%
  summarize(Y_mean = mean(Y), Y_var = var(Y))
```

```
  D     Y_mean Y_var
  <dbl>  <dbl> <dbl>
1     0    115  583.
2     1    125 1050
```

**2. Regression**

```r
summary(lm(Y ~ D, data = df_experimental))
```

```
            Estimate Std. Error t value Pr(>|t|)
(Intercept)   115.00      14.29   8.048 0.000197 ***
D              10.00      20.21   0.495 0.638288
```

The intercept is the control mean, 115. The coefficient on D is 125 − 115 = **10**, the mean comparison exactly.

Two things about this dataset that pay off later:

- Every student's treatment effect is exactly **10**, so the ATE, ATT and ATU are all 10, with no variation to argue about.
- The groups' mean Y(0) are both 115, so the selection bias is **zero**. This is a textbook-clean randomization.

Despite that, the estimate is **not statistically significant** (p = 0.64). The design is perfect and the answer is still uninformative, because n = 8. That gap between "unbiased" and "useful" is what the rest of the lecture is about.

## 3. Statistical inference

### 3.1 Sampling and inference

We are interested in **population parameters**. Since it is practically impossible to collect data from the entire population, **sample statistics** are used as point estimates for the unknown population parameter.

This is lecture 3 again, with the estimator/estimate distinction. The new part is quantifying how far the estimate might be from the parameter.

### 3.2 Hypotheses

**Definition 7.1.**

- **Null hypothesis H₀:** the assumption about the population being tested. Often formulated sceptically, meaning it posits no difference from the null value. Normally the hypothesis to be refuted.
- **Alternative hypothesis H_A:** the opposite of the null. Offers alternative statements, often a range of values differing from the null.

#### Example 7.3

For the effect of exercise on grades:

> H₀: τ = 0
> H_A: τ ≠ 0  (two-sided), or τ ≶ 0 (one-sided)

The asymmetry is deliberate. You never "accept" H₀, you only fail to reject it, because absence of evidence against a hypothesis is not evidence for it. A trial with four people per arm fails to reject almost everything.

### 3.3 p-value and significance level

**Definition 7.2.** The **p-value** is the probability of obtaining the observed test statistic, or a value more extreme in the direction of the alternative, **under the assumption that H₀ is true**.

**Definition 7.3.** The **significance level** α is a decision criterion providing a rule for how unlikely an event must be to still be considered as having occurred under H₀. If p < α, then H₀ is rejected. Otherwise H₀ is not rejected.

#### Example 7.3 (cont.)

1. H₀: τ = 0, H_A: τ ≠ 0
2. Significance level: α = 0.1
3. Test statistic 1.85, associated p-value 0.07
4. Decision: reject H₀ because p < α

The slide's graph shows the t-distribution under H₀ with **0.035 shaded in each tail**. The two tails sum to 0.07, which is the two-sided p-value. A one-sided test against τ > 0 would use only the right tail and report 0.035.

**What a p-value is not.** The definition conditions on H₀ being true, and almost every common misreading forgets that:

| Claim | Status |
| --- | --- |
| "p = 0.07, so there is a 7% chance H₀ is true" | wrong, that would be P(H₀ \| data), not P(data \| H₀) |
| "p = 0.07, so there is a 93% chance the effect is real" | wrong, same reversal |
| "p = 0.60, so there is no effect" | wrong, it means the data cannot distinguish the effect from zero, which with n = 8 is unsurprising |
| "p = 0.001, so the effect is large" | wrong, p mixes effect size with precision. A tiny effect in a huge sample gives a tiny p |

The last row is why papers report the point estimate and the confidence interval, not just stars.

### 3.4 Classical statistical inference

Traditional hypothesis testing using large sample theory proceeds as follows:

1. Choose a null hypothesis
2. Choose a test statistic
3. Determine the distribution of the test statistic under the null
4. Calculate the probability of the test statistic under the null, the p-value

In experiments, the relevant tests are mostly simple **mean comparisons** across groups:

> H₀: μ_T = μ_C
> H_A: μ_T ≠ μ_C  or  μ_T ≶ μ_C

The t-value:

> t = (x̄_T − x̄_C) / √( σ̂²_T / N_T + σ̂²_C / N_C )

provided the t-distribution can be applied to each sample mean and the samples are independent.

Read the formula as a signal-to-noise ratio. The numerator is the effect, the denominator is how much the difference would bounce around across repeated experiments. Three ways to get a large t: a big effect, low variance, or a big sample. Only the last two are under your control, which is lecture 11.

#### Example 7.4: the calculation by hand

Treatment mean 125, control mean 115, sample variances 1050 and 583, four students in each group.

> t = (125 − 115) / √(1050/4 + 583.33/4)
> = 10 / √(262.5 + 145.83)
> = 10 / √408.33
> = 10 / 20.21
> = **0.4949**

```r
t.test(df_experimental$Y[df_experimental$D == 1],
       df_experimental$Y[df_experimental$D == 0],
       var.equal = TRUE, alternative = "two.sided")
```

```
t = 0.49487, df = 6, p-value = 0.6383
alternative hypothesis: true difference in means is not equal to 0
sample estimates:
mean of x mean of y
      125       115
```

The regression gives the same t of 0.495 and the same p of 0.638.

> **A note on `var.equal`.** The formula on the slide, with σ̂²_T/N_T + σ̂²_C/N_C, is the **Welch** form, while the R command uses `var.equal = TRUE`, the **pooled** form. Here both give t = 0.4949, because the two groups have the same size, which makes the two formulas algebraically identical. They differ in the degrees of freedom: pooled uses N_T + N_C − 2 = 6 and gives p = 0.6383, Welch estimates df = 5.55 and gives p = 0.6397. With unequal group sizes the t-values differ too. R's `t.test` defaults to Welch, which is why the balance tests in exercise 6.2 report fractional degrees of freedom.

**Where is the t-statistic on the graph, and what area is the p-value?** t = 0.495 sits just right of the centre, in the fattest part of the distribution. The p-value is the area beyond +0.495 **plus** the area below −0.495, which together make up 64% of the total. Nearly the whole distribution is "at least this extreme", which is the visual version of "this experiment tells us nothing".

### 3.5 Errors in hypothesis testing

Hypothesis tests are not error-free, because estimators are subject to uncertainty. But the error rates can be calculated.

**Definition 7.4.**

- **Type I error:** rejecting H₀ even though H₀ is true.
- **Type II error:** not rejecting H₀ even though H_A is true.

| | Do not reject H₀ | Reject H₀ |
| --- | --- | --- |
| **H₀ true** | ✓ | **Type I error** |
| **H_A true** | **Type II error** | ✓ |

There is a tradeoff. The significance level α influences both: lowering α reduces the risk of a Type I error but increases the likelihood of a Type II error. Lecture 11 covers power analysis, which minimizes Type II error through the choice of sample size.

Worth fixing in your head:

- **α is the Type I error rate**, chosen by you before looking at the data. Setting α = 0.05 means accepting that one in twenty true nulls will be rejected. That is exactly the rejection-rate arithmetic from lecture 6, viewed from the other side.
- **β is the Type II error rate**, and **power = 1 − β** is the probability of detecting an effect that really exists. Power depends on the true effect size, the variance and the sample size, so unlike α it is not something you simply pick.
- Example 7.2 is a Type II error waiting to happen: every student really is helped by 10 points, and the test fails to reject anyway.

### 3.6 Confidence intervals

Many papers report only confidence intervals of the point estimates. There is a **correspondence** between hypothesis tests and confidence intervals: if a point estimate is significantly different from its null value at level α, the corresponding (1 − α) confidence interval will **not** include the null value.

So a confidence interval is a whole family of tests at once. Every value outside it would be rejected at level α, every value inside would not.

#### Example 7.5: three estimates

The second version of the figure draws two intervals per estimate: the **thick bar is the 90% interval**, the **thin whisker the 95% interval**.

| | Point estimate | 90% interval | 95% interval | Significant at 10%? | At 5%? |
| --- | --- | --- | --- | --- | --- |
| **A** | about +0.1 | crosses zero | crosses zero | **no** | **no** |
| **B** | about +0.9 | entirely above zero | entirely above zero | **yes** | **yes** |
| **C** | about −0.4 | entirely below zero | just touches zero | **yes** | **no** |

C is the one the slide is built around. It is the case where the answer depends on which threshold you picked, and it is why reporting the interval is more informative than reporting whether a star appeared.

Applied to example 7.2, the 95% interval for the treatment effect is roughly **[−39, 59]**. The true effect is 10 and sits comfortably inside, along with −30 and +50. The experiment is consistent with the treatment being strongly harmful, useless or strongly helpful.

### 3.7 Lady tasting tea, solved

The null hypothesis is that Ms. Bristol does **not** have the ability and guesses. The test statistic is the number of correctly identified cups. The distribution of successes under the null can be calculated using **permutations**:

> C(8,4) = 8! / (4!(8−4)!) = **70**

There are 70 ways to choose which four of the eight cups are the milk-first ones. Under pure guessing each is equally likely, and exactly one is right:

> p-value = **1/70 = 0.014**

The full distribution of the number of the four milk-first cups she places correctly:

| Correct | Ways | Probability |
| --- | --- | --- |
| 0 | 1 | 0.014 |
| 1 | 16 | 0.229 |
| 2 | 36 | 0.514 |
| 3 | 16 | 0.229 |
| 4 | 1 | 0.014 |

This is the hypergeometric distribution, and the test is **Fisher's exact test**. Note it is symmetric: getting none right is exactly as unlikely as getting all right, since placing all four in the wrong group is also a perfect discrimination, backwards.

**Why this example is in the course.** Nothing here is approximate. No normal distribution, no t-table, no large-sample theory. The null distribution comes from the **randomization itself**: the experimenter shuffled the cups, so the set of possible outcomes under the null is known exactly, and the p-value is a count.

This is **randomization inference**, and the lecture 5 notebook already did it without the name. Enumerating all 35 ways to treat 3 of 7 students, and seeing where the observed assignment fell in that list, is the same procedure. The classical t-test in section 3.4 is the large-sample approximation to this idea, useful when the number of possible assignments is too large to enumerate.

A practical consequence of the exact approach: with eight cups, the smallest p-value achievable is 1/70 = 0.014. Design the experiment with six cups instead and the best possible p-value is 1/20 = 0.05, so you could never reach significance at the 1% level however well she performed. The design caps what the result can show, before any data exist.

> Anecdotally, Bristol identified all eight correctly. The story comes second-hand through a colleague of Fisher's and is not in Fisher's own account, so treat it as a good story rather than a reported result.

---

## Key terms

| Term | Meaning |
| --- | --- |
| Mean comparison | x̄_T − x̄_C, the estimate of the ATT under randomization |
| Regression form | Yᵢ = β₀ + τDᵢ + uᵢ, identical to the mean comparison for a binary D |
| Null hypothesis H₀ | the sceptical assumption being tested, usually τ = 0 |
| Alternative hypothesis H_A | the opposite, two-sided (τ ≠ 0) or one-sided (τ ≶ 0) |
| p-value | P(test statistic at least this extreme \| H₀ true) |
| Significance level α | the threshold for rejecting H₀, chosen in advance |
| t-value | (x̄_T − x̄_C) / √(σ̂²_T/N_T + σ̂²_C/N_C) |
| Pooled vs Welch t-test | equal variances assumed or not. Identical t with equal group sizes, different df |
| Type I error | rejecting a true H₀, rate α |
| Type II error | failing to reject a false H₀, rate β |
| Power | 1 − β, the chance of detecting a real effect |
| Confidence interval | the set of null values that would not be rejected at level α |
| Permutation / randomization inference | the null distribution built by enumerating the possible assignments |
| Fisher's exact test | the hypergeometric test behind the lady tasting tea |

## References

From the slides:

- Bloom, N., Han, R. and Liang, J. (2024). Hybrid Working from Home Improves Retention without Damaging Performance. _Nature_ 630(8018): 920–925.
- Kauer, L. and Schmid, C. P. R. (2025). Keep Reminding Me to Get My Flu Shot. _American Journal of Health Economics_, forthcoming.

My additions:

- Fisher, R. A. (1935). _The Design of Experiments_. Oliver and Boyd. (chapter 2 is the lady tasting tea)
- Salsburg, D. (2001). _The Lady Tasting Tea: How Statistics Revolutionized Science in the Twentieth Century_. Freeman. (the source of the anecdote that she got all eight right)
