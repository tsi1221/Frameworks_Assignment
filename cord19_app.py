# cord19_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

sns.set_style("whitegrid")

# -------------------------------
# Title and Description
# -------------------------------
st.title("CORD-19 Data Explorer")
st.write("""
Explore COVID-19 research papers interactively using the CORD-19 metadata dataset.
Filter by year and visualize publication trends, top journals, and common words in titles.
""")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    # Drop rows without title or publish_time
    df = df.dropna(subset=['title', 'publish_time'])
    # Convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    # Extract year
    df['year'] = df['publish_time'].dt.year
    # Abstract word count
    df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
    return df

df = load_data()

# -------------------------------
# Interactive Filters
# -------------------------------
min_year = int(df['year'].min())
max_year = int(df['year'].max())

year_range = st.slider(
    "Select publication year range",
    min_year,
    max_year,
    (2020, 2021)
)

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader(f"Number of papers between {year_range[0]} and {year_range[1]}: {filtered_df.shape[0]}")

# -------------------------------
# Publications by Year Plot
# -------------------------------
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.set_title("Publications by Year")
st.pyplot(fig1)

# -------------------------------
# Top Journals Plot
# -------------------------------
st.subheader("Top Journals Publishing COVID-19 Papers")
top_journals = filtered_df['journal'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10,5))
top_journals.plot(kind='bar', color='salmon', ax=ax2)
ax2.set_xlabel("Journal")
ax2.set_ylabel("Number of Papers")
ax2.set_title("Top 10 Journals")
st.pyplot(fig2)

# -------------------------------
# Most Frequent Words in Titles
# -------------------------------
st.subheader("Top 20 Most Frequent Words in Titles")
titles = filtered_df['title'].dropna().str.lower().str.split()
all_words = [word for sublist in titles for word in sublist]
word_freq = Counter(all_words)
common_words = word_freq.most_common(20)

words, counts = zip(*common_words)
fig3, ax3 = plt.subplots(figsize=(12,5))
sns.barplot(x=list(words), y=list(counts), palette="viridis", ax=ax3)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
ax3.set_title("Top 20 Words in Titles")
st.pyplot(fig3)

# -------------------------------
# Sample Data Table
# -------------------------------
st.subheader("Sample Papers")
st.dataframe(filtered_df[['title', 'journal', 'year']].head(10))

# -------------------------------
# Distribution by Source
# -------------------------------
st.subheader("Paper Counts by Source")
fig4, ax4 = plt.subplots()
filtered_df['source_x'].value_counts().plot(kind='bar', color='lightgreen', ax=ax4)
ax4.set_xlabel("Source")
ax4.set_ylabel("Number of Papers")
ax4.set_title("Papers by Source")
st.pyplot(fig4)
