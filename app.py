import streamlit as st
import pandas as pd

st.set_page_config(page_title="Body Clip Finder", layout="wide")

# Load data
df = pd.read_excel("Body Clip App Data 1.xlsx", sheet_name="Master", engine="openpyxl")

# Combine OEM columns
oem_columns = ['OEM 1', 'OEM 2', 'OEM 3', 'OEM 4', 'OEM # 1', 'OEM # 2', 'OEM # 3', 'OEM # 4', 'OEM # 5']
df[oem_columns] = df[oem_columns].fillna('').astype(str)
df['OEM Combined'] = df[oem_columns].agg(' '.join, axis=1)
df['search_str'] = df.astype(str).agg(' '.join, axis=1).str.lower()

# Sidebar filters
st.sidebar.header("Filter Clips")
search_text = st.sidebar.text_input("Search all fields")
selected_colour = st.sidebar.selectbox("Colour", [""] + sorted(df['Colour'].dropna().unique().tolist()))
selected_clip_type = st.sidebar.selectbox("Body Clip Type", [""] + sorted(df['Clip Type'].dropna().unique().tolist()))
selected_hole_size = st.sidebar.selectbox("Suit Hole Size", [""] + sorted(df['Suit Hole ø (mm)'].dropna().astype(str).unique().tolist()))

if st.sidebar.button("Clear All"):
    st.experimental_rerun()

# Filter logic
filtered_df = df.copy()
if search_text:
    filtered_df = filtered_df[filtered_df['search_str'].str.contains(search_text.lower())]
if selected_colour:
    filtered_df = filtered_df[filtered_df['Colour'] == selected_colour]
if selected_clip_type:
    filtered_df = filtered_df[filtered_df['Clip Type'] == selected_clip_type]
if selected_hole_size:
    filtered_df = filtered_df[df['Suit Hole ø (mm)'].astype(str) == selected_hole_size]

# Display results
st.title("Body Clip Finder")
for _, row in filtered_df.iterrows():
    st.markdown(f"""
    <div style='background-color:#f0f0f0;padding:10px;margin-bottom:10px;border-radius:10px'>
        <h4>{row['Description']}</h4>
        <img src="{row['Image url']}" width="200"><br>
        <b>Product Number:</b> {row['Product number']}<br>
        <b>Colour:</b> {row['Colour']}<br>
        <b>Clip Type:</b> {row['Clip Type']}<br>
        <b>Suit Hole ø (mm):</b> {row['Suit Hole ø (mm)']}<br>
        <b>Working Length:</b> {row['Working Length']}<br>
        <b>Head ø:</b> {row['Head ø']}<br>
        <b>OEM References:</b> {row['OEM Combined']}
    </div>
    """, unsafe_allow_html=True)
