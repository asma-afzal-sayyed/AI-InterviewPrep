from ai_helper import generate_ai_response

def chatbot_response(message):

    prompt = f"""
    You are an Interview Preparation AI Assistant.

    Rules:
    - Reply short
    - Use simple English
    - Use bullet points when needed
    - Give interview-focused answers
    - Keep formatting clean
    - Avoid very long paragraphs

    Question:
    {message}
    """

    return generate_ai_response(prompt)