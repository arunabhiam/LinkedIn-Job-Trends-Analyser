import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned job data
df = pd.read_csv('../data/cleaned_jobs.csv')

# Split skills and count frequency per location
skill_counts = (
    df.assign(Skill=df['Skills'].str.split(', '))
      .explode('Skill')
      .dropna(subset=['Skill'])
      .groupby(['Location', 'Skill'])
      .size()
      .reset_index(name='Count')
)

# Get top 5 skills per location
top_skills = (
    skill_counts.sort_values(['Location', 'Count'], ascending=[True, False])
                .groupby('Location')
                .head(5)
)

# Pivot for heatmap
pivot = top_skills.pivot(index='Location', columns='Skill', values='Count').fillna(0)

# Plot
plt.figure(figsize=(12, 7))
sns.heatmap(pivot, cmap='coolwarm', annot=True, fmt='.0f', linewidths=0.5)
plt.title('Top 5 In-Demand Skills by City', fontsize=16)
plt.xlabel('Skill')
plt.ylabel('Location')
plt.tight_layout()
plt.show()

top_companies = df['Company'].value_counts().head(10)
top_companies.plot(kind='barh', color='skyblue')
plt.title('Top 10 Companies Hiring')
plt.xlabel('Number of Listings')
plt.show()

df['Job Type'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Job Type Distribution')
plt.ylabel('')
plt.show()

top_skills = df['Skills'].str.split(', ').explode().value_counts().head()
sns.barplot(x=top_skills.values, y=top_skills.index, palette='mako')
plt.title('Most Demanded Skills in India')
plt.show()
