import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd


# 1️⃣ Load your job dataset

# static_switzerland_jobs_map.py
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Load your jobs dataset
f_jobs_clean = pd.read_json(r"C:\Users\walisits\Documents\CIP-Project-main\data\publicjobs_cleaned.json")

# 2️⃣ Map cities to cantons
city_to_canton = {
    "Zug": "Zug",
    "Bülach": "Zürich",
    "Muttenz": "Basel-Landschaft",
    "Horgen": "Zürich",
    "Genève": "Genève",
    "Lausanne": "Vaud",
    "Bern": "Bern",
    "Basel": "Basel-Stadt",
    # Add other cities in your dataset
}
f_jobs_clean['canton_name'] = f_jobs_clean['city'].map(city_to_canton)

# 3️⃣ Count jobs per canton
job_counts = f_jobs_clean.groupby("canton_name").size().reset_index(name="job_count")

# 4️⃣ Load Swiss cantons GeoJSON (canton boundaries)
cantons_gdf = gpd.read_file(r"C:\Users\walisits\Documents\CIP-Project-main\swissBOUNDARIES3D_1_3_TLM_KANTONSGEBIET.geojson")

# 5️⃣ Merge job counts with GeoDataFrame
cantons_gdf = cantons_gdf.merge(job_counts, left_on="NAME", right_on="canton_name", how="left")
cantons_gdf["job_count"] = cantons_gdf["job_count"].fillna(0)  # fill missing cantons with 0

# 6️⃣ Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
cantons_gdf.plot(
    column="job_count",
    cmap="viridis",
    linewidth=0.8,
    edgecolor="black",
    legend=True,
    ax=ax
)
ax.set_title("Job Count per Canton — Switzerland", fontsize=16)
ax.axis("off")  # remove axes
plt.show()
# Jobs per seniority
sns.set(style="whitegrid")

# Count jobs per seniority
plt.figure(figsize=(8,5))
ax = sns.countplot(
    x='seniority',
    data=f_jobs_clean,
    palette='viridis',   # cool color gradient
    order=f_jobs_clean['seniority'].value_counts().index  # order by frequency
)

# Add counts on top of bars
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')

# Labels & title
plt.title("Jobs by Seniority", fontsize=16)
plt.xlabel("Seniority Level")
plt.ylabel("Number of Jobs")
plt.show()

# Jobs per ISCO major
sns.set(style="whitegrid")

# Create figure
plt.figure(figsize=(10,8))

# Countplot with horizontal bars
ax = sns.countplot(
    y='isco_major_name',
    data=f_jobs_clean,
    order=f_jobs_clean['isco_major_name'].value_counts().index,
    palette='viridis'
)

# Annotate each bar with count
for p in ax.patches:
    width = p.get_width()
    ax.annotate(f'{int(width)}',
                (width + 0.5, p.get_y() + p.get_height()/2),
                ha='left', va='center', fontsize=10, color='black')

# Titles and labels
plt.title("Jobs by ISCO Major", fontsize=16)
plt.xlabel("Number of Jobs")
plt.ylabel("ISCO Major")

plt.tight_layout()
plt.show()

# Read data from benefits

f_jobs_clean = pd.read_json(r"C:\Users\walisits\Documents\CIP-Project-main\data\publicjobs_cleaned.json")
benefits_clean = pd.read_json(r"C:\Users\walisits\Documents\CIP-Project-main\data\publicjobs_benefits.json")

# -----------------------------
# 1. Load job and benefits data
# -----------------------------
f_jobs_clean = pd.read_json(r"C:\Users\walisits\Documents\CIP-Project-main\data\publicjobs_cleaned.json")
benefits_clean = pd.read_json(r"C:\Users\walisits\Documents\CIP-Project-main\data\publicjobs_benefits.json")

# -----------------------------
# 2. Encode benefits as dummy variables
# -----------------------------
all_benefits = sorted({b for sublist in benefits_clean['benefits'] for b in sublist})
for b in all_benefits:
    benefits_clean[b] = benefits_clean['benefits'].apply(lambda x: 1 if b in x else 0)

# -----------------------------
# 3. Merge job info and compute FTE
# -----------------------------
merged = benefits_clean.merge(
    f_jobs_clean[['detail_url', 'fte_from', 'fte_to', 'canton']],
    on='detail_url',
    how='left'
)

# Remove rows with missing FTE
merged = merged.dropna(subset=['fte_from', 'fte_to'])

# Compute average FTE and classify as part-time / full-time
merged['fte_avg'] = merged[['fte_from', 'fte_to']].mean(axis=1)
merged['workload_type'] = merged['fte_avg'].apply(lambda x: 'Teilzeit' if x < 1 else 'Vollzeit')

# -----------------------------
# 4. Bar chart: Part-time vs Full-time % per benefit
# -----------------------------
# Compute percentage of jobs offering each benefit by workload
pct_df = merged.groupby('workload_type')[all_benefits].mean() * 100
pct_df = pct_df.transpose().sort_values(by='Vollzeit', ascending=False)

# Select top 10 benefits for readability
top_benefits = pct_df.head(10).reset_index().rename(columns={'index': 'Benefit'})
melted = top_benefits.melt(id_vars='Benefit', var_name='Workload', value_name='Percentage')

# Horizontal bar chart
plt.figure(figsize=(10,6))
sns.barplot(data=melted, y='Benefit', x='Percentage', hue='Workload')
plt.xlabel("Percentage of Jobs Offering Benefit (%)")
plt.ylabel("Benefit")
plt.title("Top 10 Benefits: Part-time vs Full-time Jobs")
plt.legend(title='Workload')
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Heatmap: Benefit occurrence by canton
# -----------------------------
heatmap_data = merged.dropna(subset=['canton']).groupby('canton')[top_benefits['Benefit']].sum()

plt.figure(figsize=(12,8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d")
plt.title("Top 10 Benefits Occurrence by Canton")
plt.xlabel("Benefit")
plt.ylabel("Canton")
plt.tight_layout()
plt.show()

# -----------------------------
# 6. Optional: Print top benefits overall
# -----------------------------
avg_pct = pct_df.mean(axis=1).sort_values(ascending=False)
print("Top benefits offered overall:")
print(avg_pct.head(10))

# Q2
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# --- Load datasets ---
with open(r"C:\Users\walisits\Documents\publicjobs_cleaned.json", "r", encoding="utf-8") as f:
    jobs_data = json.load(f)

with open(r"C:\Users\walisits\Documents\bfs_besta.json", "r", encoding="utf-8") as f:
    stats_data = json.load(f)

# --- Convert to DataFrames ---
jobs_df = pd.DataFrame(jobs_data)
stats_df = pd.DataFrame(stats_data)

# --- Process jobs dataset ---
jobs_df['posting_date'] = pd.to_datetime(jobs_df['posting_date'], unit='ms')

# Fix chained assignment warning by assigning directly
jobs_df['fte_to'] = jobs_df['fte_to'].fillna(jobs_df['fte_from'])

jobs_df['fte_avg'] = (jobs_df['fte_from'] + jobs_df['fte_to']) / 2
jobs_df['flexibility'] = jobs_df['fte_avg'].apply(lambda x: 'Teilzeit' if x < 1.0 else 'Vollzeit')
jobs_df['year_quarter'] = jobs_df['posting_date'].dt.to_period('Q').astype(str)

# Select 2026Q1 for jobs
jobs_q = jobs_df[jobs_df['year_quarter'] == '2026Q1']
jobs_flex_counts = jobs_q['flexibility'].value_counts()
jobs_flex_pct = jobs_flex_counts / jobs_flex_counts.sum() * 100  # percentage

# --- Process BFS dataset ---
emp_q = stats_df[stats_df['Geschlecht'] == 'Geschlecht - Total']
emp_q = emp_q[emp_q['Beschäftigungsgrad'].isin(['Vollzeit','Teilzeit'])]
emp_q = emp_q[emp_q['Quartal'] == '2025Q1']
emp_flex_counts = emp_q.groupby('Beschäftigungsgrad')['value'].sum()
emp_flex_pct = emp_flex_counts / emp_flex_counts.sum() * 100  # percentage

# --- Combine percentages for plotting ---
flex_compare_pct = pd.DataFrame({
    'Jobs 2026Q1': jobs_flex_pct,
    'BFS 2025Q1': emp_flex_pct
}).fillna(0)

# --- Plot grouped bar chart ---
flex_compare_pct.T.plot(kind='bar', figsize=(6,4))
plt.ylabel('Percentage (%)')
plt.title('Flexibility comparison (Part-time vs Full-time)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# --- Chi-square test on raw counts ---
flex_compare_counts = pd.DataFrame({
    'Jobs 2026Q1': [jobs_flex_counts.get('Teilzeit', 0), jobs_flex_counts.get('Vollzeit', 0)],
    'BFS 2025Q1': [emp_flex_counts.get('Teilzeit', 0), emp_flex_counts.get('Vollzeit', 0)]
}, index=['Teilzeit', 'Vollzeit'])

chi2, p, dof, expected = chi2_contingency(flex_compare_counts)
print("Chi-square p-value:", p)
# --- Chi-square test on raw counts ---
flex_compare_counts = pd.DataFrame({
    'Jobs 2026Q1': [jobs_flex_counts.get('Teilzeit', 0), jobs_flex_counts.get('Vollzeit', 0)],
    'BFS 2025Q1': [emp_flex_counts.get('Teilzeit', 0), emp_flex_counts.get('Vollzeit', 0)]
}, index=['Teilzeit', 'Vollzeit'])

# --- Print comparison table ---
print("Flexibility comparison (Jobs 2026Q1 vs BFS 2025Q1):")
print(flex_compare_counts)

chi2, p, dof, expected = chi2_contingency(flex_compare_counts)
print("Chi-square p-value:", p)