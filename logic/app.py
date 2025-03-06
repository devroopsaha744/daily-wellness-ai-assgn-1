import streamlit as st
from assessment import WellnessAssessor
import visuals

def main():
    st.set_page_config(page_title="AI Wellness Assistant", page_icon="💪", layout="wide")
    
    # Sidebar with inputs
    with st.sidebar:
        st.title("🧘 Wellness Assessment")
        st.markdown("Complete this 20-question survey to get personalized wellness recommendations!")
        
        # Question form
        with st.form("assessment_form"):
            responses = {}
            
            # Question 1
            responses['ans1'] = st.selectbox(
                "1. How often do you feel stressed by daily tasks?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 2
            responses['ans2'] = st.selectbox(
                "2. How good are you at handling stress?",
                ["Excellent", "Good", "Fair", "Poor"]
            )
            
            # Question 3
            responses['ans3'] = st.selectbox(
                "3. How confident are you in the ways you deal with stress?",
                ["Confident", "Somewhat Confident", "Not at all"]
            )
            
            # Question 4
            responses['ans4'] = st.selectbox(
                "4. How motivated are you to work on your wellness goals daily?",
                ["Very motivated", "Moderately motivated", "Slightly motivated", "Not at all"]
            )
            
            # Question 5
            responses['ans5'] = st.selectbox(
                "5. How much energy do you have when you start your day to work on your goals?",
                ["Full energy", "Some energy", "Very little energy", "None"]
            )
            
            # Question 6
            responses['ans6'] = st.selectbox(
                "6. How often do you have trouble falling asleep?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 7
            responses['ans7'] = st.selectbox(
                "7. How would you rate the quality of your sleep overall?",
                ["Excellent", "Good", "Fair", "Poor"]
            )
            
            # Question 8
            responses['ans8'] = st.selectbox(
                "8. How often do you wake up during the night?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 9
            responses['ans9'] = st.selectbox(
                "9. Do you feel refreshed when you wake up in the morning?",
                ["Always", "Most of the time", "Sometimes", "Never"]
            )
            
            # Question 10
            responses['ans10'] = st.selectbox(
                "10. How often do you feel physical signs of anxiety during your daily activities?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 11
            responses['ans11'] = st.selectbox(
                "11. How easy can you calm down when you're feeling anxious?",
                ["Very easy", "Neutral", "Somewhat difficult", "Very difficult"]
            )
            
            # Question 12
            responses['ans12'] = st.selectbox(
                "12. How often do you feel nervous for no apparent reason?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 13
            responses['ans13'] = st.selectbox(
                "13. How often do you feel emotionally drained from work or your daily responsibilities?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 14
            responses['ans14'] = st.selectbox(
                "14. How would you rate your current level of burnout?",
                ["Not at all", "Mild", "Moderate", "Severe"]
            )
            
            # Question 15
            responses['ans15'] = st.selectbox(
                "15. How often do you feel uninterested in your daily tasks?",
                ["Never", "Sometimes", "Often", "Always"]
            )
            
            # Question 16
            responses['ans16'] = st.selectbox(
                "16. Do you feel like your workload is too much to handle?",
                ["Never", "Sometimes", "Often", "Always"]
            )
                        
            # Question 17
            responses['ans17'] = st.selectbox(
                "18. How happy are you with your current eating habits?",
                ["Satisfied", "Neutral", "Unsatisfied", "Very unsatisfied"]
            )
            
            # Question 18
            responses['ans18'] = st.selectbox(
                "19. How often do you do physical activities like yoga, stretching, or exercise?",
                ["Daily", "Several times a week", "Once a week", "Never"]
            )
            
            # Question 19
            responses['ans19'] = st.selectbox(
                "20. How would you rate your ability to stay focused and concentrate on daily tasks?",
                ["Excellent", "Good", "Fair", "Poor"]
            )
            
            submitted = st.form_submit_button("Get Assessment")
    
    # Main content
    st.title("AI Wellness Assessment Dashboard")
    
    if submitted:
        with st.spinner("🔍 Analyzing your responses..."):
            assessor = WellnessAssessor()
            result = assessor.assess_responses(responses)
        
        visuals.display_results(result)

if __name__ == "__main__":
    main()