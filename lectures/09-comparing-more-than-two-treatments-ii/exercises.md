# Lecture 9: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. Every coefficient, standard error, R² and F-statistic reproduces identically in R and Python. Two places where I disagree with the official text are flagged in the margin as they come up.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)

wtlossdat      <- read_csv("Data/Out_Data/lecture9_weight_loss.csv")
df_vaccination <- read_csv("Data/Out_Data/lecture9_vaccination.csv")
```

---

## Exercise 9.1: Weight loss

You are interested in exploring three components of a weight loss intervention: A. Keeping a food diary, B. Increasing activity, C. Home visit. You investigate all eight (2³) combinations of conditions. The dataset `lecture9_weight_loss.csv` includes the variable weight loss (y). It measures the weight after the intervention minus the weight before the intervention (in kg). Notation is such that the control condition is denoted as −1.

> **Read the sign before anything else.** y is *after minus before*, so a **negative** y is weight lost and a positive y is weight gained. A treatment that "works" has a negative mean effect. Getting this backwards inverts every conclusion in the exercise.
>
> The file has 800 rows, 100 in each of the eight cells, and a `Run Order` column that plays no part here.

### Solution 1: the mean effect of each treatment

```r
mean(wtlossdat$y[wtlossdat$A == 1]) - mean(wtlossdat$y[wtlossdat$A == -1])
mean(wtlossdat$y[wtlossdat$B == 1]) - mean(wtlossdat$y[wtlossdat$B == -1])
mean(wtlossdat$y[wtlossdat$C == 1]) - mean(wtlossdat$y[wtlossdat$C == -1])
```

| Treatment | Mean effect | Direction |
| --- | --- | --- |
| A, food diary | **+0.4554** | weight **gained** |
| B, increasing activity | **−1.8920** | weight **lost** |
| C, home visit | **+0.5768** | weight **gained** |

**Only treatment B reduces weight**, by 1.89 kg on average. The other two are associated with weight *gain* of about half a kilo each, and B's effect is three to four times larger than either.

Since the design is balanced at 100 per cell, these raw differences are the main effects exactly, and they also equal twice the first-order coefficients of the ±1 regression, 2 × (+0.2277), 2 × (−0.9460) and 2 × (+0.2884).

### Solution 2: the long model

```r
mod <- lm(y ~ factor(A) * factor(B) * factor(C), data = wtlossdat)
summary(mod)
```

```
Coefficients:
                                 Estimate Std. Error t value  Pr(>|t|)
(Intercept)                       0.94324    0.10015   9.418  < 2e-16 ***
factor(A)1                        0.03498    0.14163   0.247  0.80501
factor(B)1                       -1.08863    0.14163  -7.686 4.48e-14 ***
factor(C)1                        0.89800    0.14163   6.340 3.85e-10 ***
factor(A)1:factor(B)1            -0.37744    0.20030  -1.884  0.05988 .
factor(A)1:factor(C)1             0.58690    0.20030   2.930  0.00349 **
factor(B)1:factor(C)1            -1.86071    0.20030  -9.290  < 2e-16 ***
factor(A)1:factor(B)1:factor(C)1  1.26283    0.28327   4.458 9.46e-06 ***
---
Residual standard error: 1.001 on 792 degrees of freedom
Multiple R-squared: 0.5565,  Adjusted R-squared: 0.5526
F-statistic: 142 on 7 and 792 DF,  p-value: < 2.2e-16
```

> **Porting this to Python.** `smf.ols("y ~ C(A) * C(B) * C(C)")` fails with `TypeError: 'Series' object is not callable`, because the column named `C` shadows patsy's categorical helper `C()`. Rename the columns, or build 0/1 dummies and use a plain numeric interaction, which gives the identical model. The notebook does the latter.

### Solution 3: interpreting the coefficients

The coefficients are differences between cell means, with the all-control cell as the baseline. The model has eight coefficients and the design has eight cells, so it is an exact re-parameterisation: nothing is estimated beyond the eight group averages.

| Coefficient | Reads as | Value |
| --- | --- | --- |
| Intercept | mean of the all-control cell, A = B = C = −1 | 0.9432 |
| `factor(C)1` | effect of a home visit **when A and B are both control** | +0.8980 |
| `factor(B)1` | effect of activity when A and C are control | −1.0886 |
| `factor(A)1` | effect of a food diary when B and C are control | +0.0350 |

Check the first two against the data directly: the cell with only C treated has mean 1.8412, and 0.9432 + 0.8980 = 1.8412.

> **The official solution has an arithmetic slip here.** It states "the mean of the group only treated in C but not in A and B is **1.74** and therefore the coefficient on C is 0.89 (intercept of 0.94 + 0.89 = 1.74)". But 0.94 + 0.89 = **1.83**, and the actual cell mean is **1.8412**. The logic is right and the coefficient is right, only the total is wrong.

**The substantive reading.** Almost every coefficient involving B is negative, −1.0886, −0.3774 and −1.8607, the only exception being the triple interaction at +1.2628. That again points to B as the treatment doing the work.

The three-way interaction is significant at p = 9.5 × 10⁻⁶, which is unusual and is the reason this dataset is set as the exercise: it is a case where dropping the highest-order term, as people routinely do when it looks insignificant, would be wrong. Compare the gym/diary/sleep data in [the notes](notes.md#33-estimating-the-full-model), where the same term has p = 0.26.

### What the question does not ask, and should

**The best combination is not "all three treatments".** The eight cell means are:

| Food diary | Activity | Home visit | Mean y |
| --- | --- | --- | --- |
| −1 | 1 | 1 | **−1.1081** ← most weight lost |
| 1 | 1 | −1 | −0.4879 |
| −1 | 1 | −1 | −0.1454 |
| 1 | 1 | 1 | +0.3992 ← all three treatments |
| −1 | −1 | −1 | +0.9432 |
| 1 | −1 | −1 | +0.9782 |
| −1 | −1 | 1 | +1.8412 |
| 1 | −1 | 1 | **+2.4631** ← most weight gained |

Giving all three treatments produces **+0.40 kg**, a gain. The best cell, at −1.11 kg, is activity plus home visit **without** the food diary. Adding the food diary to that combination costs 1.51 kg of the result.

This is the entire argument for running a factorial design rather than three separate two-arm trials. Three separate experiments would have estimated the three main effects, two of them positive and one negative, and the natural conclusion would have been to deploy B alone, or possibly all three. Neither is the best option available, and no amount of data from separate trials would have revealed that, because the information lives in the interaction terms which separate trials cannot estimate.

Note also that B and C interact strongly and negatively, −1.86. Holding the food diary at control, the home visit **gains** 0.90 kg on its own and **loses** 0.96 kg once activity is added — these are the coefficients `factor(C)1` and `factor(C)1 + factor(B)1:factor(C)1`, both of which condition on the other factors being at their control level. A treatment can reverse sign depending on what it is paired with, and reporting only its main effect of +0.58 hides that completely.

---

## Exercise 9.2: Flu vaccination

A research team is interested in estimating the impact of incentives and reminders on vaccination against the seasonal flu. The individual-level data is in `lecture9_vaccination.csv`, 1034 rows, with `Vaccinated` as a 0/1 outcome.

### Solution 1: the mean effect of both treatments

```r
df_vaccination %>% group_by(D_incentive) %>% summarize(Vaccinated_mean = mean(Vaccinated))
df_vaccination %>% group_by(D_reminder)  %>% summarize(Vaccinated_mean = mean(Vaccinated))
```

| Treatment | Control | Treated | Effect |
| --- | --- | --- | --- |
| Incentive | 0.5706 | 0.9400 | **+0.3694** |
| Reminder | 0.7002 | 0.8104 | **+0.1103** |

Because the outcome is a 0/1 indicator, its mean is a proportion and a difference in means is a difference in percentage points.

- The incentive makes people **36.9 percentage points** more likely to get vaccinated
- The reminder makes people **11.0 percentage points** more likely to get vaccinated

The incentive is more than three times as effective as the reminder.

### Solution 2: the regression

```r
summary(lm(Vaccinated ~ D_incentive * D_reminder, data = df_vaccination))
```

```
Coefficients:
                        Estimate Std. Error t value Pr(>|t|)
(Intercept)             0.511811   0.024127  21.213  < 2e-16 ***
D_incentive             0.370318   0.033828  10.947  < 2e-16 ***
D_reminder              0.115565   0.033828   3.416  0.00066 ***
D_incentive:D_reminder  0.002305   0.047840   0.048  0.96158
---
Residual standard error: 0.3845 on 1030 degrees of freedom
Multiple R-squared: 0.2031,  Adjusted R-squared: 0.2007
F-statistic: 87.48 on 3 and 1030 DF,  p-value: < 2.2e-16
```

The four cell means behind it:

| Incentive | Reminder | n | Vaccinated |
| --- | --- | --- | --- |
| 0 | 0 | 254 | 0.5118 |
| 0 | 1 | 263 | 0.6274 |
| 1 | 0 | 263 | 0.8821 |
| 1 | 1 | 254 | **1.0000** |

### Solution 3: which coefficients are the mean effects?

**Strictly, none of them.** This is the point of the question and it is worth being careful about.

With 0/1 coding and the interaction in the model, `D_incentive` = 0.3703 is the effect of the incentive **when the reminder is absent**, and `D_reminder` = 0.1156 is the effect of the reminder **when the incentive is absent**. The main effects average over both levels of the other factor, and are recovered as β + β_int/2:

| | Coefficient | Main effect, β + β_int/2 | Raw difference of means |
| --- | --- | --- | --- |
| Incentive | 0.370318 | **0.371471** | 0.369439 |
| Reminder | 0.115565 | **0.116718** | 0.110251 |

All three columns are nearly identical here **only because the interaction is almost exactly zero**. Had it been 15.54 as in the lecture example, they would differ substantially, as section 2.8 of [the notes](notes.md#28-the-coefficient-is-not-the-main-effect) shows.

> **A second reason the columns differ slightly.** The design is **not balanced**: the cells hold 254, 263, 263 and 254 people. The raw difference of means weights the cells by their sample sizes, while β + β_int/2 weights them equally. That is why the reminder's raw 0.1103 sits a little below its equal-weighted 0.1167. The official solution reports the raw differences as "the mean effects", which is standard practice and fine to hand in, but the two quantities are not the same thing and the sheet's own definition on slide 6 is the equal-weighted one.

### Solution 4: is there a positive interaction, and is it significant?

The interaction coefficient is **+0.0023**, so positive in sign but negligible in size, and **not significant** at p = 0.96. Taken at face value: the two treatments are additive, the incentive does the same thing whether or not a reminder was sent.

> **The data cannot answer this question, and that is worth saying.** Look at the cell means above. The incentive-plus-reminder cell is **exactly 1.0000** — every single one of those 254 people got vaccinated. The outcome is bounded at 1, so that cell is saturated.
>
> Work out what that implies. Under perfect additivity the treated-treated cell would be 0.5118 + 0.3703 + 0.1156 = **0.9977**, just under the ceiling. The observed value is 1.0000, so the interaction is 1.0000 − 0.9977 = **+0.0023**, and since no proportion can exceed 1, this is the **largest interaction the data could possibly have shown** given the other three cells.
>
> The test therefore has no power against a positive alternative. Reporting "the interaction is not significantly different from zero" is true but misleading, because a strongly positive interaction was arithmetically impossible from the start. The honest conclusion is that this design cannot detect positive complementarity between the two treatments, and a dataset with a lower baseline, or a continuous outcome, would be needed to look for it.

This also explains the residual standard error of 0.3845 and the modest R² of 0.20. A linear model on a 0/1 outcome, a linear probability model, has heteroskedastic errors by construction and can predict outside [0, 1]. It is the right tool for this exercise and the coefficients remain interpretable as percentage points, but the standard errors would normally be reported as robust.

### Solution 5: the interaction plot

```r
interaction.plot(x.factor = df_vaccination$D_incentive,
                 trace.factor = df_vaccination$D_reminder,
                 response = df_vaccination$Vaccinated,
                 type = "l",
                 xlab = "Incentive treatment",
                 trace.label = "Reminder treatment",
                 ylab = "Vaccinated")
```

Two lines, one per reminder condition, each running from incentive = 0 to incentive = 1 at the cell means from solution 2.

### Solution 6: reading the plot

Three things are visible, and each maps onto a coefficient:

- **The vertical gap between the lines** is the reminder effect, about 11 percentage points. It corresponds to `D_reminder`.
- **The slope of each line** is the incentive effect, running from roughly 0.51 to 0.88 on the lower line. It corresponds to `D_incentive`, and the slope is visibly much steeper than the gap between the lines, which is the plot's version of "the incentive is more than three times the reminder".
- **Whether the lines are parallel** is the interaction. The interaction is the difference between the two lines at x = 1 minus their difference at x = 0, which is zero exactly when the lines are parallel. Here they are almost parallel, so the interaction is close to zero.

The one thing the plot shows that the coefficient table does not: the upper line **reaches the top of the chart at x = 1**. That is the ceiling from solution 4, and it is the reason the lines are nearly parallel. The upper line could not have risen any further, so the design had no room to produce a non-parallel picture in the positive direction.
