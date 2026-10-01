# Lecture 3: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own. Non-random numbers come from `lecture3_survey.csv`. R numbers for the random draws are from the official `Design of Experiments - Exercise Solutions.html` (`set.seed(1234)`), Python numbers from [exercises.ipynb](exercises.ipynb). Random draws differ between R and Python, so the two never match exactly.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)
library(janitor)
library(randomizr)

df <- read_csv("Data/Out_Data/lecture3_survey.csv")
```

---

## Exercise 3.1: Sampling strategies

A statistics student wants to study the relationship between the time students spend on social networking sites and their performance at school. For each strategy, name the sampling method and the bias you would expect.

a) He randomly samples 40 students from the study's population, gives them the survey, asks them to fill it out and bring it back the next day.
b) He gives out the survey only to his friends, making sure each one of them fills out the survey.
c) He posts a link to an online survey on Facebook and asks his friends to fill out the survey.
d) He randomly samples five classes and asks a random sample of students from those classes to fill out the survey.

### Solution

| | Method | Probability sample? | Expected bias |
| --- | --- | --- | --- |
| a | simple random sample | yes | none from the selection. Risk of **nonresponse**: students who do not bring the survey back the next day might differ (less organised, more time online, weaker grades). |
| b | **convenience sample** (close to anecdotal evidence) | no | his friends resemble him: similar programme, habits and grades. The sample describes his circle, not the student population. Making sure all friends answer removes nonresponse, but not the bias in who was asked. |
| c | **voluntary response** on top of a convenience sample | no | only Facebook friends see the link, and only those who want to click answer. Everyone in the sample uses at least one social network, so students with zero or very little use are missing. Heavy users see the post first. |
| d | **multistage sample** (clusters = classes, then a simple random sample inside) | yes | unbiased if the classes are representative. With only five classes the result depends a lot on which classes were drawn. Classes are often homogeneous (same year, same subject), so five classes might all be first-years. Unbiased, but imprecise. |

**Ranking from best to worst:** a, d, c, b. a and d are probability samples. a is more precise for the same number of students, d is cheaper to run. b and c are not probability samples, so no statement about all students is possible.

### Points worth noting

- **c is worse than it looks for this question.** The study wants the relationship between social network time (X) and performance (Y). If almost no one with low X is in the sample, the relationship can only be seen in a narrow range of X.
- **a can be fixed cheaply:** let the students fill out the survey on the spot, or follow up with those who did not return it.
- **d and the weights:** if the classes differ in size and he samples the same number of students per class, students in small classes have a higher chance to be included. Weighting fixes this (notes, section 3.2).
- **Even a perfect sample gives an association, not a causal effect.** Weak grades could cause more time online (procrastination), and a third factor such as motivation could drive both. That is lecture 4.
- The official solution speaks of the size of the students' "network". The exercise is about time spent on social networking sites. The sampling methods are the same in both readings.

---

## Exercise 3.2: Survey on referendum preferences

You want to estimate the overall support for a referendum on measures against climate change. The dataset `lecture3_survey.csv` contains a population of 100,000 individuals.

1. What is the mean support in the population?
2. Draw a simple random sample of 1,000 individuals with `simple_ra(N = N, prob = 0.01)` from `randomizr`. What is the mean in your sample?
3. A friend has a list of car drivers (`car`). Take a random sample of 1,000 of them and calculate the mean support. What do you observe?
4. Take a clustered sample of 20 municipalities with `sample(unique(df$municipality), size = 20)`. Calculate the mean support. How does it compare to (2)?
5. Generate a sample stratified by car: split the data into car owners and non-owners, draw a random sample in each, combine them with `bind_rows` and calculate the mean support. How does it compare to the population?

### The data

| Variable | Content |
| --- | --- |
| `id` | person id, 1 to 100,000 |
| `gender` | female / male |
| `car` | Yes / No |
| `municipality` | id 1 to 2,000, 50 people per municipality on average |
| `party` | SP, SVP, Mitte, FDP |
| `support` | 1 = supports the referendum, 0 = not |

Support differs strongly by group. This explains parts 3 and 5:

```r
df %>% group_by(car) %>% summarize(support = mean(support), n = n())
```

```
# A tibble: 2 × 3
  car   support     n
  <chr>   <dbl> <int>
1 No      0.724 50018
2 Yes     0.472 49982
```

| Group | Support |
| --- | --- |
| no car / car | 72.4% / 47.2% |
| female / male | 78.7% / 41.0% |
| SP / Mitte / FDP / SVP | 77.3% / 66.1% / 54.3% / 41.9% |

### Solution 1: population mean

```r
mean(df$support)
```

```
[1] 0.5984
```

**59.8%** of the population support the referendum. This is the parameter that the samples in parts 2 to 5 try to estimate. Usually it is unknown, here we know it because the whole population is in the file.

### Solution 2: simple random sample

```r
set.seed(1234)
N <- nrow(df)
df$sample <- simple_ra(N = N, prob = 0.01)
df %>% tabyl(sample)
mean(df$support[df$sample == 1])
```

```
 sample     n percent
      0 99003 0.99003
      1   997 0.00997

[1] 0.5917753
```

| | n | Mean support |
| --- | --- | --- |
| R (official) | 997 | 0.592 |
| Python (notebook) | 975 | 0.620 |
| Population | 100,000 | 0.598 |

- `simple_ra` flips a coin with probability 1% for each person. The sample size is therefore about 1,000, not exactly 1,000 (997 in R). `complete_ra` would give exactly 1,000 (lecture 11).
- Both estimates are close to 59.8%. They differ from it and from each other by **chance only**. The standard error of a share with n = 1,000 is √(0.598 × 0.402 / 1000) ≈ 0.015, so about 95% of all random samples land between 0.567 and 0.629.

### Solution 3: car drivers only

```r
df_car <- df %>% filter(car == "Yes")

set.seed(1234)
df_car <- df_car %>%
  mutate(sample = simple_ra(N = nrow(df_car), prob = 1000 / nrow(df_car)))

mean(df_car$support[df_car$sample == 1])
```

| | n | Mean support |
| --- | --- | --- |
| R (official, `prob = 0.01`) | about 500 | 0.460 |
| Python (notebook, `prob = 1000 / 49982`) | 971 | 0.469 |
| All 49,982 car drivers | 49,982 | 0.472 |
| Population | 100,000 | 0.598 |

- **The estimate is about 13 percentage points too low**, and the majority flips: the sample says the referendum fails, the population says it passes.
- This is **sampling bias** through the sampling frame. The list only contains car drivers, and car drivers support climate measures much less (47% vs. 72%).
- **A larger sample does not help.** Even asking all 49,982 car drivers gives 47.2%. The sample is a perfect estimate of the wrong population. This is the Literary Digest mistake from 1936 (notes, section 5): a list of car and telephone owners, 2.4 million answers, wrong winner.
- In the notebook, 2,000 repeated samples of car drivers all land between about 0.42 and 0.52. Not a single one is near 0.598.

### Solution 4: cluster sample of 20 municipalities

```r
set.seed(1234)
sampled_clusters <- sample(unique(df$municipality), size = 20)

df_cluster <- df %>%
  filter(municipality %in% sampled_clusters)

mean(df_cluster$support)
```

```
[1] 0.6164773
```

| | n | Mean support |
| --- | --- | --- |
| R (official) | about 1,000 | 0.616 |
| Python (notebook) | 1,006 | 0.608 |
| Simple random sample (part 2, R) | 997 | 0.592 |
| Population | 100,000 | 0.598 |

- 20 municipalities with about 50 people each give about 1,000 people, the same size as in part 2.
- The estimate is close to the population mean, slightly further away than the simple random sample in R. With one draw each, this difference is noise. Both are within two standard errors.
- **Why the cluster sample works so well here:** the municipalities hardly differ. The spread of the 2,000 municipality means (SD 0.069) is exactly what pure chance produces with 50 people per municipality (0.069). The clusters are small copies of the population, the ideal case from the slides. In the notebook simulation the cluster sample is as precise as the simple random sample (SE 0.015 both).
- **In reality this would not hold.** Swiss votes on climate policy show a strong split between cities and the countryside. If municipalities differ, 20 clusters can by chance contain too many rural or too many urban ones. The estimate stays unbiased but becomes less precise than a simple random sample of 1,000 people.

### Solution 5: stratified by car

```r
set.seed(1234)

df_nocar <- df %>%
  filter(car == "No") %>%
  mutate(sample = simple_ra(N = nrow(.), prob = 0.01))

df_car <- df %>%
  filter(car == "Yes") %>%
  mutate(sample = simple_ra(N = nrow(.), prob = 0.01))

df_stratified <- df_car %>%
  bind_rows(df_nocar) %>%
  filter(sample == 1)

mean(df_stratified$support)
mean(df$support)
```

| | n | Mean support |
| --- | --- | --- |
| R (official) | about 1,000 | 0.613 |
| Python (notebook) | 954 (469 car, 485 no car) | 0.610 |
| Population | 100,000 | 0.598 |

- Close to the population, about one standard error above it. Again, a single draw says little.
- **Same rate in both strata (1%)**, so this is a **proportional** stratified sample: car drivers make up 50% of the population and about 50% of the sample. No weights are needed. If you took 500 from each group and the groups were not equally large, you would have to weight (notes, section 3.2).
- **Difference to part 3:** part 3 only sampled from one stratum. Here every stratum is sampled, so car drivers are represented with their correct share.
- **What stratification buys:** precision, not unbiasedness (the simple random sample is already unbiased). It helps more the more the strata differ in the outcome. Car drivers and non-drivers differ (47% vs. 72%), so the standard error falls slightly, from 0.0153 to 0.0151 in the simulation. Stratifying by gender (79% vs. 41%) would reduce it to 0.0141.

### Comparison of all designs: 2,000 samples each (notebook)

| Design | Mean of 2,000 estimates | Bias | Standard error |
| --- | --- | --- | --- |
| simple random, n = 1,000 | 0.598 | 0.000 | 0.0153 |
| car drivers only, n = 1,000 | 0.472 | −0.126 | 0.0157 |
| 20 municipalities | 0.598 | 0.000 | 0.0150 |
| stratified by car, n = 1,000 | 0.599 | 0.000 | 0.0151 |
| stratified by gender, n = 1,000 | 0.598 | −0.001 | 0.0141 |

- Bias is a property of the **design**: it shows up as the whole distribution being shifted. Only the car driver list is biased.
- The standard error is about the same for all designs here. The size of the sample, not the design, drives it.

### Points worth noting

- **File and coding on the slides:** the slide calls the file `lecture3_sampling.csv` and says car drivers have the value 1. The file is `lecture3_survey.csv` and `car` is `"Yes"` / `"No"`.
- **Part 3 in the official solution** uses `prob = 0.01` among car drivers. That draws about 500 people, not 1,000. The bias is the same, the precision lower. `prob = 1000 / nrow(df_car)` gives 1,000.
- **`Design of Experiments - Exercises.R`** uses `N` in part 2 without defining it. Add `N <- nrow(df)` (the official solution uses `dim(df)[1]`, the same thing). It also hard-codes `N = 50018` and `N = 49982` in part 5. `nrow(.)` inside `mutate` avoids typing the numbers.
- **`Design of Experiments - Exercises.py`** uses `rng` in part 4, but `rng` only exists inside the helper functions. The script stops with a `NameError` there. Define `rng = np.random.default_rng(1234)` at the top, as in the notebook.
- **`set.seed`:** without it, every run gives a new sample and new numbers. With it, the "random" draw is reproducible. The official solution sets it before every part.
- **Reading R output:** `[1] 0.5917753` is a vector of length 1, the `[1]` is the index of the first element. `tabyl` prints counts `n` and shares `percent` (0.00997 = 0.997%).
