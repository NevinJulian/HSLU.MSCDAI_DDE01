# Lecture 7: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. Exercise 7.1 is table reading with no code. Exercise 7.2 numbers come from `lecture7_working_from_home.csv` and are identical in R and Python.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)

df_home <- read_csv("Data/Out_Data/lecture7_working_from_home.csv")
```

---

## Exercise 7.1: Flu shot experiment

Kauer and Schmid (2025) study whether a letter informing consumers about vaccinations in selected pharmacies increased seasonal flu vaccination rates. They collaborated with a major Swiss health insurer. In 2016 about 22,000 letters were sent informing customers about the possibility of a flu shot in a pharmacy, the full insurance coverage, and the nearest licensed pharmacy.

### Solution 1: hypotheses

Let τ be the effect of the information letter on flu vaccination.

> H₀: τ = 0, the letter has no effect on the vaccination rate
> H_A: τ ≠ 0, the letter has an effect

Two-sided is the right default. The letter is plausibly positive, but a letter can also irritate people into inaction, and committing to a direction in advance only to find the opposite is how one-sided tests get abused.

### Solution 2: reading the table

**Table III: Treatment Effects in the 2016/17 Flu Season**

| Dep. var.: flu shot received in | Total, abs. | Total, rel. | No. of obs. |
| --- | --- | --- | --- |
| Individuals **without** a flu shot in the previous year | 2.4028\*\*\* (0.3447) | 34.158 [7.034] | 24,270 |
| Individuals **vaccinated** in the previous year | 2.3196\* (1.3611) | 3.424 [67.754] | 4,595 |

What each number is, from the table notes:

| Position | Meaning |
| --- | --- |
| the point estimate | treatment effect in **percentage points** |
| (parentheses) | standard error |
| rel. | the same effect in **percent**, relative to the control baseline |
| [square brackets] | the baseline vaccination rate in the control group, in percent |

So the letter raised the vaccination rate by:

- **2.40 percentage points** among people not vaccinated the previous year, against a baseline of 7.03%. Relative effect 2.4028 / 7.034 = **34.2%**, which is a third more vaccinations.
- **2.32 percentage points** among people vaccinated the previous year, against a baseline of 67.75%. Relative effect 2.3196 / 67.754 = **3.4%**.

**The absolute effects are nearly identical, the relative effects differ by a factor of ten.** The reason is the baseline, not the behaviour. Among people who already got vaccinated last year, two out of three were going to get vaccinated anyway, so there is far less room for a letter to change anything. The two framings answer different questions, and quoting only the 34% would be misleading.

### Solution 3: which results are statistically significant

Read the stars, and the key below the table (\*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.10).

| Row | Stars | Significant at |
| --- | --- | --- |
| without a flu shot in the previous year | \*\*\* | **1%** |
| vaccinated in the previous year | \* | **10%**, but not at 5% |

The standard errors confirm it. The implied t-values are 2.4028 / 0.3447 = **6.97** and 2.3196 / 1.3611 = **1.70**.

The second estimate is imprecise mainly because of the sample: 4,595 observations against 24,270, so its standard error is four times larger even though the point estimate is almost the same size.

### Solution 4: a problem for external validity

The sample consists of the **customers of one Swiss health insurer**. If those customers are a specific subset of the Swiss population, the result need not carry over to the country as a whole.

Concretely, a Swiss insurer's customer base can differ from the population in age, income, canton, language region and in how health-conscious people are. Anyone who chose that insurer made a choice, and the same traits that drove it could drive how they respond to a letter.

Three further external-validity limits worth naming:

- **The setting is specific.** Full insurance coverage of the shot, and a licensed pharmacy nearby, are part of the treatment. In a canton where pharmacies may not vaccinate, or where the shot is not covered, the same letter does less.
- **The time is specific.** One flu season, 2016/17. Vaccination behaviour shifted a lot after 2020.
- **It does not scale linearly.** The result is the effect of a letter on people not currently receiving such letters. If every insurer sent one every year, the novelty and the effect would both shrink.

None of this touches **internal** validity, which the randomization secures.

---

## Exercise 7.2: Working from home

Bloom, Han and Liang (2024) study hybrid working from home in a Chinese technology company in 2021–22. Employees with an **odd-numbered birthday** were assigned to the treatment group and allowed to work in hybrid mode. `lecture7_working_from_home.csv` contains the experimental sample: 1,612 rows and five columns (`treat`, `role`, `male`, `live_far`, `attrite_perc`).

> The assignment rule is worth a moment. Birth day-of-month is not random in the strict sense, but nothing about a person predicts whether their birthday falls on an odd day, so it works as a coin flip that is also **verifiable and transparent** to employees. This is a natural-experiment trick used inside a real experiment.

### Solution 1: the outcome variable

```r
df_home %>% distinct(attrite_perc)
```

Two values: **0 and 100**. It is a binary "did this person leave the firm within six months" indicator scaled to percent, so that a group mean reads directly as an attrition rate in percent and a regression coefficient reads as an effect in **percentage points**.

### Solution 2: mean comparison

```r
df_out <- df_home %>%
  group_by(treat) %>%
  summarize(attrition_mean = mean(attrite_perc))
```

| Group | n | Attrition |
| --- | --- | --- |
| Control (in-person) | 820 | **7.20%** |
| Treatment (hybrid WFH) | 792 | **4.80%** |

> Treatment effect = 4.80 − 7.20 = **−2.40 percentage points**

**Is this a large effect?** Yes. In relative terms it is a **third** of the attrition rate (2.4 / 7.2 = 33%), which is a big number for a policy that costs the firm nothing. Replacing an employee typically costs a large multiple of a monthly salary, so a third fewer departures is a serious saving. The paper's title says it: retention improves without damaging performance.

> The official solution writes "7.2-5.8=2.4". That is a typo for 7.2 − 4.8 = 2.4. It also says "2.4 percentage less likely to quit", which should be **percentage points**, since the relative change is 33%.

### Solution 3: regression

```r
summary(lm(attrite_perc ~ treat, data = df_home))
```

```
            Estimate Std. Error t value            Pr(>|t|)
(Intercept)   7.1951     0.8299   8.670 <0.0000000000000002 ***
treat        -2.3971     1.1840  -2.025              0.0431 *
```

The intercept is the control mean and the coefficient is the difference, exactly as in the notes. **p = 0.0431**, so the estimate is significant at the 5% level but not at the 1% level.

### Solution 4: managers and non-managers

```r
summary(lm(attrite_perc ~ treat, data = df_home %>% filter(role == 1)))
summary(lm(attrite_perc ~ treat, data = df_home %>% filter(role == 0)))
```

| Subgroup | n | Control | Treatment | Effect | SE | p |
| --- | --- | --- | --- | --- | --- | --- |
| Managers (`role == 1`) | 395 | 2.96% | 3.12% | **+0.17** | 1.73 | 0.922 |
| Non-managers (`role == 0`) | 1,217 | 8.59% | 5.33% | **−3.26** | 1.46 | 0.026 |

The usual reading, and the one in the official solution, is that **only non-managers react to the treatment**. The effect among non-managers is large and significant, the effect among managers is a rounding error.

That reading is defensible but overstated, see the pushback below.

### Solution 5: comparing with the paper

The point estimates and p-values are **identical** to the figure in the paper:

| | Paper | My regression |
| --- | --- | --- |
| Overall | 7.2 → 4.8, P = 0.0431 | 7.195 → 4.798, p = 0.0431 |
| Non-managers | 8.6 → 5.3, P = 0.0259 | 8.590 → 5.333, p = 0.0259 |
| Managers | 3.0 → 3.1, P = 0.922 | 2.956 → 3.125, p = 0.9222 |

The dataset is the paper's analysis sample, and the published figure is a bar chart of exactly these group means.

### Solution 6: the further splits

The second row of the paper's figure splits by gender and by commute. Both reproduce from the data, using `male` and `live_far`:

| Subgroup | n | Control | Treatment | Effect | p |
| --- | --- | --- | --- | --- | --- |
| Women (`male == 0`) | 570 | 9.19% | 4.18% | **−5.01** | 0.017 |
| Men (`male == 1`) | 1,042 | 6.15% | 5.15% | **−1.00** | 0.487 |
| Commute > 90 min (`live_far == 1`) | 611 | 6.00% | 2.89% | **−3.11** | 0.062 |
| Commute ≤ 30 min (`live_far == 0`) | 648 | 7.74% | 5.13% | **−2.61** | 0.178 |

**Do they make sense?** The story is plausible. Women in this firm carry more of the household and childcare load, so a day at home is worth more to them. Someone with a three-hour daily round trip saves far more time than someone with a half-hour one. Both are mechanisms you would have guessed in advance, which is the main thing that makes a subgroup result credible.

The official solution reads them as "only women react, men do not" and "only those with a longer commute react".

### The subgroup differences are not statistically significant

Comparing a significant subgroup against a non-significant one is not a test. The question "do these two groups respond differently" has its own estimate and its own standard error, and it is the **interaction** term:

```r
summary(lm(attrite_perc ~ treat * male, data = df_home))
```

| Interaction | Difference in effect | SE | p |
| --- | --- | --- | --- |
| `treat × role` | +3.43 | 2.75 | **0.212** |
| `treat × male` | +4.01 | 2.48 | **0.106** |
| `treat × live_far` | −0.50 | 2.56 | **0.847** |

None of the three is significant at any conventional level.

- **Managers vs non-managers:** the gap of 3.4 pp has p = 0.21. The data are consistent with the effect being the same for both.
- **Women vs men:** the gap of 4.0 pp has p = 0.11. The closest of the three, and still not significant.
- **Long vs short commute:** this one is the clearest overreading. The two point estimates are −3.11 and −2.61, a difference of **0.5 percentage points** with p = 0.85. They are as close to each other as two estimates get. One crossed the 10% threshold and the other did not, purely because of their standard errors.

> The official solution half-sees this for the commute split, noting "the point estimates are not too different (−2.6 vs −3.1)", and then concludes anyway that "only those with a longer commute react ... because working from home makes a difference for them". The second half does not follow from the data.

The general rule: **the difference between "significant" and "not significant" is not itself statistically significant** (Gelman and Stern 2006). To claim a differential effect, test the difference.

Two more reasons for caution here:

- **Multiple testing.** Three splits plus the overall effect is four tests, and the paper reports more. Some subgroup will cross a threshold by chance. The correction for this is lecture 8.
- **The commute split drops 22% of the sample.** `live_far` is missing for 353 of the 1,612 employees, which is the group whose commute is between 30 and 90 minutes. The two commute regressions run on 611 and 648 people, not on the whole sample.

### Points worth noting

- **The three covariates are balanced**, which is the lecture 6 check on this design. Regressing `role`, `male` and `live_far` on `treat` gives differences of −0.005 (p = 0.81), −0.017 (p = 0.47) and +0.028 (p = 0.33). The odd-birthday rule did its job.
- **The outcome is binary, so the errors are heteroskedastic by construction.** Robust standard errors are the safer default for a linear probability model. Here it makes almost no difference: the robust SE is 1.180 against 1.184, and p moves from 0.0431 to 0.0422. Worth checking rather than assuming.
- **A t-test gives the same answer as the regression**, as it must: Welch gives t = −2.031 and p = 0.0424, pooled gives t = −2.025 and p = 0.0431. The regression reports the pooled version.
- **`Design of Experiments - Exercises.R`** builds the paper's bar chart with `ggsignif` and hard-codes the annotation `"P = 0.0431"` rather than computing it. The Python file reproduces the three regressions with `statsmodels` and skips the plot.
