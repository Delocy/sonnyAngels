import pandas as pd

data = pd.ExcelFile('dataset/ad_ranking_clean.xlsx')
ads = pd.read_excel(data, sheet_name='Ads', header=0)
mods = pd.read_excel(data, sheet_name='Mods', header=0)

mods["real_productivity"] = mods["Productivity"] - mods["Utilisation %"]

mods.rename(columns={" accuracy ": "accuracy"}, inplace=True)

mods = mods[mods["accuracy"] != "-"]
mods = mods[mods["accuracy"] != '                 -  ']

# Remove rows with NaN values in the "accuracy" column
mods.dropna(subset=["accuracy"], inplace=True)

mods.reset_index(drop=True, inplace=True)

Weight_Real_Productivity = 0.4
Weight_Accuracy = 0.45
Weight_Handling_Time = 0.15

mods["score"] = (Weight_Real_Productivity * mods["real_productivity"]) + (Weight_Accuracy * mods["accuracy"]) / (Weight_Handling_Time * mods["handling time"])

min_score = mods["score"].min()
max_score = mods["score"].max()

# Apply Min-Max scaling to the "Score" column
mods["normalized_score"] = (mods["score"] - min_score) / (max_score - min_score)

# Display the DataFrame with the normalized "Score" column
mods["normalized_score"]
mods.to_excel("mods_score.xlsx")