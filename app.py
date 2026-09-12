import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NPT Downtime Dashboard", layout="wide")


# Load and prepare dataset
@st.cache_data
def load_data(file_path):
    df_data = pd.read_excel(file_path, sheet_name="Data")
    df_mc = pd.read_excel(file_path, sheet_name="MC ID")

    # Clean date/time and duration
    df_data["From Time"] = pd.to_datetime(df_data["From Time"])
    df_data["Date"] = df_data["From Time"].dt.date
    df_data["Duration_Hours"] = df_data["Duration (In Second)"] / 3600
    df_data["Cause"] = df_data["Cause"].fillna("Unspecified Cause")

    # Merge Line info from MC ID sheet
    df_merged = pd.merge(
        df_data, df_mc, left_on="Machine", right_on="MC ID", how="left"
    )
    df_merged["Line"] = df_merged["Line"].fillna("Unknown Line")
    return df_merged


# Replace filename with your file path
file_path = "Downtime report 2.5.2026.xlsx"
df = load_data(file_path)

st.title("🏭 Plastic Molding Machine Downtime Analysis")

# Main Navigation Tabs
tab_line, tab_mc, tab_date = st.tabs(
    ["📊 Line Wise", "🤖 Machine Wise", "📅 Date Wise Comparison"]
)

# -------------------------------------------------------------
# TAB 1: LINE WISE ANALYSIS (Existing logic)
# -------------------------------------------------------------
with tab_line:
    st.header("Line-Wise Downtime Summary")
    line_summary = (
        df.groupby("Line")["Duration_Hours"].sum().reset_index()
    )
    fig_line = px.bar(
        line_summary,
        x="Line",
        y="Duration_Hours",
        title="Total NPT Hours by Line",
        labels={"Duration_Hours": "Downtime (Hours)"},
        color="Line",
    )
    st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: MACHINE WISE ANALYSIS (Existing logic)
# -------------------------------------------------------------
with tab_mc:
    st.header("Machine-Wise Downtime Summary")
    selected_line_mc = st.selectbox(
        "Select Line for Machine Breakdown:",
        options=["All"] + list(df["Line"].unique()),
        key="mc_line_select",
    )
    df_mc_filtered = (
        df if selected_line_mc == "All" else df[df["Line"] == selected_line_mc]
    )

    mc_summary = (
        df_mc_filtered.groupby("Machine")["Duration_Hours"]
        .sum()
        .reset_index()
        .sort_values(by="Duration_Hours", ascending=False)
    )
    fig_mc = px.bar(
        mc_summary.head(15),
        x="Machine",
        y="Duration_Hours",
        title="Top Downtime Machines",
        labels={"Duration_Hours": "Downtime (Hours)"},
        color="Duration_Hours",
        color_continuous_scale="Reds",
    )
    st.plotly_chart(fig_mc, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: DATE WISE COMPARISON (New Requested Feature)
# -------------------------------------------------------------
with tab_date:
    st.header("📅 Date-Wise Comparison & Trend Analysis")

    # Sub-section Filters: Date Picker Range + Line Filter
    col_filter1, col_filter2 = st.columns(2)

    min_date = df["Date"].min()
    max_date = df["Date"].max()

    with col_filter1:
        selected_date_range = st.date_input(
            "Select Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_range_picker",
        )

    with col_filter2:
        selected_line_date = st.selectbox(
            "Filter by Line (Optional):",
            options=["All Lines"] + sorted(list(df["Line"].unique())),
            key="date_tab_line_select",
        )

    # Apply Filters
    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date = end_date = (
            selected_date_range[0]
            if isinstance(selected_date_range, tuple)
            else selected_date_range
        )

    df_date_filtered = df[
        (df["Date"] >= start_date) & (df["Date"] <= end_date)
    ]

    if selected_line_date != "All Lines":
        df_date_filtered = df_date_filtered[
            df_date_filtered["Line"] == selected_line_date
        ]

    st.markdown("---")

    if df_date_filtered.empty:
        st.warning("No data available for the selected date range and line.")
    else:
        # 1. Overall Trend: NPT Hours per Day (Increase/Decrease Visualizer)
        daily_npt = (
            df_date_filtered.groupby("Date")["Duration_Hours"]
            .sum()
            .reset_index()
        )
        daily_npt["Date_Str"] = daily_npt["Date"].astype(str)

        st.subheader("1. Daily NPT Trend (Increase vs Decrease)")

        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Bar(
                x=daily_npt["Date_Str"],
                y=daily_npt["Duration_Hours"],
                name="NPT Hours",
                marker_color="#1f77b4",
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=daily_npt["Date_Str"],
                y=daily_npt["Duration_Hours"],
                mode="lines+markers",
                name="Trend Line",
                line=dict(color="#ff7f0e", width=3),
            )
        )
        fig_trend.update_layout(
            title=f"Total Downtime Hours ({start_date} to {end_date})",
            xaxis_title="Date",
            yaxis_title="Total NPT (Hours)",
            template="plotly_white",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # 2. Daily Top Cause Analysis
        st.subheader("2. Top Downtime Cause by Day")

        # Group by Date and Cause to find top cause per day
        daily_cause = (
            df_date_filtered.groupby(["Date", "Cause"])["Duration_Hours"]
            .sum()
            .reset_index()
        )
        top_causes_per_day = daily_cause.sort_values(
            ["Date", "Duration_Hours"], ascending=[True, False]
        ).groupby("Date").first().reset_index()

        fig_cause = px.bar(
            daily_cause,
            x="Date",
            y="Duration_Hours",
            color="Cause",
            title="Daily NPT Breakdown by Cause",
            labels={"Duration_Hours": "NPT Hours", "Date": "Date"},
            barmode="stack",
        )
        st.plotly_chart(fig_cause, use_container_width=True)

        # 3. Highlighted Summary Table for Top Cause per Day
        st.subheader("📋 Top Cause Summary Table")
        top_causes_per_day["Date"] = top_causes_per_day["Date"].astype(str)
        top_causes_per_day.rename(
            columns={
                "Date": "Date",
                "Cause": "Top Downtime Cause",
                "Duration_Hours": "Impact (Hours)",
            },
            inplace=True,
        )

        st.dataframe(
            top_causes_per_day[["Date", "Top Downtime Cause", "Impact (Hours)"]].style.format(
                {"Impact (Hours)": "{:.2f}"}
            ),
            use_container_width=True,
        )
