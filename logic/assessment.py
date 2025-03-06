from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import TypedDict, List
from typing_extensions import Annotated
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AssessmentOutput(TypedDict):
    """Assessment output structure"""
    stress_management: Annotated[float, "Stress Management Score Out of 10"]
    motivation: Annotated[float, "Motivation Score Out of 10"]
    restless_night_score: Annotated[float, "Restless Night Score Out of 10"]
    anxiety_level: Annotated[float, "Anxiety Level Score Out of 10"]
    burnout_level: Annotated[float, "Burnout Level Score Out of 10"]
    balanced_weight: Annotated[float, "Balanced Weight Score Out of 10"]
    package_focus: Annotated[str, "Recommended Package: Focus Or Nutrituion Or Physical Activity"]
    report: Annotated[str, "Summary Report"]

class WellnessAssessor:
    def __init__(self):
        # Read API key from .env file
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.chat = ChatGroq(api_key=self.api_key, model="llama-3.3-70b-versatile")
        self.prompt_template = self._create_prompt_template()
        
    def _create_prompt_template(self):
        template = """
        You are an AI wellness assessment system. Based on the user's responses, predict the following KPIs:
- stress_management
- motivation
- restless_night_score
- anxiety_level
- burnout_level
- balanced_weight
- package_focus (Focus, Nutrition, or Fitness)
- report (a summary of the assessment results and recommendations)

### Assessment Questions:

1. How often do you feel stressed by daily tasks?  
   Options: Never, Sometimes, Often, Always  
   Answer: {ans1}

2. How good are you at handling stress?  
   Options: Excellent, Good, Fair, Poor  
   Answer: {ans2}

3. How confident are you in the ways you deal with stress?  
   Options: Confident, Somewhat Confident, Not at all  
   Answer: {ans3}

4. How motivated are you to work on your wellness goals daily?  
   Options: Very motivated, Moderately motivated, Slightly motivated, Not at all  
   Answer: {ans4}

5. How much energy do you have when you start your day to work on your goals?  
   Options: Full energy, Some energy, Very little energy, None  
   Answer: {ans5}

6. How often do you have trouble falling asleep?  
   Options: Never, Sometimes, Often, Always  
   Answer: {ans6}

7. How would you rate the quality of your sleep overall?  
   Options: Excellent, Good, Fair, Poor  
   Answer: {ans7}

8. How often do you wake up during the night?  
   Options: Never, Sometimes, Often, Always  
   Answer: {ans8}

9. Do you feel refreshed when you wake up in the morning?  
   Options: Always, Most of the time, Sometimes, Never  
   Answer: {ans9}

10. How often do you feel physical signs of anxiety during your daily activities?  
    Options: Never, Sometimes, Often, Always  
    Answer: {ans10}

11. How easy can you calm down when you're feeling anxious?  
    Options: Very easy, Neutral, Somewhat difficult, Very difficult  
    Answer: {ans11}

12. How often do you feel nervous for no apparent reason?  
    Options: Never, Sometimes, Often, Always  
    Answer: {ans12}

13. How often do you feel emotionally drained from work or your daily responsibilities?  
    Options: Never, Sometimes, Often, Always  
    Answer: {ans13}

14. How would you rate your current level of burnout?  
    Options: Not at all, Mild, Moderate, Severe  
    Answer: {ans14}

15. How often do you feel uninterested in your daily tasks?  
    Options: Never, Sometimes, Often, Always  
    Answer: {ans15}

16. Do you feel like your workload is too much to handle?  
    Options: Never, Sometimes, Often, Always  
    Answer: {ans16}

17. How happy are you with your current eating habits?  
    Options: Satisfied, Neutral, Unsatisfied, Very unsatisfied  
    Answer: {ans17}

18. How often do you do physical activities like yoga, stretching, or exercise?  
    Options: Daily, Several times a week, Once a week, Never  
    Answer: {ans18}

19. How would you rate your ability to stay focused and concentrate on daily tasks?  
    Options: Excellent, Good, Fair, Poor  
    Answer: {ans19}

Use this information to generate KPI predictions and a summary report.
"""  # Same template as original notebook
        return PromptTemplate(
            input_variables=[f"ans{i}" for i in range(1,20)],
            template=template
        )
    
    def assess_responses(self, responses):
        formatted_prompt = self.prompt_template.format(**responses)
        structured_llm = self.chat.with_structured_output(AssessmentOutput)
        return structured_llm.invoke(formatted_prompt)