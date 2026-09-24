# Lecture 2: Exercises

[Back to notes](notes.md)

> The solutions below are my own. All numbers come from `lecture2_math.csv` and `lecture2_gdp_life_expectancy.csv`. Check them against the official `Design of Experiments - Exercise Solutions.html`.

Setup, with paths relative to `coding_tasks/` like the course R files:

```r
library(tidyverse)
library(janitor)

df_math <- read_csv("Data/Out_Data/lecture2_math.csv")
df_gdp_life_expectancy <- read_csv("Data/Out_Data/lecture2_gdp_life_expectancy.csv")
```

---

## Exercise 2.1: Determinants of academic performance

You are interested in the determinants of academic performance.

1. What would be an example of a study that examines the impact of exercising on academic performance using cross-sectional data?
2. The same using time-series data?
3. The same using panel data?
4. Load `lecture2_math.csv`. Is there a difference in the number of countries visited in the last 12 months (`countries`) between men and women (`gender`)?
5. What is the drawback of using a scatter plot in the example above? What does it hide?
6. Does the number of gym visits in the last month (`gym_visits`) differ by gender?
7. Look at a scatter plot of `countries` and `math_points`. What do you observe?
8. Look at a scatter plot of `gym_visits` and `math_points`. What do you conclude?

### Solution 1–3: study designs

| #   | Data type       | Example study                                                                                                                                              | Variation used                                           |
| --- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | Cross-sectional | Survey all students of one course once, at the end of the semester: gym visits in the last month and exam points. `df_math` is exactly this.               | differences between students                             |
| 2   | Time-series     | Follow one student over many weeks: training hours and quiz score per week. Or one university over many years: average gym use and average grade per year. | changes within one unit over time                        |
| 3   | Panel           | Follow all students of a cohort over several semesters: gym visits per semester (from gym access logs) and credits or grades per semester.                 | both, between students and within each student over time |

- **Cross-section:** students who exercise more may differ in many other ways (discipline, free time, health).
- **Time-series:** there is only one unit, and many other things change over time too (exam periods, holidays, season).
- **Panel:** comparing each student with herself removes stable differences between students, such as ability. Differences that change over time, such as a new side job, remain.

### Solution 4: countries visited by gender

```r
df_math %>%
  group_by(gender) %>%
  summarize(countries_mean = mean(countries))
```

```
# A tibble: 2 × 2
  gender countries_mean
  <chr>           <dbl>
1 female           4.29
2 male             3.59
```

- Women visited 4.29 countries on average, men 3.59. That is a difference of 0.7 countries. The medians point the same way (4 vs. 3).
- The difference is small compared with the spread inside each group. Both groups range from 0 to 10 countries, with a standard deviation of about 2.9.
- Whether 0.7 countries is more than chance needs a statistical test (lecture 7).

```r
ggplot(data = df_math, aes(x = gender, y = countries)) +
  geom_point() +
  theme_bw()
```

### Solution 5: drawback of the scatter plot

Both variables are discrete. `gender` has two values and `countries` only whole numbers from 0 to 10. Many students share the same combination, so their points lie **exactly on top of each other**. The plot shows at most 11 dots per gender for 45 women and 41 men.

It hides **how many students are behind each dot**, and with that the whole distribution:

```r
df_math %>% tabyl(countries, gender)
```

| countries | female | male |
| --------- | ------ | ---- |
| 0         | 3      | 7    |
| 1         | 7      | 6    |
| 2         | 4      | 6    |
| 3         | 8      | 2    |
| 4         | 2      | 5    |
| 5         | 5      | 2    |
| 6         | 3      | 8    |
| 7         | 6      | 0    |
| 8         | 3      | 2    |
| 9         | 3      | 1    |
| 10        | 1      | 2    |

In the scatter plot, 7 men with 0 countries and 3 women with 0 countries both show up as a single dot. The plot also shows no summary such as a mean or median.

Ways around it:

- **Jitter:** move the points slightly sideways so they no longer overlap. Only horizontally (`height = 0`), so the values of `countries` stay exact. `set.seed()` makes the random shift reproducible.
- **Box plot:** shows median, quartiles and range per group.
- **Count table:** `tabyl(countries, gender)` as above gives the exact numbers.

```r
set.seed(1234)
ggplot(data = df_math, aes(x = gender, y = countries)) +
  geom_jitter(width = 0.2, height = 0) +
  theme_bw()

ggplot(data = df_math, aes(x = gender, y = countries)) +
  geom_boxplot() +
  theme_bw()
```

### Solution 6: gym visits by gender

```r
df_math %>%
  group_by(gender) %>%
  summarize(gym_visits_mean = mean(gym_visits))
```

```
# A tibble: 2 × 2
  gender gym_visits_mean
  <chr>            <dbl>
1 female            9.76
2 male              6.44
```

- Women went to the gym 9.8 times on average in the last month, men 6.4 times. The medians differ even more: 10 vs. 4.
- 14 of 41 men (34%) did not go at all, compared with 9 of 45 women (20%). This pile at zero pulls the male median down.
- Same caveat as in part 4: both groups spread widely (0 to 25 visits). Whether the gap is more than chance is a question for lecture 7.

```r
ggplot(data = df_math, aes(x = gender, y = gym_visits)) +
  geom_boxplot() +
  theme_bw()
```

### Solution 7: countries and math points

```r
ggplot(data = df_math, aes(x = countries, y = math_points)) +
  geom_point() +
  theme_bw()
```

- **No clear pattern.** For almost every number of countries, math points spread over a wide range. Students with 0 countries, for example, score anywhere between 59 and 165.
- The correlation is 0.13, close to zero. Correlation is not part of this lecture, it only backs up the visual impression.
- The points form columns at 0, 1, …, 10 because `countries` is discrete.

### Solution 8: gym visits and math points

```r
ggplot(data = df_math, aes(x = gym_visits, y = math_points)) +
  geom_point() +
  theme_bw() +
  labs(x = "Number of gym visits", y = "Math points")
```

- **Strong positive relationship, close to linear.** The correlation is 0.94.
- The 23 students without a gym visit score between 56 and 94 points. The 7 students with 20 or more visits score between 158 and 175.
- **What I conclude:** gym visits and math points are strongly **associated**. I cannot conclude that exercise **causes** better math results. Students choose to go to the gym, and whatever makes them go (discipline, time management, health) could also raise their points.

```mermaid
flowchart LR
    D["gym_visits"] -->|"+ ?"| Y["math_points"]
    U(("discipline,<br/>time management")) -.-> D
    U -.-> Y
```

This is why Cappelen et al. (2026) randomized the gym membership (notes, section 7).

### Points worth noting

- **Parts 4 and 6 compare means only.** A difference in means says nothing about how much the groups overlap. Report the spread too (range, standard deviation, box plot).
- **Gender and gym visits are linked.** Women go to the gym more (part 6), and gym visits go together with more math points (part 8). Part of the 16-point gender gap in math points (notes, section 4.3) could therefore run through gym visits. In a regression with both variables, the gender gap shrinks from 15.6 to 2.9 points. Regression is not part of this lecture, this is a preview of confounding in lecture 4.
- The exercise says "last 12 months", the survey question on slide 4 says "during the last year". Same thing.

---

## Exercise 2.2: GDP and life expectancy

Load `lecture2_gdp_life_expectancy.csv`. It contains the same data as the scatter plot of GDP per capita and life expectancy in the lecture.

1. How many variables and how many observations are in the dataset?
2. Classify each variable into a variable type.
3. Calculate the mean of `gdppc` and `life_expectancy` per region. What do you observe?
4. Create a graph of the relationship between `gdppc` and `life_expectancy` at the regional level (as calculated in 3). Do you observe a similar pattern as for all countries? Is the pattern linear?
5. How do you interpret your results in 4?

### Solution 1: size of the dataset

```r
df_gdp_life_expectancy %>% glimpse()
```

```
Rows: 192
Columns: 8
$ country         <chr> "Afghanistan", "Albania", "Algeria", "Andorra", …
$ iso3c           <chr> "AFG", "ALB", "DZA", "AND", …
$ region          <chr> "South Asia", "Europe & Central Asia", "Middle East & North Africa", …
$ capital         <chr> "Kabul", "Tirane", "Algiers", "Andorra la Vella", …
$ longitude       <dbl> 69.17610, 19.81720, 3.05097, 1.52180, …
$ latitude        <dbl> 34.52280, 41.33170, 36.73970, 42.50750, …
$ gdppc           <dbl> 0.4137579, 8.5751713, 5.3640280, 46.8124484, …
$ life_expectancy <dbl> 66.03500, 79.60200, 76.26100, 84.04100, …
```

(output shortened)

**192 observations (countries) and 8 variables.** `dim(df_gdp_life_expectancy)` gives the same in one line: `[1] 192   8`.

### Solution 2: variable types

| Variable          | R type | Variable type                               | Scale    |
| ----------------- | ------ | ------------------------------------------- | -------- |
| `country`         | chr    | regular categorical                         | nominal  |
| `iso3c`           | chr    | regular categorical (3-letter country code) | nominal  |
| `region`          | chr    | regular categorical                         | nominal  |
| `capital`         | chr    | regular categorical                         | nominal  |
| `longitude`       | dbl    | continuous                                  | interval |
| `latitude`        | dbl    | continuous                                  | interval |
| `gdppc`           | dbl    | continuous                                  | ratio    |
| `life_expectancy` | dbl    | continuous                                  | ratio    |

- The R type is a hint, not the answer. `chr` does not automatically mean categorical, and `dbl` does not automatically mean continuous. A count stored as `dbl` is still discrete. The type follows from what the variable measures.
- **Longitude and latitude are interval, not ratio.** Their zero (Greenwich meridian, equator) is a reference line, not the absence of something, and values can be negative. 20° E is not "twice as far east" as 10° E in any useful sense.
- **GDP per capita and life expectancy** have a real zero, so ratios make sense. A country with 40,000 USD has twice the GDP per capita of one with 20,000 USD.
- **Missing values:** `capital` is empty for 5 countries, `longitude` and `latitude` for 4. `gdppc` and `life_expectancy` are complete, which is why `mean()` in part 3 works without `na.rm = TRUE`.

### Solution 3: means per region

```r
df_gdp_life_expectancy %>%
  group_by(region) %>%
  summarize(gdppc_mean = mean(gdppc),
            life_expectancy_mean = mean(life_expectancy),
            no_countries = n())
```

```
# A tibble: 7 × 4
  region                     gdppc_mean life_expectancy_mean no_countries
  <chr>                           <dbl>                <dbl>        <int>
1 East Asia & Pacific             18.2                  73.6           31
2 Europe & Central Asia           34.8                  78.6           52
3 Latin America & Caribbean       17.3                  75.0           34
4 Middle East & North Africa      19.5                  76.7           20
5 North America                   89.7                  80.8            3
6 South Asia                       3.55                 72.8            8
7 Sub-Saharan Africa               2.65                 64.7           44
```

`no_countries` is `<int>` because `n()` returns a whole-number count.

- **GDP per capita differs enormously:** 2,650 USD in Sub-Saharan Africa vs. 89,700 USD in North America, a factor of about 34.
- **Life expectancy differs much less:** 64.7 years in Sub-Saharan Africa vs. 80.8 in North America, 16 years apart. The ranking mostly follows GDP.
- **The ranking is not perfect.** East Asia & Pacific has a slightly higher mean GDP than Latin America & Caribbean (18.2 vs. 17.3) but a lower life expectancy (73.6 vs. 75.0). South Asia is almost as poor as Sub-Saharan Africa but lives 8 years longer.
- **A few rich countries pull the means up.** In East Asia & Pacific the mean GDP is 18.2, the median only 6.3. Singapore, Macao, Australia and Hong Kong lift the mean.
- **North America has only 3 countries:** Bermuda (132.6), the United States (82.3) and Canada (54.2). Bermuda alone pushes the mean above the US value.
- **Each country counts equally**, whatever its population. In South Asia, the Maldives weigh as much as India.

### Solution 4: regional graph

Save the collapsed data first, then plot it:

```r
gdp_coll <- df_gdp_life_expectancy %>%
  group_by(region) %>%
  summarize(gdppc_mean = mean(gdppc),
            life_expectancy_mean = mean(life_expectancy),
            no_countries = n())

ggplot(data = gdp_coll, aes(x = gdppc_mean, y = life_expectancy_mean)) +
  geom_point(size = 2) +
  theme_bw() +
  xlab("GDP per capita (in 1000 USD)") + ylab("Life expectancy")
```

Or pipe straight into `ggplot()` without saving an object:

```r
df_gdp_life_expectancy %>%
  group_by(region) %>%
  summarize(gdppc_mean = mean(gdppc),
            life_expectancy_mean = mean(life_expectancy)) %>%
  ggplot(aes(x = gdppc_mean, y = life_expectancy_mean)) +
  geom_point() +
  theme_bw()
```

The seven points, sorted by GDP per capita:

| Region                     | GDP per capita (1000 USD) | Life expectancy |
| -------------------------- | ------------------------- | --------------- |
| Sub-Saharan Africa         | 2.65                      | 64.7            |
| South Asia                 | 3.55                      | 72.8            |
| Latin America & Caribbean  | 17.3                      | 75.0            |
| East Asia & Pacific        | 18.2                      | 73.6            |
| Middle East & North Africa | 19.5                      | 76.7            |
| Europe & Central Asia      | 34.8                      | 78.6            |
| North America              | 89.7                      | 80.8            |

- **Similar pattern as for all countries:** yes. Life expectancy rises steeply at low GDP and flattens at high GDP.
- **Linear:** no. From Sub-Saharan Africa to South Asia, +0.9 thousand USD goes with +8.1 years. From Europe & Central Asia to North America, +55 thousand USD goes with +2.2 years. A straight line cannot have both slopes.

### Solution 5: interpretation

- The regional averages show the same concave relationship as the countries: **diminishing returns**. Extra income goes with large gains in life expectancy where people are poor and with small gains where they are rich. The explanation from the notes applies: basics like food, water and vaccines first, biological limits later.
- **The evidence is thin.** There are only seven points. The steep part is a single step (Sub-Saharan Africa to South Asia), and the flat end is a single point (North America: 3 countries, one of them Bermuda).
- **Aggregation hides variation.** Every region contains poor and rich countries. Life expectancy in East Asia & Pacific ranges from 62 to 85 years. A pattern between region averages does not automatically hold between countries. Here it does, because the country-level plot shows the same shape.
- **No causal statement.** The slopes describe the curve, they are not the effect of income. The 8-year gap between South Asia and Sub-Saharan Africa is hardly explained by 900 USD of income alone. Other regional differences (disease burden, health systems) play a role.

### Points worth noting

- In `Design of Experiments - Exercises.R`, Exercise 2.2 plots `gdp_coll` before it is created and uses `x=gdppc`, which the collapsed data does not contain. Running the file top to bottom stops there. Run the `gdp_coll <- ...` block first and plot `gdppc_mean`.
- The official solution only calls longitude and latitude continuous. The interval classification in part 2 is my addition.
