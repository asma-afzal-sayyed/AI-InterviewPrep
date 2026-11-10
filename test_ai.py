from google import genai

client = genai.Client(
    api_key="AIzaSyA1L9Rr6LGQPP3FDG3gBR_pTwFyy4A6BXk"
)

try:

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hello"
    )

    print(response.text)

except Exception as e:

    print("ERROR:")
    print(e)