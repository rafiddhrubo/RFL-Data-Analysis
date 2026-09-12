import plotly.express as px
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE SETUP & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Operations Hub - Downtime & Performance",
    page_icon="⚙️",
    layout="wide",
)

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
# HELPER FUNCTIONS (WITH PARSING FIXES)
# -----------------------------------------------------------------------------
def parse_raw_data_sheet(df_raw):
  """Parses transaction-level 'Data' sheet with strict NPT event filtering."""
  df = df_raw.copy()

  # Clean machine names
  if "Machine" in df.columns:
    df["MC ID"] = df["Machine"].astype(str).str.strip()

  # Calculate hours cleanly
  if "Duration (In Second)" in df.columns:
    df["Hours"] = (
        pd.to_numeric(df["Duration (In Second)"], errors="coerce").fillna(0)
        / 3600.0
    )
  elif "Hours" not in df.columns and "HR" in df.columns:
    df["Hours"] = pd.to_numeric(df["HR"], errors="coerce").fillna(0)
  else:
    df["Hours"] = 0.0

  # Filter OUT zero-duration or non-downtime rows immediately
  df = df[df["Hours"] > 0].copy()

  # Filter out non-downtime machine statuses if the column exists
  if "Status" in df.columns:
    df = df[df["Status"].astype(str).str.upper() != "RUNNING"].copy()

  # Standardize Cause field
  if "Cause" in df.columns:
    df["Cause"] = df["Cause"].fillna("Unspecified Cause").astype(str).str.strip()
  else:
    df["Cause"] = "Unspecified Cause"

  # Process Date column
  date_col = None
  for col in ["From Time", "Added Date", "Date"]:
    if col in df.columns:
      date_col = col
      break

  if date_col:
    df["Parsed_DateTime"] = pd.to_datetime(df[date_col], errors="coerce")
    df["Date"] = df["Parsed_DateTime"].dt.date
  else:
    df["Date"] = "Unknown"

  # Merge Machine details (Line & MC Number)
  df = df.merge(df_mc_master, on="MC ID", how="left", suffixes=("", "_master"))
  if "MC Number_master" in df.columns:
    df["MC Number"] = df["MC Number_master"]
  if "Line_master" in df.columns:
    df["Line"] = df["Line_master"]

  df["Entry"] = 1
  return df


def parse_mc_wise_sheet(df_raw):
  """Parses wide 'MC Wise' grid tab into standard long format."""
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

      if hr > 0:
        records.append({
            "MC ID": str(mc_id).strip(),
            "MC Number": str(mc_number).strip(),
            "Cause": str(cause).strip(),
            "Entry": entry,
            "Hours": hr,
            "Date": "Aggregated Data",
        })
  df_long = pd.DataFrame(records)
  if not df_long.empty:
    df_long = df_long.merge(
        df_mc_master[["MC ID", "Line"]], on="MC ID", how="left"
    )
  return df_long


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
        df_raw = pd.read_csv(uploaded_file)
        df_parsed = parse_raw_data_sheet(df_raw)
      else:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        if "Data" in sheet_names:
          df_raw = pd.read_excel(uploaded_file, sheet_name="Data")
          df_parsed = parse_raw_data_sheet(df_raw)
        elif "MC Wise" in sheet_names:
          df_mcwise_raw = pd.read_excel(uploaded_file, sheet_name="MC Wise")
          df_parsed = parse_mc_wise_sheet(df_mcwise_raw)
        else:
          selected_sheet = st.sidebar.selectbox(
              "Select Sheet/Tab to Analyze", sheet_names, index=0
          )
          df_raw = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
          df_parsed = parse_raw_data_sheet(df_raw)

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
          )
          fig_cause.update_layout(
              yaxis={"categoryorder": "total ascending"},
              showlegend=False,
              margin=dict(l=20, r=20, t=40, b=20),
          )
          fig_cause.update_traces(
              texttemplate="%{x:.1f}h", textposition="outside"
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
            )
            fig_line.update_traces(
                textinfo="label+percent+value",
                texttemplate="%{label}<br>%{value:.1f}h (%{percent})",
            )
            fig_line.update_layout(
                margin=dict(l=20, r=20, t=40, b=20), showlegend=False
            )
            st.plotly_chart(fig_line, use_container_width=True)

      # -----------------------------------------------------------------
      # VIEW 2: MC WISE
      # -----------------------------------------------------------------
      elif npt_view == "2. MC wise":
        st.header("⚙️ Machine-Wise Cumulative NPT Loss Analysis")
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
        available_lines = ["All Lines"] + sorted(
            [str(x) for x in df_filtered["Line"].dropna().unique()]
        )
        selected_mc_line = st.selectbox(
            "Select Line to filter machine breakdown:",
            options=available_lines,
            index=0,
        )

        df_selected_line = (
            df_filtered.copy()
            if selected_mc_line == "All Lines"
            else df_filtered[df_filtered["Line"] == selected_mc_line].copy()
        )

        if not df_selected_line.empty:
          df_selected_mc_summary = generate_unique_mc_summary(df_selected_line)
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
              f"📊 {selected_mc_line} Machine Downtime Breakdown Chart"
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
              barmode="stack",
              category_orders={"MC Number": mc_order},
          )
          fig_selected_line_bar.update_layout(
              xaxis_title="Machine Number",
              yaxis_title="Downtime (Hours)",
              legend=dict(
                  orientation="h",
                  yanchor="top",
                  y=-0.22,
                  xanchor="left",
                  x=0,
              ),
              margin=dict(l=20, r=20, t=50, b=120),
          )
          st.plotly_chart(fig_selected_line_bar, use_container_width=True)
        else:
          st.warning(
              "No downtime records found for Line"
              f" {selected_mc_line}."
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
          l1, l2 = st.columns(2)
          l1.metric(
              f"Total NPT Hours for Line {selected_line}",
              f"{df_line_filtered['Hours'].sum():.2f} Hrs",
          )
          l2.metric(
              "Active Affected Machines",
              f"{df_line_filtered['MC ID'].nunique()}",
          )
          st.markdown("---")

          c1, c2 = st.columns(2)
          with c1:
            st.subheader(f"Loss Hours by Machine ({selected_line})")
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
            )
            st.plotly_chart(fig_line_mc, use_container_width=True)

          with c2:
            st.subheader(f"Top Loss Causes ({selected_line})")
            cause_line_agg = (
                df_line_filtered.groupby("Cause")["Hours"].sum().reset_index()
            )
            fig_line_causes = px.pie(
                cause_line_agg,
                names="Cause",
                values="Hours",
                hole=0.45,
                template="plotly_white",
            )
            st.plotly_chart(fig_line_causes, use_container_width=True)

          st.subheader(
              f"📋 Line {selected_line} Unique Machine Ranking Table"
          )
          df_line_mc_summary = generate_unique_mc_summary(df_line_filtered)
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
          st.warning(f"No downtime data available for Line {selected_line}.")

      # -----------------------------------------------------------------
      # VIEW 4: DATE WISE COMPARISON (WITH LINE FILTER)
      # -----------------------------------------------------------------
      elif npt_view == "4. Date wise":
        st.header("📅 Date-Wise NPT Trend & Comparison")

        valid_dates = sorted(
            [d for d in df_filtered["Date"].unique() if d != "Unknown"]
        )

        if not valid_dates or valid_dates == ["Aggregated Data"]:
          st.warning(
              "⚠️ The dataset does not contain individual date timestamps."
              " Please upload a file containing the detailed 'Data' sheet."
          )
        else:
          col_f1, col_f2 = st.columns(2)

          with col_f1:
            available_lines = ["All Lines"] + sorted(
                [str(x) for x in df_filtered["Line"].dropna().unique()]
            )
            default_index = (
                available_lines.index("DE") if "DE" in available_lines else 0
            )
            selected_date_line = st.selectbox(
                "Filter by Production Line:",
                options=available_lines,
                index=default_index,
            )

          with col_f2:
            selected_dates = st.multiselect(
                "Filter Dates for Analysis:",
                options=valid_dates,
                default=valid_dates,
            )

          # Apply Line & Date Filters
          df_date_filtered = df_filtered[
              df_filtered["Date"].isin(selected_dates)
          ].copy()
          if selected_date_line != "All Lines":
            df_date_filtered = df_date_filtered[
                df_date_filtered["Line"] == selected_date_line
            ]

          if not df_date_filtered.empty:
            st.subheader(f"📈 Daily Downtime Trend ({selected_date_line})")
            daily_trend = (
                df_date_filtered.groupby("Date")["Hours"].sum().reset_index()
            )
            daily_trend["Date"] = daily_trend["Date"].astype(str)

            fig_trend = px.line(
                daily_trend,
                x="Date",
                y="Hours",
                markers=True,
                template="plotly_white",
            )
            fig_trend.update_traces(
                line_color="#1E3A8A",
                line_width=3,
                marker_size=8,
                texttemplate="%{y:.1f}h",
                textposition="top center",
            )
            fig_trend.update_layout(
                xaxis_title="Date", yaxis_title="Downtime (Hours)"
            )
            st.plotly_chart(fig_trend, use_container_width=True)

            st.markdown("---")

            st.subheader(
                f"📊 Daily Downtime Breakdown by Cause ({selected_date_line})"
            )
            date_cause_agg = (
                df_date_filtered.groupby(["Date", "Cause"])["Hours"]
                .sum()
                .reset_index()
            )
            date_cause_agg["Date"] = date_cause_agg["Date"].astype(str)

            fig_date_cause = px.bar(
                date_cause_agg,
                x="Date",
                y="Hours",
                color="Cause",
                template="plotly_white",
                barmode="stack",
            )
            fig_date_cause.update_layout(
                xaxis_title="Date",
                yaxis_title="Downtime (Hours)",
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="left",
                    x=0,
                ),
            )
            st.plotly_chart(fig_date_cause, use_container_width=True)

            st.markdown("---")

            st.subheader(
                f"📋 Comparative Date Pivot Table ({selected_date_line})"
            )
            date_pivot = pd.pivot_table(
                df_date_filtered,
                values="Hours",
                index=["Line", "MC Number"],
                columns="Date",
                aggfunc="sum",
                fill_value=0,
            )
            date_pivot["Total Hours"] = date_pivot.sum(axis=1)
            date_pivot = date_pivot.sort_values(
                by="Total Hours", ascending=False
            )

            st.dataframe(
                date_pivot.style.format("{:.2f}"), use_container_width=True
            )

          else:
            st.warning(
                "No data found for the selected date range and line"
                " combination."
            )

    except Exception as e:
      st.error(f"Error processing NPT file: {e}")
  else:
    st.info(
        "👈 Upload your daily NPT report in the sidebar to activate the"
        " analysis options."
    )

# -----------------------------------------------------------------------------
# MODULE 2, 3, 4 STUBS
# -----------------------------------------------------------------------------
elif app_mode == "❌ Rejection Analysis":
  st.title("❌ Rejection & Scrap Analysis Module")

elif app_mode == "🏭 Production Data":
  st.title("🏭 Production Output Module")

elif app_mode == "📊 Master Summary":
  st.title("📊 Master Executive Summary Dashboard")
