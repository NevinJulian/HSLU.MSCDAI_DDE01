# Lecture 8: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. Exercise 8.1 is output reading with no dataset. Exercise 8.2 numbers come from `lecture8_painstudy.csv` and are identical in R and Python, including the Welch degrees of freedom and the confidence intervals.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)

painstudy <- read_csv("Data/Out_Data/lecture8_painstudy.csv")
```

---

## Exercise 8.1: Teaching methods

A study investigated the effectiveness of five different methods for teaching descriptive statistics: (1) traditional lecture and discussion, (2) programmed textbook instruction, (3) programmed text combined with lectures, (4) computer-based instruction, and (5) computer instruction combined with lectures. A total of 45 students participated, with 9 randomly assigned to each method. After completing the course, all students took a one-hour exam to assess their learning outcomes.

### Solution 1: hypotheses

> H₀ : μ₁ = μ₂ = μ₃ = μ₄ = μ₅, all five teaching methods produce the same average exam score
> H_A : at least two of the means μᵢ are different

Note what H_A is not. It is not "all five differ", and it is not any statement about which method is best. Rejecting H₀ licenses only the claim that the five means are not all identical.

### Solution 2: degrees of freedom

45 students in five groups, so n = 45 and k = 5.

| | | |
| --- | --- | --- |
| Numerator, df_G | k − 1 | **4** |
| Denominator, df_E | n − k | 45 − 5 = **40** |

The F-test is on F(4, 40). They sum to 44 = n − 1, which is the check: the total degrees of freedom are always one less than the sample size, split between the two sources.

### Solution 3: the distribution of scores

The plot shows the 45 individual scores by method, with a black bar at each group mean. Reading the bars off it:

| Method | Mean, read off the plot |
| --- | --- |
| Lecture | about 75 |
| Textbook | about 72.5 |
| Text + Lecture | about 74.5 |
| Computer | about 73.5 |
| Computer + Lecture | about 76 |

**The three methods that involve lectures score higher than the two that do not.** Lecture, Text + Lecture and Computer + Lecture sit at the top, while programmed textbook instruction and computer-based instruction, the two pure self-study formats, sit at the bottom. The best method, Computer + Lecture, is the one that combines both.

The groups overlap heavily, so this is an impression rather than a result. The spread within each method is roughly as large as the spread between the method means, and individual scores range from 68 to 80 across the whole plot.

> A sanity check worth doing: MSE = 3.576 in the table below, so the within-group standard deviation is √3.576 = **1.89**. That matches the visible scatter, where most groups span about four points from lowest to highest. The eye and the table agree.

### Solution 4: interpreting the ANOVA results

```
            Df  Sum Sq  Mean Sq  F value   Pr(>F)
method       4   97.36   24.339    6.805 0.000282 ***
Residuals   40  143.06    3.576
```

The impression from the plot is confirmed. **Reject H₀** at p = 0.000282, well below 0.05 and below 0.001, hence three stars. The five teaching methods do not all produce the same average exam score.

How the table is built, every number from the one before it:

| Quantity | Where it comes from | Value |
| --- | --- | --- |
| df_G | k − 1 | 4 |
| df_E | n − k | 40 |
| MSG | 97.36 / 4 | 24.339 |
| MSE | 143.06 / 40 | 3.576 |
| F | 24.339 / 3.576 | 6.805 |
| p | upper tail of F(4, 40) beyond 6.805 | 0.000282 |

The 5% critical value is F(4, 40) = 2.606 and the 1% value is 3.828. The observed 6.805 clears both comfortably.

**What this does not settle.** Which methods differ. The plot suggests the lecture-based methods beat the self-study ones, but the F-test has not tested that, and with five groups there are K = 5 × 4 / 2 = **10** pairwise comparisons. At an uncorrected 5% level the chance of at least one false positive across ten tests is 1 − 0.95¹⁰ = **40%**. The Bonferroni-adjusted level would be α* = 0.05 / 10 = **0.005**, and with group means only one to three points apart and a within-group standard deviation of 1.89, most individual pairs would not clear it.

> If the real question is "does adding lectures help", the better design is not ten pairwise tests at all. It is a single planned contrast comparing methods 1, 3 and 5 against 2 and 4, which is one test rather than ten and needs no correction. Bonferroni is the price of going fishing after the fact.

---

## Exercise 8.2: Pain relief

Amundson et al. (2017) conducted a clinical trial comparing three different treatments for pain management during knee surgery. The primary outcome was the maximum pain score reported one day after surgery, measured on a numerical rating scale from 0 to 10, with higher scores indicating more severe pain. The study included 150 participants. The data is in `lecture8_painstudy.csv`.

> The file has 150 rows and two columns, `pain` and `trt`, with 50 participants in each of the three arms. Perfectly balanced, and the observed scores run from 1 to 10. **Higher is worse**, so the best treatment is the one with the lowest mean.

### Solution 1: the distribution across groups

```r
ggplot(painstudy, aes(x = trt, y = pain, color = trt)) +
  geom_jitter(width = 0.2, height = 0, size = 2, alpha = 0.7) +
  stat_summary(fun = mean, geom = "point",
               shape = "-", size = 4, color = "black") +
  theme_bw()
```

**Group C sits clearly below the other two.** Its cloud of points is centred around 3 to 4 while A and B are centred around 6 to 7, and the separation is large enough to read off the plot without any arithmetic. A and B are closer to each other, with B slightly above A.

Since higher scores mean more pain, lower is better and **treatment C is the effective one**.

> `height = 0` in the jitter matters here. The outcome takes whole-number values from 1 to 10, so without jitter the 50 points per group would stack into ten positions and hide the density. Jittering horizontally spreads them out, jittering vertically would invent values between the integers that no participant reported.

### Solution 2: group means

```r
painstudy %>%
  group_by(trt) %>%
  summarize(pain_mean = mean(pain))
```

| Treatment | n | Mean pain | Std. dev. |
| --- | --- | --- | --- |
| A | 50 | **6.20** | 1.34 |
| B | 50 | **7.32** | 1.15 |
| C | 50 | **3.64** | 1.51 |

The visual impression is confirmed. C is 2.56 points below A and 3.68 points below B, on a 10-point scale, which is a large clinical difference rather than a statistical curiosity. B is the worst of the three.

### Solution 3: hypotheses

> H₀ : μ_A = μ_B = μ_C, the three treatments produce the same mean pain score
> H_A : at least two of the means are different

### Solution 4: the ANOVA

```r
anova_mod <- aov(pain ~ trt, data = painstudy)
summary(anova_mod)
```

```
             Df Sum Sq Mean Sq F value              Pr(>F)
trt           2  355.8   177.9   98.92 <0.0000000000000002 ***
Residuals   147  264.4     1.8
```

**Reject H₀** at the 5% level. The p-value is below the smallest number R prints, so it is reported as `< 2e-16`.

Rebuilding the table from the group means confirms every entry:

| Quantity | Value |
| --- | --- |
| df_G, df_E | 2 and 147 |
| SSG, SSE | 355.84 and 264.40 |
| MSG | 355.84 / 2 = 177.92 |
| MSE | 264.40 / 147 = 1.799 |
| F | 177.92 / 1.799 = **98.92** |
| F critical at 5% | F(2, 147) = 3.058 |

The observed F is more than thirty times the critical value. Between-group variation is 355.8 against 264.4 within, so **57% of the total variation in pain scores is explained by which treatment the patient received**, which for a clinical outcome is very large.

### Solution 5: pairwise comparisons with the Bonferroni correction

With k = 3 groups there are K = 3 × 2 / 2 = 3 comparisons:

> α* = α / K = 0.05 / 3 = **0.01667**

```r
t.test(pain ~ trt, data = painstudy %>% filter(trt %in% c("A", "B")))
t.test(pain ~ trt, data = painstudy %>% filter(trt %in% c("A", "C")))
t.test(pain ~ trt, data = painstudy %>% filter(trt %in% c("B", "C")))
```

| Comparison | Difference | t | df | p | p < 0.01667? |
| --- | --- | --- | --- | --- | --- |
| A vs B | −1.12 | −4.484 | 95.81 | 0.0000204 | **yes** |
| A vs C | +2.56 | 8.971 | 96.66 | 0.000000000000023 | **yes** |
| B vs C | +3.68 | 13.715 | 91.60 | < 0.0000000000000002 | **yes** |

**All three p-values are smaller than 0.01667, so all three null hypotheses are rejected.** Every pair of treatments differs: C beats both A and B, and A beats B.

What that means clinically, in the direction that matters:

- **C is the best treatment**, significantly less painful than both alternatives, by 2.6 and 3.7 points
- **B is the worst**, and the A vs B gap of 1.1 points is itself significant
- The ordering **C < A < B** is fully resolved, which is more than the ANOVA alone could say

The 95% confidence intervals do not come close to zero: [−1.62, −0.62] for A vs B, [1.99, 3.13] for A vs C and [3.15, 4.21] for B vs C.

### The correction makes no difference here, and that is worth noticing

Multiplying each p-value by K = 3, the equivalent way to apply Bonferroni, gives 0.000061, 6.9 × 10⁻¹⁴ and 1.9 × 10⁻²³. Every one survives by many orders of magnitude.

This is the easy case. Compare it with the income and work effort example in [the notes](notes.md#33-example-81-cont--and-a-problem-with-the-slide), where the same correction on the same number of comparisons flips two of the three decisions. The correction only ever matters for p-values sitting near the threshold, and the honest summary is that it is irrelevant when effects are this large and decisive when they are marginal. Reporting that you applied it is still right, because you do not know which case you are in until you look.

### Two points worth noting

- **The official solution uses Welch t-tests, while the ANOVA assumes equal variances.** The two are inconsistent in principle: `aov` pools a single MSE across all three groups, and `t.test` defaults to Welch, which does not pool. Here it changes nothing, because the groups are the same size, which makes the two t-statistics algebraically identical to four decimals, and only the degrees of freedom differ, 91.6 to 96.7 instead of 98. A Levene test on equal variances gives p = 0.068, so the assumption is not rejected at the 5% level, though group C's standard deviation of 1.51 against B's 1.15 is the reason it is borderline.
- **The pairwise tests discard information, and pooling it back is not free.** Each test uses only the 100 patients in its two arms, while the ANOVA's MSE pools all 150. Substituting that pooled MSE with df = 147, which is what R's `pairwise.t.test` does by default, keeps all three rejections but does not uniformly help: **A vs B gets a larger p**, 0.000051 against 0.000020, because group C's variance of 2.28 inflates the pooled estimate used for a comparison C is not part of. A vs C and B vs C get smaller p-values from the extra degrees of freedom. Pooling pays when the variances really are equal and taxes the tighter comparisons when they are not.
