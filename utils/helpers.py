"""
Utility functions for Smart Health Companion
"""

import pandas as pd
import numpy as np
import re
import json
from typing import List, Dict, Tuple, Optional
import requests
from datetime import datetime

def clean_symptoms_text(text: str) -> str:
    """
    Clean and normalize symptoms text input
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_symptoms_from_text(text: str) -> List[str]:
    """
    Extract individual symptoms from text input
    """
    common_symptoms = [
        'fever', 'headache', 'fatigue', 'cough', 'sore throat', 'runny nose',
        'body pain', 'nausea', 'vomiting', 'diarrhea', 'abdominal pain',
        'chest pain', 'shortness of breath', 'dizziness', 'loss of appetite',
        'muscle pain', 'joint pain', 'back pain', 'neck pain', 'eye pain',
        'ear pain', 'tooth pain', 'skin rash', 'itching', 'swelling',
        'numbness', 'tingling', 'weakness', 'confusion', 'memory loss',
        'anxiety', 'depression', 'insomnia', 'excessive sleep', 'weight loss',
        'weight gain', 'sweating', 'chills', 'hot flashes', 'cold hands',
        'palpitations', 'irregular heartbeat', 'high blood pressure',
        'low blood pressure', 'blurred vision', 'double vision', 'blindness',
        'hearing loss', 'ringing in ears', 'loss of balance', 'seizures',
        'paralysis', 'speech problems', 'swallowing problems', 'constipation',
        'blood in stool', 'blood in urine', 'frequent urination', 'painful urination'
    ]
    
    cleaned_text = clean_symptoms_text(text)
    found_symptoms = []
    
    for symptom in common_symptoms:
        if symptom in cleaned_text:
            found_symptoms.append(symptom)
    
    return found_symptoms

def calculate_symptom_severity(symptoms: List[str]) -> Dict[str, str]:
    """
    Calculate severity level for each symptom
    """
    severity_levels = {
        'mild': ['runny nose', 'mild cough', 'slight fatigue'],
        'moderate': ['fever', 'headache', 'body pain', 'sore throat'],
        'severe': ['chest pain', 'shortness of breath', 'severe pain', 'paralysis']
    }
    
    symptom_severity = {}
    
    for symptom in symptoms:
        if any(severe in symptom for severe in severity_levels['severe']):
            symptom_severity[symptom] = 'severe'
        elif any(moderate in symptom for moderate in severity_levels['moderate']):
            symptom_severity[symptom] = 'moderate'
        else:
            symptom_severity[symptom] = 'mild'
    
    return symptom_severity

def get_emergency_priority(symptoms: List[str]) -> str:
    """
    Determine emergency priority based on symptoms
    """
    emergency_symptoms = [
        'chest pain', 'shortness of breath', 'severe pain', 'paralysis',
        'seizures', 'loss of consciousness', 'severe bleeding', 'head injury'
    ]
    
    urgent_symptoms = [
        'high fever', 'severe headache', 'severe vomiting', 'severe diarrhea',
        'severe abdominal pain', 'severe dizziness', 'severe weakness'
    ]
    
    for symptom in symptoms:
        if any(emergency in symptom for emergency in emergency_symptoms):
            return 'immediate'
        elif any(urgent in symptom for urgent in urgent_symptoms):
            return 'urgent'
    
    return 'routine'

def format_emergency_message(patient_info: Dict, symptoms: List[str], location: str) -> str:
    """
    Format emergency alert message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity = get_emergency_priority(symptoms)
    
    message = f"""
🚨 EMERGENCY ALERT 🚨
Time: {timestamp}
Patient: {patient_info.get('name', 'Unknown')}
Location: {location}
Severity: {severity.upper()}

Symptoms:
{chr(10).join([f"• {symptom}" for symptom in symptoms])}

Please respond immediately if this is an emergency.
"""
    
    return message

def validate_location(location: str) -> bool:
    """
    Basic validation for location input
    """
    if not location or len(location.strip()) < 3:
        return False
    
    # Check if it contains at least some alphanumeric characters
    if not re.search(r'[a-zA-Z0-9]', location):
        return False
    
    return True

def format_hospital_data(hospital: Dict) -> Dict:
    """
    Format hospital data for display
    """
    return {
        'name': hospital.get('name', 'Unknown Hospital'),
        'address': hospital.get('address', 'Address not available'),
        'distance': hospital.get('distance', 'Distance unknown'),
        'rating': hospital.get('rating', 0),
        'phone': hospital.get('phone', 'Phone not available'),
        'lat': hospital.get('lat', 0),
        'lng': hospital.get('lng', 0)
    }

def get_weather_health_tips(weather_condition: str) -> List[str]:
    """
    Get health tips based on weather conditions
    """
    weather_tips = {
        'hot': [
            'Stay hydrated with plenty of water',
            'Avoid outdoor activities during peak heat hours',
            'Wear light, breathable clothing',
            'Use sunscreen with high SPF',
            'Take cool showers to regulate body temperature'
        ],
        'cold': [
            'Dress in layers to stay warm',
            'Keep your home well-heated',
            'Stay active to generate body heat',
            'Eat warm, nutritious foods',
            'Protect your skin from cold and wind'
        ],
        'rainy': [
            'Stay dry to prevent cold and flu',
            'Use proper footwear to prevent slips',
            'Keep your immune system strong',
            'Stay indoors during heavy rain',
            'Check for mold in damp areas'
        ],
        'windy': [
            'Protect your eyes from dust and debris',
            'Stay indoors if you have respiratory issues',
            'Secure loose objects outdoors',
            'Wear appropriate clothing',
            'Be cautious of falling branches'
        ]
    }
    
    return weather_tips.get(weather_condition.lower(), [
        'Maintain regular health routines',
        'Stay hydrated',
        'Get adequate sleep',
        'Exercise regularly',
        'Eat a balanced diet'
    ])

def calculate_bmi(weight_kg: float, height_m: float) -> Tuple[float, str]:
    """
    Calculate BMI and return category
    """
    if weight_kg <= 0 or height_m <= 0:
        return 0, "Invalid input"
    
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return round(bmi, 1), category

def get_bmi_health_tips(bmi_category: str) -> List[str]:
    """
    Get health tips based on BMI category
    """
    bmi_tips = {
        'Underweight': [
            'Increase caloric intake with healthy foods',
            'Include protein-rich foods in your diet',
            'Add strength training to your exercise routine',
            'Eat frequent, smaller meals throughout the day',
            'Consult a nutritionist for personalized advice'
        ],
        'Normal weight': [
            'Maintain your current healthy habits',
            'Continue regular exercise routine',
            'Eat a balanced diet with variety',
            'Get adequate sleep and rest',
            'Stay hydrated throughout the day'
        ],
        'Overweight': [
            'Gradually increase physical activity',
            'Reduce portion sizes and calorie intake',
            'Choose whole foods over processed foods',
            'Limit sugary drinks and snacks',
            'Consider working with a health coach'
        ],
        'Obese': [
            'Consult a healthcare provider for a weight loss plan',
            'Start with low-impact exercises',
            'Focus on portion control and meal planning',
            'Keep a food diary to track eating habits',
            'Set realistic weight loss goals'
        ]
    }
    
    return bmi_tips.get(bmi_category, [
        'Maintain a balanced diet',
        'Exercise regularly',
        'Get adequate sleep',
        'Stay hydrated',
        'Consult healthcare professionals for personalized advice'
    ])

def format_contact_info(name: str, phone: str = None, email: str = None) -> str:
    """
    Format contact information for display
    """
    contact_parts = [name]
    
    if phone:
        contact_parts.append(f"Phone: {phone}")
    
    if email:
        contact_parts.append(f"Email: {email}")
    
    return " | ".join(contact_parts)

def validate_contact_info(name: str, phone: str = None, email: str = None) -> Tuple[bool, str]:
    """
    Validate contact information
    """
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if not phone and not email:
        return False, "At least one contact method (phone or email) is required"
    
    if phone and not re.match(r'^\+?[\d\s\-\(\)]+$', phone):
        return False, "Invalid phone number format"
    
    if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return False, "Invalid email format"
    
    return True, "Valid contact information" 