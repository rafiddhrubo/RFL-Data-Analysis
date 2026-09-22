import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE SETUP & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operations Hub - Downtime & Performance",
    page_icon="⚙️",
    layout="wide",
)

# Custom Styling for Streamlit Elements
st.markdown(
    """
    <style>
    .main .block-container { padding-top: 1.5rem; }
    div[data-testid="stMetricValue"] { font-size: 26px; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# Master Navigation Bar
st.sidebar.title("📌 Operations Hub")
app_mode = st.sidebar.radio(
    "Select Main Module:",
    [
        "⏱️ NPT Analysis",
        "📈 NPT Progress Comparison",
        "❌ Rejection Analysis",
        "🏭 Production Data",
        "📊 Master Summary",
    ],
)

# -----------------------------------------------------------------------------
# MASTER MACHINE DATABASE
# -----------------------------------------------------------------------------
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
    {"MC ID": "IMM-160-77", "MC Number": "G8", "Line": "FG"},
]
df_mc_master = pd.DataFrame(MC_DATABASE)


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
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
            hr = df_raw.iloc[r, i + 1]
            try:
                entry = float(entry) if not pd.isna(entry) else 0.0
                hr = float(hr) if not pd.isna(hr) else 0.0
            except:
                entry, hr = 0.0, 0.0

            if hr > 0 or entry > 0:
                records.append({
                    "MC ID": str(mc_id).strip(),
                    "MC Number": str(mc_number).strip(),
                    "Cause": str(cause).strip(),
                    "Entry": entry,
                    "Hours": hr,
                })
    df_long = pd.DataFrame(records)
    if not df_long.empty:
        df_long = df_long.merge(
            df_mc_master[["MC ID", "Line"]], on="MC ID", how="left"
        )
    return df_long


def parse_data_sheet(df_raw):
    """Parses row-by-row transaction log 'Data' tab."""
    df_data = df_raw.dropna(subset=["Machine", "Cause"]).copy()

    # Extract or calculate Hours
    if "Duration (In Second)" in df_data.columns:
        df_data["Hours"] = (
            pd.to_numeric(df_data["Duration (In Second)"], errors="coerce")
            / 3600.0
        )
    elif "Duration" in df_data.columns:
        df_data["Hours"] = pd.to_timedelta(
            df_data["Duration"].astype(str), errors="coerce"
        ).dt.total_seconds() / 3600.0

    # Parse Date column using new helper column 'Date'
    if "Date" in df_data.columns:
        df_data["Date"] = pd.to_datetime(
            df_data["Date"], errors="coerce"
        ).dt.date
    elif "From Time" in df_data.columns:
        df_data["Date"] = pd.to_datetime(
            df_data["From Time"], errors="coerce"
        ).dt.date
    elif "Added Date" in df_data.columns:
        df_data["Date"] = pd.to_datetime(
            df_data["Added Date"], errors="coerce"
        ).dt.date

    df_data["MC ID"] = df_data["Machine"].astype(str).str.strip()
    df_data["Entry"] = 1.0

    return df_data


def generate_unique_mc_summary(df_input):
    """Groups data strictly by Machine so each MC Number appears exactly ONCE."""
    results = []
    total_all_hrs = df_input["Hours"].sum()

    for (mc_num, mc_id, line), group in df_input.groupby(
        ["MC Number", "MC ID", "Line"]
    ):
        tot_hrs = group["Hours"].sum()
        sorted_group = group.sort_values(by="Hours", ascending=False)
        top_cause = sorted_group.iloc[0]["Cause"]
        all_causes = ", ".join(sorted_group["Cause"].unique().tolist())

        results.append({
            "MC Number": mc_num,
            "MC ID": mc_id,
            "Line": line,
            "Cumulative Hours": round(tot_hrs, 2),
            "%": (
                f"{(tot_hrs / total_all_hrs * 100):.2f}%"
                if total_all_hrs > 0
                else "0.00%"
            ),
            "Primary Cause": top_cause,
            "All Downtime Causes": all_causes,
        })

    res_df = (
        pd.DataFrame(results)
        .sort_values(by="Cumulative Hours", ascending=False)
        .reset_index(drop=True)
    )
    res_df.index = res_df.index + 1
    res_df.index.name = "Rank"
    return res_df


# -----------------------------------------------------------------------------
# SHARED FILE UPLOADER & DATA LOADING
# -----------------------------------------------------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload NPT Report (.xlsx or .csv)",
    type=["xlsx", "xls", "csv"],
    key="npt_uploader",
)

df_parsed = pd.DataFrame()
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_parsed = pd.read_csv(uploaded_file)
        else:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names

            if "Data" in sheet_names:
                df_data_raw = pd.read_excel(uploaded_file, sheet_name="Data")
                df_parsed = parse_data_sheet(df_data_raw)
            elif "MC Wise" in sheet_names:
                df_mcwise_raw = pd.read_excel(
                    uploaded_file, sheet_name="MC Wise"
                )
                df_parsed = parse_mc_wise_sheet(df_mcwise_raw)
            else:
                selected_sheet = st.sidebar.selectbox(
                    "Select Sheet/Tab to Analyze", sheet_names, index=0
                )
                df_raw = pd.read_excel(
                    uploaded_file, sheet_name=selected_sheet
                )
                df_parsed = df_raw

        if "Machine" in df_parsed.columns and "MC ID" not in df_parsed.columns:
            df_parsed["MC ID"] = df_parsed["Machine"]

        if "MC ID" in df_parsed.columns:
            df_parsed = df_parsed.merge(
                df_mc_master,
                on="MC ID",
                how="left",
                suffixes=("", "_master"),
            )
            if "MC Number_master" in df_parsed.columns:
                df_parsed["MC Number"] = df_parsed["MC Number_master"]
            if "Line_master" in df_parsed.columns:
                df_parsed["Line"] = df_parsed["Line_master"]

        if "Hours" in df_parsed.columns:
            df_parsed["Hours"] = pd.to_numeric(
                df_parsed["Hours"], errors="coerce"
            ).fillna(0)
        elif "HR" in df_parsed.columns:
            df_parsed["Hours"] = pd.to_numeric(
                df_parsed["HR"], errors="coerce"
            ).fillna(0)

        df_filtered = df_parsed[df_parsed["Hours"] > 0].copy()

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
        df_filtered = pd.DataFrame()
else:
    df_filtered = pd.DataFrame()


# -----------------------------------------------------------------------------
# MODULE 1: NPT ANALYSIS
# -----------------------------------------------------------------------------
if app_mode == "⏱️ NPT Analysis":
    st.title("⏱️ Non-Productive Time (NPT) Analysis")

    if not df_filtered.empty:
        st.sidebar.markdown("---")
        npt_view = st.sidebar.selectbox(
            "Select NPT View:",
            ["1. Summary", "2. MC wise", "3. Line wise", "4. Date wise"],
        )

        if npt_view == "1. Summary":
            st.header("📊 NPT Overall Executive Summary")

            total_hours = df_filtered["Hours"].sum()
            total_incidents = (
                df_filtered["Entry"].sum()
                if "Entry" in df_filtered.columns
                else len(df_filtered)
            )
            affected_machines = (
                df_filtered["MC ID"].nunique()
                if "MC ID" in df_filtered.columns
                else 0
            )

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total NPT Loss", f"{total_hours:.2f} Hrs")
            kpi2.metric("Total Downtime Events", f"{int(total_incidents)}")
            kpi3.metric("Affected Machines", f"{affected_machines}")

            st.markdown("---")

            col_sum1, col_sum2 = st.columns(2)
            with col_sum1:
                st.subheader("Top Downtime Causes (Overall)")
                cause_summary = (
                    df_filtered.groupby("Cause")["Hours"]
                    .sum()
                    .reset_index()
                    .sort_values(by="Hours", ascending=False)
                )

                fig_cause = px.bar(
                    cause_summary.head(10),
                    x="Hours",
                    y="Cause",
                    orientation="h",
                    color="Hours",
                    color_continuous_scale="Reds",
                    template="plotly_white",
                    title="Top 10 Downtime Causes by Total Hours",
                )
                fig_cause.update_layout(
                    yaxis={"categoryorder": "total ascending"},
                    xaxis_title="Downtime (Hours)",
                    yaxis_title="",
                    showlegend=False,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                fig_cause.update_traces(
                    texttemplate="%{x:.1f}h",
                    textposition="outside",
                    cliponaxis=False,
                )
                st.plotly_chart(fig_cause, use_container_width=True)

            with col_sum2:
                st.subheader("NPT Distribution by Production Line")
                if "Line" in df_filtered.columns:
                    line_summary = (
                        df_filtered.groupby("Line")["Hours"].sum().reset_index()
                    )

                    fig_line = px.pie(
                        line_summary,
                        names="Line",
                        values="Hours",
                        hole=0.45,
                        template="plotly_white",
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        title="NPT Share per Production Line",
                    )
                    fig_line.update_traces(
                        textinfo="label+percent+value",
                        texttemplate="%{label}<br>%{value:.1f}h (%{percent})",
                        marker=dict(line=dict(color="#FFFFFF", width=2)),
                    )
                    fig_line.update_layout(
                        margin=dict(l=20, r=20, t=40, b=20),
                        showlegend=False,
                    )
                    st.plotly_chart(fig_line, use_container_width=True)

        elif npt_view == "2. MC wise":
            st.header("⚙️ Machine-Wise Cumulative NPT Loss Analysis")
            st.caption(
                "Each machine is listed exactly ONCE with its cumulative downtime hours and loss causes."
            )

            st.subheader(
                "🏆 Table 1: Top 10 Machines with Maximum Downtime (Overall)"
            )
            df_overall_mc = generate_unique_mc_summary(df_filtered)
            st.dataframe(
                df_overall_mc.head(10)[[
                    "MC Number",
                    "MC ID",
                    "Line",
                    "Cumulative Hours",
                    "%",
                    "Primary Cause",
                    "All Downtime Causes",
                ]],
                use_container_width=True,
            )

            st.markdown("---")
            st.subheader("🔍 Table 2: Line-Filtered Unique Machine Analysis")

            available_lines = ["All Lines"] + sorted([
                str(x) for x in df_filtered["Line"].dropna().unique()
            ])
            selected_mc_line = st.selectbox(
                "Select Line to filter machine breakdown:",
                options=available_lines,
                key="mc_wise_line_filter",
            )

            df_selected_line = (
                df_filtered
                if selected_mc_line == "All Lines"
                else df_filtered[df_filtered["Line"] == selected_mc_line]
            )

            if not df_selected_line.empty:
                df_selected_mc_summary = generate_unique_mc_summary(
                    df_selected_line
                )
                st.dataframe(
                    df_selected_mc_summary[[
                        "MC Number",
                        "MC ID",
                        "Line",
                        "Cumulative Hours",
                        "%",
                        "Primary Cause",
                        "All Downtime Causes",
                    ]],
                    use_container_width=True,
                )

        elif npt_view == "3. Line wise":
            st.header("🏭 Line-Wise NPT Breakdown")
            selected_line = st.selectbox(
                "Select Production Line to Analyze:", ["AB", "CD", "DE", "FG"]
            )
            df_line_filtered = df_filtered[df_filtered["Line"] == selected_line]

            if not df_line_filtered.empty:
                df_line_mc_summary = generate_unique_mc_summary(
                    df_line_filtered
                )
                st.dataframe(
                    df_line_mc_summary[[
                        "MC Number",
                        "MC ID",
                        "Line",
                        "Cumulative Hours",
                        "%",
                        "Primary Cause",
                        "All Downtime Causes",
                    ]],
                    use_container_width=True,
                )

        elif npt_view == "4. Date wise":
            st.header("📅 Date-Wise NPT Breakdown & Root Causes")
            if "Date" in df_filtered.columns and df_filtered["Date"].notna().any():
                df_date_valid = df_filtered[df_filtered["Date"].notna()].copy()
                df_date_valid["Date"] = pd.to_datetime(df_date_valid["Date"])

                df_date_valid["Date_Str"] = df_date_valid["Date"].dt.strftime("%Y-%m-%d")
                daily_cause_breakdown = (
                    df_date_valid.groupby(["Date_Str", "Cause"])["Hours"]
                    .sum()
                    .reset_index()
                )

                fig_stacked_date = px.bar(
                    daily_cause_breakdown,
                    x="Date_Str",
                    y="Hours",
                    color="Cause",
                    title="Daily Downtime Breakdown by Reason",
                    template="plotly_white",
                    barmode="stack",
                )
                st.plotly_chart(fig_stacked_date, use_container_width=True)
    else:
        st.info("Please upload an Excel file to begin analysis.")


# -----------------------------------------------------------------------------
# MODULE 2: NPT PROGRESS COMPARISON (NEW)
# -----------------------------------------------------------------------------
elif app_mode == "📈 NPT Progress Comparison":
    st.title("📈 NPT Progress & Period-Over-Period Comparison")
    st.caption(
        "Compare NPT performance between two specific date ranges to demonstrate operational progress in meetings."
    )

    if not df_filtered.empty and "Date" in df_filtered.columns and df_filtered["Date"].notna().any():
        df_valid = df_filtered[df_filtered["Date"].notna()].copy()
        df_valid["Date"] = pd.to_datetime(df_valid["Date"]).dt.date

        min_d = df_valid["Date"].min()
        max_d = df_valid["Date"].max()

        st.markdown("### 🗓️ Select Comparison Timeframes")
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Period 1 (Baseline / Previous Week)")
            p1_start = st.date_input(
                "P1 Start Date", value=min_d, min_value=min_d, max_value=max_d, key="p1_s"
            )
            p1_end = st.date_input(
                "P1 End Date", value=min_d + pd.Timedelta(days=7), min_value=min_d, max_value=max_d, key="p1_e"
            )

        with c2:
            st.subheader("Period 2 (Comparison / Current Week)")
            p2_start = st.date_input(
                "P2 Start Date", value=min_d + pd.Timedelta(days=8), min_value=min_d, max_value=max_d, key="p2_s"
            )
            p2_end = st.date_input(
                "P2 End Date", value=min_d + pd.Timedelta(days=15), min_value=min_d, max_value=max_d, key="p2_e"
            )

        # Filter Data for Both Periods
        df_p1 = df_valid[(df_valid["Date"] >= p1_start) & (df_valid["Date"] <= p1_end)]
        df_p2 = df_valid[(df_valid["Date"] >= p2_start) & (df_valid["Date"] <= p2_end)]

        # Global Line Filter for Comparison
        lines = ["All Lines"] + sorted([str(x) for x in df_valid["Line"].dropna().unique()])
        sel_line = st.selectbox("Filter Comparison by Line:", lines, index=0)

        if sel_line != "All Lines":
            df_p1 = df_p1[df_p1["Line"] == sel_line]
            df_p2 = df_p2[df_p2["Line"] == sel_line]

        # Metric Calculations
        p1_hrs = df_p1["Hours"].sum()
        p2_hrs = df_p2["Hours"].sum()

        p1_events = len(df_p1)
        p2_events = len(df_p2)

        hrs_delta = p2_hrs - p1_hrs
        pct_delta = ((p2_hrs - p1_hrs) / p1_hrs * 100) if p1_hrs > 0 else 0.0

        st.markdown("---")
        st.markdown("### 📊 Key Performance Indicator (KPI) Summary")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            label=f"Period 1 ({p1_start} to {p1_end})",
            value=f"{p1_hrs:.2f} Hrs",
            delta=f"{p1_events} Events",
            delta_color="off",
        )

        m2.metric(
            label=f"Period 2 ({p2_start} to {p2_end})",
            value=f"{p2_hrs:.2f} Hrs",
            delta=f"{p2_events} Events",
            delta_color="off",
        )

        # Reverse delta color convention (Negative delta is good for NPT loss)
        m3.metric(
            label="NPT Difference (Hours)",
            value=f"{hrs_delta:+.2f} Hrs",
            delta=f"{'Improved' if hrs_delta < 0 else 'Increased'}",
            delta_color="inverse" if hrs_delta != 0 else "off",
        )

        m4.metric(
            label="Percentage Change (%)",
            value=f"{pct_delta:+.2f}%",
            delta=f"{'Reduction 🎉' if pct_delta < 0 else 'Spike ⚠️'}",
            delta_color="inverse" if pct_delta != 0 else "off",
        )

        st.markdown("---")

        # ---------------------------------------------------------------------
        # VISUAL COMPARISON CHARTS
        # ---------------------------------------------------------------------
        st.markdown("### 📊 Cause-Wise Downtime Comparison")

        # Aggregate causes for both periods
        c1_agg = df_p1.groupby("Cause")["Hours"].sum().reset_index().rename(columns={"Hours": "Period 1 (Hrs)"})
        c2_agg = df_p2.groupby("Cause")["Hours"].sum().reset_index().rename(columns={"Hours": "Period 2 (Hrs)"})

        comp_df = pd.merge(c1_agg, c2_agg, on="Cause", how="outer").fillna(0)
        comp_df["Total Hours"] = comp_df["Period 1 (Hrs)"] + comp_df["Period 2 (Hrs)"]
        comp_df = comp_df.sort_values(by="Total Hours", ascending=False).head(12)

        fig_comp = go.Figure()
        fig_comp.add_trace(
            go.Bar(
                x=comp_df["Cause"],
                y=comp_df["Period 1 (Hrs)"],
                name=f"P1: {p1_start} to {p1_end}",
                marker_color="#1F77B4",
                text=comp_df["Period 1 (Hrs)"].apply(lambda x: f"{x:.1f}h" if x > 0 else ""),
                textposition="outside",
            )
        )
        fig_comp.add_trace(
            go.Bar(
                x=comp_df["Cause"],
                y=comp_df["Period 2 (Hrs)"],
                name=f"P2: {p2_start} to {p2_end}",
                marker_color="#FF7F0E" if hrs_delta > 0 else "#2CA02C",
                text=comp_df["Period 2 (Hrs)"].apply(lambda x: f"{x:.1f}h" if x > 0 else ""),
                textposition="outside",
            )
        )

        fig_comp.update_layout(
            barmode="group",
            title="Downtime Comparison by Cause (Top 12 Causes)",
            xaxis_title="Downtime Cause",
            yaxis_title="Loss Hours",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=60, b=80),
        )

        st.plotly_chart(fig_comp, use_container_width=True)

        # ---------------------------------------------------------------------
        # CAUSE-LEVEL DETAILED BREAKDOWN TABLE
        # ---------------------------------------------------------------------
        st.markdown("### 📋 Detailed Downtime Delta Breakdown Table")

        table_df = comp_df.copy()
        table_df["Difference (Hrs)"] = table_df["Period 2 (Hrs)"] - table_df["Period 1 (Hrs)"]
        
        def calc_pct(row):
            if row["Period 1 (Hrs)"] == 0:
                return "+100.00%" if row["Period 2 (Hrs)"] > 0 else "0.00%"
            val = ((row["Period 2 (Hrs)"] - row["Period 1 (Hrs)"]) / row["Period 1 (Hrs)"]) * 100
            return f"{val:+.2f}%"

        table_df["% Change"] = table_df.apply(calc_pct, axis=1)
        table_df["Status"] = table_df["Difference (Hrs)"].apply(
            lambda x: "🟢 Improved (Reduced)" if x < 0 else ("🔴 Worsened (Increased)" if x > 0 else "⚪ No Change")
        )

        st.dataframe(
            table_df[[
                "Cause",
                "Period 1 (Hrs)",
                "Period 2 (Hrs)",
                "Difference (Hrs)",
                "% Change",
                "Status",
            ]],
            use_container_width=True,
        )

    else:
        st.info("Please upload a file containing a valid 'Date' column to use the Progress Comparison module.")

# Placeholder for remaining app modules
elif app_mode == "❌ Rejection Analysis":
    st.title("❌ Rejection Analysis")
    st.info("Rejection Analysis module coming soon.")
elif app_mode == "🏭 Production Data":
    st.title("🏭 Production Data")
    st.info("Production Data module coming soon.")
elif app_mode == "📊 Master Summary":
    st.title("📊 Master Summary")
    st.info("Master Summary module coming soon.")
