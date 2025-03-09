# Wellness Assessment API

## Overview

The **Wellness Assessment API** is an AI-driven system that evaluates users' well-being based on their responses to a questionnaire. It predicts key wellness KPIs and provides personalized recommendations from the *DailyWellnessAI* platform.

## Features

- **Wellness KPI Prediction:** Predicts nine wellness KPIs (e.g., stress management, motivation, sleep quality, etc.).
- **Personalized Recommendations:** Provides recommendations for specific wellness packages (Focus, Insomnia, Fitness) based on the assessment.
- **Detailed Summary:** Generates a summary report justifying the recommendations based on user responses.

---

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/devroopsaha744/daily-wellness-ai-assgn-1.git
```

### 2. Navigate to the API Directory

```bash
cd daily-wellness-ai-assgn-1/api
```

### 3. Set Up a Virtual Environment

- **On macOS/Linux:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the `api` directory and add:

```env
GROQ_API_KEY=your_api_key_here
```

### 6. Run the API Locally

```bash
uvicorn main:app --reload
```

> *Note:* This command assumes your FastAPI application is defined in `main.py` with an instance called `app`.

### 7. Test the API

- **Root Endpoint:**  
  Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the welcome message.

- **Assessment Endpoint:**  
  Send a `POST` request to [http://127.0.0.1:8000/assess](http://127.0.0.1:8000/assess) with the sample JSON bodies below.

---

## API Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Response:**

  ```json
  {
    "message": "Welcome to the Wellness Assessment API!"
  }
  ```

### 2. Submit Wellness Assessment

- **URL:** `/assess`
- **Method:** `POST`

#### Request Format

**Headers:**
- `Content-Type: application/json`

**Body Example:**

```json
{
  "personal_details": {
    "name": "John Doe",
    "age": 30,
    "gender": "Male",
    "height": "180 cm",
    "weight": "80 kg"
  },
  "ans1": "Always",
  "ans2": "Poor",
  "ans3": "Severe",
  "ans4": "Poor",
  "ans5": "Always",
  "ans6": "Poor",
  "ans7": "Often",
  "ans8": "Often",
  "ans9": "Unhappy",
  "ans10": "Unbalanced",
  "ans11": "Never",
  "ans12": "Poor",
  "ans13": "Not at all",
  "ans14": "Poor",
  "ans15": "I constantly feel fatigued and stressed."
}
```

#### Expected Response Format

```json
{
  "stress_management": 30,
  "motivation": 20,
  "restless_night_score": 85,
  "anxiety_level": 70,
  "burnout_level": 75,
  "physical_fitness_score": 40,
  "dietary_habit_score": 50,
  "focus_score": 25,
  "overall_wellness_score": 45,
  "package": ["Focus", "Insomnia"],
  "report": "Based on your responses, you may struggle with focus, anxiety, and burnout. The Focus and Insomnia packages can help improve your mental clarity and sleep quality."
}
```

---

## Testing the API in Postman

### Sample Test Inputs and Expected Outputs

#### Person Who Needs Focus

**Input:**

```json
{
  "personal_details": {
    "name": "Alice Smith",
    "age": 28,
    "gender": "Female",
    "height": "165 cm",
    "weight": "60 kg"
  },
  "ans1": "Sometimes",
  "ans2": "Below Average",
  "ans3": "High",
  "ans4": "Poor",
  "ans5": "Rarely",
  "ans6": "Average",
  "ans7": "Occasionally",
  "ans8": "Rarely",
  "ans9": "Satisfied",
  "ans10": "Balanced",
  "ans11": "Sometimes",
  "ans12": "Average",
  "ans13": "Low",
  "ans14": "Fair",
  "ans15": "I struggle with focus at work and feel mentally drained."
}
```

**Expected Output:**

```json
{
  "stress_management": 40,
  "motivation": 30,
  "restless_night_score": 60,
  "anxiety_level": 50,
  "burnout_level": 65,
  "physical_fitness_score": 55,
  "dietary_habit_score": 60,
  "focus_score": 25,
  "overall_wellness_score": 45,
  "package": ["Focus"],
  "report": "Your responses indicate challenges with concentration and motivation. We recommend the Focus package to help boost your cognitive performance and alleviate burnout."
}
```

#### Person Who Needs Fitness

**Input:**

```json
{
  "personal_details": {
    "name": "Mark Johnson",
    "age": 35,
    "gender": "Male",
    "height": "180 cm",
    "weight": "95 kg"
  },
  "ans1": "Rarely",
  "ans2": "Good",
  "ans3": "Low",
  "ans4": "Good",
  "ans5": "Sometimes",
  "ans6": "Good",
  "ans7": "Rarely",
  "ans8": "Never",
  "ans9": "Not Satisfied",
  "ans10": "Unbalanced",
  "ans11": "Rarely",
  "ans12": "Weak",
  "ans13": "Average",
  "ans14": "Below Average",
  "ans15": "I feel sluggish and want to improve my fitness."
}
```

**Expected Output:**

```json
{
  "stress_management": 70,
  "motivation": 60,
  "restless_night_score": 40,
  "anxiety_level": 30,
  "burnout_level": 50,
  "physical_fitness_score": 30,
  "dietary_habit_score": 35,
  "focus_score": 55,
  "overall_wellness_score": 45,
  "package": ["Fitness"],
  "report": "Your responses suggest you struggle with physical fitness, diet, and overall strength. The Fitness package is recommended to improve your physical activity and nutritional habits."
}
```

#### Perfectly Healthy Person

**Input:**

```json
{
  "personal_details": {
    "name": "David Lee",
    "age": 26,
    "gender": "Male",
    "height": "175 cm",
    "weight": "70 kg"
  },
  "ans1": "Rarely",
  "ans2": "Excellent",
  "ans3": "Very Low",
  "ans4": "High",
  "ans5": "Never",
  "ans6": "Excellent",
  "ans7": "Never",
  "ans8": "Never",
  "ans9": "Very Satisfied",
  "ans10": "Balanced",
  "ans11": "Daily",
  "ans12": "Strong",
  "ans13": "Very High",
  "ans14": "Excellent",
  "ans15": "I feel great and always motivated."
}
```

**Expected Output:**

```json
{
  "stress_management": 95,
  "motivation": 95,
  "restless_night_score": 5,
  "anxiety_level": 5,
  "burnout_level": 5,
  "physical_fitness_score": 95,
  "dietary_habit_score": 95,
  "focus_score": 95,
  "overall_wellness_score": 97,
  "package": ["Focus", "Insomnia", "Fitness"],
  "report": "Your responses indicate excellent overall wellness with high scores in all areas. We recommend all three packages to further enhance your holistic well-being, giving you a comprehensive selection of services."
}
```

---

## Contributing

If you want to contribute to the project, please submit a pull request or open an issue.

---

## License

This project is licensed under the MIT License.
