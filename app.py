
import streamlit as st
import pandas as pd

# Set page configuration with favicon
st.set_page_config(
    page_title="Body Clip Finder",
    page_icon="favicon.png",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Calibri', sans-serif;
            background-color: #FFFFFF;
            color: #000000;
        }
        .stSelectbox, .stTextInput {
            background-color: #BFBFBF;
        }
        .clip-card {
            background-color: #BFBFBF;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Load the Excel data
df = pd.read_excel(excel_file, sheet_name="Master", engine="openpyxl")

# Combine all OEM columns into one list for filtering
oem_columns = ['OEM 1', 'OEM 2', 'OEM 3', 'OEM 4']
df['OEM Brand'] = df[oem_columns].bfill(axis=1).iloc[:, 0]

# Sidebar filters
st.sidebar.header("Filter Clips")
selected_colour = st.sidebar.selectbox("Colour", sorted(df['Colour'].dropna().unique()))
selected_oem = st.sidebar.selectbox("OEM Brand", sorted(df['OEM Brand'].dropna().unique()))
selected_hole_size = st.sidebar.selectbox("Suit Hole Size", sorted(df['Suit Hole ø (mm)'].dropna().astype(str).unique()))
selected_clip_type = st.sidebar.selectbox("Body Clip Type", sorted(df['Clip Type'].dropna().unique()))

# Filter the dataframe
filtered_df = df[
    (df['Colour'] == selected_colour) &
    (df['OEM Brand'] == selected_oem) &
    (df['Suit Hole ø (mm)'].astype(str) == selected_hole_size) &
    (df['Clip Type'] == selected_clip_type)
]

# Display results
st.title("Matching Body Clips")

for _, row in filtered_df.iterrows():
    st.markdown(f"""
        <div class="clip-card">
            <h4>{row['Description']}</h4>
            <img src="{row['Image url']}" alt="Clip Image">
            <p><strong>Product Number:</strong> {row['Product number']}</p>
            <p><strong>Colour:</strong> {row['Colour']}</p>
            <p><strong>Clip Type:</strong> {row['Clip Type']}</p>
            <p><strong>Suit Hole Ø (mm):</strong> {row['Suit Hole ø (mm)']}</p>
            <p><strong>Working Length:</strong> {row['Working Length']}</p>
            <p><strong>Head Ø:</strong> {row['Head ø']}</p>
            <p><strong>OEM References:</strong> {', '.join([str(row[col]) for col in oem_columns if pd.notna(row[col])])}</p>
        </div>
    """, unsafe_allow_html=True)
