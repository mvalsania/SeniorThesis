import os
import numpy as np
import pandas as pd

os.chdir("/Users/marcovalsania/Desktop/Synthetic Data")

df_real = pd.read_excel("AiAData.xlsx")
df_real.columns = ["Date", "CoughSOB2plus", "Fever2plus", "SOB", "None"]
df_real["Date"] = pd.to_datetime(df_real["Date"])

symptom_map = {
    "Cough/SOB & 2+ other symptoms": "CoughSOB2plus",
    "2+ of fever, chills, headache, body aches, sore throat, loss of taste/smell": "Fever2plus",
    "Cough or Shortness of Breath (SOB)": "SOB",
    "None": "None"
}

age_choices = ["18–29", "30–39", "40–49", "50–59", "60–69", "70+", "Unknown"]
age_probs   = [0.20,    0.25,    0.20,    0.15,    0.10,    0.05,    0.05]

race_choices = ["Asian", "Black", "Latino", "Multi", "Native", "Other", "PI", "Unknown", "White"]
race_probs   = [0.10,    0.10,    0.30,     0.05,    0.01,    0.03,     0.01,    0.10,      0.30]

zip_choices = [
    "90001","90002","90003","90004","90005","90006","90007","90008","90010",
    "90011","90012","90013","90014","90015","90016","90017","90018","90019",
    "90020","90021","90022","90023","90024","90025","90026","90027","90028",
    "90029","90030","90031","90032","90033","90034","90035","90036","90037",
    "90038","90039","90040","90041","90042","90043","90044","90045","90046",
    "90047","90048","90049","90056","90057","90058","90059","90061","90062",
    "90063","90064","90065","90066","90067","90068","90069","90071","90077",
    "90089","90094"
]

total_per_week = 1000
carryover_rate = 0.90
new_per_week   = total_per_week - int(carryover_rate * total_per_week)

all_responses   = []
respondent_pool = {}
next_id         = 10000

for i, row in df_real.iterrows():
    week_start    = row["Date"]
    symptoms_list = []
    for label, col in symptom_map.items():
        symptoms_list.extend([label] * int(row[col]))
    np.random.shuffle(symptoms_list)

    if i == 0:
        current_ids = []
        for _ in range(total_per_week):
            respondent_id = next_id
            next_id      += 1
            age_val  = np.random.choice(age_choices, p=age_probs)
            race_val = np.random.choice(race_choices, p=race_probs)
            zip_val  = np.random.choice(zip_choices)
            respondent_pool[respondent_id] = {"Age": age_val, "Race": race_val, "Zip": zip_val}
            current_ids.append(respondent_id)
    else:
        carryover_count = int(carryover_rate * total_per_week)
        carried_ids     = np.random.choice(current_ids, size=carryover_count, replace=False).tolist()
        new_ids         = []
        for _ in range(new_per_week):
            respondent_id = next_id
            next_id      += 1
            age_val  = np.random.choice(age_choices, p=age_probs)
            race_val = np.random.choice(race_choices, p=race_probs)
            zip_val  = np.random.choice(zip_choices)
            respondent_pool[respondent_id] = {"Age": age_val, "Race": race_val, "Zip": zip_val}
            new_ids.append(respondent_id)
        current_ids = carried_ids + new_ids

    for idx_resp, respondent_id in enumerate(current_ids):
        offset      = np.random.randint(0, 7)
        start_date  = week_start + pd.Timedelta(days=offset)
        label       = symptoms_list[idx_resp]
        cough       = int(label in ["Cough or Shortness of Breath (SOB)", "Cough/SOB & 2+ other symptoms"])
        cste        = int(label in ["2+ of fever, chills, headache, body aches, sore throat, loss of taste/smell", "Cough/SOB & 2+ other symptoms"])
        both        = int(label == "Cough/SOB & 2+ other symptoms")
        sick        = int(cough or cste or both)
        demo        = respondent_pool[respondent_id]
        all_responses.append({
            "id": respondent_id,
            "Start": start_date,
            "week": week_start,
            "Race": demo["Race"],
            "Age": demo["Age"],
            "Zip": demo["Zip"],
            "Cough": cough,
            "CSTE": cste,
            "Both": both,
            "Sick": sick
        })

df_synthetic = pd.DataFrame(all_responses)
df_synthetic.to_csv("SyntheticData.csv", index=False)
print("SyntheticData.csv saved")
