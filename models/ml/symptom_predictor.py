# ml/symptom_predictor.py

import pickle

# Load the trained symptom analyzer pipeline
model_path = 'C:file_path_symptom_model.pkl'

with open(model_path, 'rb') as f:
    symptom_pipeline = pickle.load(f)

print("✅ Symptom analyzer model loaded successfully!")

# Function to predict medicine based on symptom
def predict_medicine(symptom):
    prediction = symptom_pipeline.predict([symptom])
    return prediction[0]

# If you want to test manually:
if __name__ == "__main__":
    user_input = input("Enter your symptom: ")
    recommended_medicine = predict_medicine(user_input)
    print(f"Recommended Medicine for '{user_input}': {recommended_medicine}")





