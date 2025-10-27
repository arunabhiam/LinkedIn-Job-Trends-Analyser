import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="LinkedIn Job Trends", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_jobs.csv")
    return df


df = load_data()

st.title("💼 LinkedIn Job Trends Dashboard")
st.markdown("Explore trends in tech job postings across India")

# --- SIDEBAR ---
st.sidebar.header("🔍 Filters")
keywords = sorted(df['Keyword'].dropna().unique())
locations = sorted(df['Location'].dropna().unique())

selected_keyword = st.sidebar.multiselect("Select Keywords", keywords, default=keywords)
selected_location = st.sidebar.multiselect("Select Locations", locations, default="India")
intern_only = st.sidebar.checkbox("Show Internships Only", value=False)

filtered_df = df[(df['Keyword'].isin(selected_keyword)) & (df['Location'].isin(selected_location))]
if intern_only:
    filtered_df = filtered_df[filtered_df['is_internship'] == 1]

# --- METRICS CARDS ---
total_jobs = len(filtered_df)
intern_count = filtered_df['is_internship'].sum()
fulltime_count = total_jobs - intern_count

col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", total_jobs)
col2.metric("Internships", intern_count)
col3.metric("Full-time", fulltime_count)
col1, col2 = st.columns(2)

# Job Count by Keyword
with col1:
    job_count = filtered_df['Keyword'].value_counts().reset_index()
    job_count.columns = ['Keyword', 'Count']
    fig, ax = plt.subplots(figsize=(5,2.5))
    sns.barplot(data=job_count, x='Keyword', y='Count', palette='cool', ax=ax)
    ax.set_xlabel(""); ax.set_ylabel("Jobs")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right', fontsize=9)
    sns.despine(left=True, bottom=True)
    st.subheader("📊 Jobs by Keyword")
    st.pyplot(fig)

# Job Count by Location
with col2:
    loc_count = filtered_df['Location'].value_counts().reset_index()
    loc_count.columns = ['Location', 'Count']
    fig, ax = plt.subplots(figsize=(5,2.5))
    sns.barplot(data=loc_count, x='Location', y='Count', palette='crest', ax=ax)
    ax.set_xlabel(""); ax.set_ylabel("Jobs")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right', fontsize=9)
    sns.despine(left=True, bottom=True)
    st.subheader("📍 Jobs by Location")
    st.pyplot(fig)

# --- SECTION 3: Internship Ratio ---
st.subheader("🧑‍🎓 Internship vs Full-time")
intern_counts = filtered_df['is_internship'].value_counts()
fulltime_count = intern_counts.get(0, 0)
intern_count = intern_counts.get(1, 0)

fig, ax = plt.subplots(figsize=(3,3))  # small figure
ax.pie([fulltime_count, intern_count], labels=['Full-time', 'Internship'],
       autopct='%1.1f%%', startangle=90, colors=['#9b59b6','#3498db'], textprops={'fontsize':10})
ax.axis('equal')

st.pyplot(fig, use_container_width=False)


# --- Top 5 Skills Heatmap ---
st.subheader("🔥 Top Skills by City")
if 'Skills' in filtered_df.columns and filtered_df['Skills'].notnull().any():
    skill_counts = (
        filtered_df.assign(Skill=filtered_df['Skills'].str.split(', '))
        .explode('Skill')
        .groupby(['Location', 'Skill'])
        .size()
        .reset_index(name='Count')
    )
    top_skills = skill_counts.groupby('Skill')['Count'].sum().nlargest(5).index
    filtered_skills = skill_counts[skill_counts['Skill'].isin(top_skills)]
    pivot = filtered_skills.pivot_table(index='Skill', columns='Location', values='Count', fill_value=0)

    fig, ax = plt.subplots(figsize=(7,2.5))
    sns.heatmap(pivot, cmap='YlOrBr', annot=True, fmt=".0f", cbar=False, linewidths=.5,
                linecolor='gray', annot_kws={"size":8})
    ax.set_xlabel(""); ax.set_ylabel("")
    st.pyplot(fig)
else:
    st.info("No skill data available for selected filters 🫤")

st.subheader("📋 Job Listings")
def highlight_intern(row):
    return ['background-color: #d0f0fd' if row.is_internship==1 else '' for _ in row]

st.dataframe(filtered_df[['Title', 'Company', 'Location', 'Keyword', 'Job Type', 'is_internship', 'Link']].style.apply(highlight_intern, axis=1))

