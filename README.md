# Methods

## 1. Epidemic Threshold Computation

To estimate the null (baseline) and alternative (epidemic) proportions of influenza‐like illness (ILI) in the community, we compute weekly per‐person probabilities using ED‐visit data and treatment‐seeking rates. All model parameters are treated as hyperparameters in our `estimate_required_sample_sizes()` function (Appendix A) and the accompanying Shiny app, allowing users to override defaults.

**Parameters:**

* `pop`: Total population of Los Angeles County (LA County).
* `annual_ed_rate`: Annual ED visits per 1,000 people in LA County.
* `non_epi_rate`: Proportion of ED visits due to ILI during non‐epidemic weeks.
* `threshold_rate`: Proportion of ED visits due to ILI at the epidemic threshold.
* `ili_seek_rate`: Percentage of individuals with ILI who seek ED care.
* `alpha`: Significance level (Type I error rate).
* `target_power`: Desired power (1 – Type II error rate).

We derive weekly probabilities *p₀* and *p₁* as follows:

```math
p₀ = \frac{\bigl( pop \times \frac{annual\_ed\_rate}{1000} \bigr) / 52 \times non\_epi\_rate}{ili\_seek\_rate \times pop},
\\
p₁ = \frac{\bigl( pop \times \frac{annual\_ed\_rate}{1000} \bigr) / 52 \times threshold\_rate}{ili\_seek\_rate \times pop}.
```

These compute “normal” vs. “epidemic” weekly ED visits, adjust by care‐seeking probability, and normalize by population.

### Base‐Case Defaults

| Parameter        | Default Value | Source / Notes                          |
| ---------------- | ------------- | --------------------------------------- |
| `pop`            | 9,825,708     | LACDPH (2023)                           |
| `annual_ed_rate` | 322           | CHCF ED Almanac (2023)                  |
| `non_epi_rate`   | 0.0385        | RespWatch mean non‐epidemic (2019–2023) |
| `threshold_rate` | 0.0540        | Mean + 2 SD non‐epidemic rates          |
| `ili_seek_rate`  | 0.019         | Flu Near You: 31.6% × ED subset (\~6%)  |
| `alpha`          | 0.05          | CDC standard                            |
| `target_power`   | 0.90          | CDC standard                            |

<details>
<summary>Footnotes & Data Sources</summary>

1. **Population**: LA County population estimate (July 1, 2023). LACDPH.
2. **Annual ED rate**: 322 visits per 1,000 persons per year. California Health Care Foundation. “Emergency Departments Almanac 2023.”
3. **Baseline & Threshold**: Derived from LA County RespWatch ILI surveillance data (2019–2023). Non‐epi mean (0.016), threshold = mean + 2 SD (\~0.054).
4. **ILI seek rate**: Flu Near You crowdsourced symptom reporting (2016–2019). Smolinski *et al.* (2015).
5. **Alpha / Power**: Conventional outbreak‐detection standards (Type I α=0.05, power=0.90).

</details>

---

## 2. Minimum Sample Size Estimation

Given *p₀* and *p₁*, we estimate the minimum `n` to detect an increase under (`alpha`, `target_power`) using six one‐sided binomial‐proportion tests:

1. Exact binomial inversion
2. Normal (Wald) approximation
3. Wilson score interval
4. Wilson score + continuity correction
5. Jeffreys interval
6. Agresti–Coull interval

**Procedure:**

1. **Range of `n`**: 1,000 to 12,000 (step = 100).
2. **Exact & Wald** (analytical):

   * Under *H₀*(*p₀*), invert distribution to find rejection threshold.
   * Compute power under *H₁*(*p₁*); select smallest `n` with power ≥ `target_power`.
3. **Wilson, Jeffreys, Agresti–Coull, ...** (simulation):

   * For each `n`, draw 100,000 Binomial(`n`, *p₁*) samples.
   * Compute observed rate $\hat p$ and 95% one‐sided lower bound $L$.
   * Reject *H₀* if $L > p₀$; empirical power = proportion of rejections.
   * Choose smallest `n` with empirical power ≥ `target_power`.
4. **Results**: Tabulate and plot required sample sizes vs. method; annotate power curves and 90% threshold.

<details>
<summary>Appendix A</summary>
Complete R/Python code for all tests and functions `estimate_required_sample_sizes()` can be found in Appendix A of the thesis repository.

</details>

---

## 3. Synthetic Data Generation

To allow individual‐level analysis while matching weekly aggregates from the LAC DpH Angelenos in Action program, we generated a synthetic dataset (`SyntheticData.csv`).

1. **Weekly records**: 1,000 simulated responses per week.
2. **Carry‐over IDs**: Retain 90% of prior‐week IDs; introduce 10% new IDs.
3. **Demographics**:

   * **Age**: Sample from {18–29, 30–39, 40–49, 50–59, 60–69, 70+, Unknown}.
   * **Race/Ethnicity**: {Asian, Black, Latino, Multi, Native, Other, PI, Unknown, White}.
   * **ZIP code**: Random draw from LA County ZIP list.
4. **Response date**: Random date within the 7‐day week window.
5. **Symptom flags**: Compute binary indicators:

   * `Sick`, `Cough`, `CSTE` (≥2 of fever, chills, sore throat, headache, body ache, loss of taste/smell), `Both` (Cough & CSTE).
   * Ensure weekly aggregates exactly match published per‐1,000 rates.

See Appendix C for code and Appendix D for the original `AiAData.xlsx` aggregates.

---

## 4. Change‐Point Detection

We applied the Pruned Exact Linear Time (PELT) algorithm using `cpt.meanvar` (R **changepoint** package) to detect weeks with abrupt shifts in mean/variance of the ILI proxy. BIC was used as penalty to prevent overfitting.

<details>
<summary>Reference</summary>
Killick, Fearnhead & Eckley (2012), *Journal of the American Statistical Association*; `cpt.meanvar` docs.
</details>

---

## 5. Cross‐Correlation Function (CCF)

Computed sample CCF among subgroups to detect lead‐lag patterns. Significant positive correlations at lag *k* indicate subgroup A symptom spikes precede subgroup B by *k* weeks.

<details>
<summary>Reference</summary>
Box, Jenkins, Reinsel & Ljung (2015), *Time Series Analysis: Forecasting and Control*.
</details>

---

## 6. Hotspot Analysis (Getis–Ord \$G\_i^\*\$)

For each ZIP code \$i\$, compute:

```math
G_i^* = \frac{\sum_j w_{ij} x_j - \bar X \sum_j w_{ij}}{\sigma \sqrt{[n \sum_j w_{ij}^2 - (\sum_j w_{ij})^2]/(n -1)}},
```

where \$x\_j\$ is ILI count at ZIP \$j\$, \$w\_{ij}\$ spatial weights, \$ar X\$ global mean, \$\sigma\$ global SD. Positive \$G\_i^\*\$ marks ILI hotspots. Excluded ZIPs with <10 respondents/month.

<details>
<summary>Reference</summary>
Getis & Ord (1992), *Geographical Analysis*.
</details>
