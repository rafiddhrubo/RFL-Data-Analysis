import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="DE Line Operations Dashboard", layout="wide")

# Sidebar - Module Selection (Master Dashboard Navigation)
st.sidebar.title("📌 Operations Hub")
app_mode = st.sidebar.radio(
    "Select Analysis Module:",
    ["⏱️ NPT Analysis", "❌ Rejection Analysis", "🏭 Production Data", "📊 Master Summary"]
)

st.sidebar.markdown("---")
st.sidebar.header("📁 File Upload Area")

# -----------------------------------------------------------------------------
# MODULE 1: NPT ANALYSIS
# -----------------------------------------------------------------------------
if app_mode == "⏱️ NPT Analysis":
    st.title("⏱️ Non-Productive Time (NPT) Analysis Dashboard")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Daily NPT File (.xlsx or .csv)", 
        type=["xlsx", "xls", "csv"],
        key="npt_uploader"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                df_mc_mapping = None
            else:
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # Load MC ID mapping tab automatically if available
                if "MC ID" in sheet_names:
                    df_mc_mapping = pd.read_excel(uploaded_file, sheet_name="MC ID")
                else:
                    df_mc_mapping = None

                selected_sheet = st.sidebar.selectbox("Select Sheet/Tab to Analyze", sheet_names, index=0)
                df_raw = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

                if "Summary" in selected_sheet or "Mc Downtime Report" in str(df_raw.columns[0]):
                    df = df_raw.copy()
                    df.columns = df.iloc[0]
                    df = df[1:].reset_index(drop=True)
                    df = df.dropna(subset=["Cause"])
                else:
                    df = df_raw.copy()

            # Column Standardization
            column_mapping = {}
            for col in df.columns:
                str_col = str(col).strip().lower()
                if str_col in ['cause', 'downtime cause', 'npt cause']:
                    column_mapping[col] = 'Cause'
                elif str_col in ['hr', 'total hours', 'duration (in second)']:
                    column_mapping[col] = 'Hours'
                elif str_col in ['entry', 'entries', 'incidents']:
                    column_mapping[col] = 'Entry'
                elif str_col in ['machine', 'mc id', 'machine id']:
                    column_mapping[col] = 'MC ID'
                elif str_col in ['machine no.', 'mc number', 'mc no', 'mc no.']:
                    column_mapping[col] = 'MC Number'

            df = df.rename(columns=column_mapping)

            # Process MC ID and MC Number Mapping if Machine data is present
            if 'MC ID' in df.columns or 'MC Number' in df.columns:
                if df_mc_mapping is not None:
                    # Merge with master MC ID sheet if missing one of the columns
                    if 'MC ID' in df.columns and 'MC Number' not in df.columns:
                        df = df.merge(df_mc_mapping, left_on='MC ID', right_on='MC ID', how='left')
                    elif 'MC Number' in df.columns and 'MC ID' not in df.columns:
                        df = df.merge(df_mc_mapping, left_on='MC Number', right_on='MC Number', how='left')
                
                # Reorder columns to display MC ID and MC Number side-by-side
                cols = list(df.columns)
                if 'MC ID' in cols and 'MC Number' in cols:
                    cols.remove('MC ID')
                    cols.remove('MC Number')
                    df = df[['MC ID', 'MC Number'] + cols]

            # Numeric Conversions
            if 'Hours' in df.columns:
                df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce').fillna(0)
            if 'Entry' in df.columns:
                df['Entry'] = pd.to_numeric(df['Entry'], errors='coerce').fillna(0)

            # Filter valid records
            df_valid = df[df['Cause'].astype(str).str.lower() != 'nan'].copy()
            if 'Hours' in df_valid.columns:
                df_filtered = df_valid[df_valid['Hours'] > 0].sort_values(by='Hours', ascending=False)
            else:
                df_filtered = df_valid

            # Metrics Row
            st.subheader("📊 NPT Key Metrics")
            m1, m2, m3 = st.columns(3)
            
            total_npt = df_filtered['Hours'].sum() if 'Hours' in df_filtered.columns else 0
            total_entries = df_filtered['Entry'].sum() if 'Entry' in df_filtered.columns else len(df_filtered)
            top_cause = df_filtered.iloc[0]['Cause'] if not df_filtered.empty else "N/A"
            
            m1.metric("Total NPT Loss", f"{total_npt:.2f} Hours")
            m2.metric("Total Downtime Incidents", f"{int(total_entries)}")
            m3.metric("Top Downtime Cause", f"{top_cause}")

            st.markdown("---")

            # Top 10 Pareto Chart & Pie Chart
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📈 Top 10 NPT Causes Breakdown")
                df_top10 = df_filtered.head(10).copy()
                if 'Hours' in df_top10.columns:
                    fig = px.bar(
                        df_top10,
                        x='Cause',
                        y='Hours',
                        color='Hours',
                        text_auto='.1f',
                        title='Top 10 NPT Downtime Drivers (Hours)',
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🥧 Top 5 Loss Contribution")
                if 'Hours' in df_top10.columns:
                    fig_pie = px.pie(
                        df_top10.head(5),
                        names='Cause',
                        values='Hours',
                        hole=0.4
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            # Top 10 NPT Loss Summary Table with Explicit Ranking
            st.subheader("🏆 Top 10 NPT Loss Summary Ranking")
            
            df_top10_table = df_filtered.head(10).copy().reset_index(drop=True)
            df_top10_table.index = df_top10_table.index + 1  # 1-based index rank
            df_top10_table.index.name = "Rank"

            st.dataframe(df_top10_table, use_container_width=True)

        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.info("Please verify the uploaded file format.")
    else:
        st.info("👈 Please upload an NPT file in the sidebar to begin analysis.")

# -----------------------------------------------------------------------------
# MODULE 2: REJECTION ANALYSIS (Modular placeholder for expansion)
# -----------------------------------------------------------------------------
elif app_mode == "❌ Rejection Analysis":
    st.title("❌ Quality & Rejection Analysis Dashboard")
    uploaded_rejection_file = st.sidebar.file_uploader(
        "Upload Rejection File (.xlsx or .csv)", 
        type=["xlsx", "xls", "csv"],
        key="rej_uploader"
    )

    if uploaded_rejection_file is not None:
        df_rej = pd.read_excel(uploaded_rejection_file) if uploaded_rejection_file.name.endswith('.xlsx') else pd.read_csv(uploaded_rejection_file)
        st.subheader("Rejection Data Preview")
        st.dataframe(df_rej.head(), use_container_width=True)
    else:
        st.info("👈 Upload your Rejection Log File to view Quality Metrics.")

# -----------------------------------------------------------------------------
# MODULE 3: PRODUCTION DATA (Modular placeholder for expansion)
# -----------------------------------------------------------------------------
elif app_mode == "🏭 Production Data":
    st.title("🏭 Production Output & Efficiency Dashboard")
    uploaded_prod_file = st.sidebar.file_uploader(
        "Upload Production File (.xlsx or .csv)", 
        type=["xlsx", "xls", "csv"],
        key="prod_uploader"
    )

    if uploaded_prod_file is not None:
        df_prod = pd.read_excel(uploaded_prod_file) if uploaded_prod_file.name.endswith('.xlsx') else pd.read_csv(uploaded_prod_file)
        st.subheader("Production Data Preview")
        st.dataframe(df_prod.head(), use_container_width=True)
    else:
        st.info("👈 Upload your Daily Production Report to track line output.")

# -----------------------------------------------------------------------------
# MODULE 4: MASTER SUMMARY
# -----------------------------------------------------------------------------
elif app_mode == "📊 Master Summary":
    st.title("📊 Plant Executive Master Overview")
    st.markdown("""
    Welcome to the **DE Line Master Operations Center**. 
    Select individual analysis modules from the left navigation panel to upload and evaluate:
    * **⏱️ NPT Analysis:** Measure machine breakdowns, downtime causes, and top loss drivers.
    * **❌ Rejection Analysis:** Monitor quality scrap rates, defect types, and part rejections.
    * **🏭 Production Data:** Track target vs actual production volumes and line efficiency.
    """)
