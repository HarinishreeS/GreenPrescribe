import pickle
import os

# Paths to the model and vectorizer
model_path = 'C:/Users/Harinishree/OneDrive/Documents/GreenPrescribe/greenprescribe-backend/models/ml/symptom_model.pkl'
vectorizer_path = 'C:/Users/Harinishree/OneDrive/Documents/GreenPrescribe/greenprescribe-backend/models/ml/symptom_vectorizer.pkl'

# Ensure that the files exist before loading
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

if not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")

# Load the model and vectorizer
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

print("Model and vectorizer loaded successfully!")