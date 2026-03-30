<p align="center">
  <img src="static/description/icon.png" alt="WellnessCheck" width="120"/>
</p>

# WellnessChecker

**WellnessCheck** is a specialized Odoo module designed to help Human Resources departments track and improve employee morale through non-intrusive, anonymous daily check-ins. 

In a modern workplace, understanding the emotional state of a workforce is key to retention and productivity. WellnessCheck provides the tools to bridge the gap between management and employees.

---

## 🌟 Key Features

### 1. Daily Wellness Pulse
- **Automatic Login Popup**: Upon the first login of the day, employees are greeted with a friendly wellness wizard.
- **Mood Tracking**: A visual mood slider (1-10) for quick sentiment reporting.
- **Open Feedback**: Three targeted questions to capture qualitative data on performance, stress, and general happiness.

### 2. Intelligent Sentiment Analysis
- **Keyword Recognition**: The module automatically parses feedback to detect positive or negative trends.
- **Automated Summary**: Generates a brief textual analysis based on combining numerical scores and textual sentiment.
- **Classification**: Categorizes responses into "Happy," "Neutral," or "Sad" for high-level reporting.

### 3. HR Wellness Dashboard
- **Visual Analytics**: Interactive charts (pie charts, line graphs) to visualize organizational happiness over time.
- **Trend Identification**: Spot morale dips or peaks immediately.
- **Anonymity by Design**: Focuses on collective data trends rather than individual monitoring, encouraging honest feedback.

---

## 🚀 Installation

1. Place the `wellness_check` folder into your Odoo `addons` directory.
2. Update the App List in Odoo and search for "WellnessCheck".
3. Install the module.
4. Ensure employees have the necessary permissions assigned via the "Human Resources" access groups.

---

## 🛠️ Technical Details

- **Dependencies**: `base`, `web`, `hr`.
- **Framework**: Developed for Odoo 17+ (compatible with standard web assets).
- **Backend Service**: Uses a JavaScript service (`wellness_check_service.js`) to trigger the check-in wizard asynchronously after login.

---

## 📁 Project Structure

- `models/`: Defines the data structure for wellness records and question templates.
- `wizard/`: Contains the logic and view for the daily popup survey.
- `static/src/js/`: Handles the client-side trigger logic for the login survey.
- `views/`: Dashboard, form, and tree views for HR oversight.

