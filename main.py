from fastapi.middleware.cors import CORSMiddleware  
from fastapi import FastAPI
from pydantic import BaseModel
import motor.motor_asyncio
from bson import ObjectId
import pickle
from fuzzywuzzy import process
from models.ml.feedback_model import process_feedback
# Create FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from your frontend (you can add more origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, or specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (e.g., GET, POST)
    allow_headers=["*"],  # Allows all headers
)

# Correct paths
model_path = 'C:/Users/Harinishree/OneDrive/Documents/GreenPrescribe/greenprescribe-backend/models/ml/symptom_model.pkl'

with open(model_path, 'rb') as f:
    symptom_pipeline = pickle.load(f)


print("Model loaded successfully!")

# Home Remedies Dictionary
# Expanded Home Remedies Dictionary with more symptoms
home_remedies = {
    "headache": {
        "remedy": "Mint tea or Rest in a dark room",
        "details": [
            "Mint Tea: Use fresh mint leaves to brew a relaxing tea. Mint has menthol that can help soothe tension headaches.",
            "Rest in a Dark Room: Sit in a quiet, dark room to reduce light sensitivity and relieve pressure."
        ]
    },
    "fever": {
        "remedy": "Cold Compress and Hydration",
        "details": [
            "Cold Compress: Apply a cold compress to the forehead or back of the neck. It helps to bring down body temperature.",
            "Hydration: Drink plenty of fluids like water, coconut water, or herbal teas to prevent dehydration."
        ]
    },
    "cold and cough": {
        "remedy": "Honey and Lemon Tea",
        "details": [
            "Honey: Natural honey helps soothe the throat and reduces coughing.",
            "Lemon: Rich in vitamin C, lemon helps in boosting immunity.",
            "Tea: Herbal teas like chamomile or ginger tea can also help clear congestion."
        ]
    },
    "inflammation and pain": {
        "remedy": "Turmeric in Warm Milk",
        "details": [
            "Turmeric: Known for its anti-inflammatory properties, turmeric can help reduce swelling and pain.",
            "Warm Milk: Mix turmeric into warm milk (golden milk) for a soothing drink that reduces inflammation and promotes relaxation."
        ]
    },
    "muscle pain": {
        "remedy": "Hot Water Compress or Gentle Stretching",
        "details": [
            "Hot Water Compress: Applying a hot compress or heating pad to sore muscles can help alleviate pain by relaxing the muscles.",
            "Gentle Stretching: Light stretching can improve blood circulation and relieve tension in the muscles."
        ]
    },
    "stomach pain": {
        "remedy": "Ginger Tea or Warm Water",
        "details": [
            "Ginger Tea: Ginger has natural anti-nausea properties and helps reduce stomach cramps and bloating.",
            "Warm Water: Sipping warm water can relax the digestive system and alleviate stomach discomfort."
        ]
    },
    "nausea and vomiting": {
        "remedy": "Peppermint Tea or Ginger Ale",
        "details": [
            "Peppermint Tea: Peppermint calms the stomach and helps in reducing nausea.",
            "Ginger Ale: The ginger in ginger ale helps settle the stomach, especially for morning sickness or nausea caused by motion sickness."
        ]
    },
    "sore throat": {
        "remedy": "Saltwater Gargle",
        "details": [
            "Saltwater Gargle: Gargling warm salt water can help reduce throat inflammation and kill bacteria.",
            "Honey and Lemon: A mix of honey and lemon in warm water can help soothe the throat and reduce irritation."
        ]
    },
    "body ache": {
        "remedy": "Warm Bath with Epsom Salt",
        "details": [
            "Epsom Salt Bath: Soaking in a warm bath with Epsom salt can help relax muscles and reduce inflammation.",
            "Gentle Massage: A light massage can improve circulation and alleviate aches in the body."
        ]
    },
    "diarrhea": {
        "remedy": "BRAT Diet (Banana, Rice, Applesauce, Toast)",
        "details": [
            "Banana: Bananas are easy on the stomach and can help replenish lost nutrients.",
            "Rice: Plain rice is easy to digest and helps bind the stool.",
            "Applesauce: Applesauce is gentle on the stomach and provides some fiber.",
            "Toast: Plain, dry toast helps absorb excess stomach acid and can prevent further irritation."
        ]
    },
    "constipation": {
        "remedy": "Increase Fiber and Warm Water",
        "details": [
            "Fiber-Rich Foods: Incorporating foods like whole grains, fruits, and vegetables can help with regular bowel movements.",
            "Warm Water: Drinking warm water can help stimulate the digestive system and relieve constipation."
        ]
    },
    "allergy symptoms": {
        "remedy": "Steam Inhalation with Eucalyptus",
        "details": [
            "Steam Inhalation: Inhaling steam infused with eucalyptus oil can help clear nasal congestion and soothe irritated sinuses.",
            "Eucalyptus Oil: Known for its anti-inflammatory properties, eucalyptus oil can help relieve allergy symptoms."
        ]
    },
    "back pain": {
        "remedy": "Gentle Yoga Stretch",
        "details": [
            "Yoga Stretch: Gentle yoga poses can help relieve tension in the back and improve flexibility.",
            "Hot Compress: Applying heat to the back can relax muscles and alleviate pain."
        ]
    },
    "joint pain": {
        "remedy": "Hot and Cold Therapy",
        "details": [
            "Hot Therapy: Applying heat to the affected joint can help relax muscles and reduce stiffness.",
            "Cold Therapy: Ice packs can reduce inflammation and numb the area to ease pain."
        ]
    },
    "toothache": {
        "remedy": "Clove Oil Application",
        "details": [
            "Clove Oil: Clove oil has analgesic properties that can numb the pain and reduce inflammation in the tooth and gums.",
            "Saltwater Gargle: Gargling warm salt water can help clean the area and reduce swelling."
        ]
    },
    "fatigue": {
        "remedy": "Rest and Hydration",
        "details": [
            "Adequate Sleep: Ensuring sufficient sleep and rest is crucial for recharging energy levels.",
            "Hydration: Drink water and healthy fluids to prevent dehydration, which can cause fatigue."
        ]
    },
    "stress": {
        "remedy": "Deep Breathing and Meditation",
        "details": [
            "Deep Breathing: Engage in deep breathing exercises to reduce stress and calm the mind.",
            "Meditation: Regular meditation can help manage stress and improve overall well-being."
        ]
    },
    "anxiety": {
        "remedy": "Lavender Oil or Chamomile Tea",
        "details": [
            "Lavender Oil: Lavender has calming properties that can help reduce anxiety and promote relaxation.",
            "Chamomile Tea: Chamomile is a natural sedative that can help calm nerves and reduce anxiety symptoms."
        ]
    },
    "insomnia": {
        "remedy": "Warm Milk and Relaxation Techniques",
        "details": [
            "Warm Milk: Drinking warm milk before bed can help induce sleep by boosting serotonin levels.",
            "Relaxation Techniques: Practicing relaxation techniques such as progressive muscle relaxation can help you fall asleep faster."
        ]
    },
    "acne": {
        "remedy": "Tea Tree Oil or Aloe Vera",
        "details": [
            "Tea Tree Oil: Tea tree oil has antibacterial properties and can help reduce acne breakouts.",
            "Aloe Vera: Aloe vera can help reduce inflammation and promote healing of acne lesions."
        ]
    }
}

# MongoDB Client setup
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")  # Assuming MongoDB is running locally
db = client["greenprescribe"]  # Database name
feedback_collection = db["feedback"]  # Collection name


# Define the request structures
class SymptomRequest(BaseModel):
    symptoms: str

class FeedbackRequest(BaseModel):
    feedback: str
    symptoms: str = None  
    recommended_medicine: str = None
    recommended_home_remedy: str = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the GreenPrescribe API!"}

# API to predict medicine and home remedy
@app.post("/predict")
def predict_medicine(request: SymptomRequest):
    symptoms = request.symptoms
    print(f"Symptoms received: {symptoms}")

    # Use the pipeline to predict medicine
    prediction = symptom_pipeline.predict([symptoms])[0]

    # Try to find a matching home remedy
    remedy = "No specific home remedy found."
    remedy_details = []
    matches = process.extractOne(symptoms.lower(), home_remedies.keys())
    if matches and matches[1] > 80:  # 80 is the threshold for matching accuracy
        remedy = home_remedies[matches[0]]["remedy"]
        remedy_details = home_remedies[matches[0]]["details"]

    prescription_card = {
        "Prescription Card": {
            "Symptoms Reported": symptoms.title(),
            "Recommended Medicine": prediction,
            "Suggested Home Remedy": {
                "remedy": remedy,
                "details": remedy_details,
                "doctor_note": "Please follow dosage instructions carefully. Consult a physician if symptoms persist."
            }
        }
    }

    return prescription_card



@app.post("/submit_feedback/")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        feedback_data = feedback.dict()
        
        # Process the sentiment
        sentiment = process_feedback(feedback.feedback)
        feedback_data['sentiment'] = sentiment
        
        # Add feedback to the database
        result = await feedback_collection.insert_one(feedback_data)
        
        return {"message": "Feedback submitted successfully", "feedback_id": str(result.inserted_id), "sentiment": sentiment}
    except Exception as e:
        print(f"Error while submitting feedback: {e}")
        return {"message": "❌ Failed to send feedback. Please try again."}

# Endpoint to get feedback from MongoDB
@app.get("/get_feedback/{feedback_id}")
async def get_feedback(feedback_id: str):
    feedback = await feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    
    if feedback:
        feedback["_id"] = str(feedback["_id"])  # Convert ObjectId to string
        return feedback
    else:
        return {"message": "Feedback not found"}
