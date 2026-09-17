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

def block_ra(blocks: Iterable, prob: float = 0.5, seed: int | None = None) -> np.ndarray:
    s = pd.Series(blocks).astype("category")
    z = np.zeros(len(s), dtype=int); rng = np.random.default_rng(seed)
    for lvl in s.cat.categories:
        mask = (s == lvl).to_numpy(); n = int(mask.sum())
        n_t = int(round(n * prob))
        idx_local = rng.choice(np.flatnonzero(mask), size=n_t, replace=False)
        z[idx_local] = 1
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
    
    
# ==========
# Lecture 2 
# ==========

df_math = pd.read_csv(os.path.join(DATA_DIR, "lecture2_math.csv"))

## Relationship between two categorical variables: cross table ----

ct_counts = pd.crosstab(df_math["gender"], df_math["class_rating"])
print("\n[L2] Cross-tab counts:\n", ct_counts)

ct_perc_all = crosstab_with_perc(df_math, "gender", "class_rating", margin="all")
print("\n[L2] Cross-tab % (all):\n", ct_perc_all)

## Relationship between categorical and numeric variable: Graphical way  ---- 
plt.figure()
for g, sub in df_math.groupby("gender", dropna=False):
    x = np.full(len(sub), {"male":0, "female":1}.get(str(g), 0))
    plt.scatter(x, sub["math_points"], alpha=0.8, label=str(g))
plt.xticks([0,1], ["male","female"])
plt.xlabel("gender"); plt.ylabel("math_points")
plt.title("math_points by gender")
plt.tight_layout(); plt.legend(); plt.savefig("outputs/lec2_points_scatter.png"); plt.close()

plt.figure()
df_math.boxplot(column="math_points", by="gender")
plt.suptitle(""); plt.title("math_points by gender"); plt.xlabel("gender"); plt.ylabel("math_points")
plt.tight_layout(); plt.savefig("outputs/lec2_points_boxplot.png"); plt.close()

## Relationship between categorical and numeric variable: Numeric way  ---- 

print("\n[L2] Mean by gender:\n",
      df_math.groupby("gender", dropna=False)["math_points"].mean().reset_index(name="math_points_mean"))

## Relationship between two numeric variables: scatter plot ----

plt.figure()
plt.scatter(df_math["gym_visits"], df_math["math_points"], s=30)
plt.xlabel("gym_visits"); plt.ylabel("math_points"); plt.title("gym_visits vs math_points")
plt.tight_layout(); plt.savefig("outputs/lec2_gym_vs_points.png"); plt.close()

df_gdp_life = pd.read_csv(os.path.join(DATA_DIR, "lecture2_gdp_life_expectancy.csv"))
plt.figure()
plt.scatter(df_gdp_life["gdppc"], df_gdp_life["life_expectancy"], s=40)
plt.ylabel("Life expectenacy at birth"); plt.xlabel("GDP per capita (in 1000 USD)")
plt.title("GDP vs Life Expectancy")
plt.tight_layout(); plt.savefig("outputs/lec2_gdp_life.png"); plt.close()


# ==========
# Lecture 7 
# ==========

df_experimental = pd.read_csv(os.path.join(DATA_DIR, "lecture5_experimental_data.csv"))

print("\n[L7] Group means/vars:\n",
      df_experimental.groupby("D").agg(Y_mean=("Y","mean"), Y_var=("Y","var")).reset_index())

print("\n[L7] OLS summary:\n", smf.ols("Y ~ D", data=df_experimental).fit().summary())

print("\n[L7] Manual calc 10/sqrt(583./4+1050/4):", 10/np.sqrt(583./4+1050/4))

t_eq = stats.ttest_ind(
    df_experimental.loc[df_experimental["D"]==1, "Y"],
    df_experimental.loc[df_experimental["D"]==0, "Y"],
    equal_var=True
)
print("\n[L7] t.test equal var:", t_eq)


# ==========
# Lecture 8 
# ==========

df_work = pd.read_csv(os.path.join(DATA_DIR, "lecture8_income_work_effort.csv"))
mean_all = float(df_work["work_effort"].mean())

fig, ax = plt.subplots()
x = df_work["work_order"].astype(int)
x_j = jitter_series(x, width=0.2)
ax.scatter(x_j, df_work["work_effort"], s=40, alpha=0.85)
ax.axhline(mean_all, linestyle="dashed")
ax.set_xticks([1,2,3]); ax.set_xticklabels(["Low","Medium","High"])
ax.set_ylabel("Work Effort"); ax.set_xlabel("Income"); ax.set_title("Work Effort by Income (jitter)")
grp_means = df_work.groupby("work_order")["work_effort"].mean()
ax.scatter(grp_means.index.values, grp_means.values, s=250, color="black", marker="_")
fig.tight_layout(); fig.savefig("outputs/lec8_work_jitter.png"); plt.close(fig)


# =========
# Lecture 9 
# =========

df_factorial = pd.read_csv(os.path.join(DATA_DIR, "lecture9_academic_performance.csv"))

## 2 by 2 design: Estimating main effects ----

print("\n[L9] 2x2 cell means:\n",
      df_factorial.groupby(["D_gym","D_diary"])["Y"].mean().reset_index(name="Y_mean"))


# Let us calculate the exact values of the four subgroups and then repeat the 
# calculations on slide 7. 

# a) Mean calculation

y1 = df_factorial.loc[(df_factorial.D_gym==0) & (df_factorial.D_diary==0), "Y"].mean()
y2 = df_factorial.loc[(df_factorial.D_gym==0) & (df_factorial.D_diary==1), "Y"].mean()
y3 = df_factorial.loc[(df_factorial.D_gym==1) & (df_factorial.D_diary==0), "Y"].mean()
y4 = df_factorial.loc[(df_factorial.D_gym==1) & (df_factorial.D_diary==1), "Y"].mean()

# b) Effect of exercising treatment (D_gym)
gym_eff_1 = (y3+y4)/2-(y1+y2)/2
gym_eff_2 = df_factorial.loc[df_factorial.D_gym==1, "Y"].mean() - df_factorial.loc[df_factorial.D_gym==0, "Y"].mean()
print("\n[L9] Gym effect (two ways):", gym_eff_1, gym_eff_2)
# Result: the calculations on the lines above are identical. 

# c) Effect of learning diary treatment (D_diary)

diary_eff_1 = (y2+y4)/2-(y1+y3)/2
diary_eff_2 = df_factorial.loc[df_factorial.D_diary==1, "Y"].mean() - df_factorial.loc[df_factorial.D_diary==0, "Y"].mean()
print("[L9] Diary effect (two ways):", diary_eff_1, diary_eff_2)
# Result: the calculations on the lines above are identical. 

# d) Output as on slide 8
print("\n[L9] Mean by D_gym:\n",
      df_factorial.groupby("D_gym")["Y"].mean().reset_index(name="Y_mean"))
print("\n[L9] Mean by D_diary:\n",
      df_factorial.groupby("D_diary")["Y"].mean().reset_index(name="Y_mean"))

## 2 by 2 design: Graphical illustration 1 ----

def _summ(df, key):
    tmp = df.groupby(key).agg(Y_mean=("Y","mean"), Y_sd=("Y","std"), nobs=("Y","size")).reset_index()
    tmp["Y_se"] = tmp["Y_sd"]/np.sqrt(tmp["nobs"])
    tmp["Y_min"] = tmp["Y_mean"] - 1.96*tmp["Y_se"]
    tmp["Y_max"] = tmp["Y_mean"] + 1.96*tmp["Y_se"]
    return tmp

df_groups_gym = _summ(df_factorial, "D_gym")
df_groups_diary = _summ(df_factorial, "D_diary")

fig, ax = plt.subplots()
ax.plot(df_groups_gym["D_gym"], df_groups_gym["Y_mean"], marker="o")
ax.set_xticks([0,1]); ax.set_xlabel("Exercising treatment"); ax.set_ylabel("Math points")
fig.tight_layout(); fig.savefig("outputs/lec9_lines_gym.png"); plt.close(fig)

fig, ax = plt.subplots()
ax.plot(df_groups_diary["D_diary"], df_groups_diary["Y_mean"], marker="o")
ax.set_xticks([0,1]); ax.set_xlabel("Diary treatment"); ax.set_ylabel("Math points")
fig.tight_layout(); fig.savefig("outputs/lec9_lines_diary.png"); plt.close(fig)

## 2 by 2 design: Graphical illustration 2 ----

fig, ax = plt.subplots()
yerr = np.vstack((df_groups_gym["Y_mean"]-df_groups_gym["Y_min"], df_groups_gym["Y_max"]-df_groups_gym["Y_mean"]))
ax.errorbar(df_groups_gym["D_gym"].astype(str), df_groups_gym["Y_mean"], yerr=yerr, fmt="o", capsize=6)
ax.set_xlabel("Exercising treatment"); ax.set_ylabel("Math points")
fig.tight_layout(); fig.savefig("outputs/lec9_err_gym.png"); plt.close(fig)

fig, ax = plt.subplots()
yerr = np.vstack((df_groups_diary["Y_mean"]-df_groups_diary["Y_min"], df_groups_diary["Y_max"]-df_groups_diary["Y_mean"]))
ax.errorbar(df_groups_diary["D_diary"].astype(str), df_groups_diary["Y_mean"], yerr=yerr, fmt="o", capsize=6)
ax.set_xlabel("Diary treatment"); ax.set_ylabel("Math points")
fig.tight_layout(); fig.savefig("outputs/lec9_err_diary.png"); plt.close(fig)

## 2 by 2 design: regression

results_factorial = smf.ols("Y ~ D_diary*D_gym", data=df_factorial).fit()
print("\n[L9] OLS 2x2 with interaction:\n", results_factorial.summary())
coef_plot(results_factorial, "2x2 OLS", "outputs/lec9_coef_2x2.png")

## Higher-order designs ----

df_cut = df_factorial.groupby(["D_gym","D_diary","D_sleep"])["Y"].mean().reset_index()
results_factorial_cut = smf.ols("Y ~ D_diary*D_gym*D_sleep", data=df_cut).fit()
print("\n[L9] 3-way on aggregated means:\n", results_factorial_cut.summary())

results_factorial_full = smf.ols("Y ~ D_diary*D_gym*D_sleep", data=df_factorial).fit()
print("\n[L9] 3-way on full data:\n", results_factorial_full.summary())
coef_plot(results_factorial_full, "3-way OLS", "outputs/lec9_coef_3way.png")

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
d3 = df_factorial.groupby(["D_gym","D_diary","D_sleep"])["Y"].mean().reset_index()
sc = ax.scatter(d3["D_gym"], d3["D_diary"], d3["D_sleep"], s=80, c=d3["Y"], cmap="viridis")
for _, r in d3.iterrows():
    ax.text(r["D_gym"], r["D_diary"], r["D_sleep"], f'{r["Y"]:.1f}')
ax.set_xlabel("D_gym"); ax.set_ylabel("D_diary"); ax.set_zlabel("D_sleep")
ax.set_title("Cube Plot (mean Y)")
fig.tight_layout(); fig.savefig("outputs/lec9_cube_plot.png"); plt.close(fig)


results_factorial = smf.ols("Y ~ D_diary*D_gym*D_sleep", data=df_factorial).fit()
print("\n[L9] 3-way on aggregated means:\n", results_factorial.summary())


# ==========
# Lecture 11 
# ==========

## Power analysis ----

analysis = TTestIndPower()
n_per_group = analysis.solve_power(effect_size=0.10, power=0.80, alpha=0.05, ratio=1.0, alternative="two-sided")
print(f"\n[L11] Required n per group (d=0.10, power=0.80, alpha=0.05): {math.ceil(n_per_group)}")

## Types of randomizations ----

df = pd.DataFrame({"id": np.arange(1, 1000+1), "gender": np.array(["male"]*500 + ["female"]*500)})

np.random.seed(1234)  # demo; functions also accept seed
df["treatment"] = simple_ra(N=1000, prob=0.5, seed=1234)
print("[L11] sum(simple_ra):", int(df["treatment"].sum()))

df["treatment"] = complete_ra(N=1000, prob=0.5, seed=1234)
print("[L11] sum(complete_ra):", int(df["treatment"].sum()))

df["treatment"] = block_ra(df["gender"], prob=0.5, seed=1234)
print("\n[L11] block_ra crosstab:\n", pd.crosstab(df["gender"], df["treatment"]))
