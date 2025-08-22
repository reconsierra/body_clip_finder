
import streamlit as st
import pandas as pd

# Page config for iPhone 14 screen
st.set_page_config(page_title="Body Clip Finder", layout="wide")

# Load data
df = pd.read_excel("Body Clip App Data 1.xlsx", sheet_name="Master", engine="openpyxl")

# Combine OEM columns into one string column
oem_columns = ['OEM 1', 'OEM 2', 'OEM 3', 'OEM 4']
df['OEM Combined'] = df[oem_columns].fillna('').astype(str).agg(' '.join, axis=1)

# Sidebar filters with clear labels
st.sidebar.header("🔍 Search and Filter Clips")
search_text = st.sidebar.text_input("Search by Keyword")
selected_colour = st.sidebar.selectbox("Filter by Colour", [""] + sorted(df['Colour'].dropna().unique().tolist()))
selected_clip_type = st.sidebar.selectbox("Filter by Clip Type", [""] + sorted(df['Clip Type'].dropna().unique().tolist()))
selected_hole_size = st.sidebar.selectbox("Filter by Hole Size", [""] + sorted(df['Suit Hole ø (mm)'].dropna().astype(str).unique().tolist()))

# Clear All button
if st.sidebar.button("Clear All"):
    search_text = ""
    selected_colour = ""
    selected_clip_type = ""
    selected_hole_size = ""

# Filter logic
filtered_df = df.copy()

if search_text:
    search_text_lower = search_text.lower()
    filtered_df = filtered_df[filtered_df.apply(lambda row: search_text_lower in str(row.values).lower(), axis=1)]

if selected_colour:
    filtered_df = filtered_df[filtered_df['Colour'] == selected_colour]

if selected_clip_type:
    filtered_df = filtered_df[filtered_df['Clip Type'] == selected_clip_type]

if selected_hole_size:
    filtered_df = filtered_df[df['Suit Hole ø (mm)'].astype(str) == selected_hole_size]

# Display results
st.title("📎 Matching Body Clips")

for _, row in filtered_df.iterrows():
    st.markdown(f'''
    <div style="background-color:#f0f0f0;padding:10px;margin-bottom:10px;border-radius:8px">
        <h4>{row['Description']}</h4>
        <img src="{row['Image url']}" width="200">
        <p><strong>Product Number:</strong> {row['Product number']}</p>
        <p><strong>Colour:</strong> {row['Colour']}</p>
        <p><strong>Clip Type:</strong> {row['Clip Type']}</p>
        <p><strong>Suit Hole ø (mm):</strong> {row['Suit Hole ø (mm)']}</p>
        <p><strong>Working Length:</strong> {row['Working Length']}</p>
        <p><strong>Head ø:</strong> {row['Head ø']}</p>
        <p><strong>OEM References:</strong> {row['OEM Combined']}</p>
    </div>
    ''', unsafe_allow_html=True)
