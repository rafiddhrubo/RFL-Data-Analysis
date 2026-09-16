import pandas as pd
import plotly.express as px
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
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #1E3A8A; }
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
    """Parses row-by-row transaction log 'Data' tab to extract dates and durations."""
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

    # Parse Date column
    if "From Time" in df_data.columns:
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
# MODULE 1: NPT ANALYSIS
# -----------------------------------------------------------------------------
if app_mode == "⏱️ NPT Analysis":
    st.title("⏱️ Non-Productive Time (NPT) Analysis")

    uploaded_file = st.sidebar.file_uploader(
        "Upload NPT Report (.xlsx or .csv)",
        type=["xlsx", "xls", "csv"],
        key="npt_uploader",
    )

    if uploaded_file is not None:
        try:
            df_parsed = pd.DataFrame()

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

            st.sidebar.markdown("---")
            npt_view = st.sidebar.selectbox(
                "Select NPT View:",
                ["1. Summary", "2. MC wise", "3. Line wise", "4. Date wise"],
            )

            # -----------------------------------------------------------------
            # VIEW 1: SUMMARY
            # -----------------------------------------------------------------
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
                kpi2.metric(
                    "Total Downtime Events", f"{int(total_incidents)}"
                )
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
                            df_filtered.groupby("Line")["Hours"]
                            .sum()
                            .reset_index()
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

            # -----------------------------------------------------------------
            # VIEW 2: MC WISE
            # -----------------------------------------------------------------
            elif npt_view == "2. MC wise":
                st.header("⚙️ Machine-Wise Cumulative NPT Loss Analysis")
                st.caption(
                    "Each machine is listed exactly ONCE with its cumulative downtime hours and loss causes."
                )

                st.subheader(
                    "🏆 Table 1: Top 10 Machines with Maximum Downtime (Overall)"
                )

                df_overall_mc = generate_unique_mc_summary(df_filtered)
                df_top10_mc = df_overall_mc.head(10)

                st.dataframe(
                    df_top10_mc[[
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
                    index=(
                        available_lines.index("AB")
                        if "AB" in available_lines
                        else 0
                    ),
                    key="mc_wise_line_filter",
                )

                if selected_mc_line == "All Lines":
                    df_selected_line = df_filtered.copy()
                    st.caption(
                        "Displaying unique machine breakdown for **All Production Lines**"
                    )
                else:
                    df_selected_line = df_filtered[
                        df_filtered["Line"] == selected_mc_line
                    ].copy()
                    st.caption(
                        f"Displaying unique machine breakdown specifically for **Line {selected_mc_line}**"
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

                    st.subheader(
                        f"📊 Line {selected_mc_line} Machine Downtime Breakdown Chart"
                    )

                    chart_data = (
                        df_selected_line.groupby(["MC Number", "Cause"])["Hours"]
                        .sum()
                        .reset_index()
                    )
                    mc_order = df_selected_mc_summary["MC Number"].tolist()

                    fig_selected_line_bar = px.bar(
                        chart_data,
                        x="MC Number",
                        y="Hours",
                        color="Cause",
                        template="plotly_white",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        barmode="stack",
                        category_orders={"MC Number": mc_order},
                    )

                    fig_selected_line_bar.update_layout(
                        title=dict(
                            text=f"Cumulative Downtime Breakdown by Machine ({selected_mc_line} Line)",
                            y=0.98,
                            x=0.01,
                            xanchor="left",
                            yanchor="top",
                        ),
                        xaxis_title="Machine Number",
                        yaxis_title="Downtime (Hours)",
                        legend_title_text="Downtime Cause:",
                        legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=-0.22,
                            xanchor="left",
                            x=0,
                            font=dict(size=11),
                        ),
                        margin=dict(l=20, r=20, t=50, b=120),
                    )

                    fig_selected_line_bar.update_traces(
                        texttemplate="%{y:.1f}h",
                        textposition="inside",
                        insidetextanchor="middle",
                        marker_line_color="#FFFFFF",
                        marker_line_width=1,
                    )

                    st.plotly_chart(
                        fig_selected_line_bar, use_container_width=True
                    )
                else:
                    st.warning(
                        f"No downtime records found for Line {selected_mc_line} in the uploaded report."
                    )

            # -----------------------------------------------------------------
            # VIEW 3: LINE WISE
            # -----------------------------------------------------------------
            elif npt_view == "3. Line wise":
                st.header("🏭 Line-Wise NPT Breakdown")

                selected_line = st.selectbox(
                    "Select Production Line to Analyze:", ["AB", "CD", "DE", "FG"]
                )

                df_line_filtered = df_filtered[
                    df_filtered["Line"] == selected_line
                ].copy()

                if not df_line_filtered.empty:
                    st.subheader(f"📍 Line {selected_line} Analysis Overview")

                    total_line_hrs = df_line_filtered["Hours"].sum()
                    line_machines_affected = df_line_filtered[
                        "MC ID"
                    ].nunique()

                    l1, l2 = st.columns(2)
                    l1.metric(
                        f"Total NPT Hours for Line {selected_line}",
                        f"{total_line_hrs:.2f} Hrs",
                    )
                    l2.metric(
                        "Active Affected Machines", f"{line_machines_affected}"
                    )

                    st.markdown("---")

                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader(
                            f"Loss Hours by Machine ({selected_line} Line)"
                        )

                        mc_line_agg = (
                            df_line_filtered.groupby("MC Number")["Hours"]
                            .sum()
                            .reset_index()
                            .sort_values(by="Hours", ascending=False)
                        )

                        fig_line_mc = px.bar(
                            mc_line_agg,
                            x="MC Number",
                            y="Hours",
                            color="Hours",
                            color_continuous_scale="Teal",
                            template="plotly_white",
                            title=f"Machine Downtime Ranking (Line {selected_line})",
                        )
                        fig_line_mc.update_layout(
                            xaxis_title="Machine Number",
                            yaxis_title="Downtime (Hours)",
                            showlegend=False,
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        fig_line_mc.update_traces(
                            texttemplate="%{y:.1f}h",
                            textposition="outside",
                            cliponaxis=False,
                        )
                        st.plotly_chart(fig_line_mc, use_container_width=True)

                    with c2:
                        st.subheader(f"Top Loss Causes ({selected_line} Line)")

                        cause_line_agg = (
                            df_line_filtered.groupby("Cause")["Hours"]
                            .sum()
                            .reset_index()
                        )

                        fig_line_causes = px.pie(
                            cause_line_agg,
                            names="Cause",
                            values="Hours",
                            hole=0.45,
                            template="plotly_white",
                            color_discrete_sequence=px.colors.qualitative.Set3,
                            title=f"Causes Share (Line {selected_line})",
                        )
                        fig_line_causes.update_traces(
                            textinfo="label+percent",
                            texttemplate="%{label}<br>%{percent}",
                            marker=dict(line=dict(color="#FFFFFF", width=2)),
                        )
                        fig_line_causes.update_layout(
                            margin=dict(l=20, r=20, t=40, b=20),
                            showlegend=False,
                        )
                        st.plotly_chart(
                            fig_line_causes, use_container_width=True
                        )

                    st.subheader(
                        f"📋 Line {selected_line} Unique Machine Ranking Table"
                    )
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

                else:
                    st.warning(
                        f"No downtime data available for Line {selected_line}."
                    )

            # -----------------------------------------------------------------
            # VIEW 4: DATE WISE (DE LINE SPECIFIC)
            # -----------------------------------------------------------------
            elif npt_view == "4. Date wise":
                st.header("📅 Date-Wise Loss Hours & Causes (DE Line)")

                # Strictly filter for DE Line first
                df_de_line = df_filtered[df_filtered["Line"] == "DE"].copy()

                if df_de_line.empty:
                    st.warning("No downtime data found for DE Line in the uploaded report.")
                elif "Date" in df_de_line.columns and df_de_line["Date"].notna().any():
                    df_de_valid = df_de_line[df_de_line["Date"].notna()].copy()
                    df_de_valid["Date"] = pd.to_datetime(df_de_valid["Date"])

                    min_date = df_de_valid["Date"].min().date()
                    max_date = df_de_valid["Date"].max().date()

                    col_d1, _ = st.columns(2)
                    with col_d1:
                        date_range = st.date_input(
                            "Select Date Range (DE Line):",
                            value=(min_date, max_date),
                            min_value=min_date,
                            max_value=max_date,
                        )

                    if isinstance(date_range, tuple) and len(date_range) == 2:
                        start_d, end_d = date_range
                        df_de_date_filtered = df_de_valid[
                            (df_de_valid["Date"].dt.date >= start_d)
                            & (df_de_valid["Date"].dt.date <= end_d)
                        ]
                    else:
                        df_de_date_filtered = df_de_valid.copy()

                    if not df_de_date_filtered.empty:
                        st.markdown("---")

                        # Graph 1: Date vs Loss Hours (Line Trend Chart)
                        daily_de_trend = (
                            df_de_date_filtered.groupby(
                                df_de_date_filtered["Date"].dt.strftime("%Y-%m-%d")
                            )["Hours"]
                            .sum()
                            .reset_index()
                        )

                        fig_de_trend = px.line(
                            daily_de_trend,
                            x="Date",
                            y="Hours",
                            markers=True,
                            template="plotly_white",
                            title="DE Line: Date vs Loss Hours",
                            labels={"Hours": "Loss Hours", "Date": "Date"},
                        )
                        fig_de_trend.update_traces(
                            line_color="#1E3A8A", line_width=3, marker_size=8
                        )
                        fig_de_trend.update_layout(
                            xaxis_title="Date",
                            yaxis_title="Total Loss Hours",
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        st.plotly_chart(fig_de_trend, use_container_width=True)

                        st.markdown("---")

                        # Graph 2: Reasons of Loss Hours (Bar Chart)
                        de_cause_summary = (
                            df_de_date_filtered.groupby("Cause")["Hours"]
                            .sum()
                            .reset_index()
                            .sort_values(by="Hours", ascending=False)
                        )

                        fig_de_cause_bar = px.bar(
                            de_cause_summary,
                            x="Hours",
                            y="Cause",
                            orientation="h",
                            color="Hours",
                            color_continuous_scale="Reds",
                            template="plotly_white",
                            title="DE Line: Loss Hours by Reason / Cause",
                            labels={"Hours": "Loss Hours", "Cause": "Downtime Reason"},
                        )
                        fig_de_cause_bar.update_layout(
                            yaxis={"categoryorder": "total ascending"},
                            xaxis_title="Loss Hours",
                            yaxis_title="Reason / Cause",
                            showlegend=False,
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        fig_de_cause_bar.update_traces(
                            texttemplate="%{x:.1f}h",
                            textposition="outside",
                            cliponaxis=False,
                        )
                        st.plotly_chart(fig_de_cause_bar, use_container_width=True)

                    else:
                        st.warning("No data found for the selected date range on DE Line.")
                else:
                    st.warning("The uploaded report lacks valid 'Date' entries required for date-wise analysis.")

        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

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
