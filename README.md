# Methods

## 1. Epidemic Threshold Computation

For calculating the null and alternative hypothesis proportions of ILI in the community, we estimate the baseline and epidemic threshold for the percentage of the population with ILI each week. We use the following parameters:

* **pop**: Total population of Los Angeles County.
* **annual\_ed\_rate**: Annual ED visits per 1,000 people in LA County.
* **non\_epi\_rate**: Proportion of ED visits due to ILI during non-epidemic weeks.
* **threshold\_rate**: Proportion of ED visits due to ILI at the epidemic threshold.
* **ili\_seek\_rate**: Percentage of individuals with ILI who seek ED care.
* **alpha**: Significance level for sample-size estimation (Type I error rate).
* **target\_power**: Desired power for sample-size estimation (1 – Type II error rate).

We calculate the baseline rate (`p0`) and epidemic-threshold rate (`p1`) as:

```text
p0 = ((pop * (annual_ed_rate / 1000)) / 52 * non_epi_rate) / (ili_seek_rate * pop)
p1 = ((pop * (annual_ed_rate / 1000)) / 52 * threshold_rate) / (ili_seek_rate * pop)
```

These formulas compute weekly ED visits during "normal" and "influenza" weeks, adjust for the probability of an ILI case seeking ED care, and normalize by the population to obtain individual-level probabilities.

### Base-case Parameter Values

| Variable         | Value     |
| ---------------- | --------- |
| pop              | 9,825,708 |
| annual\_ed\_rate | 322       |
| non\_epi\_rate   | 0.0385    |
| threshold\_rate  | 0.0540    |
| ili\_seek\_rate  | 0.019     |
| alpha            | 0.05      |
| target\_power    | 0.90      |

> **Notes:**
>
> * Population estimate (July 1, 2023): LACDPH
> * ED visit rate: California Health Care Foundation Emergency Departments Almanac 2023
> * Baseline & threshold rates: LA County RespWatch (2019–2023)
> * ILI seek rate: Flu Near You (2016–2019)

---

## 2. Minimum Sample Size Estimation

After defining `p0` and `p1`, we estimate the minimum sample size `n_min` required to detect an increase under the given `alpha` and `target_power`. We use six methods:

1. **Exact binomial**
2. **Wald (Normal)**
3. **Wilson score**
4. **Wilson score with continuity correction**
5. **Jeffreys interval**
6. **Agresti–Coull interval**

### Procedure

1. **Define sample-size range**: Candidate `n` from 1,000 to 12,000 in increments of 100.
2. **Exact & Wald tests**:

   * Invert the binomial/Normal distribution under the null to find the rejection threshold.
   * Compute power under the alternative and select the smallest `n` where power ≥ 90 %.
3. **Wilson, Wilson CC, Jeffreys, Agresti–Coull**:

   * Simulate 100,000 samples of size `n` from `p1`.
   * For each sample, compute the observed rate `p̂` and the one-sided 95 % lower confidence bound `L`.
   * Declare detection if `L > p0`.
   * Estimate empirical power as the proportion of detections and choose the smallest `n` where power ≥ 90 %.
4. **Summarize results**: Compile required `n` for each method and visualize power vs. `n`.

---

## 3. Synthetic Data Creation

To preserve weekly symptom distributions while enabling individual-level analysis, we generated a synthetic dataset (`SyntheticData.csv`). Key steps:

1. **Reconstruct weekly records**: Generate 1,000 individual responses per week.
2. **Carry-over respondents**: Retain 90 % of IDs each week; introduce 10 % new IDs.
3. **Demographic assignment**: Sample age group, race/ethnicity, and ZIP code to match aggregate distributions.
4. **Date assignment**: Randomly assign each response a date within its week.
5. **Symptom flags**: Compute binary indicators (`Sick`, `Cough`, `CSTE`, `Both`) ensuring aggregate rates match published data.

---

## 4. Change Point Detection

We applied the PELT algorithm (via `cpt.meanvar` in the **changepoint** R package) to detect weeks with abrupt changes in mean or variance of the ILI proxy, using BIC as penalty.

---

## 5. Cross-correlation Function (CCF)

We computed sample cross-correlation functions among subgroups to explore lead-lag relationships in symptom upticks. Positive correlation at lag *k* indicates Group 1 symptoms precede Group 2 by *k* weeks.

---

## 6. Hotspot Analysis (Getis–Ord Gi\*)

For each ZIP code, we computed:

```text
Gi* = (∑_j w_ij x_j – X̄ ∑_j w_ij) / (σ √([n ∑_j w_ij^2 – (∑_j w_ij)^2] / (n–1)))
```

Locations with large positive Gi\* are ILI hotspots. ZIPs with <10 respondents per month were excluded.

---

## References

* LA County Department of Public Health. “Los Angeles County Population Estimates (July 1, 2023).”
* California Health Care Foundation. “Emergency Departments Almanac 2023.”
* LA County Dept. of Public Health. “RespWatch: Influenza-Like Illness Surveillance.”
* Smolinski MS, et al. “Flu Near You: Crowdsourced Symptom Reporting.” *Am J Public Health*, 2015.
* Getis A, Ord JK. *Geographical Analysis*, 1992.
