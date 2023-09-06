import pandas as pd
import matplotlib.pyplot as plt

data = pd.ExcelFile('dataset/ad_ranking_raw.xlsx')
ads = pd.read_excel(data, sheet_name='ads dimension (dim table)', header=1)
mods = pd.read_excel(data, sheet_name='moderator dimension (dim table)', header=0)

ads.head(10)
mods.head(10)

## filling null with 0 for punish_num
ads['punish_num'].fillna(0, inplace=True)

# plotting punish_num on boxplot
plt.figure(figsize=(8, 6))  # Set the figure size
plt.hist(ads['punish_num'], bins=20, edgecolor='k', alpha=0.7)
plt.title('Histogram of punish_num')
plt.xlabel('punish_num')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

## cleaning delivery_country column
def split_market(entry):
    if pd.notna(entry):
        if '/' in entry:
            return entry.split('/')
        elif '&' in entry:
            return entry.split('&')
        elif entry == 'USCA':
            return ['US', 'CA']
        elif entry == 'MENA':
            return ['ME', 'NA']
        else:
            return [entry]
    else:
        return [entry] 

ads['queue_market_list'] = ads['queue_market'].apply(split_market)

ads['queue_market_list'] = ads['queue_market_list'].apply(lambda x: ['Others'] if 'Other' in x else x)

## cleaning ad_revenue
ads['ad_revenue'].fillna(0, inplace=True)

## remove moderators with null productivity and utilisation
mods = mods.dropna(subset=['Productivity', 'Utilisation %'])

def contains_dash(value):
    return '-' in str(value)

## remove moderators with null accuracy
mods = mods[~mods[' accuracy '].apply(contains_dash)]
mods.head(20)
print(mods.dtypes)

with pd.ExcelWriter('dataset/ad_ranking_clean.xlsx') as writer:
    ads.to_excel(writer, sheet_name='Ads', index=False)

    mods.to_excel(writer, sheet_name='Mods', index=False)