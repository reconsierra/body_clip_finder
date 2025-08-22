
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

# Initialise session state for filters
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "selected_colour" not in st.session_state:
    st.session_state.selected_colour = ""
if "selected_clip_type" not in st.session_state:
    st.session_state.selected_clip_type = ""
if "selected_hole_size" not in st.session_state:
    st.session_state.selected_hole_size = ""
if "selected_oem" not in st.session_state:
    st.session_state.selected_oem = ""

# Input widgets
st.session_state.search_text = st.sidebar.text_input("Search by Keyword", value=st.session_state.search_text)
st.session_state.selected_colour = st.sidebar.selectbox("Filter by Colour", [""] + sorted(df['Colour'].dropna().unique()), index=0)
st.session_state.selected_clip_type = st.sidebar.selectbox("Filter by Clip Type", [""] + sorted(df['Clip Type'].dropna().unique()), index=0)
st.session_state.selected_hole_size = st.sidebar.selectbox("Filter by Hole Size", [""] + sorted(df['Suit Hole ø (mm)'].dropna().astype(str).unique()), index=0)

# OEM dropdown
oem_names = pd.unique(df[oem_columns].values.ravel('K'))
oem_names = sorted([oem for oem in oem_names if pd.notna(oem)])
st.session_state.selected_oem = st.sidebar.selectbox("Filter by OEM Name", [""] + oem_names, index=0)

# Clear All button
if st.sidebar.button("Clear All"):
    st.session_state.search_text = ""
    st.session_state.selected_colour = ""
    st.session_state.selected_clip_type = ""
    st.session_state.selected_hole_size = ""
    st.session_state.selected_oem = ""
    st.experimental_rerun()


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

if selected_oem:
    filtered_df = filtered_df[df[oem_columns].apply(lambda row: selected_oem in row.values, axis=1)]

# Display results
st.title(f"Body Clip Finder ({len(filtered_df)})")

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
