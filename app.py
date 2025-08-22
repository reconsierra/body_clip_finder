
import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Body Clip Finder",
    page_icon="favicon.png",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
        body, html, .reportview-container {
            font-family: 'Calibri', sans-serif;
            background-color: #FFFFFF;
            color: #000000;
        }
        .stSelectbox label, .stTextInput label {
            color: #737373;
        }
        .stButton>button {
            background-color: #CC0000;
            color: #FFFFFF;
        }
        .card {
            background-color: #BFBFBF;
            padding: 1em;
            margin-bottom: 1em;
            border-radius: 8px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_excel("Body Clip App Data.xlsx", sheet_name="Master", engine="openpyxl")

# Combine OEM columns into one list for filtering
oem_columns = ['OEM 1', 'OEM 2', 'OEM 3', 'OEM 4']
df['OEM Combined'] = df[oem_columns].fillna('').agg(' '.join, axis=1)

# Sidebar filters

selected_oem_name = st.sidebar.selectbox("OEM Name", ['AUDI', 'BMW', 'CITROEN', 'DAIHATSU', 'DATSUN', 'FORD', 'GM', 'HOLDEN', 'HONDA', 'HYUNDAI', 'KIA', 'LEXUS', 'MAZDA', 'MERCEDES BENZ', 'MITSUBISHI', 'NISSAN', 'PEOGEOT', 'RENAULT', 'SUBARU', 'SUZUKI', 'TOYOTA', 'UNIVERSAL', 'VW'])
st.sidebar.header("Filter Clips")
selected_colour = st.sidebar.selectbox("Colour", sorted(df['Colour'].dropna().unique()))
selected_oem = st.sidebar.selectbox("OEM Brand", sorted(pd.
# Apply OEM name filter
if selected_oem_name:
    df = df[df[oem_columns].apply(lambda row: selected_oem_name in row.values, axis=1)]
Series(df[oem_columns].values.ravel()).dropna().unique()))
selected_hole_size = st.sidebar.selectbox("Suit Hole Size", sorted(df['Suit Hole ø (mm)'].dropna().astype(str).unique()))
selected_clip_type = st.sidebar.selectbox("Body Clip Type", sorted(df['Clip Type'].dropna().unique()))

# Filter data
filtered_df = df[
    (df['Colour'] == selected_colour) &
    (df[oem_columns].apply(lambda row: selected_oem in row.values, axis=1)) &
    (df['Suit Hole ø (mm)'].astype(str) == selected_hole_size) &
    (df['Clip Type'] == selected_clip_type)
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
            <p><strong>Clip Type:</strong> {row['Clip Type']}</p>
            <p><strong>Suit Hole Ø (mm):</strong> {row['Suit Hole ø (mm)']}</p>
            <p><strong>Working Length:</strong> {row['Working Length']}</p>
            <p><strong>Head Ø:</strong> {row['Head ø']}</p>
            <p><strong>OEM References:</strong> {row['OEM Combined']}</p>
        </div>
    """, unsafe_allow_html=True)
