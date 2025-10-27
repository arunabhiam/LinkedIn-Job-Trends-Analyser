# cleaner.py
import pandas as pd
import re

skills_list = ['Python', 'SQL', 'Machine Learning', 'Excel', 'Power BI',
               'Tableau', 'Communication', 'AWS', 'Deep Learning', 'Statistics']

def extract_skills(description):
    found = [skill for skill in skills_list if re.search(rf"\b{skill}\b", description, re.IGNORECASE)]
    return ', '.join(found)

df = pd.read_csv('../data/raw_jobs.csv')

df['Skills'] = df['Title'].apply(extract_skills)

df.to_csv('../data/cleaned_jobs.csv', index=False)
print("🧹 Cleaned job data saved to data/cleaned_jobs.csv")


# Load cleaned dataset
df = pd.read_csv('../data/cleaned_jobs.csv')

# --- Internship flag ---
df['is_internship'] = df['Title'].apply(
    lambda x: 1 if re.search(r'\bintern\b|\binternship\b', str(x), re.IGNORECASE) else 0
)

# --- Remote flag ---
df['is_remote'] = df.apply(
    lambda row: 1 if re.search(r'\bremote\b|\bwork\s*from\s*home\b|\bhybrid\b', f"{row['Title']} {row['Location']}", re.IGNORECASE)
    else 0,
    axis=1
)

df.to_csv('../data/cleaned_jobs.csv', index=False)

print("✅ Added columns 'Is_Internship' and 'Is_Remote' successfully!")
print("\nInternship distribution:\n", df['is_internship'].value_counts())
print("\nRemote job distribution:\n", df['is_remote'].value_counts())

