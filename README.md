# Design of Data Experiments

Notes, exercises and code for the module **Design of Data Experiments** at HSLU / University of Lucerne, fall semester 2026.

|                   |                                               |
| ----------------- | --------------------------------------------- |
| Lecturer          | Lukas Schmid                                  |
| Module type       | Compulsory                                    |
| Schedule          | Thursdays, 16:15–17:55                        |
| Format            | Alternating onsite (HSLU) and online (Zoom)   |
| Language for code | R (Python versions of all files are provided) |

## About the module

The first part covers the foundations of data analysis: scientific methods, relationships between variables, sampling and threats to internal validity. The second part is about experiments: which types exist, how to set one up and how to analyse the data it produces. Every lecture is followed by a tutorial with practical exercises.

## Weekly format

| Time        | Part                                                                                          |
| ----------- | --------------------------------------------------------------------------------------------- |
| 16:15–17:00 | Lecture                                                                                       |
| 17:00–17:10 | Break                                                                                         |
| 17:10–17:55 | Tutorial (group work on the exercises, on campus in reserved rooms or in Zoom breakout rooms) |

## Assessment

- Written paper-and-pencil exam at the end of the semester, counts **100%** of the grade
- Covers all lecture and tutorial topics
- No laptop, no smartphone
- Allowed aids: non-programmable, non-communicating calculator and a personal cheat sheet of **4 double-sided A4 pages** (handwritten or printed)
- You must be able to read and interpret **R output** as shown in the lectures and exercises

## Schedule

| #   | Date   | Topic                                 | Mode   | Key topics                                                                                                                                           | Notes                                                                                                       |
| --- | ------ | ------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1   | 17 Sep | Scientific methods                    | onsite | qualitative vs. quantitative research, theory and evidence, causal graphs, experimental methods                                                      | [notes](lectures/01-scientific-methods/notes.md) · [exercises](lectures/01-scientific-methods/exercises.md) |
| 2   | 24 Sep | Relationship between variables        | online | types of variables, levels of measurement, relationships, data types                                                                                 |                                                                                                             |
| 3   | 01 Oct | Sampling                              | online | anecdotal evidence, estimator vs. estimate, sampling techniques, internal and external validity                                                      |                                                                                                             |
| 4   | 08 Oct | Threats to internal validity          | onsite | confounders, reverse causality, functional form, measurement error, placebo, non-compliance, attrition, spillovers, Hawthorne and John Henry effects |                                                                                                             |
| 5   | 15 Oct | Introduction to experiments           | online | experimental vs. observational research, types of experiments, potential outcomes, SUTVA                                                             |                                                                                                             |
| –   | 22 Oct | Self study                            | –      |                                                                                                                                                      |                                                                                                             |
| 6   | 29 Oct | Comparing two treatments I            | onsite | manipulation, causal estimands, randomization, correlation vs. causal effects, balance tests                                                         |                                                                                                             |
| 7   | 05 Nov | Comparing two treatments II           | onsite | treatment effect estimation, statistical inference, errors in hypothesis testing                                                                     |                                                                                                             |
| 8   | 12 Nov | Comparing more than two treatments I  | online | ANOVA, Bonferroni correction                                                                                                                         |                                                                                                             |
| 9   | 19 Nov | Comparing more than two treatments II | online | 2×2 factorial design, higher-order designs                                                                                                           |                                                                                                             |
| 10  | 26 Nov | Conjoint experiments                  | onsite | assumptions, identification, estimation, implementation, interpretation                                                                              |                                                                                                             |
| –   | 03 Dec | Guest lecture                         | online |                                                                                                                                                      |                                                                                                             |
| 11  | 10 Dec | Implementation of an experiment       | onsite | study design, power calculation, ethics application, pre-registration, randomization types, stratification                                           |                                                                                                             |
| 12  | 17 Dec | Questions and answers                 | online |                                                                                                                                                      |                                                                                                             |

## Course material from the lecturer

| File                                              | Content                                                 |
| ------------------------------------------------- | ------------------------------------------------------- |
| `Design of Experiments - Lecture Codes.R`         | All code used in the slides                             |
| `Design of Experiments - Exercises.R`             | Code to solve the exercises                             |
| `Design-of-Experiments---Exercise-Solutions.html` | Exercise solutions with R code, output and explanations |
| `Data.zip`                                        | All datasets for lectures and exercises                 |

Both `.R` files also exist as Python versions.

## Repository structure

```
.
├── README.md
├── lectures/
│   └── 01-scientific-methods/
│       ├── notes.md        # lecture content
│       └── exercises.md    # exercises with own solutions
├── code/                   # R and Python files from the course
└── data/                   # datasets from Data.zip
```

## Setup

Install [R](https://www.r-project.org) and RStudio. Helpful resources listed in the syllabus:

- Peter Büchel, _Prep Course to R and RStudio for MSCIDS_ (script)
- Edureka, _R Programming Tutorial for Beginners_ (video)
- [UCLA Statistical Methods and Data Analytics](https://stats.oarc.ucla.edu/r/) (R help, examples, regression)
- [swirl](https://swirlstats.com), an interactive R package for learning R
