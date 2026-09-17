
rm(list=ls())
setwd("C:/Schmidlu/Dropbox/_Uni Luzern/Lehre/Design of Experiments")

data_path <- "./Data/Out_Data/"
options(scipen = 999) # 


library(janitor)
library(tidyverse)


# Exercise 2.1 ----

df_math <- read_csv("Data/Out_Data/lecture2_math.csv")

df_math %>% 
  group_by(gender) %>%
  summarize(countries_mean=mean(countries))

ggplot(data=df_math,aes(x=gender,y=countries)) + 
  geom_point() + 
  theme_bw(base_size=24)

ggplot(data=df_math,aes(x=gender,y=countries)) + 
  geom_jitter(width = 0.2, height=0) + 
  theme_bw(base_size=24)

ggplot(data=df_math,aes(x=gender,y=countries)) + 
  geom_boxplot() + 
  theme_bw(base_size=24)

df_math %>% 
  group_by(gender) %>%
  summarize(gym_visits_mean=mean(gym_visits))

ggplot(data=df_math,aes(x=gender,y=gym_visits)) + 
  geom_boxplot() + 
  theme_bw(base_size=24)

ggplot(data=df_math,aes(x=countries,y=math_points)) + 
  geom_point() + 
  theme_bw(base_size=24)

ggplot(data=df_math,aes(x=gym_visits,y=math_points)) + 
  geom_point() + 
  theme_bw(base_size=24) + 
  labs(x="Number of gym visits",y="Math points")

# Exercise 2.2 ----

df_gdp_life_expectancy <- read_csv("Data/Out_Data/lecture2_gdp_life_expectancy.csv")

df_gdp_life_expectancy %>% 
  glimpse()

ggplot(data=gdp_coll,aes(x=gdppc,y=life_expectancy)) + 
  geom_point(size=2) +
  theme_bw(base_size=12)

gdp_coll <- df_gdp_life_expectancy %>% 
  group_by(region) %>%
  summarize(gdppc_mean=mean(gdppc),
            life_expectancy_mean=mean(life_expectancy),
            no_countries=n()) 

ggplot(data=gdp_coll,aes(x=gdppc_mean,y=life_expectancy_mean)) + 
  geom_point(size=2) +
  theme_bw(base_size=12)+ ylab("Life expectancy") + xlab("GDP per capita")

df_gdp_life_expectancy %>% 
  group_by(region) %>%
  summarize(gdppc_mean=mean(gdppc),
            life_expectancy_mean=mean(life_expectancy),
            no_countries=n()) %>%
  ggplot(aes(x=gdppc_mean,y=life_expectancy_mean)) + 
  geom_point() +
  theme_bw()

# Exercise 3.2  ----

df <- read_csv("Data/Out_Data/lecture3_survey.csv")

mean(df$support)

set.seed(1234)
df$sample <- simple_ra(N = N, prob=0.01)
df %>% tabyl(sample)

mean(df$support[df$sample==1])

df_car <- df %>% 
  filter(car=="Yes") 

df_car <- df_car %>% 
  mutate(sample=simple_ra(N = dim(df_car)[1], prob=0.01 ))

mean(df_car$support[df_car$sample==1])

sampled_clusters <- sample(unique(df$municipality), size = 20)

df_cluster <- df %>% 
  filter(municipality %in% sampled_clusters) 

mean(df_cluster$support)

set.seed(1234)

df_nocar <- df %>% 
  filter(car=="No") %>% 
  mutate(sample=simple_ra(N = 50018, prob=0.01 ))

df_car <- df %>% 
  filter(car=="Yes") %>% 
  mutate(sample=simple_ra(N = 49982, prob=0.01 ))

df_stratified <- df_car %>%
  bind_rows(df_nocar) %>%
  filter(sample==1)

mean(df_stratified$support)
mean(df$support)


# Exercise 4.2  ----

df_schooling <- read_csv("Data/Out_Data/lecture4_schooling_earnings.csv")

ggplot(aes(x=years_schooling,y=earnings),data=df_schooling) + 
  geom_point() +
  theme_bw()

summary(lm(earnings~years_schooling,data=df_schooling))
summary(lm(earnings~years_schooling+motivation,data=df_schooling))


# Exercise 6.1  ----

df_exercising <- read_csv("./Data/Out_Data/lecture6_exercising.csv")

df_exercising$ICE <- df_exercising$Y1-df_exercising$Y0

mean(df_exercising$Y1[df_exercising$D==1])-mean(df_exercising$Y0[df_exercising$D==1])


mean(df_exercising$ICE)
mean(df_exercising$ICE[df_exercising$D==1])

mean(df_exercising$Y0[df_exercising$D==1])-mean(df_exercising$Y0[df_exercising$D==0])


# Exercise 6.2  ----

df_balance <- read_csv("./Data/Out_Data/lecture6_balance_table.csv")

## t-test for X1 

t_test1 <- t.test(X1 ~ treatment, data = df_balance)
print(t_test1)

t_test1$estimate[1]
t_test1$estimate[2]
t_test1$p.value

## balance table using crosstable and flextable

library(crosstable)
library(flextable)
my_table <- crosstable(df_balance %>% select(-id),
                       by="treatment", 
                       test=TRUE, 
                       unique_numeric = 1,
                       funs=c(mean=mean, "std error"=sd)) %>% as_flextable()
print(my_table)


## balance table manual

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
    mean_treated = t_test$estimate[2],  # 2 = treatment == 1
    mean_control = t_test$estimate[1],  # 1 = treatment == 0
    p_value = t_test$p.value
  ))
}

balance_out %>%
  filter(p_value<0.1)

balance_out %>%
  filter(p_value<0.05)


# Exercise 7.2  ----

df_home <- read_csv("Data/Out_Data/lecture7_working_from_home.csv")

df_home %>% distinct(attrite_perc)

df_out <- df_home %>% 
  group_by(treat) %>%
  summarize(attrition_mean=mean(attrite_perc))
print(df_out)

summary(lm(attrite_perc~treat,data=df_home))

summary(lm(attrite_perc~treat,data=df_home %>% filter(role==1)))
summary(lm(attrite_perc~treat,data=df_home %>% filter(role==0)))

library(ggsignif)

ggplot(df_out, aes(x=treat, y=attrition_mean,fill=factor(treat),
                   label=round(attrition_mean,1))) +
  geom_col(width = 1) + 
  geom_text(aes(y=attrition_mean+0.3),size=8) + 
  geom_signif(y_position = c(8.3), xmin = c(0.0), xmax = c(1.0),
    annotation = c("P = 0.0431"), tip_length = 0.1) +
  scale_fill_manual(values = c("#1f4e79", "#e84d22"),
                    breaks=c(0,1),
                    label=c("In-person (control)",
                            "Hybrid WFH (treatment)"))   +
  scale_y_continuous(limits = c(0,9)) + 
  theme_bw(base_size=18) + 
  theme(axis.title.x = element_blank(), 
        axis.text.x = element_blank(), axis.ticks.x = element_blank()) + 
  ylab("Attrition (%)")  + 
  theme(legend.position = "bottom",
        legend.title = element_blank())


  

# Exercise 8.2 ----

painstudy <- read_csv("Data/Out_Data/lecture8_painstudy.csv")

ggplot(painstudy, aes(x = trt, y = pain, color = trt)) +
  geom_jitter(width = 0.2, height=0, size = 2, alpha = 0.7) +
  stat_summary(fun = mean, geom = "point", 
               shape = "-", size = 4, color = "black") +
  theme_bw()

painstudy %>% 
  group_by(trt) %>% 
  summarize(pain_mean=mean(pain))

anova_mod <- aov(pain ~ trt, data = painstudy)
summary(anova_mod)

t.test(pain~trt,data=painstudy %>% filter(trt %in% c("A","B")))
t.test(pain~trt,data=painstudy %>% filter(trt %in% c("A","C")))
t.test(pain~trt,data=painstudy %>% filter(trt %in% c("B","C")))



# Exercise 9.1 ----

wtlossdat <- read_csv("Data/Out_Data/lecture9_weight_loss.csv")

mean(wtlossdat["y"][wtlossdat["A"] == 1]) -
  mean(wtlossdat["y"][wtlossdat["A"] == -1])

mean(wtlossdat["y"][wtlossdat["B"] == 1]) -
  mean(wtlossdat["y"][wtlossdat["B"] == -1])

mean(wtlossdat["y"][wtlossdat["C"] == 1]) -
  mean(wtlossdat["y"][wtlossdat["C"] == -1])

mod <- lm(y ~ factor(A) * factor(B)  * factor(C), data = wtlossdat)
summary(mod)



# Exercise 9.2 ----

df_vaccination <- read_csv("Data/Out_Data/lecture9_vaccination.csv")

df_vaccination %>% 
  group_by(D_incentive) %>%
  summarize(Vaccinated_mean=mean(Vaccinated))

df_vaccination %>% 
  group_by(D_reminder) %>%
  summarize(Vaccinated_mean=mean(Vaccinated))

summary(lm(Vaccinated ~ D_incentive*D_reminder, data=df_vaccination))

interaction.plot(x.factor=df_vaccination$D_incentive,
                 trace.factor=df_vaccination$D_reminder,
                 response=df_vaccination$Vaccinated, type="l",
                 xlab="Incentive treatment",trace.label="Reminder treatment",
                 ylab="Vaccinated")



# Exercise 10.1 ----

load("Data/Out_Data/lecture10_vacuum_cleaner.Rdata")

library(cjoint)
results <- amce(choice~Name+Color+Price, data=df_conjoint,
                cluster=TRUE, respondent.id="id")

plot(results, xlab="Change in Pr(Purchase)",
     ylim=c(-.3,.3), breaks=c(-0.2, 0, 0.2,0.4),  
     text.size=13,
     color="black",
     mex=3) 


# Exercise 10.2 ----

load("./Data/Out_Data/lecture10_immigration.RData")

library(janitor)

df_immigration %>% 
  tabyl(`Language Skills`,Gender) %>% 
  adorn_percentages("all")%>%
  adorn_pct_formatting(digits = 1)

df_immigration %>% 
  tabyl(Education,Job) %>% 
  adorn_percentages("all")%>%
  adorn_pct_formatting(digits = 1)

results <- amce(Chosen_Immigrant ~  Gender + Education + `Language Skills` +
                    +  Job +`Reason for Application` , 
                data=df_immigration,
                cluster=TRUE, 
                respondent.id="CaseID")

plot(results , 
     xlab="Change in Pr(Immigrant Preferred for Admission to U.S.)",
     ylim=c(-.3,.3), 
     breaks=c(-.2, 0, .2), 
     labels=c("-.2","0",".2"), text.size=13) 

plot(results , 
     xlab="Change in Pr(Immigrant Preferred for Admission to U.S.)",
     ylim=c(-.3,.3), 
     breaks=c(-.2, 0, .2), 
     labels=c("-.2","0",".2"), text.size=13, 
     plot.theme = theme_bw()) 


# Exercise 11.1 ----

library(pwrss)

power.t.student(d = 0.2,
                power = 0.80,
                alpha = 0.05,
                alternative = "two.sided",
                design = "independent")

power.t.student(d = 0.2,
                power = 0.9,
                alpha = 0.05,
                alternative = "two.sided",
                design = "independent")

power.t.student(d = 0.2,
                power = 0.95,
                alpha = 0.05,
                alternative = "two.sided",
                design = "independent")

power.t.student(d = 0.2,
                power = 0.80,
                alpha = 0.01,
                alternative = "two.sided",
                design = "independent")

df_experimental <- read_csv("Data/Out_Data/lecture11_income_performance.csv")
summary(lm(Y~D,data=df_experimental))

# Exercise 11.2 ----

set.seed(1234)
simple_ra(N = 8, prob=0.5)
complete_ra(N = 8, prob=0.5)

df_randomization <- read_csv("./Data/Out_Data/lecture11_ratings_revenues.csv")

strata_rs(strata = df_randomization$High_Quality)

