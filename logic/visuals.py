import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from typing import Dict

def create_radar_chart(scores: Dict[str, float]) -> go.Figure:
    """
    Create a radar chart for wellness metrics.
    """
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Wellness Metrics',
        line=dict(color='#1f77b4')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], color='gray'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,  # Moved to the top level
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_bar_chart(title: str, value: float, max_value: int = 10) -> go.Figure:
    """
    Create a bar chart for a single KPI.
    """
    fig = go.Figure(go.Bar(
        x=[value],
        y=[title],
        orientation='h',
        marker=dict(color='#1f77b4'),
        text=[f"{value}/{max_value}"],
        textposition='auto'
    ))
    fig.update_layout(
        xaxis=dict(range=[0, max_value], showgrid=False),
        yaxis=dict(showgrid=False),
        height=100,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def display_kpi_gauge(title: str, value: float, max_value: int = 10):
    """
    Display a gauge chart for a KPI.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': 'gray'},
            'bar': {'color': '#1f77b4'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': 'gray'
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

def display_results(response: Dict):
    """
    Display all results with enhanced visuals.
    """
    st.subheader("📊 Wellness Assessment Results")
    
    # Radar Chart
    scores = {k: v for k, v in response.items() if isinstance(v, (int, float))}
    st.plotly_chart(create_radar_chart(scores))
    
    # Gauges for Key KPIs
    st.subheader("🔑 Key Metrics")
    cols = st.columns(3)
    with cols[0]: display_kpi_gauge("Stress Management", response['stress_management'])
    with cols[1]: display_kpi_gauge("Motivation", response['motivation'])
    with cols[2]: display_kpi_gauge("Burnout Level", response['burnout_level'])
    
    # Bar Charts for All KPIs
    st.subheader("📈 Detailed KPI Scores")
    for kpi, score in scores.items():
        st.plotly_chart(create_bar_chart(kpi.replace("_", " ").title(), score))
    
    # Report with Highlighted Recommendations
    st.subheader("📝 Personalized Recommendations")
    st.markdown("### 🎯 Recommended Package Focus")
    st.markdown(
        f"<div style='background-color: #e6f3ff; padding: 15px; border-radius: 10px;'>"
        f"<h3 style='color: #1f77b4;'>✨ {response['package_focus']}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("### 📋 Summary Report")
    st.markdown(
        f"<div>"
        f"<p style='font-size: 16px; line-height: 1.6;'>{response['report']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )