import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import folium
from streamlit_folium import folium_static
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .emergency-button {
        background-color: #e74c3c;
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #ecf0f1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load the disease prediction model and data
@st.cache_resource
def load_model_and_data():
    """Load the trained model and symptom data"""
    try:
        # Create sample data for demonstration
        symptoms_data = {
            'fever': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            'headache': [1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            'fatigue': [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            'cough': [0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
            'sore_throat': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            'runny_nose': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            'body_pain': [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            'nausea': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            'vomiting': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            'diarrhea': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            'abdominal_pain': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        }
        
        diseases = ['Dengue', 'Common Cold', 'Migraine', 'Tension Headache', 
                   'Chronic Fatigue', 'Bronchitis', 'Pneumonia', 'Fibromyalgia', 
                   'Food Poisoning', 'Gastroenteritis']
        
        return symptoms_data, diseases
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Disease information database
disease_info = {
    'Dengue': {
        'description': 'A viral infection transmitted by mosquitoes',
        'symptoms': ['High fever', 'Severe headache', 'Body pain', 'Fatigue', 'Nausea'],
        'first_aid': [
            'Rest and stay hydrated',
            'Take acetaminophen for fever and pain',
            'Avoid aspirin and ibuprofen',
            'Monitor for severe symptoms',
            'Seek immediate medical attention if symptoms worsen'
        ],
        'diet': [
            'Drink plenty of fluids (water, coconut water, oral rehydration solutions)',
            'Eat light, easily digestible foods',
            'Include fruits rich in vitamin C',
            'Avoid fried and spicy foods',
            'Consume protein-rich foods for recovery'
        ],
        'emergency_signs': [
            'Severe abdominal pain',
            'Persistent vomiting',
            'Bleeding from gums or nose',
            'Difficulty breathing',
            'Cold, clammy skin'
        ]
    },
    'Common Cold': {
        'description': 'A viral infection of the upper respiratory tract',
        'symptoms': ['Runny nose', 'Sore throat', 'Cough', 'Congestion', 'Mild fever'],
        'first_aid': [
            'Rest and get plenty of sleep',
            'Stay hydrated with warm fluids',
            'Use saline nasal drops',
            'Gargle with warm salt water',
            'Take over-the-counter medications for symptoms'
        ],
        'diet': [
            'Drink warm fluids (tea, soup, broth)',
            'Eat vitamin C rich foods',
            'Include honey for sore throat',
            'Avoid dairy if it increases mucus',
            'Eat light, nutritious meals'
        ],
        'emergency_signs': [
            'High fever above 103°F',
            'Severe headache',
            'Difficulty breathing',
            'Chest pain',
            'Symptoms lasting more than 10 days'
        ]
    },
    'Migraine': {
        'description': 'A neurological condition causing severe headaches',
        'symptoms': ['Intense headache', 'Nausea', 'Sensitivity to light', 'Aura', 'Dizziness'],
        'first_aid': [
            'Rest in a quiet, dark room',
            'Apply cold or warm compress to head/neck',
            'Stay hydrated',
            'Practice relaxation techniques',
            'Take prescribed medications if available'
        ],
        'diet': [
            'Stay hydrated with water',
            'Eat regular meals to avoid low blood sugar',
            'Avoid trigger foods (chocolate, caffeine, aged cheese)',
            'Include magnesium-rich foods',
            'Eat ginger for nausea relief'
        ],
        'emergency_signs': [
            'Worst headache of your life',
            'Headache with fever and stiff neck',
            'Headache with confusion or difficulty speaking',
            'Headache after head injury',
            'Headache with vision problems'
        ]
    }
}

# Diet suggestions for general health
general_diet_tips = {
    'Hydration': 'Drink 8-10 glasses of water daily',
    'Fruits': 'Include 2-3 servings of fruits daily',
    'Vegetables': 'Eat 3-5 servings of vegetables daily',
    'Protein': 'Include lean protein in every meal',
    'Whole Grains': 'Choose whole grains over refined grains',
    'Healthy Fats': 'Include nuts, seeds, and olive oil',
    'Limit Processed Foods': 'Avoid highly processed and sugary foods',
    'Regular Meals': 'Eat at regular intervals to maintain blood sugar'
}

def predict_disease(symptoms_input, symptoms_data, diseases):
    """Predict disease based on symptoms"""
    if not symptoms_data or not diseases:
        return "Common Cold", 0.8  # Default fallback
    
    # Convert symptoms to feature vector
    feature_vector = []
    available_symptoms = list(symptoms_data.keys())
    
    for symptom in available_symptoms:
        if symptom.replace('_', ' ') in symptoms_input.lower():
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    
    # Simple rule-based prediction (in real app, use trained ML model)
    if sum(feature_vector) == 0:
        return "Common Cold", 0.6
    
    # Calculate similarity scores
    scores = []
    for i in range(len(diseases)):
        score = sum([feature_vector[j] * symptoms_data[symptom][i] 
                    for j, symptom in enumerate(available_symptoms)])
        scores.append(score)
    
    max_score = max(scores)
    predicted_disease = diseases[scores.index(max_score)]
    confidence = min(max_score / len(available_symptoms), 0.95)
    
    return predicted_disease, confidence

def get_nearby_hospitals(location):
    """Get nearby hospitals using Google Maps API"""
    try:
        # For demonstration, return sample hospital data
        # In production, use Google Maps API
        sample_hospitals = [
            {
                'name': 'City General Hospital',
                'address': '123 Main Street, Downtown',
                'distance': '0.5 km',
                'rating': 4.5,
                'phone': '+1-555-0123',
                'lat': 40.7128,
                'lng': -74.0060
            },
            {
                'name': 'Community Medical Center',
                'address': '456 Oak Avenue, Midtown',
                'distance': '1.2 km',
                'rating': 4.2,
                'phone': '+1-555-0456',
                'lat': 40.7589,
                'lng': -73.9851
            },
            {
                'name': 'Emergency Care Hospital',
                'address': '789 Pine Street, Uptown',
                'distance': '2.1 km',
                'rating': 4.7,
                'phone': '+1-555-0789',
                'lat': 40.7505,
                'lng': -73.9934
            }
        ]
        return sample_hospitals
    except Exception as e:
        st.error(f"Error fetching hospitals: {e}")
        return []

def send_emergency_alert(contact_info, location, symptoms):
    """Send emergency alert via SMS/Email"""
    try:
        # For demonstration, show alert message
        # In production, integrate with Twilio for SMS or smtplib for email
        st.success(f"🚨 Emergency alert sent to {contact_info}")
        st.info(f"Location: {location}")
        st.info(f"Symptoms: {symptoms}")
        return True
    except Exception as e:
        st.error(f"Error sending alert: {e}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Smart Health Companion</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-powered personal health advisor")
    
    # Load model and data
    symptoms_data, diseases = load_model_and_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["Health Assessment", "Nearby Hospitals", "Diet & Nutrition", "Emergency Help", "Health Tips"]
    )
    
    if page == "Health Assessment":
        st.markdown('<h2 class="sub-header">🔍 Health Assessment</h2>', unsafe_allow_html=True)
        
        # Symptom input
        st.write("### Describe your symptoms:")
        symptoms_input = st.text_area(
            "Enter your symptoms (e.g., fever, headache, fatigue, cough):",
            height=100,
            placeholder="Describe how you're feeling..."
        )
        
        if st.button("🔬 Analyze Symptoms", type="primary"):
            if symptoms_input.strip():
                with st.spinner("Analyzing your symptoms..."):
                    # Predict disease
                    predicted_disease, confidence = predict_disease(symptoms_input, symptoms_data, diseases)
                    
                    # Display results
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.write(f"**Predicted Condition:** {predicted_disease}")
                    st.write(f"**Confidence:** {confidence:.1%}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show disease information
                    if predicted_disease in disease_info:
                        info = disease_info[predicted_disease]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📋 Description")
                            st.write(info['description'])
                            
                            st.subheader("🚨 Emergency Signs")
                            for sign in info['emergency_signs']:
                                st.write(f"• {sign}")
                        
                        with col2:
                            st.subheader("⚕️ First Aid Steps")
                            for step in info['first_aid']:
                                st.write(f"• {step}")
                            
                            st.subheader("🍎 Diet Recommendations")
                            for diet in info['diet']:
                                st.write(f"• {diet}")
                    else:
                        st.info("General health advice will be provided based on your symptoms.")
                        
                        st.subheader("⚕️ General First Aid")
                        st.write("• Rest and stay hydrated")
                        st.write("• Monitor your symptoms")
                        st.write("• Seek medical attention if symptoms worsen")
                        
                        st.subheader("🍎 General Diet Tips")
                        for tip, advice in general_diet_tips.items():
                            st.write(f"• **{tip}:** {advice}")
            else:
                st.warning("Please enter your symptoms to get started.")
    
    elif page == "Nearby Hospitals":
        st.markdown('<h2 class="sub-header">🏥 Nearby Hospitals</h2>', unsafe_allow_html=True)
        
        # Location input
        location = st.text_input("Enter your location (city, address, or coordinates):", 
                                placeholder="e.g., New York, NY or 40.7128, -74.0060")
        
        if st.button("🔍 Find Hospitals"):
            if location:
                with st.spinner("Finding nearby hospitals..."):
                    hospitals = get_nearby_hospitals(location)
                    
                    if hospitals:
                        # Create map
                        map_center = [hospitals[0]['lat'], hospitals[0]['lng']]
                        m = folium.Map(location=map_center, zoom_start=12)
                        
                        for hospital in hospitals:
                            folium.Marker(
                                location=[hospital['lat'], hospital['lng']],
                                popup=f"<b>{hospital['name']}</b><br>{hospital['address']}<br>Phone: {hospital['phone']}",
                                icon=folium.Icon(color='red', icon='info-sign')
                            ).add_to(m)
                        
                        folium_static(m)
                        
                        # Display hospital list
                        st.subheader("📋 Hospital Details")
                        for i, hospital in enumerate(hospitals, 1):
                            with st.expander(f"{i}. {hospital['name']}"):
                                st.write(f"**Address:** {hospital['address']}")
                                st.write(f"**Distance:** {hospital['distance']}")
                                st.write(f"**Rating:** {hospital['rating']} ⭐")
                                st.write(f"**Phone:** {hospital['phone']}")
                    else:
                        st.warning("No hospitals found in your area.")
            else:
                st.warning("Please enter your location to find nearby hospitals.")
    
    elif page == "Diet & Nutrition":
        st.markdown('<h2 class="sub-header">🍎 Diet & Nutrition</h2>', unsafe_allow_html=True)
        
        # Diet recommendations based on condition
        condition = st.selectbox(
            "Select your health condition (optional):",
            ["General Health", "Dengue", "Common Cold", "Migraine", "Diabetes", "Hypertension"]
        )
        
        if condition == "General Health":
            st.subheader("🌱 General Nutrition Guidelines")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Daily Recommendations:**")
                for tip, advice in general_diet_tips.items():
                    st.write(f"• **{tip}:** {advice}")
            
            with col2:
                st.write("**Healthy Meal Ideas:**")
                st.write("• **Breakfast:** Oatmeal with berries and nuts")
                st.write("• **Lunch:** Grilled chicken salad with vegetables")
                st.write("• **Dinner:** Salmon with quinoa and steamed vegetables")
                st.write("• **Snacks:** Greek yogurt, fruits, or mixed nuts")
        else:
            if condition in disease_info:
                info = disease_info[condition]
                st.subheader(f"🍎 Diet Recommendations for {condition}")
                for diet in info['diet']:
                    st.write(f"• {diet}")
            else:
                st.info("General diet recommendations:")
                for tip, advice in list(general_diet_tips.items())[:4]:
                    st.write(f"• **{tip}:** {advice}")
    
    elif page == "Emergency Help":
        st.markdown('<h2 class="sub-header">🚨 Emergency Help</h2>', unsafe_allow_html=True)
        
        st.warning("⚠️ This feature is for demonstration purposes. In a real emergency, call your local emergency number immediately.")
        
        # Emergency contact setup
        st.subheader("📞 Emergency Contact Setup")
        contact_name = st.text_input("Emergency Contact Name:")
        contact_phone = st.text_input("Emergency Contact Phone:")
        contact_email = st.text_input("Emergency Contact Email:")
        
        # Current symptoms for emergency alert
        emergency_symptoms = st.text_area("Current symptoms (for emergency alert):")
        current_location = st.text_input("Your current location:")
        
        if st.button("🚨 SEND EMERGENCY ALERT", type="primary"):
            if contact_name and (contact_phone or contact_email):
                if send_emergency_alert(f"{contact_name} ({contact_phone or contact_email})", 
                                     current_location, emergency_symptoms):
                    st.success("Emergency alert sent successfully!")
                    st.info("Your emergency contact has been notified with your location and symptoms.")
            else:
                st.error("Please provide at least one contact method (phone or email).")
        
        # Emergency numbers
        st.subheader("📞 Important Emergency Numbers")
        emergency_numbers = {
            "United States": "911",
            "United Kingdom": "999",
            "Canada": "911",
            "Australia": "000",
            "India": "112",
            "Germany": "112",
            "France": "112",
            "Japan": "119"
        }
        
        for country, number in emergency_numbers.items():
            st.write(f"**{country}:** {number}")
    
    elif page == "Health Tips":
        st.markdown('<h2 class="sub-header">💡 Health Tips</h2>', unsafe_allow_html=True)
        
        # Daily health tips
        st.subheader("🌅 Daily Health Tips")
        
        tips = [
            "Start your day with a glass of warm water with lemon",
            "Take regular breaks from screen time to reduce eye strain",
            "Practice deep breathing exercises for stress relief",
            "Stay hydrated throughout the day",
            "Get at least 7-8 hours of quality sleep",
            "Include physical activity in your daily routine",
            "Eat a rainbow of fruits and vegetables",
            "Practice good posture while sitting and standing",
            "Limit processed foods and added sugars",
            "Maintain regular health check-ups"
        ]
        
        for i, tip in enumerate(tips, 1):
            st.write(f"{i}. {tip}")
        
        # Seasonal health advice
        st.subheader("🌤️ Seasonal Health Advice")
        current_month = datetime.now().month
        
        if current_month in [12, 1, 2]:  # Winter
            st.write("**Winter Health Tips:**")
            st.write("• Stay warm and layer clothing")
            st.write("• Boost immunity with vitamin C")
            st.write("• Moisturize skin to prevent dryness")
            st.write("• Exercise indoors when weather is extreme")
        elif current_month in [3, 4, 5]:  # Spring
            st.write("**Spring Health Tips:**")
            st.write("• Manage seasonal allergies")
            st.write("• Get outdoors for vitamin D")
            st.write("• Spring clean your living space")
            st.write("• Start outdoor exercise routines")
        elif current_month in [6, 7, 8]:  # Summer
            st.write("**Summer Health Tips:**")
            st.write("• Stay hydrated in hot weather")
            st.write("• Protect skin from UV rays")
            st.write("• Exercise during cooler hours")
            st.write("• Eat light, refreshing foods")
        else:  # Fall
            st.write("**Fall Health Tips:**")
            st.write("• Prepare for flu season")
            st.write("• Maintain regular sleep schedule")
            st.write("• Eat seasonal fruits and vegetables")
            st.write("• Stay active as days get shorter")

if __name__ == "__main__":
    main() 