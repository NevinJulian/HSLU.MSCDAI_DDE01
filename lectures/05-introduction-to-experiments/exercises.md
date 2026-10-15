# Lecture 5: Exercises

[Back to notes](notes.md) · [Notebook](exercises.ipynb)

> The solutions below are my own, checked against the official `Design of Experiments - Exercise Solutions.html`. All four exercises are conceptual, there is no code to run. The [notebook](exercises.ipynb) works through the potential outcome example from the lecture instead.

---

## Exercise 5.1: Five scientific studies

Based on what you can infer from the abstracts, to what extent does each study fulfil the criteria for an experiment? If it does, what type?

The two criteria from the lecture: the treatment is **assigned by the researcher**, and there is a **control group**.

### Solution

| # | Topic | Experiment? | Type | The giveaway in the abstract |
| --- | --- | --- | --- | --- |
| 1 | Wealth tax rates and declared wealth | **No** | observational, natural experiment | "Exploiting rich intranational variation", "**quasi-randomly** assigned differential tax reforms". The cantons changed their own tax rates. The authors found the variation, they did not create it. |
| 2 | Working-memory training in schools | **Yes** | **field experiment** | "a **randomized** educational intervention with 6–7-year-old children", carried out inside regular school teaching |
| 3 | Monetary payments and Covid-19 vaccination | **Yes** | **field experiment** | "large preregistered **randomized controlled trial**" with 8,286 participants, linked to administrative vaccination records |
| 4 | Altruistic punishment and cooperation | **Yes** | **laboratory experiment** | "Here we show **experimentally**", cooperation "flourishes if altruistic punishment is possible, and breaks down if it is ruled out". The abstract gives no detail on participants or setting, which is itself typical of an abstract lab game. |
| 5 | Platform convergence in US and French elections | **No** | observational | a dataset of websites and manifestos, analysed with an **RDD**. No intervention at all. |

### Points worth noting

- **1 and 5 are the interesting ones.** Both use a design that gets close to an experiment without being one. Study 1 calls its variation "quasi-random", study 5 compares candidates who **narrowly** qualified against those who narrowly failed. Both exploit something that looks like a coin flip in the world. That is the natural experiment family, and it is a separate HSLU course.
- **The word "randomized" is the tell**, but read what is randomized. In study 3 it is the payment, in study 2 the training. In study 1 the word "quasi" does the opposite job.
- **4 is lab rather than field**, but the abstract is thin. The reasoning is indirect: the task is an abstract cooperation game with punishment that is "costly and yields no material gain", which is a designed game rather than something encountered in everyday life. The official solution reaches the same conclusion by the same route.
- **Field versus lab is about the setting, not the sample size.** Study 2 has children in their own classrooms, study 3 uses a real vaccination decision with administrative follow-up. Both are field.
- Study 3 also quantifies the result in a way worth remembering: payments of 24 US dollars raised vaccination by **4.2 percentage points** from a baseline of **71.6%**. This is example 5.4 on the slides.

The papers, for reference:

| # | Paper |
| --- | --- |
| 1 | Brülhart, Gruber, Krapf and Schmidheiny, Behavioral Responses to Wealth Taxes: Evidence from Switzerland |
| 2 | Berger, Fehr, Hermes, Schunk and Winkel, The Impact of Working-Memory Training on Children's Cognitive and Noncognitive Skills |
| 3 | Campos-Mercade et al. (2021), Monetary incentives increase COVID-19 vaccinations, _Science_ |
| 4 | Fehr and Gächter (2002), Altruistic punishment in humans, _Nature_ |
| 5 | Di Tella, Kotti, Le Pennec and Pons (2023), Keep Your Enemies Closer: Strategic Platform Adjustments during US and French Elections, NBER WP 31503 |

---

## Exercise 5.2: The effectiveness of parachutes

A parody in the _British Medical Journal_ questioned whether parachutes are effective in preventing death under severe "gravitational challenge", pointing out that no randomized trial has ever assigned parachutes to skydivers. Why is it reasonable to believe parachutes work anyway?

### Solution

Because the effect is **enormous and uniform**. Almost nobody survives a jump from altitude without a parachute, and almost everybody survives with one. A difference that large cannot be produced by selection, since there is no plausible confounder that separates the two groups so completely.

The lecture 4 language makes it precise. For confounding to explain the pattern, some variable Z would have to:

- determine almost perfectly who jumps with a parachute, and
- determine almost perfectly who survives,

and do both in the same direction with essentially no exceptions. No candidate exists. The pattern also holds across every characteristic you could condition on: income, intelligence, body size, age, training. A confounder that survives all of those stratifications is not a realistic object.

### Points worth noting

- **The real argument is the effect size relative to the plausible bias.** Randomization matters most when the effect is small and the selection is strong, which is the normal case in social science. Beta-carotene (lecture 4) moved lung cancer risk by 18%, which is well inside what confounding can produce. Parachutes move survival from near 0 to near 1.
- **There is also a mechanism**, and it is understood, measurable and testable without any human jumping: terminal velocity with and without drag. Causal claims get stronger when the effect and the mechanism point the same way.
- **The parody has a real target.** The original BMJ paper (Smith and Pell 2003) was arguing against the reflex that nothing counts as evidence without an RCT. A [2018 follow-up](https://blogs.bmj.com/bmj/2018/12/13/we-jumped-from-planes-without-parachutes-and-lived-to-tell-the-tale/) actually ran the trial, randomizing volunteers to jump with a parachute or an empty backpack, from aircraft **parked on the ground**. No injuries in either arm. The joke is a lesson in external validity: a perfectly executed randomized trial on the wrong population answers nothing.
- **The lesson is not "RCTs are unnecessary".** It is that the value of randomization depends on how much bias is plausible. Where that is near zero, observation is enough. Where it is large, as in schooling and earnings in lecture 4, it is not.

---

## Exercise 5.3: Experimental design I

The management of your company is thinking about introducing free coffee and free lunch sandwiches for all employees. The company has many offices. Design an experiment to assess the effect on employee morale. Do you worry about spillovers, and can you do anything about them?

### Solution

**Design.** Randomize at the **office level**, not the employee level. Draw a random subset of offices to receive free coffee and sandwiches for a fixed period, leave the rest unchanged, and measure morale in both before and after.

| Element | Choice |
| --- | --- |
| Unit of randomization | office |
| Treatment | free coffee and lunch sandwiches for everyone in the office |
| Control | no change |
| Outcome | morale, from a short survey run in all offices, plus something behavioural such as turnover or absence days |
| Timing | measure the outcome before and after, so each office is its own baseline |

**Yes, spillovers are the main worry**, and they are exactly why the randomization is at office level. If you gave free lunch to half the people in one office:

- untreated colleagues would hear about it, and some would be given a sandwich by a treated colleague
- others would be annoyed at being left out, which pushes their morale **down** and inflates the measured difference

Randomizing whole offices means the people who interact daily share the same treatment status. Employees in different offices have little contact, so the no-interference part of SUTVA is plausible.

### Points worth noting

- **This is the standard answer and it has a price.** The effective sample size is the number of **offices**, not the number of employees. With 20 offices you have 20 independent units, however many people work in them. That is a real loss of power (lecture 11).
- **Morale is self-reported, so the Hawthorne effect is live.** People who know they are in a study about free lunch will answer the morale question differently. Mitigation: run the survey as a routine HR survey rather than announcing a study, and add a hard outcome such as retention.
- **The John Henry effect runs the other way.** Control offices that find out about the treated ones may react, which here would mean lower morale out of resentment rather than extra effort. Either way the comparison is contaminated. Geographic separation helps, a company-wide announcement would ruin it.
- **Balance check first.** With only a handful of offices, a single draw can easily put all the large or all the head-office sites in one group. Stratify by office size and country before randomizing (lectures 6 and 11).
- **An alternative when the number of offices is small:** stagger the rollout. Every office gets the perk eventually, in a randomized order, and the offices not yet treated serve as controls. Easier to sell internally, since nobody is permanently excluded.

---

## Exercise 5.4: Experimental design II

You are asked to help design a website for the admission office. Experts came up with several competing ideas of what it should look like. Your task is to evaluate them. How would you design an experiment?

### Solution

**A/B test.** Randomly assign each visitor to one of the designs when they arrive, and compare the outcome across variants.

| Element | Choice |
| --- | --- |
| Unit of randomization | visitor, held fixed by a cookie so a returning visitor always sees the same design |
| Treatment | the competing designs, one per arm |
| Outcome | something the admission office actually cares about: started applications, completed applications, requests for information. Time on page and clicks are weaker proxies. |
| Evaluation | the outcome from application data, plus an optional feedback form |

With more than two candidate designs this is an A/B/n test. The randomization logic does not change, but the number of comparisons does, and testing many variants against one control inflates the chance of a false positive. That correction is lecture 8.

### Points worth noting

- **Define the outcome before launching.** A design can raise clicks and lower completed applications. The admission office wants applications, so that is the metric, and the Bing example in the notes makes the same point about balancing revenue against user experience.
- **Run for whole weeks.** Weekday and weekend visitors differ, and application traffic is seasonal around deadlines. Stopping as soon as a result looks good is one of the most common ways to produce a false positive.
- **Spillovers are mild but not zero** in the version where applicants talk to each other or share links, and a shared link must not hand the recipient a different design than the sender saw.
- **External validity caveat:** the winning design is the best one for the people who already visit the site. It says nothing about people who never arrive.
- **The real argument for A/B testing here** is the one from the Bing example: experts disagree, and prior judgement about which design will perform is unreliable. The test is cheap, so run it rather than argue.
