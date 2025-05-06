%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%2345678901234567890123456789012345678901234567890123456789012345678901234567890
%        1         2         3         4         5         6         7         8
% THESIS Discussion

% !TEX root = ../Thesis_template.tex

\chapter{Methods}
\label{methods}

\section{Epidemic Threshold Computation}
\label{sec:sec21}

For calculating the null and alternative hypothesis proportions of ILI in the community, we start by estimating the baseline and the epidemic threshold for the percentage of the population with ILI at any given week. In order to do this, we use the following parameters:
\begin{itemize}
  \item $\text{pop}$: Total population of Los Angeles County. 
  \item $\text{annual\_ed\_rate}$: Annual ED visits per 1,000 people in the Los Angeles County.
  \item $\text{non\_epi\_rate}$: Proportion of ED visits due to ILI during non-epidemic weeks.
  \item $\text{threshold\_rate}$: Proportion of ED visits due to ILI at the epidemic threshold. 
  \item $\text{ili\_seek\_rate}$: Percentage of all individuals with ILI that seek ED Care. The inverse of this would be the case-to-ED-visit ratio. 
  \item $\text{alpha}$: Significance level for sample-size estimation, i.e., the maximum allowable probability of falsely declaring an outbreak when none exists (Type I error rate).
  \item $\text{target\_power}$: Desired power for sample-size estimation, i.e., the probability of correctly detecting an outbreak when it occurs (1 – Type II error rate).
\end{itemize}

We then manipulate these variables to obtain  $p_0$ (baseline rate) and $p_1$ (threshold rate) by using the following formula:

\begin{align}
  p_0 &= \frac{\Bigl(\text{pop}\times\frac{\text{annual\_ed\_rate}}{1000}\Bigr)/52 \;\times\;\text{non\_epi\_rate}}
            {\text{ili\_seek\_rate}\;\times\;\text{pop}},\\
  p_1 &= \frac{\Bigl(\text{pop}\times\frac{\text{annual\_ed\_rate}}{1000}\Bigr)/52 \;\times\;\text{threshold\_rate}}
            {\text{ili\_seek\_rate}\;\times\;\text{pop}}.
\end{align}\footnote{Based on previous work performed by the Los Angeles County Department of Public Health.}


In essence, in Equations 2.1 and 2.2, we are calculating weekly ED visits in LA County during ``normal" and ``influenza" weeks, and then dividing those values by the probability that someone with influenza visits the ED, assuming that this probability remains constant in each case, to obtain the number of residents with in LA with ILI during ``normal" and ``influenza" weeks. We then divide that number by the total population of LA County to convert it into the probability that a single individual has ILI in each scenario. 

As seen in Appendix A, in order to maximize reusability, our code treats each of these variables as a hyperparameter to be defined by the user in both a consolidated function\footnote{\texttt{estimate\_required\_sample\_sizes()}} and the shiny app we created. Nonetheless, we use the following values for each variable to create a base case scenario and approximate the minimum sample size required by AiA. It must be noted, though, that the exact magnitude of some of these variables remains contested within the epidemiological community. 
For our base case sample size calculation, we used the following values:
\begin{table}[H]
  \centering
  \begin{tabular}{@{}lr@{}}
    \toprule
    Variable                 & Value               \\
    \midrule
    $\displaystyle \text{pop}$             & 9{,}825{,}708       \\
    $\displaystyle \text{annual\_ed\_rate}$    & 322 \\
    $\displaystyle \text{non\_epi\_rate}$      & 0.0385                \\
    $\displaystyle \text{threshold\_rate}$     & 0.0540                \\
    $\displaystyle \text{ili\_seek\_rate}$     & 0.019                 \\
    $\displaystyle \text{alpha}$               & 0.05                 \\
    $\displaystyle \text{target\_power}$      & 0.90                 \\
    \bottomrule
  \end{tabular}
  \caption{Base‐case parameter values for epidemic‐threshold and sample‐size estimation}
  \label{tab:basecase_params}
\end{table}
\pagebreak

\noindent The most recent population estimate for the LA County (9,825,708 as of July 1, 2023) was obtained from the Los Angeles County Department of Public Health.\footnote{Los Angeles County Department of Public Health. “Los Angeles County Population Estimates (July 1, 2023).” Los Angeles County Department of Public Health. \url{http://www.publichealth.lacounty.gov/epi/docs/2023-LAC-Population-8RE.pdf}. Accessed 16 Feb. 2025.}

\bigskip
\noindent The annual ED visit rate of 322 visits per 1,000 persons per year was obtained from the most recent California Health Care Foundation Emergency Departments Almanac (2023)\footnote{California Health Care Foundation. “Emergency Departments Almanac 2023.” California Health Care Foundation, Dec. 2023. \url{https://www.chcf.org/wp-content/uploads/2023/12/EmergencyDepartmentsAlmanac2023.pdf}. Accessed 16 Feb. 2025.}.

\bigskip
\noindent The baseline rate of ILI ED visits was calculated by computing the mean ILI ED‐visit proportion during non‐epidemic weeks (0.016) for the last few years using historical Los Angeles County RespWatch data (2019–2023)\footnote{Los Angeles County Department of Public Health. “RespWatch: Influenza-Like Illness Surveillance.” Los Angeles County Department of Public Health. \url{http://publichealth.lacounty.gov/acd/RespWatch/}. Accessed 16 Feb. 2025.}. The complete computations can be found at the bottom of Appendix A. 

\bigskip
\noindent The epidemic threshold rate (0.04) was defined as the mean non‐epidemic ILI ED‐visit rate plus two standard deviations ($\approx$98th percentile observations), using the same RespWatch dataset\footnote{Los Angeles County Department of Public Health. “RespWatch: Influenza-Like Illness Surveillance.” Los Angeles County Department of Public Health. \url{http://publichealth.lacounty.gov/acd/RespWatch/}. Accessed 16 Feb. 2025.}. Similarly, the complete computations can be found at the bottom of Appendix A.

\bigskip
\noindent The proportion of symptomatic ILI cases who seek ED care (0.019) was calculated by multiplying the average fraction of Flu Near You participants who reported seeking care (31.6\% for 2016–2019) by the subset of those who attended an ED ($\approx$6\%)\footnote{Smolinski, Mark S., et al. “Flu Near You: Crowdsourced Symptom Reporting Spanning 2 Influenza Seasons.” \textit{American Journal of Public Health}, U.S. National Library of Medicine, Oct. 2015. \url{https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4566540/}. Accessed 16 Feb. 2025.}.

\bigskip
\noindent The Type I error rate and the target power follow the conventional standards used by the CDC for outbreak detections. 


\section{Minimum Sample Size Estimation}
\label{sec:sec22}

After defining the null and alternative hypothesis proportions \(p_0\) and \(p_1\), we determine a range of potential of minimum sample sizes \(n_{min}\) required to detect an increase from \(p_0\) to \(p_1\) under the Type I error and power constraints. To obtain a robust range for \(n_{min}\), we calculate the minimum sample size required by AiA using six different binomial proportion confidence intervals: Exact binomial, Normal (Wald) approximation, Wilson, Wilson CC, Jeffreys, and Agresti–Coull\footnote{Black CL, O’Halloran A, Hung MC, Srivastav A, Lu PJ, Garg S, et al. Vital Signs: Influenza Hospitalizations and Vaccination Coverage by Race and Ethnicity—United States, 2009–10 Through 2021–22 Influenza Seasons. \textit{MMWR Morb Mortal Wkly Rep}. 2022 Oct 28;71(43):1366–1373. doi:10.15585/mmwr.mm7143e1. \url{https://www.cdc.gov/mmwr/volumes/71/wr/pdfs/mm7143e1-H.pdf}. Accessed 18 Apr. 2025.}. For the first two tests, we identify the smallest value \(n_{min}\) from a range of values of \(n\) using a closed-form analytical solution, whereas for the last four tests, we do so by running a series of Monte Carlo simulations. The complete code used to perform these calculations can be found in Appendix A.

\begin{enumerate}
  \item \textbf{Defining Sample Size Range}:  
    We assessed candidate sample sizes \(n\) ranging from 1,000 to 12,000 in 100-unit increments. These range and increments allowed us to identify where the power curve exceeded the 90\% threshold in a way that balanced computational efficiency and the level of accuracy required by AiA. 
    
  \item \textbf{Exact and Normal Tests}:  
    For each candidate sample size \(n\) we performed the following calculations:
    \begin{enumerate}[label=(\alph*)]
      \item Under the null \(p_0\), we inverted the binomial distribution (in the case of the Exact test), or the Normal distribution (in the case of the Wald test), to identify the smallest observed proportion \(\hat p\) that would lead to rejection at the 5\% alpha level.  
      \item To calculate the power at each n, we computed the probability of obtaining a value that is as high or higher than \(p\) under the alternative, \(p_1\).
      
    \end{enumerate}
    
We then selected the smallest value of \(n\) for which the computed power met or exceeded 90\%.  

\pagebreak

  \item \textbf{Wilson score, Wilson with continuity correction, Jeffreys, and Agresti–Coull tests}:  
For each of the four one‐sided interval methods, and each sample size \(n\), we:
\begin{enumerate}[label=(\alph*)]
  \item Drew (simulated) 100,000 independent samples of size \(n\)  from the alternative, \(p_1\).  
  \item For each draw, we calculated the observed ILI rate \(\hat p\) and then constructed the corresponding lower one-sided 95\% confidence bound \(L\), resulting in an interval \([L,\,1]\). 
  \item We rejected the null in favor of the alternative whenever \(L > p_0\). In other words, we considered a ``detection" whenever the interval’s lower bound excluded the null. This effectively ensured that we maintained the desired 5\% alpha level. 
 
\end{enumerate}

Lastly, we obtained the empirical power for each \(n\) by calculating the proportion of the 100,000 simulations in which we rejected the null. 

  \item \textbf{Determine Minimum Sample Size and Summarize Results.}  
    For each of the six frameworks, we scanned the computed power values across our grid and selected the smallest \(n\) at which power $\geq$ 90 \%.  These ``required \(n\)” values were then compiled into a summary table and illustrated with power-versus-\(n\) plots marking the 90\% line.
\end{enumerate}

\section{Synthetic Data Creation}
\label{sec:sec22}

To enable individual‐level analyses while preserving the weekly symptom distributions reported by the Los Angeles County Department of Public Health’s Angelenos in Action program, we generated a synthetic dataset of 1,000 responses per week with aggregate proportions that matched exactly the published results. The code used to generate the dataset can be found on Appendix C and the the original weekly aggregates scrapped from the LACDPH's website and stored in \texttt{AiAData.xlsx} can be found in Appendix D. 

\begin{enumerate}
  \item \textbf{Reconstruction of weekly records:} We started by generating 1,000 individual records for each reported week.
  \item \textbf{Carry‐over respondents:} We assigned unique five‐digit IDs (starting at 10,000). We retained 90\% of IDs each subsequent week from the prior week (with demographics fixed) and introduced 10 \% new IDs (with newly sampled demographics and five-digit IDs) to mimic the natural churn that we would expect to see in the actual dataset.
  \item \textbf{Demographic assignment:} We semi-randomly assigned demographics to each ID by pulling from certain distributions that matched the aggregate demographic distributions of LA County. It must be noted that this does not hold in practice in the actual dataset. 
    \begin{itemize}
      \item \emph{Age group:} Sample from \{“18–29”, “30–39”, “40–49”, “50–59”, “60–69”, “70+”, “Unknown”\}.  
      \item \emph{Race/ethnicity:} Sample from \{“Asian”, “Black”, “Latino”, “Multi”, “Native”, “Other”, “PI”, “Unknown”, “White”\}.  
      \item \emph{zip code:} For this variable we drew fully randomly from a hard‐coded list of Los Angeles County zip codes.
    \end{itemize}
  \item \textbf{Date assignment:} we randomly assigned each record a response date within the corresponding seven‐day week window to further approximate the characteristics of the real dataset.
  \item \textbf{Symptom flags:} We computed four binary indicators obtained —\texttt{Sick}, \texttt{Cough}, \texttt{CSTE\footnote{CSTE is defined as the presence of at least two of the following symptoms: fever, chills, sore throat, headache, body ache, or loss of taste/smell.}}, and \texttt{Both (Cough and CSTE)}—based on the reported symptoms categories and we ensured that each week matched, in aggregate, the reported rates per 1,000 respondents for each category (as established in in \texttt{AiAData.xlsx}). 
\end{enumerate}

The resulting file, \texttt{SyntheticData.csv}, contains individual‐level records with demographics and symptom flags that, when aggregated, mimic very closely the historical AiA weekly symptom distributions.  
\section{Change Point Detection}
\label{sec:sec23}
We used the Pruned Exact Linear Time (PELT) algorithm via the \texttt{cpt.meanvar} function to spot weeks where the behaviour of our ILI proxy changed abruptly. The PELT algorithm works by evaluating each possible split in the series and evaluating how well the data before and after each split point would fit simple models with a constant mean and variance. To prevent overfitting, each additional split must improve the overall fit by more than a user-specified penalty -- in this case BIC (Bayesian Information Criterion)\footnote{\texttt{cpt.meanvar} in \emph{changepoint}: Methods for Changepoint Detection, version 2.3. Available at \url{https://cran.r-project.org/web/packages/changepoint/changepoint.pdf}. Accessed 22 Apr.\ 2025.}. The detected change points then mark those weeks where the mean and/or variance of our ILI proxy appears to change, signaling the potential the start or end of a potential ILI outbreak.



\section{Cross Correlation Function}
\label{sec:sec24}
To explore temporal relationships between the symptoms expressed by different groups, we compute the sample cross‐correlation function (CCF) among different subgroups. Significant positive correlations at positive lags indicate that upticks in the presence of symptoms in the first group tend to lead upticks in the presence of symptoms in the second group by $k$ weeks\footnote{Box GE, Jenkins GM, Reinsel GC, Ljung GM. Time Series Analysis: Forecasting and Control. Wiley; 2015.}.

\section{Hot Spot Analysis (Getis–Ord \(G_i^*\))}
\label{sec:sec25}
In order to identify hotspots of ILI activity we use the Getis–Ord \(G_i^*\) statistic.  For each zipcode, we compute
\[
G_i^* = \frac{\sum_j w_{ij} x_j - \bar{X} \sum_j w_{ij}}
{\sigma \sqrt{[n\,\sum_j w_{ij}^2 - (\sum_j w_{ij})^2]/(n-1)}},
\]  
where \(x_j\) is the count of ILI-indicative responses at zipcode \(j\), \(w_{ij}\) are spatial weights, \(\bar{X}\) is the global mean, and \(\sigma\) is the global standard deviation\footnote{Getis A, Ord JK. The analysis of spatial association by use of distance statistics. \textit{Geographical Analysis}. 1992 Apr;24(3):189–206. doi:10.1111/j.1538-4632.1992.tb00261.x.}.  Locations with large positive \(G_i^*\) values  are identified as “hot spots” of unusually high incidence.

We did this analysis over different months as an attempt to observe the spatial evolution of ILI. In order to avoid introducing spurious results, we excluded all zipcodes with less than 10 respondents on any given month from our analysis. 
