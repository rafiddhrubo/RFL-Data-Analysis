import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit Configuration
st.set_page_config(page_title="Operations Hub - NPT & Performance", layout="wide")

# Master Master Navigation Bar
st.sidebar.title("📌 Operations Hub")
app_mode = st.sidebar.radio(
    "Select Analysis Module:",
    ["⏱️ NPT Analysis", "❌ Rejection Analysis", "🏭 Production Data", "📊 Master Summary"]
)

# Embedded MC Master Database (Mapped by Line)
MC_DATABASE = [
    {"MC ID": "BMM-05L-11", "MC Number": "BMM-A1", "Line": "BMM"},
    {"MC ID": "BMM-05L-04", "MC Number": "BMM-A2", "Line": "BMM"},
    {"MC ID": "BMM-05L-03", "MC Number": "BMM-A3", "Line": "BMM"},
    {"MC ID": "BMM-05L-06", "MC Number": "BMM-A4", "Line": "BMM"},
    {"MC ID": "BMM-05L-05", "MC Number": "BMM-A5", "Line": "BMM"},
    {"MC ID": "BMM-05L-16", "MC Number": "BMM-A6", "Line": "BMM"},
    {"MC ID": "IMM-250-69", "MC Number": "A1", "Line": "AB"},
    {"MC ID": "IMM-250-176", "MC Number": "A2", "Line": "AB"},
    {"MC ID": "IMM-250-171", "MC Number": "A3", "Line": "AB"},
    {"MC ID": "IMM-250-174", "MC Number": "A4", "Line": "AB"},
    {"MC ID": "IMM-250-68", "MC Number": "A5", "Line": "AB"},
    {"MC ID": "IMM-250-287", "MC Number": "B1", "Line": "AB"},
    {"MC ID": "IMM-250-164", "MC Number": "B2", "Line": "AB"},
    {"MC ID": "IMM-250-148", "MC Number": "B3", "Line": "AB"},
    {"MC ID": "IMM-250-165", "MC Number": "B4", "Line": "AB"},
    {"MC ID": "IMM-250-163", "MC Number": "B5", "Line": "AB"},
    {"MC ID": "IMM-250-127", "MC Number": "B6", "Line": "AB"},
    {"MC ID": "IMM-160-41", "MC Number": "B7", "Line": "AB"},
    {"MC ID": "IMM-160-25", "MC Number": "B8", "Line": "AB"},
    {"MC ID": "IMM-250-282", "MC Number": "B9", "Line": "AB"},
    {"MC ID": "IMM-250-166", "MC Number": "B10", "Line": "AB"},
    {"MC ID": "IMM-250-61", "MC Number": "C1", "Line": "CD"},
    {"MC ID": "IMM-250-147", "MC Number": "C2", "Line": "CD"},
    {"MC ID": "IMM-250-21", "MC Number": "C3", "Line": "CD"},
    {"MC ID": "IMM-250-121", "MC Number": "C4", "Line": "CD"},
    {"MC ID": "IMM-250-123", "MC Number": "C5", "Line": "CD"},
    {"MC ID": "IMM-250-67", "MC Number": "C6", "Line": "CD"},
    {"MC ID": "IMM-120-88", "MC Number": "C7", "Line": "CD"},
    {"MC ID": "IMM-250-125", "MC Number": "C8", "Line": "CD"},
    {"MC ID": "IMM-120-58", "MC Number": "C9", "Line": "CD"},
    {"MC ID": "IMM-160-56", "MC Number": "C10", "Line": "CD"},
    {"MC ID": "IMM-120-31", "MC Number": "C11", "Line": "CD"},
    {"MC ID": "IMM-160-55", "MC Number": "C12", "Line": "CD"},
    {"MC ID": "IMM-250-120", "MC Number": "D1", "Line": "CD"},
    {"MC ID": "IMM-250-126", "MC Number": "D2", "Line": "CD"},
    {"MC ID": "IMM-250-124", "MC Number": "D3", "Line": "CD"},
    {"MC ID": "IMM-250-122", "MC Number": "D4", "Line": "CD"},
    {"MC ID": "IMM-250-172", "MC Number": "D5", "Line": "CD"},
    {"MC ID": "IMM-90-5", "MC Number": "D6", "Line": "DE"},
    {"MC ID": "IMM-250-175", "MC Number": "D7", "Line": "DE"},
    {"MC ID": "IMM-250-79", "MC Number": "D8", "Line": "DE"},
    {"MC ID": "IMM-160-34", "MC Number": "D9", "Line": "DE"},
    {"MC ID": "IMM-160-35", "MC Number": "D10", "Line": "DE"},
    {"MC ID": "IMM-120-85", "MC Number": "D11", "Line": "DE"},
    {"MC ID": "IMM-160-42", "MC Number": "D12", "Line": "DE"},
    {"MC ID": "IMM-250-180", "MC Number": "E1", "Line": "DE"},
    {"MC ID": "IMM-250-179", "MC Number": "E2", "Line": "DE"},
    {"MC ID": "IMM-250-131", "MC Number": "E3", "Line": "DE"},
    {"MC ID": "IMM-250-151", "MC Number": "E4", "Line": "DE"},
    {"MC ID": "IMM-250-157", "MC Number": "E5", "Line": "DE"},
    {"MC ID": "IMM-90-2", "MC Number": "E6", "Line": "DE"},
    {"MC ID": "IMM-90-1", "MC Number": "E7", "Line": "DE"},
    {"MC ID": "IMM-160-69", "MC Number": "E8", "Line": "DE"},
    {"MC ID": "IMM-250-138", "MC Number": "E9", "Line": "DE"},
    {"MC ID": "IMM-250-6", "MC Number": "E10", "Line": "DE"},
    {"MC ID": "IMM-160-68", "MC Number": "E11", "Line": "DE"},
    {"MC ID": "IMM-160-71", "MC Number": "E12", "Line": "DE"},
    {"MC ID": "IMM-250-286", "MC Number": "F1", "Line": "FG"},
    {"MC ID": "IMM-250-97", "MC Number": "F2", "Line": "FG"},
    {"MC ID": "IMM-250-14", "MC Number": "F3", "Line": "FG"},
    {"MC ID": "IMM-250-60", "MC Number": "F4", "Line": "FG"},
    {"MC ID": "IMM-260-2", "MC Number": "F5", "Line": "FG"},
    {"MC ID": "IMM-250-18", "MC Number": "F6", "Line": "FG"},
    {"MC ID": "IMM-250-15", "MC Number": "F7", "Line": "FG"},
    {"MC ID": "IMM-250-16", "MC Number": "F8", "Line": "FG"},
    {"MC ID": "IMM-250-208", "MC Number": "F9", "Line": "FG"},
    {"MC ID": "IMM-160-70", "MC Number": "F10", "Line": "FG"},
    {"MC ID": "IMM-160-85", "MC Number": "F11", "Line": "FG"},
    {"MC ID": "IMM-250-47", "MC Number": "G1", "Line": "FG"},
    {"MC ID": "IMM-250-74", "MC Number": "G2", "Line": "FG"},
    {"MC ID": "IMM-160-73", "MC Number": "G3", "Line": "FG"},
    {"MC ID": "IMM-160-78", "MC Number": "G4", "Line": "FG"},
    {"MC ID": "IMM-250-284", "MC Number": "G5", "Line": "FG"},
    {"MC ID": "IMM-160-81", "MC Number": "G6", "Line": "FG"},
    {"MC ID": "IMM-160-72", "MC Number": "G7", "Line": "FG"},
    {"MC ID": "IMM-160-77", "MC Number": "G8", "Line": "FG"}
]
df_mc_master = pd.DataFrame(MC_DATABASE)

def parse_mc_wise_sheet(df_raw):
    """Parses wide 'MC Wise' grid tab into a clean long format dataframe."""
    records = []
    cols = df_raw.columns
    for i in range(4, len(cols), 2):
        mc_id = cols[i]
        if pd.isna(mc_id) or "Unnamed" in str(mc_id):
            continue
        mc_number = df_raw.iloc[0, i]
        
        for r in range(2, len(df_raw)):
            cause = df_raw.iloc[r, 0]
            if pd.isna(cause) or str(cause).strip().lower() == "total":
                continue
            entry = df_raw.iloc[r, i]
            hr = df_raw.iloc[r, i+1]
            try:
                entry = float(entry) if not pd.isna(entry) else 0.0
                hr = float(hr) if not pd.isna(hr) else 0.0
            except:
                entry, hr = 0.0, 0.0
                
            if hr > 0 or entry > 0:
                records.append({
                    'MC ID': str(mc_id).strip(),
                    'MC Number': str(mc_number).strip(),
                    'Cause': str(cause).strip(),
                    'Entry': entry,
                    'Hours': hr
                })
    df_long = pd.DataFrame(records)
    if not df_long.empty:
        df_long = df_long.merge(df_mc_master[['MC ID', 'Line']], on='MC ID', how='left')
    return df_long

# -----------------------------------------------------------------------------
# MODULE 1: NPT ANALYSIS
# -----------------------------------------------------------------------------
if app_mode == "⏱️ NPT Analysis":
    st.title("⏱️ NPT Analysis Dashboard (MC Wise & Line Performance)")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Daily NPT File (.xlsx or .csv)", 
        type=["xlsx", "xls", "csv"],
        key="npt_uploader"
    )

    if uploaded_file is not None:
        try:
            df_parsed = pd.DataFrame()
            
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
                df_parsed = df_raw
            else:
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # Check for MC Wise tab or raw Data tab
                if "MC Wise" in sheet_names:
                    df_mcwise_raw = pd.read_excel(uploaded_file, sheet_name="MC Wise")
                    df_parsed = parse_mc_wise_sheet(df_mcwise_raw)
                else:
                    selected_sheet = st.sidebar.selectbox("Select Sheet/Tab to Analyze", sheet_names, index=0)
                    df_raw = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                    df_parsed = df_raw

            # Ensure columns are normalized
            if 'Machine' in df_parsed.columns and 'MC ID' not in df_parsed.columns:
                df_parsed['MC ID'] = df_parsed['Machine']
            
            if 'MC ID' in df_parsed.columns:
                # Merge master MC ID & Line mappings
                df_parsed = df_parsed.merge(df_mc_master, on='MC ID', how='left', suffixes=('', '_master'))
                if 'MC Number_master' in df_parsed.columns:
                    df_parsed['MC Number'] = df_parsed['MC Number_master']
                if 'Line_master' in df_parsed.columns:
                    df_parsed['Line'] = df_parsed['Line_master']

            # Make sure numeric fields exist
            if 'Hours' in df_parsed.columns:
                df_parsed['Hours'] = pd.to_numeric(df_parsed['Hours'], errors='coerce').fillna(0)
            elif 'HR' in df_parsed.columns:
                df_parsed['Hours'] = pd.to_numeric(df_parsed['HR'], errors='coerce').fillna(0)

            # Filter out zero hour entries
            df_filtered = df_parsed[df_parsed['Hours'] > 0].copy()

            # --- TOP 10 NPT SUMMARY TABLE (RANKED BY HOURS HIGHEST TO LOWEST) ---
            st.subheader("🏆 Top 10 NPT Loss Summary Ranking (MC Wise)")
            
            # Sort from highest to lowest hours
            df_top10 = df_filtered.sort_values(by="Hours", ascending=False).head(10).copy()
            
            total_loss_hours = df_filtered['Hours'].sum()
            df_top10['%'] = (df_top10['Hours'] / total_loss_hours * 100).map('{:.2f}%'.format) if total_loss_hours > 0 else "0.00%"
            df_top10['Hours'] = df_top10['Hours'].round(2)

            # Format final table columns
            df_top10_table = df_top10.reset_index(drop=True)
            df_top10_table.index = df_top10_table.index + 1
            df_top10_table.index.name = "Rank"

            display_cols = ['Cause', 'Hours', '%', 'MC Number', 'MC ID', 'Line']
            avail_cols = [c for c in display_cols if c in df_top10_table.columns]

            st.dataframe(df_top10_table[avail_cols], use_container_width=True)

            st.markdown("---")

            # --- SEPARATE ANALYSIS & GRAPH FOR DE LINE ---
            st.header("⚡ DE Line NPT Dedicated Analysis")
            st.caption("Machines: D6 to D12 (IMM-90-5 to IMM-160-42) & E1 to E12 (IMM-250-180 to IMM-160-71)")

            df_de_line = df_filtered[df_filtered['Line'] == 'DE'].copy()

            if not df_de_line.empty:
                col_de1, col_de2 = st.columns([2, 1])

                with col_de1:
                    st.subheader("📊 DE Line NPT Loss by Machine Number")
                    fig_de_bar = px.bar(
                        df_de_line.groupby(['MC Number', 'Cause'])['Hours'].sum().reset_index(),
                        x='MC Number',
                        y='Hours',
                        color='Cause',
                        title="DE Line NPT Loss Distribution across Machines (D6 - E12)",
                        text_auto='.1f',
                        barmode='stack'
                    )
                    st.plotly_chart(fig_de_bar, use_container_width=True)

                with col_de2:
                    st.subheader("🥧 DE Line Top Loss Causes")
                    df_de_cause = df_de_line.groupby('Cause')['Hours'].sum().reset_index().sort_values(by='Hours', ascending=False)
                    fig_de_pie = px.pie(
                        df_de_cause.head(5),
                        names='Cause',
                        values='Hours',
                        hole=0.4,
                        title="DE Line Top Downtime Causes"
                    )
                    st.plotly_chart(fig_de_pie, use_container_width=True)

                # DE Line Specific Summary Table
                st.subheader("📋 DE Line NPT Incident Log Table")
                df_de_summary = df_de_line.sort_values(by="Hours", ascending=False).reset_index(drop=True)
                df_de_summary.index = df_de_summary.index + 1
                df_de_summary.index.name = "Rank"
                st.dataframe(df_de_summary[avail_cols], use_container_width=True)

            else:
                st.warning("No DE Line NPT loss incidents detected in the uploaded file.")

        except Exception as e:
            st.error(f"Error parsing NPT file: {e}")
            st.info("Make sure your Excel file contains 'MC Wise' or standard data columns.")
    else:
        st.info("👈 Upload your daily NPT Excel report in the sidebar to generate analysis.")

# -----------------------------------------------------------------------------
# MODULE 2: REJECTION ANALYSIS
# -----------------------------------------------------------------------------
elif app_mode == "❌ Rejection Analysis":
    st.title("❌ Rejection & Scrap Analysis Module")
    st.info("Upload Rejection log files here to analyze scrap rate and defect causes.")

# -----------------------------------------------------------------------------
# MODULE 3: PRODUCTION DATA
# -----------------------------------------------------------------------------
elif app_mode == "🏭 Production Data":
    st.title("🏭 Production Output Module")
    st.info("Upload Production log files here to analyze hourly output and targets.")

# -----------------------------------------------------------------------------
# MODULE 4: MASTER SUMMARY
# -----------------------------------------------------------------------------
elif app_mode == "📊 Master Summary":
    st.title("📊 Master Executive Summary Dashboard")
    st.markdown("Consolidated multi-file view across NPT, Quality, and Production.")
