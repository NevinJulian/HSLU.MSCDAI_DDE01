import os
import math
import warnings
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.power import TTestIndPower
import pyreadr


# ---- Set paths and make folder for output ----

os.chdir(r"C:\Schmidlu\Dropbox\_Uni Luzern\Lehre\Design of Experiments")
print("cwd:", os.getcwd())
DATA_DIR = os.path.join("C:/Schmidlu/Dropbox/_Uni Luzern/Lehre/Design of Experiments", "Data", "Out_Data")
os.makedirs("outputs", exist_ok=True)

# ---- Functions ----

def simple_ra(N: int, prob: float = 0.5, seed: int = None) -> np.ndarray:
    if not (0 <= prob <= 1):
        raise ValueError("prob must be in [0,1]")
    rng = np.random.default_rng(seed)
    return (rng.random(N) < prob).astype(int)

def complete_ra(N: int, prob: float = 0.5, seed: int = None) -> np.ndarray:
    if not (0 <= prob <= 1):
        raise ValueError("prob must be in [0,1]")
    rng = np.random.default_rng(seed)  # THIS MAKES IT REPRODUCIBLE    
    n_t = int(round(N * prob))
    idx = rng.choice(N, size=n_t, replace=False)    
    z = np.zeros(N, dtype=int)
    z[idx] = 1
    return z

def strata_rs(strata: Iterable, prob: float = 0.5, seed: int = None) -> np.ndarray:
    strata = pd.Series(strata).astype("category")
    z = np.zeros(len(strata), dtype=int)
    rng = np.random.default_rng(seed)
    for lvl in strata.cat.categories:
        mask = strata == lvl
        z[mask.values] = simple_ra(mask.sum(), prob, seed=seed)
    return z

def fit_ols_clustered(formula: str, data: pd.DataFrame, cluster: Optional[pd.Series] = None):
    mod = smf.ols(formula, data=data)
    if cluster is None:
        return mod.fit()
    return mod.fit(cov_type="cluster", cov_kwds={"groups": cluster})

def fit_logit_clustered(formula: str, data: pd.DataFrame, cluster: Optional[pd.Series] = None):
    mod = smf.logit(formula, data=data)
    res = mod.fit(disp=False, method="lbfgs")
    if cluster is not None:
        res = res.get_robustcov_results(cov_type="cluster", groups=cluster)
    return res

def jitter_series(y: pd.Series, width: float = 0.2) -> np.ndarray:
    return y.to_numpy() + rng.uniform(-width, width, size=y.shape[0])

def coef_plot(result, title: str, outfile: str, zero_at: float = 0.0):
    coefs = result.params.copy(); ses = result.bse
    if "Intercept" in coefs.index:
        coefs = coefs.drop("Intercept"); ses = ses.drop("Intercept")
    ci_low = coefs - 1.96 * ses; ci_high = coefs + 1.96 * ses
    order = np.argsort(coefs.values)
    labels = coefs.index.values[order]; vals = coefs.values[order]
    low = ci_low.values[order]; high = ci_high.values[order]
    plt.figure()
    y = np.arange(len(vals))
    plt.hlines(y, low, high); plt.plot(vals, y, "o"); plt.axvline(zero_at, linestyle="--")
    plt.yticks(y, labels); plt.title(title); plt.xlabel("Coefficient (95% CI)")
    plt.tight_layout(); plt.savefig(outfile); plt.close()

def crosstab_with_perc(df: pd.DataFrame, row: str, col: str, margin: str = "all") -> pd.DataFrame:
    ct = pd.crosstab(df[row], df[col], dropna=False)
    if margin == "all":
        denom = ct.values.sum()
        perc = ct / denom if denom else ct
    elif margin == "row":
        perc = ct.div(ct.sum(axis=1).replace(0, np.nan), axis=0)
    elif margin == "col":
        perc = ct.div(ct.sum(axis=0).replace(0, np.nan), axis=1)
    else:
        raise ValueError("margin must be one of {'all','row','col'}")
    return (perc * 100).round(1)

def build_balance_table(df: pd.DataFrame, treat_col: str, vars_to_test: list[str]) -> pd.DataFrame:
    rows = []
    for v in vars_to_test:
        g = df.groupby(treat_col)[v]
        est1 = g.mean().get(1, np.nan); est0 = g.mean().get(0, np.nan)
        t_res = stats.ttest_ind(
            df.loc[df[treat_col] == 1, v].astype(float),
            df.loc[df[treat_col] == 0, v].astype(float),
            equal_var=False, nan_policy="omit",
        )
        rows.append({"variable": v, "mean_treated": est1, "mean_control": est0, "p_value": t_res.pvalue})
    return pd.DataFrame(rows)

def interaction_line_plot(x_levels, trace_levels, cell_means, xlab: str, trace_label: str, ylab: str, outfile: str):
    plt.figure()
    for t in trace_levels:
        plt.plot(x_levels, [cell_means[(x, t)] for x in x_levels], marker="o", label=str(t))
    plt.xlabel(xlab); plt.ylabel(ylab); plt.legend(title=trace_label, loc="best")
    plt.tight_layout(); plt.savefig(outfile); plt.close()

# ===================================================
# Exercise 2.1 — Determinants of academic performance
# ===================================================

df_math = pd.read_csv(os.path.join(DATA_DIR, "lecture2_math.csv"))
print(df_math.groupby("gender", dropna=False)["countries"].mean())

plt.figure()
for g, sub in df_math.groupby("gender", dropna=False):
    plt.scatter([g] * len(sub), sub["countries"])
plt.tight_layout(); plt.savefig("outputs/e2_1_countries_scatter.png"); plt.close()

df_math.boxplot(column="countries", by="gender"); plt.suptitle(""); plt.title("")
plt.tight_layout(); plt.savefig("outputs/e2_1_countries_box.png"); plt.close()

genders = ["female", "male"]
plt.figure()
for i, g in enumerate(genders):
    sub = df_math[df_math["gender"] == g]
    x = np.full(len(sub), i)
    plt.scatter(jitter_series(pd.Series(x), 0.2), sub["countries"])
plt.xticks(ticks=range(len(genders)), labels=genders)
plt.tight_layout(); plt.savefig("outputs/e2_1_countries_jitter.png"); plt.close()


print(df_math.groupby("gender", dropna=False)["gym_visits"].mean())
df_math.boxplot(column="gym_visits", by="gender"); plt.suptitle(""); plt.title("")
plt.tight_layout(); plt.savefig("outputs/e2_1_gym_box.png"); plt.close()

plt.figure(); plt.scatter(df_math["countries"], df_math["math_points"])
plt.xlabel("countries"); plt.ylabel("math_points")
plt.tight_layout(); plt.savefig("outputs/e2_1_countries_vs_math.png"); plt.close()

plt.figure(); plt.scatter(df_math["gym_visits"], df_math["math_points"])
plt.xlabel("Number of gym visits"); plt.ylabel("Math points")
plt.tight_layout(); plt.savefig("outputs/e2_1_gym_vs_math.png"); plt.close()

# =======================================
# Exercise 2.2 — GDP and life expectancy
# ======================================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture2_gdp_life_expectancy.csv"))
print(df.info())

plt.figure(); plt.scatter(df["gdppc"], df["life_expectancy"])
plt.xlabel("gdppc"); plt.ylabel("life_expectancy")
plt.tight_layout(); plt.savefig("outputs/e2_2_raw_scatter.png"); plt.close()

gdp_coll = df.groupby("region", dropna=False).agg(
    gdppc_mean=("gdppc", "mean"),
    life_expectancy_mean=("life_expectancy", "mean"),
    no_countries=("region", "size"),
).reset_index()
print(gdp_coll)

plt.figure(); plt.scatter(gdp_coll["gdppc_mean"], gdp_coll["life_expectancy_mean"])
plt.xlabel("GDP per capita"); plt.ylabel("Life expectancy")
plt.tight_layout(); plt.savefig("outputs/e2_2_region_means.png"); plt.close()

# ===============================================
# Exercise 3.2 — Survey on referendum preferences
# ===============================================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture3_survey.csv"))
print(df["support"].mean())

N = len(df)
df["sample"] = simple_ra(N=N, prob=0.01, seed=1234)
print(df["sample"].value_counts(dropna=False))
print(df.loc[df["sample"] == 1, "support"].mean())

# Note: This number differ from the R solution of 0.5917 because Python samples
#       different individuals. 

df_car = df[df["car"] == "Yes"].copy()
df_car["sample"] = simple_ra(N=len(df_car), prob=0.01)
print(df_car.loc[df_car["sample"] == 1, "support"].mean())

sampled_clusters = rng.choice(df["municipality"].unique(), size=20, replace=False)
df_cluster = df[df["municipality"].isin(sampled_clusters)]
print(df_cluster["support"].mean())

df_nocar = df[df["car"] == "No"].copy()
df_car2 = df[df["car"] == "Yes"].copy()
df_nocar["sample"] = simple_ra(N=len(df_nocar), prob=0.01)
df_car2["sample"] = simple_ra(N=len(df_car2), prob=0.01)
df_strat = pd.concat([df_car2, df_nocar], ignore_index=True)
df_strat = df_strat[df_strat["sample"] == 1]
print(df_strat["support"].mean()); print(df["support"].mean())

# ===========================================
# Exercise 4.2 — Threats to internal validity
# ===========================================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture4_schooling_earnings.csv"))
plt.figure(); plt.scatter(df["years_schooling"], df["earnings"])
plt.xlabel("years_schooling"); plt.ylabel("earnings")
plt.tight_layout(); plt.savefig("outputs/e4_2_scatter.png"); plt.close()

res1 = smf.ols("earnings ~ years_schooling", data=df).fit()
print(res1.summary())

res2 = smf.ols("earnings ~ years_schooling + motivation", data=df).fit()
print(res2.summary())

# ===============================
# Exercise 6.1 — Causal estimands
# ===============================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture6_exercising.csv"))
df["ICE"] = df["Y1"] - df["Y0"]
ate = df["Y1"].mean() -df["Y0"].mean() 
print(ate)

att = df.loc[df["D"] == 1, "Y1"].mean() - df.loc[df["D"] == 1, "Y0"].mean()
print(att)

sel_bias = df.loc[df["D"] == 1, "Y0"].mean() - df.loc[df["D"] == 0, "Y0"].mean()
print(sel_bias)

# ============================
# Exercise 6.2 — Balance tests
# ============================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture6_balance_table.csv"))
t_res = stats.ttest_ind(
    df.loc[df["treatment"] == 1, "X1"].astype(float),
    df.loc[df["treatment"] == 0, "X1"].astype(float),
    equal_var=False, nan_policy="omit",
)
print("X1 treated mean:", df.loc[df["treatment"] == 1, "X1"].mean())
print("X1 control mean:", df.loc[df["treatment"] == 0, "X1"].mean())
print("p-value of t-test:", t_res.pvalue)

cols = list(df.columns)
candidate_vars = cols[2 : min(2 + 50, len(cols))]
balance_out = build_balance_table(df, "treatment", candidate_vars)
print(balance_out[balance_out["p_value"] < 0.1]); 
print(balance_out[balance_out["p_value"] < 0.05])
len(balance_out[balance_out["p_value"] < 0.1]) / len(balance_out)
len(balance_out[balance_out["p_value"] < 0.05]) / len(balance_out)


bal.to_csv("outputs/e6_2_balance.csv", index=False)

# ================================
# Exercise 7.2 — Working from home
# ================================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture7_working_from_home.csv"))
print(df["attrite_perc"].drop_duplicates())

df_out = df.groupby("treat")["attrite_perc"].mean().rename("attrition_mean").reset_index()
print(df_out)
print(smf.ols("attrite_perc ~ treat", data=df).fit().summary())
print(smf.ols("attrite_perc ~ treat", data=df[df["role"] == 1]).fit().summary())
print(smf.ols("attrite_perc ~ treat", data=df[df["role"] == 0]).fit().summary())


# ==========================
# Exercise 8.2 — Pain relief
# ==========================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture8_painstudy.csv"))

trt_labels = ["Treatment A", "Treatment B", "Treatment C"]
unique_trts = df["trt"].unique()

plt.figure()

for trt in unique_trts:
    sub = df[df["trt"] == trt]
    x_val = list(unique_trts).index(trt)
    x = np.full(len(sub), x_val)
    plt.scatter(jitter_series(pd.Series(x), 0.2), sub["pain"], alpha=0.7, s=20)
    plt.scatter([x_val], [sub["pain"].mean()], marker="_", s=80)

plt.xticks(ticks=range(len(trt_labels)), labels=trt_labels)
plt.ylabel("Pain Score")
plt.title("Pain Scores by Treatment Group")
plt.tight_layout()
plt.savefig("outputs/e8_2_jitter_mean.png")
plt.close()
plt.savefig("outputs/e8_2_jitter_mean.png"); plt.close()

print(df.groupby("trt")["pain"].mean())

aov_res = smf.ols("pain ~ C(trt)", data=df).fit()
print(anova_lm(aov_res, typ=2))
for pair in [("A","B"),("A","C"),("B","C")]:
    a = df[df["trt"]==pair[0]]["pain"]; b = df[df["trt"]==pair[1]]["pain"]
    print(pair, stats.ttest_ind(a, b, equal_var=False, nan_policy="omit"))

# ==========================
# Exercise 9.1 — Weight loss
# ===========================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture9_weight_loss.csv"))
def _diff_y(col): return df.loc[df[col]==1,"y"].mean() - df.loc[df[col]==-1,"y"].mean()
print(_diff_y("A"))
print(_diff_y("B")) 
print(_diff_y("C"))

df["A"] = df["A"].astype("category")
df["B"] = df["B"].astype("category")
df["C"] = df["C"].astype("category")

mod = smf.ols("y ~ A*B*C", data=df).fit()
print(mod.summary())

# ==================================
# Exercise 9.2 — Vaccination 2x2 RCT
# ==================================

df = pd.read_csv(os.path.join(DATA_DIR, "lecture9_vaccination.csv"))
print(df.groupby("D_incentive")["Vaccinated"].mean())
print(df.groupby("D_reminder")["Vaccinated"].mean())

res = smf.ols("Vaccinated ~ C(D_incentive)*C(D_reminder)", data=df).fit()
print(res.summary())

x_levels = sorted(df["D_incentive"].unique()); t_levels = sorted(df["D_reminder"].unique())
means = df.groupby(["D_incentive","D_reminder"])["Vaccinated"].mean().to_dict()
interaction_line_plot(x_levels, t_levels, means,
                      xlab="Incentive treatment", trace_label="Reminder treatment",
                      ylab="Vaccinated", outfile="outputs/e9_2_interaction.png")


# ===================================
# Exercise 10.2 — Immigrant admission
# ===================================

path = os.path.join(DATA_DIR, "lecture10_immigration.RData")
rd = pyreadr.read_r(path)
df = rd["df_immigration"]

pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
print(crosstab_with_perc(df, "Language Skills", "Gender"))
print(crosstab_with_perc(df, "Education", "Job"))

df = df.rename(columns=lambda s: str(s).replace(" ", "_"))
for c in ["Gender","Education","Language_Skills","Job","Reason_for_Application"]:
    df[c] = df[c].astype("category")
formula = "Chosen_Immigrant ~ C(Gender) + C(Education) + C(Language_Skills) + C(Job) + C(Reason_for_Application)"
logit_res = fit_logit_clustered(formula, df, cluster=df["CaseID"])
print(logit_res.summary())
coef_plot(logit_res, "AMCE proxy (Immigration conjoint)", "outputs/e10_2_coef_logit.png")


# ===========================================
# Exercise 11.1 — Income and job performance
# ===========================================

power = TTestIndPower()
for target_power in [0.80, 0.90, 0.95]:
    n = power.solve_power(effect_size=0.2, power=target_power, alpha=0.05, alternative="two-sided")
    print(f"n per group for d=0.2, power={target_power}: {math.ceil(n)}")
n = power.solve_power(effect_size=0.2, power=0.80, alpha=0.01, alternative="two-sided")
print(f"n per group for d=0.2, power=0.80, alpha=0.01: {math.ceil(n)}")

df = pd.read_csv(os.path.join(DATA_DIR, "lecture11_income_performance.csv"))
print(smf.ols("Y ~ D", data=df).fit().summary())

# ====================================
# Exercise 11.2 — Ratings and revenues
# ====================================

print("simple_ra:", simple_ra(N=8, prob=0.5, seed=1234))
print("complete_ra:", complete_ra(N=8, prob=0.5, seed=1234))

df = pd.read_csv(os.path.join(DATA_DIR, "lecture11_ratings_revenues.csv"))
df["Z"] = strata_rs(df['High_Quality'], prob=0.5, seed=1234)
print(df["Z"])

