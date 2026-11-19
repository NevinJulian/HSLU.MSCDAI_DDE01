# Lecture 9: Comparing more than two treatments II

**Date:** 19 Nov 2026 (online) · **Lecturer:** Lukas Schmid · [Exercises](exercises.md) · [Notebook](exercises.ipynb)

## Contents

1. [Motivation](#1-motivation)
2. [The 2 by 2 factorial design](#2-the-2-by-2-factorial-design)
3. [Higher-order designs](#3-higher-order-designs)
4. [Key terms](#key-terms)

The slides give definition 9.1 and examples 9.1 and 9.2. The recomputed numbers, the relationship between the regression coefficients and the main effects, the correction to slide 7, and the reasons the ±1 coding exists are my additions, sources at the end.

Lecture 8 asked whether several treatments differ at all, and then which pairs differ. This lecture changes the question. When treatments can be given **together**, the interesting quantity is no longer "which single condition is best" but "what does combining them do", and that is something neither ANOVA nor a pairwise t-test is built to answer.

---

## 1. Motivation

#### Example 9.1: Impact of gym and learning diary

We want to explore the impact of both a randomized treatment regarding gym access and a randomized treatment that reminded students to write a learning diary on points in a math exam (Y). We have data on 1000 students:

| ID | Y | D_gym | D_diary |
| --- | --- | --- | --- |
| 1 | 173 | 1 | 1 |
| 2 | 178 | 1 | 1 |
| 3 | 153 | 0 | 1 |
| … | … | … | … |
| 1000 | 140 | 0 | 1 |

> **Data note.** The file is `lecture9_academic_performance.csv`, 1000 rows. It carries `D_gym`, `D_diary`, `D_sleep` and `Y`, plus pre-built interaction columns (`D_gym_diary`, `D_sleep_gym`, `D_sleep_diary`, `D_sleep_diary_gym`) that you do not need if you let the formula build them. The design is **perfectly balanced**: 250 students in each of the four 2 × 2 cells and 125 in each of the eight 2 × 2 × 2 cells. That balance matters more than it looks, and section 2.8 is where it starts to.

## 2. The 2 by 2 factorial design

### 2.1 General setup

#### Definition 9.1: Factorial design

A factorial design is an experimental design where the investigator selects a fixed number of factors with k ≥ 2 levels and then measures response variables at each factor-level combination. The factors can be quantitative or qualitative.

Examples:

- Qualitative factors: going to the gym and a learning diary
- Two quantitative variables: temperature and CO₂ concentration

### 2.2 Difference to ANOVA

In ANOVA, the goal is to compare the individual experimental conditions with each other. In a factorial experiment, the goal is generally to compare **combinations** of experimental conditions.

#### Example 9.2: Impact of gym and learning diary (cont.)

In an ANOVA design, we are interested in whether any experimental condition (gym, learning diary) has an impact on academic performance. In a factorial design, we are interested in whether the impact of specific combinations (e.g. going to the gym *and* keeping a learning diary) improves academic performance.

The practical difference is what you do with the four cells. ANOVA treats them as four unordered groups and asks whether the four means are equal. A factorial design treats them as a 2 × 2 grid and asks two structured questions instead: what does each treatment do on average, and does one treatment change what the other does. The second question has no counterpart in lecture 8.

### 2.3 The table and the main effects

We can illustrate the qualitative 2 by 2 design in the following table:

| Y | Gym | Diary |
| --- | --- | --- |
| y₁ | No | No |
| y₂ | No | Yes |
| y₃ | Yes | No |
| y₄ | Yes | Yes |

where yᵢ stands for the mean of Y in a certain cell. Throughout this lecture, we assume that the treatment groups have the same number of observations.

The mean effects (ME) of going to the gym (treatment A) and of writing a learning diary (treatment B) are:

> ME(A) = ȳ(A+) − ȳ(A−) = (y₃ + y₄)/2 − (y₁ + y₂)/2
>
> ME(B) = ȳ(B+) − ȳ(B−) = (y₂ + y₄)/2 − (y₁ + y₃)/2

Read the subscripts off the table rather than memorising them. For gym, the "Yes" rows are y₃ and y₄, so those go on top. For diary, the "Yes" rows are y₂ and y₄.

> The equal-group-size assumption is doing real work in these formulas. Averaging the two cells with weight ½ each is only the same as the overall treated mean when both cells hold the same number of people. Section 2.8 and [exercise 9.2](exercises.md#exercise-92-flu-vaccination) show what happens when they do not.

### 2.4 The calculation

#### Example 9.1 (cont.)

In R, we can calculate the group means as follows:

```r
df_factorial %>%
  group_by(D_gym, D_diary) %>%
  summarize(Y_mean = mean(Y))
```

```
  D_gym D_diary Y_mean
  <int>   <int>  <dbl>
1     0       0  126.8
2     0       1  147.0
3     1       0  140.8
4     1       1  176.6
```

Based on this, we can calculate the main effect for exercising (`D_gym`) as:

> (176.6 + 140.8)/2 − (147.0 + 126.8)/2 = 158.7 − 136.9 = **21.8**

**The slide's diary line pairs the wrong cells.** It is printed as

> (176.6 + 126.8)/2 − (147.0 + 140.8)/2 = 161.8 − 133.8 = 28.0

The two results, 161.8 and 133.8, are right and so is the answer of 28.0. The fraction above them is not: as written it works out to 151.7 − 143.9 = **7.8**. The cells 126.8 and 147.0 have been swapped between the numerators. The correct statement is

> (176.6 + 147.0)/2 − (140.8 + 126.8)/2 = 161.8 − 133.8 = **28.0**

which is just ME(B) = (y₂ + y₄)/2 − (y₁ + y₃)/2 from section 2.3, with y₂ = 147.0 the no-gym diary cell. Worth catching, because a student reproducing the printed fraction gets 7.8 and has no way to tell which of the two numbers to trust.

Unrounded, the cell means are 126.80, 147.04, 140.84 and 176.62, giving ME(gym) = **21.81** and ME(diary) = **28.01**.

### 2.5 The same thing, one factor at a time

This is equivalent to calculating the means per group and then taking the difference (see lecture 7).

```r
df_factorial %>% group_by(D_gym) %>% summarize(Y_mean = mean(Y))
```

```
  D_gym Y_mean
1     0  136.9
2     1  158.7
```

```r
df_factorial %>% group_by(D_diary) %>% summarize(Y_mean = mean(Y))
```

```
  D_diary Y_mean
1       0  133.8
2       1  161.8
```

The two routes agree exactly, 21.81 and 28.01 either way. That equality is **not** a general fact: it holds here because the design is balanced. Collapsing over the other factor gives the right answer only when the other factor is equally represented in both arms of the one you are looking at.

Often, those differences are illustrated as a line between the two group means, or with a 95% confidence interval on each mean, which has the advantage that the reader directly observes the uncertainty of the estimates.

### 2.6 Interaction effects

Often we are interested in whether treatment A works better under treatment conditions B (B+) or under control conditions (B−). In our example, we want to explore whether the impact of the gym is higher for individuals who keep a learning diary than for those who do not.

> INT(A, B) = ME(A | B+) − ME(A | B−)

#### Example 9.1 (cont.)

The mean effect of the gym treatment is 176.6 − 147.0 = **29.6** for those with a diary and 140.8 − 126.8 = **14.0** for those with no diary. The difference is **15.6**, and thus the gym effect is 15.6 points higher if a person also keeps a learning diary. Unrounded, 29.58 − 14.04 = **15.54**.

Two properties worth knowing:

- **The interaction is symmetric.** INT(A, B) = INT(B, A). Computing it as "what the diary does to the gym effect" and as "what the gym does to the diary effect" gives the same 15.54. There is one interaction in a 2 × 2 design, not two, and which treatment you call the moderator is a storytelling choice rather than a statistical one.
- **It is a difference of differences**, so it needs all four cells. No pair of cells identifies it, which is why a factorial design cannot be assembled after the fact from two separate two-arm experiments.

### 2.7 The regression framework

We can also implement this design in a regression of the following form:

> Y = β₀ + Aβ₁ + Bβ₂ + A × Bβ₃ + u

where A and B are indicator variables (0 or 1) for the respective treatments and A × B is their interaction.

```r
results_factorial = lm(Y ~ D_diary * D_gym, data = df_factorial)
summary(results_factorial)
```

```
Coefficients:
               Estimate Std. Error t value Pr(>|t|)
(Intercept)     126.800      1.723  73.604  < 2e-16 ***
D_diary          20.240      2.436   8.308 3.17e-16 ***
D_gym            14.040      2.436   5.763 1.10e-08 ***
D_diary:D_gym    15.540      3.445   4.510 7.25e-06 ***
```

Every coefficient is a cell mean or a difference of cell means:

| Coefficient | Equals | Value |
| --- | --- | --- |
| β₀ | y₁, the no-gym no-diary cell | 126.80 |
| β₂ (`D_diary`) | y₂ − y₁, the diary effect **when gym = 0** | 20.24 |
| β₁ (`D_gym`) | y₃ − y₁, the gym effect **when diary = 0** | 14.04 |
| β₃ (interaction) | (y₄ − y₂) − (y₃ − y₁) | 15.54 |

The regression is therefore just a re-parameterisation of the four cell means: four cells, four coefficients, no information gained or lost. What it adds is standard errors and p-values, which the table of means does not give you.

### 2.8 The coefficient is not the main effect

This is the thing to get straight, and the slides do not say it outright.

**β₁ = 14.04 is not ME(A) = 21.81.** With 0/1 indicators and an interaction in the model, β₁ is the effect of the gym **at diary = 0**, a simple effect in one row of the table. The main effect averages over both rows. The two are related by

> ME(A) = β₁ + β₃/2 = 14.04 + 15.54/2 = **21.81**

and they coincide only when β₃ = 0. Quoting `D_gym` as "the effect of the gym" in a model that also contains the interaction is a common and real mistake: here it understates the average effect by a third.

So in the regression output above, **none of the printed coefficients is a main effect**. They are a baseline cell and three contrasts.

### 2.9 The ±1 notation

In some textbooks and applications, the control condition is not denoted as 0 but as −1. This has the advantage that we can calculate the treatment effects more easily in R.

```
  D_gym D_diary Y_mean
1    -1      -1  126.8
2    -1       1  147.0
3     1      -1  140.8
4     1       1  176.6
```

```r
sum(df_groups_mod["D_gym"] * df_groups_mod["Y_mean"]) / 2
21.81
```

Multiplying each cell mean by ±1 and halving is exactly ME(A) written as one expression: the two treated cells enter positively, the two control cells negatively, and dividing by 2 turns the sum of four cells into a difference of two averages.

**The deeper reason to use ±1 is section 2.8.** Re-run the regression with A and B coded ±1 instead of 0/1 and the coefficients change meaning:

| | 0/1 coding | ±1 coding |
| --- | --- | --- |
| Intercept | 126.80, the control cell | 147.83, the **grand mean** |
| β_A | 14.04, gym effect at diary = 0 | 10.905, **half** the main effect |
| β_B | 20.24, diary effect at gym = 0 | 14.005, half the main effect |
| β_AB | 15.54 | 3.885, a quarter of the interaction |

Under ±1 coding, 2 × β_A = **21.81**, the main effect, straight out of the regression with no correction. That is the property worth having: the coefficients become orthogonal contrasts, so each one keeps its meaning whether or not the others are in the model. Under 0/1 coding they do not, which is why β₁ moved when the interaction was added.

The scaling catches people out. The interaction coefficient under ±1 is a **quarter** of the 0/1 one, not a half, because both factors get rescaled. Multiply by 4 to compare: 4 × 3.885 = 15.54.

## 3. Higher-order designs

#### Example 9.2: Higher-order designs

In addition to the gym and learning diary treatment, we also conducted an experiment that varied the length of sleep by reminding students to go to bed one hour earlier. Same 1000 students, now with `D_sleep` as well.

### 3.1 Setup and main effects

With three factors there are 2³ = **8** cells:

| Y | Gym | Diary | Sleep |
| --- | --- | --- | --- |
| y₁ | No | No | No |
| y₂ | No | No | Yes |
| y₃ | No | Yes | No |
| y₄ | No | Yes | Yes |
| y₅ | Yes | No | No |
| y₆ | Yes | No | Yes |
| y₇ | Yes | Yes | No |
| y₈ | Yes | Yes | Yes |

The main effects use the mean values of the outcome in the respective groups, four cells against four:

> Gym: (y₅ + y₆ + y₇ + y₈)/4 − (y₁ + y₂ + y₃ + y₄)/4
>
> Diary: (y₃ + y₄ + y₇ + y₈)/4 − (y₁ + y₂ + y₅ + y₆)/4
>
> Sleep: (y₂ + y₄ + y₆ + y₈)/4 − (y₁ + y₃ + y₅ + y₇)/4

Each one splits the eight cells down the middle along its own factor, which is the same operation as the 2 × 2 case with four cells per side instead of two.

```r
df_factorial %>%
  group_by(D_gym, D_diary, D_sleep) %>%
  summarize(Y = mean(Y))
```

| D_gym | D_diary | D_sleep | Y |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 115.7 |
| 0 | 0 | 1 | 137.9 |
| 0 | 1 | 0 | 127.2 |
| 0 | 1 | 1 | 166.8 |
| 1 | 0 | 0 | 124.3 |
| 1 | 0 | 1 | 157.4 |
| 1 | 1 | 0 | 154.3 |
| 1 | 1 | 1 | 199.0 |

Giving main effects of **21.81** for gym, **28.01** for diary and **34.91** for sleep. The first two are unchanged from the 2 × 2 analysis, which is what balance buys you: adding a third factor does not disturb the first two when every combination is equally represented.

### 3.2 The cube plot

A graphical way to illustrate these means is a cube plot: the eight cell means at the eight corners of a cube, with each axis one factor. Edges connect cells that differ in exactly one treatment, so the length of an edge is that treatment's effect holding the other two fixed, and comparing parallel edges is reading an interaction off the picture.

### 3.3 Estimating the full model

The best way to implement this design in a regression framework is:

> Y = β₀ + Aβ₁ + Bβ₂ + Cβ₃ + A × Bβ₄ + A × Cβ₅ + B × Cβ₆ + A × B × Cβ₇ + u

where A, B and C are indicator variables for the respective treatments and the others are interaction terms. Here it is very important to always estimate the **full/long model** and not omit some interaction terms (Muralidharan, Romero and Wüthrich 2025).

```r
summary(lm(Y ~ D_diary * D_gym * D_sleep, data = df_factorial))
```

```
Coefficients:
                       Estimate Std. Error t value Pr(>|t|)
(Intercept)             115.680      1.833  63.101  < 2e-16 ***
D_diary                  11.560      2.593   4.459 9.18e-06 ***
D_gym                     8.600      2.593   3.317 0.000943 ***
D_sleep                  22.240      2.593   8.578  < 2e-16 ***
D_diary:D_gym            18.440      3.667   5.029 5.84e-07 ***
D_diary:D_sleep          17.360      3.667   4.735 2.51e-06 ***
D_gym:D_sleep            10.880      3.667   2.967 0.003075 **
D_diary:D_gym:D_sleep    -5.800      5.185  -1.119 0.263597
```

Eight cells, eight coefficients, again an exact re-parameterisation.

**Why the full model matters.** The three two-way interactions are all significant and sizeable, 18.44, 17.36 and 10.88 against main-effect coefficients of 8 to 22. Drop them and their content does not disappear, it gets absorbed into the terms that remain, so the surviving coefficients stop estimating what their names say. The `R ~ A * B * C` syntax expands to the full set automatically, which is why the slide writes it that way rather than listing terms.

The three-way interaction here is **not** significant, p = 0.26. That is a result about this dataset, not a licence to drop it: the Muralidharan et al. argument is that the specification should be decided by the design, not by which terms happen to clear a threshold. Dropping a term because its p-value is large is a model selection step, and it invalidates the inference on everything left in the model.

> Note the cost of going further. A 2ᵏ design has 2ᵏ cells and 2ᵏ coefficients, so a fourth factor means 16 cells, and the per-cell sample size halves each time a factor is added. With 1000 students that is 125 per cell at k = 3 and 62 at k = 4. The standard errors in the table above are already noticeably larger than in the 2 × 2 version, 2.59 against 2.44 on the main terms and 5.19 on the triple interaction, which is why the highest-order term is usually the first one to come out insignificant.

---

## Key terms

| Term | Meaning |
| --- | --- |
| Factorial design | design measuring the response at every combination of factor levels |
| Factor | a treatment that can be on or off, independently of the others |
| Cell | one combination of factor levels, e.g. gym yes and diary no |
| Main effect ME(A) | average effect of A, averaging over the levels of the other factors |
| Simple effect | effect of A at one fixed level of the other factor, e.g. y₃ − y₁ |
| Interaction INT(A, B) | ME(A\|B+) − ME(A\|B−), a difference of differences, symmetric in A and B |
| 0/1 coding | indicator coding; with an interaction present, β₁ is a simple effect, not ME(A) |
| ±1 coding | effect coding; intercept is the grand mean and 2β₁ is ME(A) |
| Balanced design | equal n in every cell, which makes the one-factor-at-a-time means agree with the cell averages |
| 2ᵏ design | k binary factors, 2ᵏ cells, 2ᵏ coefficients in the full model |
| Full/long model | every main effect and every interaction up to order k |
| Cube plot | the eight means of a 2³ design drawn at the corners of a cube |

## References

From the slides:

- Muralidharan, Karthik, Mauricio Romero and Kaspar Wüthrich (2025). Factorial Designs, Model Selection, and (Incorrect) Inference in Randomized Experiments. _Review of Economics and Statistics_ 107(3): 589–604.

My additions:

- The ME(A) = β₁ + β₃/2 identity in section 2.8 and the coding comparison in section 2.9, both checked numerically against the dataset in [the notebook](exercises.ipynb).
