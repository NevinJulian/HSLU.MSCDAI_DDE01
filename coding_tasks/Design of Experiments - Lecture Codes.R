# Load packages and set working directory ----
library(scales)
library(tidyverse)
library(openintro)
library(xtable)
library(grid)
library(gridExtra)
library(RColorBrewer)
library(latex2exp)
library(scidesignR)
library(randomizr)
library(openintro)

try(setwd("C:/SchmidLu/Dropbox/_Uni Luzern/Lehre/Design of Experiments"))

rm(list=ls())

path_overleaf <- "C:/Schmidlu/Dropbox/Apps/Overleaf/Design of Experiments"
data_path <- "./Data/Out_Data/"


# Lecture 2 -----

df_math <- read_csv("Data/Out_Data/lecture2_math.csv")

## Relationship between two categorical variables: cross table ----

library(janitor)

df_math %>% tabyl(gender,class_rating)

df_math %>% 
  tabyl(gender,class_rating) %>% 
  adorn_percentages("all")%>%
  adorn_pct_formatting(digits = 1)

## Relationship between categorical and numeric variable: Graphical way  ---- 

ggplot(data=df_math,aes(x=gender,y=math_points)) + 
  geom_point() + 
  theme_bw(base_size=24)

ggplot(data=df_math,aes(x=gender,y=math_points)) + 
  geom_boxplot() + 
  theme_bw(base_size=24)

## Relationship between categorical and numeric variable: Numeric way  ---- 

df_math %>% 
  group_by(gender) %>%
  summarize(math_points_mean=mean(math_points))


## Relationship between two numeric variables: scatter plot ----

ggplot(data=df_math,aes(x=gym_visits,y=math_points)) + 
  geom_point() + 
  theme_bw(base_size=24)

df_gdp_life_expectancy <- read_csv("Data/Out_Data/lecture2_gdp_life_expectancy.csv")

ggplot(df_gdp_life_expectancy,aes(gdppc,life_expectancy)) +
  geom_point(size=3) +
  ylab("Life expectenacy at birth") + xlab("GDP per capita (in 1000 USD)") + 
  theme_bw(base_size=42) 


# Lecture 7 ----

df_experimental <- read_csv("Data/Out_data/lecture5_experimental_data.csv")

## Classical statistical inference ----

df_experimental %>%
  group_by(D) %>%
  summarize(Y_mean=mean(Y),
            Y_var=var(Y)) 

summary(lm(Y~D,data=df_experimental))

10/sqrt(583./4+1050/4)

t.test(df_experimental$Y[df_experimental$D==1],
       df_experimental$Y[df_experimental$D==0],
       var.equal = TRUE,alternative = "two.sided")



# Lecture 8 ----

df_work <- read_csv("Data/Out_Data/lecture8_income_work_effort.csv")

mean_all <- mean(df_work$work_effort) # overall mean

# Note regarding the graph below: We use geom_jitter instead of geom_point because
# we do not see the number of points when using geom_point. For example, there are 
# four individuals in the low income category with a work effort of 4 but we only
# see a single point. When jittering the data with the arguments height=0 and width=0.2, 
# the graph minimally sets apart the four points on the x-axis (but not on the y-axis
# because height=0)

ggplot(df_work,aes(y=work_effort,x=factor(work_order),colour=factor(work_order)))+
  geom_jitter(width=0.2,height=0.0,size=4)+
  scale_colour_manual(values=c("blue","red","darkgreen") ,guide="none") +
  scale_x_discrete(label=c("Low","Medium","High")) +
  theme_bw(base_size=32) +
  geom_hline(yintercept =mean_all,linetype="dashed") + 
  ylab("Work Effort") + xlab("Income") +
  geom_point(data = df_work %>% 
               group_by(work_order) %>% 
               summarize(work_effort_mean = mean(work_effort)), 
             mapping = aes(y = work_effort_mean, x = work_order), 
             size = 15, color = 'black', shape = '-') 



# Lecture 9 ----

df_factorial <- read_csv("Data/Out_Data/lecture9_academic_performance.csv")

## 2 by 2 design: Estimating main effects ----

df_factorial %>% 
  group_by(D_gym,D_diary) %>%
  summarize(Y_mean=mean(Y)) %>%
  mutate(Y_mean = sprintf("%.1f", Y_mean))

# Let us calculate the exact values of the four subgroups and then repeat the 
# calculations on slide 7. 

# a) Mean calculation

y1 <- mean(df_factorial$Y[df_factorial$D_gym==0 & df_factorial$D_diary==0])
y2 <- mean(df_factorial$Y[df_factorial$D_gym==0 & df_factorial$D_diary==1])
y3 <- mean(df_factorial$Y[df_factorial$D_gym==1 & df_factorial$D_diary==0])
y4 <- mean(df_factorial$Y[df_factorial$D_gym==1 & df_factorial$D_diary==1])

# b) Effect of exercising treatment (D_gym)

(y3+y4)/2-(y1+y2)/2

mean(df_factorial$Y[df_factorial$D_gym==1])-mean(df_factorial$Y[df_factorial$D_gym==0])

# Result: the calculations on the lines above are identical. 

# c) Effect of learning diary treatment (D_diary)

(y2+y4)/2-(y1+y3)/2

mean(df_factorial$Y[df_factorial$D_diary==1])-mean(df_factorial$Y[df_factorial$D_diary==0])

# Result: the calculations on the lines above are identical. 

# d) Output as on slide 8

df_factorial %>% 
  group_by(D_gym) %>%
  summarize(Y_mean=mean(Y))%>%
  mutate(Y_mean = sprintf("%.1f", Y_mean))

df_factorial %>% 
  group_by(D_diary) %>%
  summarize(Y_mean=mean(Y))%>%
  mutate(Y_mean = sprintf("%.1f", Y_mean))

## 2 by 2 design: Graphical illustration 1 ----

df_groups_gym <- df_factorial %>% 
  group_by(D_gym) %>%
  summarize(Y_mean=mean(Y),
            Y_sd=sd(Y),
            nobs=n()) %>%
  mutate(Y_se=Y_sd/sqrt(nobs),
         Y_min=Y_mean-1.96*Y_se,
         Y_max=Y_mean+1.96*Y_se)

df_groups_diary <- df_factorial %>% 
  group_by(D_diary) %>%
  summarize(Y_mean=mean(Y),
            Y_sd=sd(Y),
            nobs=n()) %>%
  mutate(Y_se=Y_sd/sqrt(nobs),
         Y_min=Y_mean-1.96*Y_se,
         Y_max=Y_mean+1.96*Y_se)

g1 <- ggplot(df_groups_gym,aes(y=Y_mean,x=D_gym)) +
  geom_point(size=6) +
  geom_line(linewidth=1.3) +
  theme_bw(base_size=32) +
  scale_x_continuous(breaks=c(0,1),labels=c(0,1)) +
  scale_y_continuous(limits=c(130,160)) +
  xlab("Gym treatment") + ylab("Math points") 

g2 <- ggplot(df_groups_diary,aes(y=Y_mean,x=D_diary)) +
  geom_point(size=6) +
  geom_line(linewidth=1.3) +
  theme_bw(base_size=32) +
  scale_x_continuous(breaks=c(0,1),labels=c(0,1)) +
  scale_y_continuous(limits=c(130,170)) +
  xlab("Diary treatment") + ylab("Math points") 

library(patchwork)
(g1 + g2) +
  plot_layout(guides = "collect") 

## 2 by 2 design: Graphical illustration 2 ----

limits <- aes(ymax = Y_max, ymin=Y_min)

g1 <- ggplot(df_groups_gym,aes(y=Y_mean,x=factor(D_gym))) +
  geom_errorbar(limits, width=0.5,linewidth=1.5) +
  geom_point(size=8) +
  theme_bw(base_size=42)  +
  scale_y_continuous(limits=c(130,170)) +
  xlab("Gym treatment") + ylab("Math points") 

g2 <- ggplot(df_groups_diary,aes(y=Y_mean,x=factor(D_diary))) +
  geom_errorbar(limits, width=0.5,linewidth=1.5) +
  geom_point(size=8) +
  scale_y_continuous(limits=c(130,170)) +
  theme_bw(base_size=42)  +
  xlab("Diary treatment") + ylab("Math points") 

(g1 + g2) +
  plot_layout(guides = "collect") 

## 2 by 2 design: regression and interaction ----

results_factorial = lm(Y ~ D_diary*D_gym, data=df_factorial)
summary(results_factorial)

df_out <- broom::tidy(results_factorial)


ggplot(df_groups,aes(y=Y_mean,x=D_gym,
                     group=factor(D_diary),
                     shape=factor(D_diary))) +
  geom_point(size=6) +
  geom_line(size=1.3) +
  theme_bw(base_size=46) +
  scale_x_continuous(breaks=c(0,1),labels=c(0,1)) +
  scale_y_continuous(limits=c(120,180)) +
  xlab("Exercising treatment") + ylab("Math points")  + 
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())

interaction.plot(df_factorial$D_gym,
                 df_factorial$D_diary,
                 df_factorial$Y, type="l",
                 xlab="Exercising treatment",trace.label="Diary treatment",
                 ylab="Math score")


## Higher-order designs ----

df_cut <- df_factorial %>% 
  group_by(D_gym,D_diary,D_sleep) %>%
  summarize(Y=mean(Y))

results_factorial = lm(Y ~ D_diary*D_gym*D_sleep, data=df_cut)
summary(results_factorial)

FrF2::cubePlot(
  results_factorial,
  eff1 = 'D_gym',
  eff2 = 'D_diary',
  eff3 = 'D_sleep',
  main = "Cube Plot for Academic Performance",
  round = 1,
  cex.title = 1
)

summary(lm(Y ~ D_diary*D_gym*D_sleep, data=df_factorial))

# Lecture 10 ----

## Restaurant and ratings conjoint ----

load("./Data/Out_Data/lecture10_restaurant.RData")

df_conjoint %>% 
  group_by(Name) %>% 
  summarize(mean_choice=mean(choice))

lm.out <- lm(formula = choice ~ factor(Name) + factor(Rating) + factor(Price),
             data = df_conjoint)
summary(lm.out)


library(cjoint)
results <- amce(choice~Name+Rating+Price, data=df_conjoint,
                cluster=TRUE, respondent.id="id")

plot(results, xlab="Change in Pr(Restaurant Visit)",
     ylim=c(-.3,.3), breaks=round(seq(-0.3,0.5,0.1),1),  
     text.size=13, 
     plot.theme = theme_bw(base_size=20) + theme(legend.position = "none")) 

# Lecture 11 ----

## Power analysis ----

library(pwrss)

power.t.student(d = 0.10,
                power = 0.80,
                alpha = 0.05,
                alternative = "two.sided",
                design = "independent")


## Types of randomizations ----

library(randomizr)
library(janitor)

df <- tibble(id=c(1:1000),
             gender=c(rep("male",500),rep("female",500)))

set.seed(1234)
df$treatment <- simple_ra(N = 1000, prob = 0.5)
sum(df$treatment)

set.seed(1234)
df$treatment <- complete_ra(N = 1000, prob = 0.5)
sum(df$treatment)

set.seed(1234)
df$treatment <- block_ra(blocks = df$gender)
df %>% tabyl(gender,treatment)



