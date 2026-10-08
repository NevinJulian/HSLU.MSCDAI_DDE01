# Lecture 4: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. R output is from the official solution, Python numbers from [exercises.ipynb](exercises.ipynb). Exercise 4.2 has no random draws, so R and Python give identical numbers here.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)

df_schooling <- read_csv("Data/Out_Data/lecture4_schooling_earnings.csv")
```

---

## Exercise 4.1: Threats to internal validity

Look at the following statements and argue what could be violated in terms of internal validity.

1. "The more firefighters fight a fire, the greater is the damage."
2. "The higher the unemployment rate, the lower is GDP growth."
3. "People who exercise more tend to lose weight."
4. "In families with more than one kid, the younger ones have a higher likelihood of being born with Down syndrome."
5. "Students who barely miss a scholarship do not have worse grades than those who barely achieved a scholarship."

### Solution

| # | Threat | Mechanism | Direction |
| --- | --- | --- | --- |
| 1 | **Confounder:** severity of the fire | a big fire causes both more firefighters and more damage | **upward**. Cor(severity, firefighters) positive, Cor(severity, damage) positive. The true effect of an extra firefighter on damage is presumably negative. |
| 2 | **Reverse causality** | weak GDP growth causes firms to lay people off, so growth drives unemployment just as much as the other way round | either way. The two are determined simultaneously (Okun's law is a correlation, not a direction). |
| 3 | **Confounder:** the desire to lose weight | people who want to lose weight exercise more **and** eat better, sleep more, drink less | **upward**. Part of what looks like the effect of exercise is the rest of the diet. |
| 4 | **Confounder:** the mother's age | older mothers have a higher risk of a child with Down syndrome, and a later-born child is by construction born to an older mother | **upward**. Birth order has no causal effect of its own here. |
| 5 | **John Henry effect** | students who barely missed the scholarship know it and work harder to catch up | **downward**. The real effect of the scholarship is masked because the control group raises its effort. |

### Points worth noting

- **1, 3 and 4 are the same mistake with different clothes.** A third variable drives both sides. In 1 and 4 the true effect of the named variable is probably zero or even reversed, so the entire observed relationship is bias.
- **2 could also be read as a confounder** (a demand shock that moves both), but the clean answer is reverse causality, since GDP growth demonstrably causes unemployment.
- **5 is the odd one out and is worth a second look.** "Barely missing" versus "barely achieving" is a deliberately good design (a regression discontinuity): just above and just below a cutoff, students are almost identical, so the comparison should be clean. The design handles the classical threats. What it cannot handle is the **implementation** threat, which is that people on the losing side know they lost. That is the point of the exercise: a good design still fails on human reactions.
- **4 also has a measurement side.** Down syndrome is detected by screening, and screening is more common for older mothers. More testing finds more cases.

---

## Exercise 4.2: Years of schooling and earnings

You are interested in the impact of years of schooling on earnings.

1. What could be confounders of this relationship?
2. Load `lecture4_schooling_earnings.csv` and look at a scatter plot between years of schooling and earnings. What do you observe?
3. Based on the graph, what slope do you expect?
4. Regress earnings on years of schooling. How does it compare to your guess in (3)?
5. Add a measure of motivation to the regression. How do the results change? Was the estimate in (4) biased, and in which direction?

### The data

| Variable | Content |
| --- | --- |
| `years_schooling` | years of schooling, 10.0 to 27.7 |
| `motivation` | motivation score, 12.0 to 26.0 |
| `earnings` | monthly earnings in Swiss francs, 5,455 to 10,780 |

1,023 observations. Schooling and motivation correlate at 0.97, which is the whole exercise in one number.

### Solution 1: confounders

| Confounder | Effect on schooling | Effect on earnings |
| --- | --- | --- |
| **Motivation** | motivated people stay in school longer | motivated people work harder and get promoted |
| **Ability** | easier to pass exams, so school is cheaper in effort | more productive at work |
| **Parental background** (education, income, network) | pays for and expects more education | pays for the first job through contacts |

All three have **positive** correlations with both sides, so all three bias the estimate **upwards** (notes, section 2.1). Part 5 shows this with motivation.

- This is the classic problem in labour economics. It is why schooling is studied with natural experiments: changes in compulsory schooling laws, distance to the nearest college, quarter of birth.
- **Signalling** (lecture 1, example 1.3) is a different objection: even a perfectly estimated effect does not say whether schooling makes people productive or only reveals who was already productive.

### Solution 2: scatter plot

```r
ggplot(aes(x = years_schooling, y = earnings), data = df_schooling) +
  geom_point() +
  theme_bw()
```

There is an obvious, tight, positive and apparently **linear** relationship. The cloud is narrow: earnings are almost fully determined by schooling in this data (R² = 0.98 in part 4). No curvature, so no functional form problem (notes, section 2.3).

### Solution 3: guess the slope

Read two points off the graph:

| Years of schooling | Earnings |
| --- | --- |
| 15 | about 6,500 |
| 25 | about 10,000 |

Slope = 3,500 / 10 = **about 350 francs per year of schooling**.

In the data the group means are 6,742 around 15 years and 10,168 around 25, which gives 343. The eyeball estimate is good.

### Solution 4: short regression

```r
summary(lm(earnings ~ years_schooling, data = df_schooling))
```

```
Coefficients:
                Estimate Std. Error t value            Pr(>|t|)
(Intercept)     1706.308     29.820   57.22 <0.0000000000000002 ***
years_schooling  338.957      1.518  223.29 <0.0000000000000002 ***

Residual standard error: 198.7 on 1021 degrees of freedom
Multiple R-squared:  0.9799, Adjusted R-squared:  0.9799
```

**339 francs per year of schooling**, very close to the 350 guessed in part 3. Highly significant, R² = 0.98.

Python gives the same numbers (notebook): 338.957 with a standard error of 1.518.

### Solution 5: adding motivation

```r
summary(lm(earnings ~ years_schooling + motivation, data = df_schooling))
```

```
Coefficients:
                  Estimate Std. Error t value            Pr(>|t|)
(Intercept)     1500.10919    0.15297    9806 <0.0000000000000002 ***
years_schooling  149.98408    0.03061    4899 <0.0000000000000002 ***
motivation       200.00844    0.03138    6373 <0.0000000000000002 ***

Residual standard error: 0.9965 on 1020 degrees of freedom
Multiple R-squared:      1,  Adjusted R-squared:      1
```

| | Intercept | Schooling | Motivation | Residual SE | R² |
| --- | --- | --- | --- | --- | --- |
| without motivation | 1,706.3 | **339.0** | – | 198.7 | 0.980 |
| with motivation | 1,500.1 | **150.0** | 200.0 | 1.0 | 1.000 |

**Yes, the estimate in (4) was biased, upwards.** The effect of schooling drops from 339 to 150 francs. More than half of what looked like the return to schooling was the return to motivation, which schooling was standing in for.

The omitted variable bias formula from the notes checks out exactly:

```
bias = γ · δ
γ = effect of motivation on earnings          = 200.008
δ = slope of motivation on years_schooling    =   0.945
γ · δ                                         = 188.973
339.0 − 150.0                                 = 188.973 ✓
```

### Points worth noting

- **The data were simulated.** Residual SE 0.9965 and R² = 1 mean the true model is `earnings = 1500 + 150 · schooling + 200 · motivation + noise` with a noise standard deviation of exactly 1. That is why the coefficients land on round numbers. The exercise is a demonstration of the formula, not a real labour market estimate.
- **Correlation 0.97 between schooling and motivation is extreme.** With collinearity like this, both coefficients would normally be very imprecise. Here they are not, because the noise is practically zero. In real data you cannot separate two variables that move together this closely.
- **The short regression is not "wrong".** 339 is the correct answer to a different question: how much more does someone with one more year of schooling earn on average. It is only wrong as a **causal** statement about what an extra year of schooling does.
- **Controlling for motivation fixes this only because motivation is measured.** Ability and family background are still missing, so even 150 is an upper bound on the causal effect. This is the limit of solution 1 in the notes.
- **Never control for something that sits between D and Y.** If more schooling causes higher motivation, controlling for motivation removes part of the real effect. The exercise assumes motivation comes first.
- **Reading R output:** `Residual standard error: 198.7 on 1021 degrees of freedom` is 1,023 observations minus 2 estimated parameters. In the second model 1,020 = 1,023 − 3. `<0.0000000000000002` is R's way of printing a p-value below its display threshold, not a precise value.
- **`Design of Experiments - Exercises.py`** reproduces both regressions correctly with `statsmodels`. The R file reads the data from `Data/Out_Data/`, the official solution HTML from `../Data/Out_Data/`, depending on the working directory.
