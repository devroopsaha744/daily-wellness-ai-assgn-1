from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

app = FastAPI()


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Wellness Assessment API!"}

# --- TypedDict for Output ---
class AssessmentOutput(TypedDict):
    """Assessment output containing individual KPIs (as percentages out of 100), recommended packages, and a summary report."""
    stress_management: Annotated[float, "Percentage score (0-100) for Stress Management KPI. Reflects how well the user manages daily stress."]
    motivation: Annotated[float, "Percentage score (0-100) for Motivation KPI. Represents the user's drive and energy to pursue wellness goals."]
    restless_night_score: Annotated[float, "Percentage score (0-100) for Restless Night Score KPI. Indicates the frequency of sleep disturbances and overall sleep quality."]
    anxiety_level: Annotated[float, "Percentage score (0-100) for Anxiety Level KPI. Measures how often the user experiences anxiety, especially before sleep."]
    burnout_level: Annotated[float, "Percentage score (0-100) for Burnout Level KPI. Reflects how overwhelmed or emotionally drained the user feels."]
    physical_fitness_score: Annotated[float, "Percentage score (0-100) for Physical Fitness KPI. Assesses the user's level of physical activity and strength."]
    dietary_habit_score: Annotated[float, "Percentage score (0-100) for Diet & Nutrition KPI. Evaluates the user's satisfaction with and balance of their eating habits."]
    focus_score: Annotated[float, "Percentage score (0-100) for Cognitive Performance and Focus KPI. Measures the user's ability to concentrate and stay focused on tasks."]
    overall_wellness_score: Annotated[float, "Aggregated overall wellness percentage score (0-100) based on all the individual KPIs."]
    package: Annotated[List[str], "List of recommended packages. Options include 'Focus', 'Fitness', and 'Insomnia'. The recommendation can be a single package, a combination of packages, or all three packages based on the assessment."]
    report: Annotated[str, "A detailed summary report of the assessment results and recommendations based on the KPI analysis."]

# --- Pydantic Model for Input ---
class PersonalDetails(BaseModel):
    name: str
    age: int
    gender: str
    height: str
    weight: str

class AssessmentInput(BaseModel):
    personal_details: PersonalDetails
    ans1: str
    ans2: str
    ans3: str
    ans4: str
    ans5: str
    ans6: str
    ans7: str
    ans8: str
    ans9: str
    ans10: str
    ans11: str
    ans12: str
    ans13: str
    ans14: str
    ans15: Optional[str] = None  # Optional field with default None

# --- Prompt Template ---
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

# --- FastAPI Endpoint ---
@app.post("/assess")
async def assess_wellness(data: AssessmentInput):
    try:
        # Prepare inputs for the prompt
        personal_details = data.personal_details.dict()
        answers = {
            f"ans{i}": getattr(data, f"ans{i}") for i in range(1, 16)
        }

        # Format the prompt
        prompt = prompt_template.format(**personal_details, **answers)

        # Run the assessment using the LLM
        structured_llm = chat.with_structured_output(AssessmentOutput)
        results = structured_llm.invoke(prompt)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Run the FastAPI App ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)