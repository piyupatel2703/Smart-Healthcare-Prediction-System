# HealthPulse AI — Smart Healthcare Prediction System

Streamlit project inspired by the user's CareerPath AI deployment style. A responsive, interactive healthcare dashboard and educational screening demo.

## Run locally (Windows)
1. Install Python 3.10+.
2. Download/extract the project.
3. Open the folder in VS Code.
4. In VS Code Terminal run:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. The app opens in your browser. On your phone, use the deployed Render URL.

## GitHub
Create a new public repository and upload all project files. Keep `app.py` and `requirements.txt` in the repository root.

## Render deployment
1. Push the project to GitHub.
2. On Render, choose **New → Web Service** and connect the repository.
3. Environment: Python.
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Deploy. The included `render.yaml` can also be used as a blueprint.

## Features
- Dashboard metrics and illustrative charts
- Health Risk Assessment form
- Transparent, simplified demo scoring
- Conditional wellness prompts
- Health Insights page
- About/project page
- Responsive Streamlit layout

## Disclaimer
This is a classroom prototype. It does not use a validated clinical model, is not a medical device and must not be used to diagnose, predict, or treat disease. Dashboard metrics are illustrative. The app does not save or upload health form values.
