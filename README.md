### Yoga Planner Bot

Yoga Planner Bot is a smart Streamlit tool that curates customized yoga routines based on your profile and intentions, helping you build a consistent and mindful practice. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI’s GPT-4 model, the app delivers curated yoga sequences that you can practice anytime, anywhere.

## Folder Structure

```
Yoga-Planner-Bot/
├── yoga-planner-bot.py
├── README.md
└── requirements.txt
```

- **yoga-planner-bot.py**: The main Streamlit application.
- **requirements.txt**: A list of required Python packages.
- **README.md**: This documentation file.

## Features

- **User Profile Input:**  
  Collect key user details such as age, height, weight, sex, injury history, yoga goals, experience level, and practice preferences (pace, time of day, duration).

- **AI-Personalized Yoga Routine:**  
  Receive a yoga plan tailored to your selected session duration (10–15 mins to 1+ hour). Each plan includes:
  - A sequence overview
  - A curated list of yoga poses with instructions and durations
  - Modifications for beginners or injuries
  - Practice recommendations
  - Wellness tips for consistency and setup

- **Visually Organized Pose Layout:**  
  Pose instructions are displayed in a clean 4-column grid with numbered subheadings and markdown formatting for readability.

- **Download Your Plan:**  
  Export your customized yoga regimen as a `.txt` file for future reference.

- **Guided Streamlit Interface:**  
  Intuitive interface that walks users through input, generation, display, and download of their personalized plan.

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key (get yours [here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository** (or download it):
   ```bash
   git clone https://github.com/akash301191/Yoga-Planner-Bot.git
   cd Yoga-Planner-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   venv\Scripts\activate           # On Windows
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run yoga-planner-bot.py
   ```
2. **Open your browser** to the displayed URL (usually `http://localhost:8501`).
3. **Interact with the app**:
   - Enter your OpenAI API key.
   - Fill in your profile and yoga preferences.
   - Click **"Generate My Personalized Yoga Plan"**.
   - View the yoga sequence, modifications, and tips.
   - Click the **Download** button to save your plan.
   - **Disclaimer:** Always consult a certified yoga instructor or healthcare professional before starting a new practice.

## Code Overview

- **`render_profile`**: Collects user inputs across two columns (personal info & yoga preferences).
- **`initialize_openai_model`**: Initializes the OpenAI model with the provided key.
- **`generate_yoga_plan`**: Uses an Agno agent to generate a JSON yoga plan based on the profile.
- **`display_yoga_plan`**: Formats the yoga plan into structured sections and displays poses in a 4-column layout with markdown.
- **`main`**: Manages the app flow, from input to AI interaction, display, disclaimer, and download.

## Contributions

Contributions are welcome! Feel free to fork this repo, suggest improvements, or open a pull request. Be sure to maintain code quality and provide supporting documentation where needed.
