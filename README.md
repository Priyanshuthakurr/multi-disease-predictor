# 🏥 Smart Health Companion

An AI-powered health assistant that helps users with health-related queries, disease prediction, and emergency assistance.

## 🌟 Features

### 🔍 Health Assessment
- **Symptom Analysis**: Input your symptoms and get AI-powered disease predictions
- **Disease Information**: Detailed information about predicted conditions
- **First Aid Guidance**: Step-by-step first aid instructions
- **Emergency Signs**: Know when to seek immediate medical attention

### 🏥 Nearby Hospitals
- **Location-based Search**: Find hospitals near your location
- **Interactive Map**: Visual map with hospital locations
- **Hospital Details**: Contact information, ratings, and distances

### 🍎 Diet & Nutrition
- **Condition-specific Diet**: Personalized diet recommendations based on health conditions
- **General Nutrition**: Healthy eating guidelines and meal suggestions
- **BMI Calculator**: Calculate BMI and get personalized health tips

### 🚨 Emergency Help
- **Emergency Alerts**: Send alerts to emergency contacts
- **Contact Management**: Store and manage emergency contacts
- **Emergency Numbers**: Quick access to emergency numbers worldwide

### 💡 Health Tips
- **Daily Health Tips**: Practical health advice for everyday wellness
- **Seasonal Health**: Weather and season-specific health recommendations
- **Lifestyle Guidance**: Tips for maintaining a healthy lifestyle

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Machine Learning**: Scikit-learn (Random Forest for disease prediction)
- **Data Processing**: Pandas, NumPy
- **Natural Language Processing**: spaCy, NLTK
- **Maps Integration**: Folium, Google Maps API
- **Emergency Services**: Twilio API (SMS), smtplib (Email)
- **Data Storage**: CSV files, Pickle for models

## 📁 Project Structure

```
smart-health-companion/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── data/
│   └── symptoms.csv       # Symptoms and disease dataset
│
├── model/
│   ├── train_model.py     # Model training script
│   ├── disease_model.pkl  # Trained ML model (generated)
│   └── symptom_mapping.pkl # Symptom mapping (generated)
│
├── utils/
│   └── helpers.py         # Utility functions
│
└── .env                   # Environment variables (create this)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-health-companion
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model**
   ```bash
   python model/train_model.py
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 Dataset

The application uses a comprehensive symptoms dataset with:
- **50+ symptoms** including fever, headache, fatigue, cough, etc.
- **10 common diseases** like Dengue, Common Cold, Migraine, etc.
- **Binary mapping** of symptoms to diseases for ML training

### Sample Data Structure
```csv
symptom,dengue,common_cold,migraine,tension_headache
fever,1,1,0,0
headache,1,0,1,1
fatigue,1,1,0,0
cough,0,1,0,0
```

## 🤖 Machine Learning Model

### Model Details
- **Algorithm**: Random Forest Classifier
- **Features**: 50+ symptoms (binary features)
- **Target**: Disease classification (10 diseases)
- **Accuracy**: ~95% (on training data)

### Training Process
1. Load symptoms dataset
2. Prepare feature matrix (symptoms) and target vector (diseases)
3. Train Random Forest model
4. Evaluate model performance
5. Save trained model and symptom mapping

## 🔧 Configuration

### API Keys Setup

#### Google Maps API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Maps JavaScript API and Places API
4. Create credentials (API key)
5. Add to `.env` file

#### Twilio API (for SMS alerts)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Get a Twilio phone number
4. Add credentials to `.env` file

### Environment Variables
```bash
# Required for full functionality
GOOGLE_MAPS_API_KEY=your_api_key_here
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number

# Optional
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## 📱 Usage Guide

### Health Assessment
1. Navigate to "Health Assessment" in the sidebar
2. Enter your symptoms in the text area
3. Click "Analyze Symptoms"
4. Review the predicted condition and recommendations

### Finding Hospitals
1. Go to "Nearby Hospitals"
2. Enter your location (city, address, or coordinates)
3. Click "Find Hospitals"
4. View hospitals on the interactive map

### Emergency Help
1. Access "Emergency Help" section
2. Set up emergency contacts
3. Use the emergency alert button when needed
4. Review emergency numbers for your country

## 🎯 Example Use Cases

### Case 1: Fever and Body Pain
**User Input**: "I have high fever and severe body pain"
**App Response**:
- Predicted Disease: Dengue
- First Aid: Rest, hydration, acetaminophen
- Emergency Signs: Severe abdominal pain, bleeding
- Diet: Fluids, vitamin C, avoid fried foods

### Case 2: Headache and Nausea
**User Input**: "I have intense headache with nausea"
**App Response**:
- Predicted Disease: Migraine
- First Aid: Rest in dark room, cold compress
- Emergency Signs: Worst headache, vision problems
- Diet: Avoid triggers, stay hydrated

## 🔒 Privacy & Security

- **Local Processing**: All symptom analysis is done locally
- **No Data Storage**: User data is not stored permanently
- **Secure APIs**: API keys are stored in environment variables
- **Emergency Alerts**: Only sent when explicitly requested

## ⚠️ Important Disclaimers

1. **Not Medical Advice**: This app is for informational purposes only
2. **Emergency Situations**: Always call emergency services for serious conditions
3. **Professional Consultation**: Consult healthcare professionals for medical decisions
4. **Accuracy**: Predictions are based on limited training data

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy automatically

### Local Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 app:main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Medical professionals for health information validation
- Open-source community for libraries and tools
- Streamlit team for the amazing web framework
- Scikit-learn team for ML capabilities

## 📞 Support

For support, email support@smarthealthcompanion.com or create an issue in the repository.

---

**Built with ❤️ for better health awareness and emergency preparedness** 