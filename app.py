
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Body Clip Finder",
    page_icon="favicon.png",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Calibri&display=swap');
        html, body, [class*="css"] {
            font-family: 'Calibri', sans-serif;
            background-color: #FFFFFF;
            color: #000000;
        }
        .card {
            background-color: #BFBFBF;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .card img {
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_excel("Body Clip App Data.xlsx", sheet_name="Master", engine="openpyxl")
df['Colour'] = df['Colour'].astype(str)
df['Suit Hole ø (mm)'] = df['Suit Hole ø (mm)'].astype(str)
df['Clip Type.1'] = df['Clip Type.1'].astype(str)
oem_columns = ['OEM 1', 'OEM 2', 'OEM 3', 'OEM 4']
df['OEM Combined'] = df[oem_columns].fillna('').agg(','.join, axis=1)
df['OEM Combined'] = df['OEM Combined'].str.replace(',,', ',').str.strip(',')

# Extract unique OEM brands
oem_values = set()
for col in oem_columns:
    oem_values.update(df[col].dropna().astype(str).unique())
oem_values = sorted(oem_values)

# Sidebar filters
st.sidebar.header("Filter Clips")
selected_colour = st.sidebar.selectbox("Colour", sorted(df['Colour'].dropna().unique()))
selected_oem = st.sidebar.selectbox("OEM Brand", oem_values)
selected_hole_size = st.sidebar.selectbox("Suit Hole Size", sorted(df['Suit Hole ø (mm)'].dropna().unique()))
selected_clip_type = st.sidebar.selectbox("Body Clip Type", sorted(df['Clip Type.1'].dropna().unique()))

# Filter data
filtered_df = df[
    (df['Colour'] == selected_colour) &
    (df['Suit Hole ø (mm)'] == selected_hole_size) &
    (df['Clip Type.1'] == selected_clip_type) &
    (df['OEM Combined'].str.contains(selected_oem))
]

# Display results
st.title("Matching Body Clips")
for _, row in filtered_df.iterrows():
    st.markdown(f"""
    <div class="card">
        <h4>{row['Description']}</h4>
        <img src="{row['Image url']}" alt="Clip Image">
        <p><strong>Product Number:</strong> {row['Product number']}</p>
        <p><strong>Colour:</strong> {row['Colour']}</p>
        <p><strong>Clip Type:</strong> {row['Clip Type.1']}</p>
        <p><strong>Suit Hole Ø (mm):</strong> {row['Suit Hole ø (mm)']}</p>
        <p><strong>Working Length:</strong> {row['Working Length']}</p>
        <p><strong>Head Ø:</strong> {row['Head ø']}</p>
        <p><strong>OEM References:</strong> {row['OEM Combined']}</p>
    </div>
    """, unsafe_allow_html=True)
