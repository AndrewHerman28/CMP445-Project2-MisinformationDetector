from urllib.parse import urlparse
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# === Read in Data ===
fake_news_data = pd.read_csv("../Data/Raw/Fake_News_Detection/Fake.csv")
true_news_data = pd.read_csv("../Data/Raw/Fake_News_Detection/True.csv")
liar_data = pd.read_csv("../Data/Raw/LIAR/train.tsv", sep='\t')

# ===== Map LIAR Labels to binary =====
# 0 = true, mostly-true, half-true
# 1 = false, barely-true, pants-fire
liar_label_map = {
    'true': 0,
    'half-true': 0,
    'mostly-true': 0,
    'barely-true': 1,
    'pants-fire': 1,
    'false': 1
}

# === Add SCHEMA field ===
liar_data['hasMisinformation'] = liar_data['label'].map(liar_label_map)
liar_data['title'] = None
liar_data['text'] = liar_data['statement']
liar_data['domain'] = None
liar_df = liar_data[['title', 'text', 'domain', 'hasMisinformation']]

# ===== Add SCHEMA to Fake News Data =====
fake_news_data["hasMisinformation"] = 1
fake_news_data["domain"] = None
fake_df = fake_news_data[["title", "text", "domain", "hasMisinformation"]]

# ===== Add SCHEMA to True News Data =====
true_news_data["hasMisinformation"] = 0
true_news_data["domain"] = None
true_df = true_news_data[["title", "text", "domain", "hasMisinformation"]]

# ===== Merge True / Fake News Data =====
fake_news_df = pd.concat([fake_df, true_df], ignore_index=True)

# === Merge Datasets into one DataFrame ===
df = pd.concat([liar_df, fake_news_df], ignore_index=True)

df.to_csv("../Data/Processed/merged_data.csv", index=False)
