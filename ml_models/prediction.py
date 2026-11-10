import pickle

# Load files
model = pickle.load(open("ml_models/model.pkl", "rb"))
vectorizer = pickle.load(open("ml_models/vectorizer.pkl", "rb"))

def predict_job_role(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    return prediction[0]