# Lecture 8: Comparing more than two treatments I

**Date:** 12 Nov 2026 (online) · **Lecturer:** Lukas Schmid · [Exercises](exercises.md) · [Notebook](exercises.ipynb)

## Contents

1. [Motivation](#1-motivation)
2. [Analysis of variance](#2-analysis-of-variance)
3. [Bonferroni correction](#3-bonferroni-correction)
4. [Key terms](#key-terms)

The slides give definitions 8.1 and 8.2 and examples 8.1 to 8.3. The recomputed numbers, the family-wise error arithmetic, the answers to the open questions on slides 11 and 12, and the correction to slide 15 are my additions, sources at the end.

Lecture 7 compared two groups. With three or more the t-test no longer answers the question being asked, and running it on every pair creates a new problem. This lecture is both halves of that: ANOVA for the joint test, Bonferroni for the pairwise follow-up.

---

## 1. Motivation

#### Example 8.1: Income and work effort

You want to explore whether higher income leads to more effort at work. You conduct an experiment with 27 students, randomly divided into three income groups. After assigning income levels, you measure each student's work effort on a scale from 0 to 10.

| ID | Group | Work effort |
| --- | --- | --- |
| 1 | L | 4 |
| … | … | … |
| 10 | M | 6 |
| … | … | … |
| 27 | H | 8 |

> Question: do the average work efforts differ systematically between the groups?

> **Data note.** The file is `lecture8_income_work_effort.csv`, 27 rows, three columns. The group column is `work` and its values are **T, M, H**, not L, M, H: `T` is German *tief* and is the slides' "Low". `work_order` is 1/2/3 and exists only to force the plotting order, since alphabetically H would come first. The group means match the slide exactly, so it is the same data under a different label.

**Why not just run t-tests.** Two reasons, and they are different.

1. The question itself is a joint one. "Do the averages differ systematically" is a single hypothesis about all three groups at once. Three separate two-group tests answer three different questions, and nothing tells you how to combine the answers.
2. Three tests at α = 0.05 do not give a 5% error rate. If the tests were independent and the null were true everywhere, the chance of at least one false positive is 1 − 0.95³ = **14.3%**. With five groups there are ten pairs and it is 1 − 0.95¹⁰ = **40.1%**. Run enough comparisons and something crosses the threshold by construction.

ANOVA solves the first problem. The Bonferroni correction in section 3 solves the second.

## 2. Analysis of variance

### 2.1 Key idea

When we want to compare means across two or more groups, we use ANOVA. The core idea is to break down the total variation in the data into two sources:

> Total Variation (SST) = Between-Group Variation (SSG) + Within-Group Variation (SSE)

Notation: SS = Sum of Squares, T = Total, G = Groups (between), E = Error (within).

- If all group means are similar, between-group variation is small
- If group means differ strongly, between-group variation is large

The decomposition is an identity, not an approximation. On this dataset it holds exactly:

> SSG 24.5185 + SSE 26.4444 = SST 50.9630

Written out, the three sums are over every observation:

| | Formula | What it measures |
| --- | --- | --- |
| SST | Σᵢ (Yᵢ − ȳ)² | spread of all 27 points around the overall mean |
| SSG | Σ_groups nᵢ(ȳᵢ − ȳ)² | spread of the three group means around the overall mean |
| SSE | Σ_groups Σ_{i in group} (Yᵢ − ȳᵢ)² | spread of points around their **own** group mean |

### 2.2 The picture

The slide's graph plots every student's work effort against their income group, with a **black bar at each group mean** and a **dashed line at the overall mean**.

Read the two sources off it directly:

- **Between-group variation** is how far the three black bars sit from the dashed line
- **Within-group variation** is how far the dots scatter around their own black bar

ANOVA is the ratio of the first to the second. The eye does this automatically, which is why the plot comes before the formula. Example 8.2 below is the formal version of the same exercise.

### 2.3 The test statistic

We define two quantities, each a sum of squares scaled by its own degrees of freedom:

> MSG = SSG / (k − 1)  the mean square **between** groups
> MSE = SSE / (n − k)  the mean square **within** groups

Both are variances, so their ratio follows an F-distribution under the null.

#### Definition 8.1: ANOVA

The F-test checks whether the means of groups are equal:

> H₀ : μ₁ = μ₂ = μ₃ = ⋯ = μ_k
> H_A : at least two of the means μᵢ are different

The F-statistic:

> F = Variability between groups / Variability within groups = MSG / MSE

Under H₀ this follows an F distribution with df_G = k − 1 and df_E = n − k degrees of freedom.

Written out:

> MSG = (1 / (k − 1)) Σᵢ₌₁ᵏ nᵢ (x̄ᵢ − x̄)²
>
> MSE = (1 / (n − k)) SSE = (1 / (n − k)) Σᵢ₌₁ᵏ (nᵢ − 1) σ̂ᵢ²

where nᵢ is the sample size of group i, x̄ᵢ its mean, x̄ the overall mean and σ̂ᵢ² the estimated variance within group i. If the F-statistic is large enough, this suggests the group means differ and we reject H₀.

Three things worth fixing in your head:

- **MSE is a pooled within-group variance**, a weighted average of the three group variances. It is the same pooled estimate as the two-group t-test in lecture 7, extended to k groups. It carries no information about where the group means sit.
- **H_A is vague on purpose.** Rejecting tells you *some* pair differs, not which. That is the whole motivation for section 3.
- **The F-test is one-sided even though H_A is "different in either direction".** Only large F counts as evidence, because MSG can only be inflated by the means being spread out. An F below 1 means the group means are closer together than chance would produce, which is not evidence against H₀.

### 2.4 The calculation

#### Example 8.1 (cont.)

Three groups of nine individuals each:

- Means: x̄_L = 3.89, x̄_M = 5.00, x̄_H = 6.22
- Variances: σ̂²_L = 1.36, σ̂²_M = 1.00, σ̂²_H = 0.94
- Overall mean: x̄ = 5.04

Test at the 5% significance level.

**Between groups.** Each group has nᵢ = 9 and k − 1 = 2:

> MSG = (1/2) × 9 × [(3.889 − 5.037)² + (5.000 − 5.037)² + (6.222 − 5.037)²]
> = 4.5 × [1.3178 + 0.0014 + 1.4042]
> = 4.5 × 2.7234
> = **12.2593**

**Within groups.** Each group has nᵢ − 1 = 8 and n − k = 24:

> MSE = (1/24) × 8 × (1.3611 + 1.0000 + 0.9444)
> = (8/24) × 3.3056
> = **1.1019**

**The ratio.**

> F = 12.2593 / 1.1019 = **11.126** on df_G = 2 and df_E = 24

The 5% critical value is F(2, 24) = 3.403 and the p-value is **0.00038**. Reject H₀: the average work efforts do differ between income groups.

### 2.5 Reading the R output

```r
results_anova = aov(response ~ work, data = work_all)
summary(results_anova)
```

```
            Df Sum Sq Mean Sq F value  Pr(>F)
work         2   24.5    12.3    11.1 0.00038 ***
Residuals   24   26.4     1.1
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

The slide asks three questions.

**Where are MSG and MSE?** The `Mean Sq` column. The `work` row is the between-group line, so MSG = **12.3**. The `Residuals` row is the within-group line, so MSE = **1.1**. The naming is a regression convention: "residuals" is what is left after the group means are fitted, which is exactly the within-group variation.

**How is the F-value calculated?** 12.3 / 1.1 = 11.1, the top `Mean Sq` divided by the bottom one. Degrees of freedom are in `Df`: 2 = k − 1 and 24 = n − k, which sum to 26 = n − 1.

**Is the difference between groups significant?** Yes. p = 0.00038, well below 0.05 and below 0.001, hence three stars. We reject the hypothesis that all three income groups produce the same average work effort.

> R prints `Sum Sq` and `Mean Sq` to three significant figures. The unrounded values are SSG = 24.5185, SSE = 26.4444, MSG = 12.2593, MSE = 1.1019 and F = 11.1261. Dividing the rounded 24.5/2 = 12.25 and 26.4/24 = 1.10 reproduces the printed column, so nothing is lost, but quote the unrounded F if you reproduce this in a report.

### 2.6 Example 8.2: four datasets, four F-values

The slide shows four panels, each with five groups and group means drawn as black bars, and asks you to assign the F-values **0.95, 4.38, 56.69 and 290.9**.

Do it by eye first, using section 2.2: compare the spread of the black bars against the scatter within each cluster. The within-group spread is roughly the same in all four panels, about one unit, so the ranking is decided entirely by how far apart the group means sit.

| Panel | Group means run from | Spread of means | F |
| --- | --- | --- | --- |
| **Dataset 1** | 10 to 10 | none, all five sit on the same line | **0.95** |
| **Dataset 4** | 10 to about 11.5 | 1.5, comparable to the within-group scatter | **4.38** |
| **Dataset 3** | 10 to about 15.5 | 5.5, clearly larger than the scatter | **56.69** |
| **Dataset 2** | 10 to about 22 | 12, clusters do not overlap at all | **290.9** |

Reading the means off the panels and assuming a within-group standard deviation of 1 reproduces the ranking and roughly the magnitudes: MSG comes out near 0, 4.3, 53 and 233 against the four candidates. Close enough to confirm the assignment, and the exact values depend on the within-group variance which cannot be read precisely off a printed plot.

Two things the panel comparison teaches:

- **F near 1 is what "no effect" looks like.** Dataset 1's F of 0.95 is not small, it is *typical*. Under H₀ the expected value of F is df_E/(df_E − 2), just above 1, because MSG and MSE are then both estimating the same variance.
- **Dataset 4 is the interesting one.** Its F of 4.38 on df (4, 45) gives p ≈ 0.004, so it is significant at the 1% level despite the groups overlapping heavily on the plot. A visible difference and a detectable difference are not the same thing, and with n = 50 the test sees a pattern the eye calls noise.

### 2.7 What ANOVA does not tell you

A significant F-test tells us that at least one mean differs from another mean. It does **not** tell us which means differ from each other.

In example 8.1 that gap is real: the three group means are 3.89, 5.00 and 6.22, and the F-test alone does not establish which of the three pairwise gaps is doing the work. The obvious way to find out is to do t-tests of the multiple groups, which is section 3, with the correction that makes it legitimate.

## 3. Bonferroni correction

### 3.1 The problem

Running many t-tests between groups increases the risk of **Type I errors**, false positives. The solution is to adjust the significance level.

The arithmetic from section 1 again, stated as the quantity being controlled. The **family-wise error rate** is the probability of at least one false rejection across the whole set of comparisons. At α = 0.05 per test:

| Groups k | Comparisons K | FWER if all nulls true |
| --- | --- | --- |
| 3 | 3 | 14.3% |
| 4 | 6 | 26.5% |
| 5 | 10 | 40.1% |
| 6 | 15 | 53.7% |

The per-test error rate is still 5% in every row. What grows is the chance that *somewhere* in the family a true null gets rejected.

### 3.2 Definition 8.2: Bonferroni correction

If we perform K comparisons, adjust α as:

> α* = α / K

For k groups:

> K = k(k − 1) / 2

Reject H₀ for any pairwise test if p < α*.

Why dividing works: the probability of at least one false positive is at most the sum of the individual probabilities, whatever the dependence between the tests. K tests at α/K each therefore give a family-wise rate of at most K × α/K = α. This is Boole's inequality, and because it is an upper bound the correction is **conservative**: the true family-wise rate is usually below α, so you lose some power. Tukey's HSD is the standard alternative for exactly this comparison and is less conservative, but Bonferroni needs no assumptions and can be applied to any set of p-values, which is why it is the one taught first.

> Equivalently, multiply each p-value by K and compare against the original α. R's `p.adjust(p, method = "bonferroni")` does it that way. Same decisions, and it is easier to report.

### 3.3 Example 8.1 (cont.) — and a problem with the slide

Test for our example on income and work effort with three groups (K = 3) whether the means between the groups are different, at α = 0.05.

> α* = 0.05 / 3 = **0.01667**

The slide then lists three p-values:

| Slide | p |
| --- | --- |
| H₀: μ_L = μ_M | 0.003 |
| H₀: μ_L = μ_H | 0.00003 |
| H₀: μ_L = μ_H | 0.85 |

**Two problems here.**

**The third line repeats the second.** With three groups the comparisons are L–M, L–H and M–H. The third must be **μ_M = μ_H**, so the label is a typo.

**None of the three p-values comes from this dataset.** I ran every pairwise test that could reasonably be meant:

| Comparison | Two-sample t (pooled) | Two-sample t (Welch) | Pooled-SD pairwise, df = 24 | Tukey HSD |
| --- | --- | --- | --- | --- |
| L vs M | 0.0455 | 0.0458 | 0.0342 | 0.0837 |
| L vs H | 0.00029 | 0.00031 | 0.000086 | 0.0002 |
| M vs H | 0.0182 | 0.0182 | 0.0210 | 0.0530 |

Nothing produces 0.003, and nothing comes close to 0.85 — the M and H groups have means 5.00 and 6.22 with variances around 1, so no test is going to call them indistinguishable. The ANOVA output on slide 11 reproduces exactly, so the dataset is right and it is slide 15 that is wrong.

**What the data actually say.** Using plain two-sample t-tests against α* = 0.01667:

| Comparison | Difference | p | p < 0.01667? |
| --- | --- | --- | --- |
| Low vs Medium | −1.11 | 0.0455 | **no** |
| Low vs High | −2.33 | 0.00029 | **yes** |
| Medium vs High | −1.22 | 0.0182 | **no** |

Only the **Low versus High** comparison survives the correction. The other two would both have been significant at an uncorrected 5% level, and both lose it, Medium vs High only barely (0.0182 against 0.01667).

This is a better teaching example than the slide's version, and it is worth saying out loud in the exam: the ANOVA rejects decisively at p = 0.00038, and after correcting for three comparisons the only pair we can individually separate is the two extremes. "Something differs" and "I can say which pairs differ" are genuinely different claims, and the second is more expensive.

> Note also that the pairwise tests above throw away information. Each uses only the 18 students in its two groups, while the ANOVA's MSE pools all 27. The `pooled-SD` column uses MSE with df = 24 instead, which is what R's `pairwise.t.test` does by default and is generally the sharper choice when the equal-variance assumption holds. It does not change any decision here, and it is not uniformly sharper either: Low vs High and Low vs Medium both gain, Medium vs High loses slightly, because pooling imports the variance of the group that is not in the comparison.

### 3.4 Example 8.3: Exam date and academic performance

Mouritsen, Davis and Jones (2016) explore whether it matters for performance on which day an exam is taken. They suspect students taking the test later in the exam period have an advantage over students taking it early, because of information leakage. The data are from an accounting exam taken on four subsequent days, n = 1,457.

**Descriptives**

| Day | N | Mean | Std. deviation |
| --- | --- | --- | --- |
| 1 | 174 | 0.8529 | 0.1533 |
| 2 | 207 | 0.8229 | 0.1713 |
| 3 | 338 | 0.7999 | 0.1419 |
| 4 | 738 | 0.7138 | 0.1788 |
| Total | 1,457 | 0.7657 | 0.1674 |

**ANOVA**

| | Sum of squares | df | Mean square | F | p |
| --- | --- | --- | --- | --- | --- |
| Between groups | 4.354 | 3 | 1.451 | 57.835 | .000 |
| Within groups | 36.459 | 1,453 | .025 | | |
| Total | 40.812 | 1,456 | | | |

The table is internally consistent: 4.354/3 = 1.451, 36.459/1453 = 0.0251, their ratio is 57.84, and the degrees of freedom are k − 1 = 3 and n − k = 1,453 summing to 1,456 = n − 1.

**Do the results support their conjecture?** No, and this is the point of the example.

The F-test is overwhelming, p < 0.001, so the four days certainly differ. But the conjecture was that later students do **better**, and the means run **0.853 → 0.823 → 0.800 → 0.714**: performance falls monotonically across the exam period. The result is significant in the opposite direction.

**Why.** When investigating this surprising pattern, the authors find that students with higher cumulative GPAs tend to take the exam earlier in the testing period:

| Average GPA | Day 1 | Day 2 | Day 3 | Day 4 | Overall |
| --- | --- | --- | --- | --- | --- |
| Course 2020 | 3.43 | 3.37 | 3.29 | 3.01 | 3.15 |
| Course 2010 | 3.25 | 3.07 | 3.05 | 2.90 | 3.02 |
| Average by day | 3.32 | 3.16 | 3.18 | 2.96 | 3.08 |

Across the four days the correlation between average GPA and average exam score is **0.96**. The day groups differ because the students in them differ, not because of anything the exam date did.

This is the **self-selection** problem from lecture 4, in a lecture about a test statistic. Students chose their exam day, so day is not randomly assigned and the four groups were never comparable to begin with. ANOVA is a test of whether the group means differ, and nothing more: it is as happy to detect a selection effect as a treatment effect, and it cannot tell you which one it found. A significant F answers "are these groups different", never "did the treatment do it".

> Worth noting how unbalanced the design is. Day 4 holds 738 of the 1,457 students and day 1 holds 174. ANOVA handles unequal group sizes without complaint, since nᵢ appears in the MSG formula, but it does mean the overall mean sits close to day 4, and it is a further hint that the day was chosen rather than assigned.

---

## Key terms

| Term | Meaning |
| --- | --- |
| ANOVA | test of whether k ≥ 2 group means are all equal |
| SST | total sum of squares, spread of all observations around the overall mean |
| SSG | between-group sum of squares, spread of the group means around the overall mean |
| SSE | within-group sum of squares, spread of observations around their own group mean |
| Decomposition | SST = SSG + SSE, an exact identity |
| MSG | SSG / (k − 1), the between-group mean square |
| MSE | SSE / (n − k), the pooled within-group variance |
| F-statistic | MSG / MSE, large when the group means are spread out relative to the noise |
| df_G, df_E | k − 1 and n − k, the numerator and denominator degrees of freedom |
| Residuals row | R's name for the within-group line of the ANOVA table |
| Family-wise error rate | probability of at least one false rejection across a set of tests |
| K | number of pairwise comparisons, k(k − 1)/2 |
| Bonferroni correction | α* = α/K, controls the family-wise rate at α for any dependence |
| Conservative | a procedure whose true error rate is below its nominal level, at the cost of power |
| Tukey HSD | the standard less conservative alternative for all pairwise comparisons |

## References

From the slides:

- Amundson, A. W., Johnson, R. L., Abdel, M. P., Mantilla, C. B., Panchamia, J. K., Taunton, M. J. and Kralovec, M. E. (2017). A Three-arm Randomized Clinical Trial Comparing Continuous Femoral Plus Single-injection Sciatic Peripheral Nerve Blocks versus Periarticular Injection with Ropivacaine or Liposomal Bupivacaine for Patients Undergoing Total Knee Arthroplasty. _Anesthesiology_ 126(6): 1139–1150.
- Mouritsen, M. L., Davis, J. T. and Jones, S. C. (2016). ANOVA Analysis of Student Daily Test Scores in Multi-Day Test Periods. _Journal of Learning in Higher Education_ 12(2): 73–82.

My additions:

- Boole's inequality, the one-line justification for why dividing α by K works regardless of dependence between the tests.
- Tukey, J. W. (1949). Comparing Individual Means in the Analysis of Variance. _Biometrics_ 5(2): 99–114. (the HSD procedure referred to above)
