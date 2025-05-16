# ml/symptom_analyzer.py

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample training data (symptoms)
X_train = [
    "headache",
    "fever",
    "cold and cough",
    "inflammation and pain",
    "muscle pain",
    "stomach pain",
    "nausea and vomiting",
    "sore throat",
    "body ache",
    "diarrhea",
    "constipation",
    "allergy symptoms",
    "back pain",
    "joint pain",
    "toothache",
    "fatigue",
    "stress",
    "anxiety",
    "insomnia",
    "acne"
]

# Corresponding medicines (labels)
Y_train = [
    "Paracetamol",         
    "Antipyretic",         
    "Cough Syrup",          
    "Anti-inflammatory",    
    "Painkiller",           
    "Antacid",              
    "Antiemetic",           
    "Lozenges",             
    "Pain Reliever",        
    "Oral Rehydration Salts", 
    "Laxative",             
    "Antihistamine",        
    "Muscle Relaxant",      
    "Analgesic",             
    "Pain Reliever",         
    "Energy Supplement",     
    "Anxiolytic",           
    "Anxiolytic",           
    "Sleep Aid",           
    "Topical Cream"         
]

# Create the pipeline (vectorizer + model)
pipeline = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the pipeline
pipeline.fit(X_train, Y_train)

# Save the trained pipeline
model_path = 'C:file_path_symptom_analyzer.pkl'

with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print("✅ Symptom analyzer model (pipeline) trained and saved successfully!")

# Optional: Test prediction (you can remove below part after testing)
user_input = input("Enter your symptom: ")
prediction = pipeline.predict([user_input])
print(f"Recommended Medicine for '{user_input}': {prediction[0]}")
