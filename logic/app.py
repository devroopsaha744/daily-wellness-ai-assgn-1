import os
import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import TypedDict, List
from typing_extensions import Annotated
from dotenv import load_dotenv
import numpy as np

# --- SETUP ---
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

class AssessmentOutput(TypedDict):
    stress_management: Annotated[float, "Percentage score (0-100) for Stress Management KPI"]
    motivation: Annotated[float, "Percentage score (0-100) for Motivation KPI"]
    restless_night_score: Annotated[float, "Percentage score (0-100) for Restless Night Score KPI"]
    anxiety_level: Annotated[float, "Percentage score (0-100) for Anxiety Level KPI"]
    burnout_level: Annotated[float, "Percentage score (0-100) for Burnout Level KPI"]
    physical_fitness_score: Annotated[float, "Percentage score (0-100) for Physical Fitness KPI"]
    dietary_habit_score: Annotated[float, "Percentage score (0-100) for Diet & Nutrition KPI"]
    focus_score: Annotated[float, "Percentage score (0-100) for Cognitive Performance and Focus KPI"]
    overall_wellness_score: Annotated[float, "Percentage score (0-100) based on all the individual KPIs"]
    package: Annotated[List[str], "List of recommended packages. Options include 'Focus', 'Fitness', and 'Insomnia'. The recommendation can be a single package, a combination of packages, or all three packages based on the assessment."]
    report: Annotated[str, "A detailed summary report of the assessment results and recommendations based on the KPI analysis."]

template = """
You are an AI wellness assessment system designed to evaluate users' well-being and provide personalized insights. This assessment system analyzes responses and generates wellness reports, recommending specific services and packages from *DailyWellnessAI* to help users improve their mental and physical health. While this system itself is not called *DailyWellnessAI*, all recommendations are part of the *DailyWellnessAI* platform.

Based on the user's responses to the following 15 questions, along with their personal details (Name, Age, Gender, Height, Weight), predict the following KPIs as percentages out of 100:
- stress_management
- motivation
- restless_night_score
- anxiety_level
- burnout_level
- physical_fitness_score
- dietary_habit_score
- focus_score
- overall_wellness_score

**Recommendation System:**
Based on the predicted KPIs, recommend one of the following *DailyWellnessAI* packages:
- Focus (for low concentration, motivation, or burnout)
- Insomnia (for sleep disturbances, restlessness, or anxiety before sleep)
- Fitness (for low physical activity, poor dietary habits, or weak physical strength)

If the overall_wellness_score is greater than 90 (or 95), recommend all three packages and let the user choose among them, emphasizing that DailyWellnessAI offers holistic well-being solutions.

**Summary Report:**
Provide a brief wellness summary explaining the predicted KPIs and recommended package(s) based on the user's responses. Justify the recommendations by highlighting key factors affecting the user's well-being and how DailyWellnessAI can help improve them. Take into account the user's age, gender, height, and weight when providing recommendations.

### Personal Details:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Height: {height}
- Weight: {weight}

### Assessment Questions:

1. How often do you feel stressed by daily tasks?
   Answer: {ans1}
2. How well do you handle stress?
   Answer: {ans2}
3. How would you rate your current level of burnout?
   Answer: {ans3}
4. How well can you concentrate on your daily tasks?
   Answer: {ans4}
5. How often do you have trouble falling asleep?
   Answer: {ans5}
6. How would you rate the quality of your sleep?
   Answer: {ans6}
7. How often do you wake up during the night?
   Answer: {ans7}
8. How often do you feel anxious before sleep?
   Answer: {ans8}
9. How happy are you with your eating habits?
   Answer: {ans9}
10. How balanced is your diet?
    Answer: {ans10}
11. How often do you exercise or do physical activity?
    Answer: {ans11}
12. How would you rate your physical strength?
    Answer: {ans12}
13. How motivated are you to work on your wellness goals daily?
    Answer: {ans13}
14. How would you rate your overall health and well-being?
    Answer: {ans14}
15. Any more remarks about yourself that you want to add?
    Answer: {ans15}
"""

chat = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile", temperature=0.2)
prompt_template = PromptTemplate(
    input_variables=["name", "age", "gender", "height", "weight"] + [f"ans{i}" for i in range(1, 16)],
    template=template
)

def run_assessment(personal_details, answers):
    prompt = prompt_template.format(**personal_details, **answers)
    structured_llm = chat.with_structured_output(AssessmentOutput)
    return structured_llm.invoke(prompt)

# --- VISUALIZATION FUNCTIONS ---

def get_emoji(score):
    if score < 20:
        return "😢"
    elif score < 40:
        return "😞"
    elif score < 60:
        return "😐"
    elif score < 80:
        return "🙂"
    else:
        return "😄"

def create_overall_wellness_donut(score):
    color = '#FF5252' if score < 50 else '#FFC107' if score < 75 else '#4CAF50'
    fig = go.Figure(go.Pie(
        values=[score, 100 - score],
        hole=0.7,
        textinfo='none',
        marker_colors=[color, '#E0E0E0'],
        showlegend=False
    ))
    fig.update_layout(
        annotations=[dict(
            text=f"{get_emoji(score)}",
            font_size=24,
            showarrow=False
        )],
        title=dict(text="Overall Wellness", x=0.5, font=dict(size=16)),
        margin=dict(t=20, b=20, l=20, r=20),
        height=300
    )
    return fig

def create_kpi_bar_chart(kpis, values):
    colors = ['#FF5252' if v < 50 else '#FFC107' if v < 75 else '#4CAF50' for v in values]
    fig = go.Figure(go.Bar(
        x=kpis,
        y=values,
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition='auto'
    ))
    fig.update_layout(
        title="KPI Breakdown",
        xaxis=dict(title="KPI"),
        yaxis=dict(title="Score (%)", range=[0, 100]),
        margin=dict(l=40, r=40, t=60, b=40),
        height=400
    )
    return fig

def create_radar_chart(data):
    categories = [
        'Stress Management',
        'Motivation',
        'Sleep Quality',
        'Anxiety Control',
        'Burnout Resistance',
        'Physical Fitness',
        'Diet & Nutrition',
        'Focus'
    ]
    values = [
        float(data['stress_management']),
        float(data['motivation']),
        100 - float(data['restless_night_score']),
        100 - float(data['anxiety_level']),
        100 - float(data['burnout_level']),
        float(data['physical_fitness_score']),
        float(data['dietary_habit_score']),
        float(data['focus_score'])
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(76, 175, 80, 0.3)',
        line=dict(color='#4CAF50', width=2),
        name='Your Profile'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10))
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20),
        height=400
    )
    return fig

def create_bullet_charts_combined(data):
    bullet_data = [
        ("Stress Management", float(data['stress_management'])),
        ("Motivation", float(data['motivation'])),
        ("Sleep Quality", 100 - float(data['restless_night_score'])),
        ("Anxiety Control", 100 - float(data['anxiety_level'])),
        ("Burnout Resistance", 100 - float(data['burnout_level'])),
        ("Physical Fitness", float(data['physical_fitness_score'])),
        ("Diet & Nutrition", float(data['dietary_habit_score'])),
        ("Focus", float(data['focus_score']))
    ]
    rows, cols = 2, 4
    target = 80
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[item[0] for item in bullet_data])
    for i, (label, val) in enumerate(bullet_data):
        row = i // cols + 1
        col = i % cols + 1
        fig.add_trace(go.Bar(
            x=[val],
            y=[""],
            orientation="h",
            marker_color='#4CAF50' if val >= target else '#FF5252',
            text=[f"{val}%"],
            textposition='inside',
            showlegend=False
        ), row=row, col=col)
        fig.update_xaxes(range=[0, 100], row=row, col=col)
        # Use data coordinate reference instead of "domain"
        fig.add_shape(
            type="line",
            x0=target, x1=target,
            y0=0, y1=1,
            xref=f"x{i+1}",
            yref=f"y{i+1}",
            line=dict(color="black", width=2, dash="dash")
        )
    fig.update_layout(height=400, width=1000, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def combine_report(results):
    packages = results["package"]
    rec_text = ", ".join(packages) if packages else "None"
    final_text = f"### Report\n{results['report']}\n\n**Recommended Packages:** {rec_text}"
    return final_text

# --- GRADIO APP FUNCTION ---

def gradio_assessment(
    name, age, gender, height, weight,
    ans1, ans2, ans3, ans4, ans5,
    ans6, ans7, ans8, ans9, ans10,
    ans11, ans12, ans13, ans14, ans15
):
    personal_details = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight
    }
    answers = {
        "ans1": ans1, "ans2": ans2, "ans3": ans3, "ans4": ans4, "ans5": ans5,
        "ans6": ans6, "ans7": ans7, "ans8": ans8, "ans9": ans9, "ans10": ans10,
        "ans11": ans11, "ans12": ans12, "ans13": ans13, "ans14": ans14,
        "ans15": ans15 or None
    }
    results = run_assessment(personal_details, answers)
    overall_score = int(float(results["overall_wellness_score"]))
    donut_fig = create_overall_wellness_donut(overall_score)

    kpis = [
        "Stress Management", "Motivation", "Sleep Quality",
        "Anxiety Control", "Burnout Resistance", "Physical Fitness",
        "Diet & Nutrition", "Focus"
    ]
    values = [
        float(results["stress_management"]),
        float(results["motivation"]),
        100 - float(results["restless_night_score"]),
        100 - float(results["anxiety_level"]),
        100 - float(results["burnout_level"]),
        float(results["physical_fitness_score"]),
        float(results["dietary_habit_score"]),
        float(results["focus_score"])
    ]
    bar_fig = create_kpi_bar_chart(kpis, values)
    radar_fig = create_radar_chart(results)
    bullet_fig = create_bullet_charts_combined(results)
    report_text = combine_report(results)
    return donut_fig, bar_fig, radar_fig, bullet_fig, report_text

# --- BUILD GRADIO INTERFACE ---

def build_app():
    with gr.Blocks() as demo:
        gr.Markdown("# 🌿 DailyWellnessAI Assessment")
        gr.Markdown("Fill out the questionnaire below to receive personalized insights and recommendations.")

        with gr.Row():
            with gr.Column():
                name = gr.Textbox(label="Your Name", placeholder="Enter your name")
                age = gr.Number(label="Your Age")
                gender = gr.Dropdown(label="Your Gender", choices=["Male", "Female", "Other"], value="Male")
                height = gr.Textbox(label="Your Height (e.g., 180 cm)", placeholder="Enter your height")
                weight = gr.Textbox(label="Your Weight (e.g., 80 kg)", placeholder="Enter your weight")
            with gr.Column():
                ans1 = gr.Dropdown(label="1. How often do you feel stressed by daily tasks?",
                                   choices=["Never", "Sometimes", "Often", "Always"], value="Never")
                ans2 = gr.Dropdown(label="2. How well do you handle stress?",
                                   choices=["Excellent", "Good", "Fair", "Poor"], value="Good")
                ans3 = gr.Dropdown(label="3. How would you rate your current level of burnout?",
                                   choices=["None", "Mild", "Moderate", "Severe"], value="None")
                ans4 = gr.Dropdown(label="4. How well can you concentrate on your daily tasks?",
                                   choices=["Excellent", "Good", "Fair", "Poor"], value="Good")
                ans5 = gr.Dropdown(label="5. How often do you have trouble falling asleep?",
                                   choices=["Never", "Rarely", "Sometimes", "Always"], value="Rarely")
                ans6 = gr.Dropdown(label="6. How would you rate the quality of your sleep?",
                                   choices=["Excellent", "Good", "Fair", "Poor"], value="Good")
                ans7 = gr.Dropdown(label="7. How often do you wake up during the night?",
                                   choices=["Never", "Rarely", "Sometimes", "Often"], value="Rarely")
                ans8 = gr.Dropdown(label="8. How often do you feel anxious before sleep?",
                                   choices=["Never", "Rarely", "Sometimes", "Often"], value="Rarely")
            with gr.Column():
                ans9 = gr.Dropdown(label="9. How happy are you with your eating habits?",
                                   choices=["Very happy", "Happy", "Unhappy", "Very unhappy"], value="Happy")
                ans10 = gr.Dropdown(label="10. How balanced is your diet?",
                                    choices=["Very balanced", "Balanced", "Unbalanced", "Very unbalanced"], value="Balanced")
                ans11 = gr.Dropdown(label="11. How often do you exercise or do physical activity?",
                                    choices=["Daily", "Several times a week", "Once a week", "Never"], value="Daily")
                ans12 = gr.Dropdown(label="12. How would you rate your physical strength?",
                                    choices=["Excellent", "Good", "Fair", "Poor"], value="Good")
                ans13 = gr.Dropdown(label="13. How motivated are you to work on your wellness goals daily?",
                                    choices=["Very motivated", "Moderately motivated", "Slightly motivated", "Not at all"], value="Very motivated")
                ans14 = gr.Dropdown(label="14. How would you rate your overall health and well-being?",
                                    choices=["Excellent", "Good", "Fair", "Poor"], value="Good")
                ans15 = gr.Textbox(label="15. Any more remarks about yourself (optional):", placeholder="Optional", lines=3)

        with gr.Row():
            submit_btn = gr.Button("Submit Assessment")
        
        with gr.Row():
            gr.Markdown("## Results")
        with gr.Row():
            donut_plot = gr.Plot(label="Overall Wellness Donut")
            bar_plot = gr.Plot(label="KPI Bar Chart")
        with gr.Row():
            radar_plot = gr.Plot(label="Radar Chart")
            bullet_plot = gr.Plot(label="Bullet Charts")
        with gr.Row():
            report_md = gr.Markdown(label="Assessment Report")

        submit_btn.click(
            fn=gradio_assessment,
            inputs=[name, age, gender, height, weight, ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8, ans9, ans10, ans11, ans12, ans13, ans14, ans15],
            outputs=[donut_plot, bar_plot, radar_plot, bullet_plot, report_md]
        )
    return demo

if __name__ == "__main__":
    demo_app = build_app()
    demo_app.launch(server_name="0.0.0.0", server_port=7860, share=True)