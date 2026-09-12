if not df_selected_line.empty:
                    df_selected_mc_summary = generate_unique_mc_summary(df_selected_line)
                    
                    st.dataframe(
                        df_selected_mc_summary[['MC Number', 'MC ID', 'Line', 'Cumulative Hours', '%', 'Primary Cause', 'All Downtime Causes']], 
                        use_container_width=True
                    )

                    # Dynamic Visual Stacked Bar Chart (Fixed Text Overlap & Indentation)
                    st.subheader(f"📊 Line {selected_mc_line} Machine Downtime Breakdown Chart")
                    
                    chart_data = df_selected_line.groupby(['MC Number', 'Cause'])['Hours'].sum().reset_index()
                    mc_order = df_selected_mc_summary['MC Number'].tolist()
                    
                    fig_selected_line_bar = px.bar(
                        chart_data,
                        x='MC Number',
                        y='Hours',
                        color='Cause',
                        title=f"Cumulative Downtime Breakdown by Machine ({selected_mc_line} Line)",
                        template='plotly_white',
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        barmode='stack',
                        category_orders={'MC Number': mc_order}
                    )
                    
                    # Layout fixes for title and legend overlapping
                    fig_selected_line_bar.update_layout(
                        title=dict(
                            text=f"Cumulative Downtime Breakdown by Machine ({selected_mc_line} Line)",
                            y=0.98,
                            x=0.01,
                            xanchor='left',
                            yanchor='top'
                        ),
                        xaxis_title="Machine Number",
                        yaxis_title="Downtime (Hours)",
                        legend_title_text="Downtime Cause:",
                        legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=-0.25,  # Moves legend cleanly below chart to eliminate header overlap
                            xanchor="left",
                            x=0,
                            font=dict(size=11)
                        ),
                        margin=dict(l=20, r=20, t=60, b=120)
                    )
                    
                    # Clean inline text labels
                    fig_selected_line_bar.update_traces(
                        texttemplate='%{y:.1f}h',
                        textposition='inside',
                        insidetextanchor='middle',
                        marker_line_color='#FFFFFF',
                        marker_line_width=1
                    )
                    
                    st.plotly_chart(fig_selected_line_bar, use_container_width=True)
                else:
                    st.warning(f"No downtime records found for Line {selected_mc_line} in the uploaded report.")
