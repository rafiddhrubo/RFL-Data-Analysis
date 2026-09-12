import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit Page Setup
st.set_page_config(page_title="NPT Downtime Dashboard", layout="wide")

st.title("🏭 Plastic-7.2 Daily NPT Analysis Dashboard")
st.caption("Upload daily Excel downtime reports to calculate losses, top causes, and machine breakdowns.")

# Sidebar File Uploader
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Daily NPT File (.xlsx or .csv)", 
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            
            # Allow user to pick sheet if multiple exist
            selected_sheet = st.sidebar.selectbox("Select Sheet/Tab to Analyze", sheet_names, index=0)
            df_raw = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            
            # Format detection for structured 'Summary' tabs vs raw 'Data' tabs
            if "Summary" in selected_sheet or "Mc Downtime Report" in str(df_raw.columns[0]):
                df = df_raw.copy()
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
                df = df.dropna(subset=["Cause"])
            else:
                df = df_raw.copy()

        # Data Cleaning & Normalization
        # Renaming columns for uniform processing
        column_mapping = {}
        for col in df.columns:
            str_col = str(col).strip()
            if str_col.lower() in ['cause', 'downtime cause', 'npt cause']:
                column_mapping[col] = 'Cause'
            elif str_col.lower() in ['hr', 'total hours', 'duration (in second)', 'total hours']:
                column_mapping[col] = 'Hours'
            elif str_col.lower() in ['entry', 'entries', 'incidents']:
                column_mapping[col] = 'Entry'
        
        df = df.rename(columns=column_mapping)

        # Convert numerical columns safely
        if 'Hours' in df.columns:
            # Handle duration in seconds if raw logs uploaded
            if "Duration (In Second)" in df.columns or df['Hours'].mean() > 500:
                df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce') / 3600.0
            else:
                df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
        
        if 'Entry' in df.columns:
            df['Entry'] = pd.to_numeric(df['Entry'], errors='coerce')

        # Filter out invalid rows (Totals or 0-hour entries)
        df_valid = df[df['Cause'].astype(str).str.lower() != 'nan'].copy()
        if 'Hours' in df_valid.columns:
            df_filtered = df_valid[df_valid['Hours'] > 0].sort_values(by='Hours', ascending=False)
        else:
            df_filtered = df_valid

        # Overview Key Metrics
        st.subheader("📊 Key Performance Metrics")
        m1, m2, m3 = st.columns(3)
        
        total_npt = df_filtered['Hours'].sum() if 'Hours' in df_filtered.columns else 0
        total_entries = df_filtered['Entry'].sum() if 'Entry' in df_filtered.columns else len(df_filtered)
        top_cause = df_filtered.iloc[0]['Cause'] if not df_filtered.empty else "N/A"
        
        m1.metric("Total NPT Downtime Loss", f"{total_npt:.2f} Hours")
        m2.metric("Total Downtime Incidents", f"{int(total_entries)}")
        m3.metric("Top Loss Contributor", f"{top_cause}")

        st.markdown("---")

        # Visualizations
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("📉 Pareto Downtime Loss Distribution")
            if 'Hours' in df_filtered.columns:
                fig = px.bar(
                    df_filtered,
                    x='Cause',
                    y='Hours',
                    color='Hours',
                    color_continuous_scale='Reds',
                    title='Non-Productive Time (NPT) by Cause (Hours)',
                    labels={'Hours': 'Lost Hours', 'Cause': 'Downtime Cause'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("🥧 Downtime Share (%)")
            if 'Hours' in df_filtered.columns:
                fig_pie = px.pie(
                    df_filtered.head(7), 
                    names='Cause', 
                    values='Hours',
                    title='Top Loss Drivers Share'
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # Detailed Data Breakdown Table
        st.subheader("📋 Top NPT Loss Summary")
        st.dataframe(df_filtered, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file structure: {e}")
        st.info("Ensure your file follows the standard format or select the correct tab from the sidebar.")

else:
    st.info("👈 Upload your daily NPT report (Excel or CSV) using the sidebar to run the analysis.")
