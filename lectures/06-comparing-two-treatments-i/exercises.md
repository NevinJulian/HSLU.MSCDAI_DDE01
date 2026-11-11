# Lecture 6: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. Numbers come from `lecture6_exercising.csv` and `lecture6_balance_table.csv` and are identical in R and Python, since nothing here is randomly drawn.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)

df_exercising <- read_csv("Data/Out_Data/lecture6_exercising.csv")
df_balance    <- read_csv("Data/Out_Data/lecture6_balance_table.csv")
```

---

## Exercise 6.1: Causal estimands

Data on 20 individuals randomly assigned to free gym access. `D` is 1 if the individual has free access to a gym, `Y` is the points in an exam. Yᵢ(1) and Yᵢ(0) are the potential outcomes.

| ID | Dᵢ | Yᵢ | Yᵢ(0) | Yᵢ(1) | τᵢ |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 82 | 80 | 82 | 2 |
| 2 | 0 | 95 | 95 | 99 | 4 |
| 3 | 0 | 125 | 125 | 135 | 10 |
| 4 | 0 | 140 | 140 | 154 | 14 |
| 5 | 0 | 140 | 140 | 138 | −2 |
| 6 | 1 | 131 | 125 | 131 | 6 |
| 7 | 0 | 95 | 95 | 107 | 12 |
| 8 | 1 | 144 | 145 | 144 | −1 |
| 9 | 0 | 135 | 135 | 139 | 4 |
| 10 | 0 | 135 | 135 | 138 | 3 |
| 11 | 1 | 94 | 95 | 94 | −1 |
| 12 | 0 | 145 | 145 | 146 | 1 |
| 13 | 1 | 151 | 150 | 151 | 1 |
| 14 | 0 | 95 | 95 | 97 | 2 |
| 15 | 1 | 135 | 130 | 135 | 5 |
| 16 | 1 | 113 | 100 | 113 | 13 |
| 17 | 1 | 138 | 125 | 138 | 13 |
| 18 | 1 | 135 | 120 | 135 | 15 |
| 19 | 0 | 90 | 90 | 104 | 14 |
| 20 | 1 | 125 | 125 | 125 | 0 |

The last column is the answer to part 2. Note that `Y` is always the potential outcome matching the actual `D`, which is SUTVA holding in the data.

### Solution 1: SUTVA in this example

SUTVA means the potential outcomes of an individual depend only on **their own** treatment status, not on anyone else's. Concretely here:

| Part | What it rules out in this example |
| --- | --- |
| **No interference** | my exam points must not depend on whether **you** got free gym access. Violated if the treated students drag their untreated friends along to the gym, or if exam points are graded on a curve, where one student's improvement mechanically lowers everyone else's rank |
| **Only one version of the treatment** | "free gym access" must mean the same thing for all ten treated students. Violated if some get a 24-hour gym next to campus and others a gym open three afternoons a week |

The curve point is worth keeping, because it is easy to miss and it makes the outcome definition itself interfere.

### Solution 2: individual causal effects

τᵢ = Yᵢ(1) − Yᵢ(0), the last column of the table above.

They range from **−2 to +15**, and four of the twenty are negative or zero. No single number describes what the gym does to an individual.

### Solution 3: ATE

```r
df_exercising$ICE <- df_exercising$Y1 - df_exercising$Y0
mean(df_exercising$ICE)
```

> τ = (1/N) Σ τᵢ = 115 / 20 = **5.75**

### Solution 4: ATT

```r
mean(df_exercising$ICE[df_exercising$D == 1])
```

> τ_ATT = (1/N_t) Σ_{i:Dᵢ=1} τᵢ = 53 / 10 = **5.3**

The ten treated individuals are IDs 1, 6, 8, 11, 13, 15, 16, 17, 18, 20, and their effects sum to 53.

For completeness, the ATU is 62 / 10 = **6.2**, and the ATE is the average of the two because the groups are the same size: (5.3 + 6.2) / 2 = 5.75.

### Solution 5: a test of the randomization assumptions

If randomization worked, the treatment and control groups should be comparable in their **potential outcomes**, not just in the observed ones. Normally this is impossible to check. Here the full table is given, so it can be done directly:

```r
mean(df_exercising$Y0[df_exercising$D == 1]) - mean(df_exercising$Y0[df_exercising$D == 0])
mean(df_exercising$Y1[df_exercising$D == 1]) - mean(df_exercising$Y1[df_exercising$D == 0])
```

| Comparison | Difference |
| --- | --- |
| mean Y(0), treated − control | **0.0** |
| mean Y(1), treated − control | **−0.9** |

The Y(0) means are identical and the Y(1) means are very close. The randomization worked.

The Y(0) line is the important one, because it **is** the selection bias from the notes. It being zero is why the naive comparison works here:

> naive = E[Y|D=1] − E[Y|D=0] = **5.3** = ATT + 0

In a real experiment you cannot run this test, because Y(0) for the treated and Y(1) for the controls are the missing half of the table. The feasible version is the **balance table** on pre-treatment covariates, which is exercise 6.2.

### Points worth noting

- **ATT (5.3) is not ATE (5.75), even with perfect randomization.** The difference is pure chance in this one draw. Randomization makes them equal **in expectation**, not in any single sample.
- **The naive comparison equals the ATT exactly, not the ATE.** The decomposition in the notes is naive = ATT + selection bias, so with zero selection bias you recover the ATT. It estimates the ATE only because randomization also makes ATT = ATE in expectation.
- **A negative τᵢ is not an error.** IDs 5, 8 and 11 are worse off under treatment. An average effect of 5.75 hides four people it did not help.
- The R file's first calculation, `mean(Y1[D==1]) - mean(Y0[D==1])`, is the ATT written out the long way. It gives 5.3, the same as `mean(ICE[D==1])`.

---

## Exercise 6.2: Balance tests

`lecture6_balance_table.csv` contains a treatment variable and 50 covariates (X1 to X50), 1,246 rows and 52 columns including `id`.

### Solution 1: t-test for X1

```r
t_test1 <- t.test(X1 ~ treatment, data = df_balance)
print(t_test1)
```

```
	Welch Two Sample t-test

data:  X1 by treatment
t = -7.6729, df = 1236.7, p-value = 0.00000000000003393
alternative hypothesis: true difference in means between group 0 and group 1 is not equal to 0
95 percent confidence interval:
 -0.5733304 -0.3398421
sample estimates:
mean in group 0 mean in group 1
    0.007866302     0.464452558
```

**Interpretation.** The control mean is 0.008, the treatment mean is 0.464, a difference of about 0.46. The p-value is 3.4 × 10⁻¹⁴, so the difference is massively significant. On this covariate the groups are not comparable.

**Do you have to reject the research design based on this?** Not on this one variable alone. With 50 covariates, some will come out significant by chance, so a single rejection is not yet evidence of a broken randomization. Parts 4 and 5 look at all 50 together.

That is the official answer, and it is the right one for the question as asked. It is not the right conclusion for **this** data, see the pushback below.

### Solution 2: where the numbers are stored

`t.test` returns a list, so the components can be pulled out by name:

```r
t_test1$estimate[1]   # mean in group 0: 0.007866302
t_test1$estimate[2]   # mean in group 1: 0.4644526
t_test1$p.value       # 0.00000000000003393281
```

`View(t_test1)` shows the whole object. Other useful fields are `$statistic` (the t-value), `$parameter` (degrees of freedom), `$conf.int` and `$stderr`. This is what part 5 needs in order to build the table in a loop.

### Solution 3: balance table with crosstable

```r
library(crosstable)
library(flextable)

my_table <- crosstable(df_balance %>% select(-id),
                       by = "treatment",
                       test = TRUE,
                       unique_numeric = 1,
                       funs = c(mean = mean, "std error" = sd)) %>%
  as_flextable()
print(my_table)
```

`select(-id)` drops the identifier, which has no business in a balance table. `unique_numeric = 1` forces variables with few distinct values to be treated as numeric rather than categorical. Note that `funs` labels `sd` as "std error", which is wrong: the standard deviation is not the standard error. The table prints the SD.

### Solution 4: rejection rates

| Level | Variables below it | Rejection rate | Expected under the null |
| --- | --- | --- | --- |
| **10%** | X1, X2, X9, X28 | **4 / 50 = 8%** | 10% |
| **5%** | X1, X2 | **2 / 50 = 4%** | 5% |

Both rates are slightly **below** what the null predicts. Taken at face value, the randomization worked.

### Solution 5: the same table by hand

Loop over the 50 covariates, run a t-test for each, collect the results:

```r
balance_out <- tibble(
  variable = character(),
  mean_treated = numeric(),
  mean_control = numeric(),
  p_value = numeric()
)

for (i in 1:50) {
  varname <- names(df_balance)[i + 2]
  df_balance$var <- as.vector(df_balance[[i + 2]])

  t_test <- t.test(var ~ treatment, data = df_balance)

  balance_out <- bind_rows(balance_out, tibble(
    variable = varname,
    mean_treated = t_test$estimate[2],
    mean_control  = t_test$estimate[1],
    p_value = t_test$p.value
  ))
}

balance_out %>% filter(p_value < 0.1)
```

```
# A tibble: 4 × 4
  variable mean_treated mean_control  p_value
  <chr>           <dbl>        <dbl>    <dbl>
1 X1             0.464       0.00787 3.39e-14
2 X2             0.404      -0.00959 5.24e-12
3 X9            -0.0583      0.0438  7.57e- 2
4 X28            0.0545     -0.0501  6.22e- 2
```

`i + 2` skips `id` and `treatment`, which are the first two columns. `estimate[2]` is the group with `treatment == 1`, because `t.test` orders the groups by the factor level.

### The randomization did not work, and the rejection rate hides it

This is where I disagree with the official solution, which concludes that both rejection rates are below expectation and leaves it there.

Look at the four p-values rather than counting them:

| Variable | p-value | Expected number of tests this extreme, out of 50 |
| --- | --- | --- |
| X1 | 3.4 × 10⁻¹⁴ | 1.7 × 10⁻¹² |
| X2 | 5.2 × 10⁻¹² | 2.6 × 10⁻¹⁰ |
| X9 | 0.076 | 3.8 |
| X28 | 0.062 | 3.1 |

X9 and X28 are exactly what chance produces. Running 50 tests, you expect three or four p-values in that range, and finding two is unremarkable.

X1 and X2 are a different object entirely. If the groups were really balanced on X1, a difference this large would show up in roughly one out of every 600 **billion** 50-test batches. That is not an unlucky draw, it is a treatment assignment related to X1 and X2.

The rejection rate misses this because it throws away everything except whether each p-value crossed a line. Two p-values of 10⁻¹⁴ count the same as two p-values of 0.049.

**What I would actually conclude:** the design is broken, the assignment depends on X1 and X2, and the estimate will be confounded by whatever they measure. Controlling for X1 and X2 in the main regression would be a partial repair, and only if they are genuinely pre-treatment.

### Points worth noting

- **The sign of the t-statistic depends on the direction.** R's formula interface computes group 0 minus group 1, so `t = −7.67`. Computing treated minus control gives `+7.67`. Same test, same p-value.
- **`t.test` in R defaults to Welch**, not the pooled test, which is why `df = 1236.7` rather than 1244. The pooled version needs `var.equal = TRUE`, and that is what the lecture 7 formula assumes.
- **Balance tests have low power for small imbalances.** A non-significant p-value does not mean the groups are identical, only that any difference is small relative to the noise. With n = 1,246 the test here has plenty of power, but in a 60-person experiment a balance table proves very little.
- **`Design of Experiments - Exercises.py`** uses `equal_var=False`, matching R's default, and defines `build_balance_table` as a helper. It slices covariates with `cols[2:52]`, which relies on `id` and `treatment` being the first two columns, same assumption as the R loop.
