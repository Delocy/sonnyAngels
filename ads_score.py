import pandas as pd
import numpy as np

data = pd.ExcelFile('dataset/ad_ranking_clean.xlsx')
ads = pd.read_excel(data, sheet_name='Ads', header=0)
mods = pd.read_excel(data, sheet_name='Mods', header=0)

# Decision weights used
latest_weight = 20
start_weight = 20
adrev_weight = 35
st_weight = 25

# Ad Revenue Score
ads["adrev_diff"] = ads["ad_revenue"] - ads["avg_ad_revenue"]
adrev_max = ads["adrev_diff"].max()
adrev_min = ads["adrev_diff"].min()
ads["adrev_score"] = (ads["adrev_diff"] - adrev_min) / (adrev_max - adrev_min) * adrev_weight

# Baseline ST Score
st_max = ads["baseline_st"].max()
st_min = ads["baseline_st"].min()
ads["st_score"] = (st_max - ads["baseline_st"]) / (st_max - st_min) * st_weight

# Latest Punish Score
ads['p_date_dateform'] = pd.to_datetime(ads['p_date'], format='%Y%m%d')
ads['days_from_latest_to_p'] = (ads['p_date_dateform'] - ads['latest_punish_begin_date']).dt.days
latest_max = ads["days_from_latest_to_p"].max()
latest_min = ads["days_from_latest_to_p"].min()
ads['latest_punish_score'] = ((ads["days_from_latest_to_p"] - latest_min) / (latest_max - latest_min) * latest_weight) / np.where(ads["punish_num"] > 0, ads["punish_num"], 1)

# Start Time Score
ads['days_from_start_to_p'] = (ads['p_date_dateform'] - ads['start_time']).dt.days
start_max = ads["days_from_start_to_p"].max()
start_min = ads["days_from_start_to_p"].min()
ads["start_score"] = (start_max - ads["days_from_start_to_p"]) / (start_max - start_min) * start_weight

# Total Score
ads["total_score"] = ads["start_score"] + ads["latest_punish_score"] + ads["st_score"] + ads["adrev_score"]

# Apply Min-Max scaling to the "total_score" column

min_score = ads["total_score"].min()
max_score = ads["total_score"].max()

ads["normalized_score"] = (ads["total_score"] - min_score) / (max_score - min_score)

# Display the DataFrame with the normalized "total_score" column
ads["normalized_score"]
ads.to_excel("ads_score.xlsx")