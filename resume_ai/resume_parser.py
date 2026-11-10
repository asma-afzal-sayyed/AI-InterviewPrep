import pdfplumber

from ai_helper import generate_ai_response
from ml_models.prediction import predict_job_role


def analyze_resume(pdf_file):

    text = ""

    try:

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

    except:

        return """
❌ Invalid PDF File.

Please upload a proper resume PDF.
"""

    # ML Prediction
    predicted_role = predict_job_role(text)

    prompt = f"""
    Analyze this resume.

    Give response in SHORT format only.

    Format:

    Resume Score: score out of 100

    ✅ Skills Found
    - skill names only

    ❌ Missing Skills
    - important missing skills only

    🚀 Suggestions
    - 3 short points only

    Keep response clean and professional.

    Resume:
    {text}
    """

    # Gemini AI Response
    ai_response = generate_ai_response(prompt)

    result = f"""
🎯 Predicted Job Role:
{predicted_role}

{ai_response}
"""

    return result