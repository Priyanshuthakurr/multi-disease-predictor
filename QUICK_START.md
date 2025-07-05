# 🚀 Quick Start Guide - Smart Health Companion

## ⚡ Get Started in 5 Minutes

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Train the Model**
```bash
python model/train_model.py
```

### 3. **Run the App**
```bash
streamlit run app.py
```

### 4. **Open Your Browser**
Navigate to: `http://localhost:8501`

---

## 🎯 What You Can Do Right Now

### ✅ **Health Assessment**
- Enter symptoms like "fever, headache, fatigue"
- Get AI-powered disease predictions
- View first aid instructions
- See emergency warning signs

### ✅ **Find Hospitals**
- Enter your location
- View nearby hospitals on interactive map
- Get contact information and ratings

### ✅ **Diet & Nutrition**
- Get condition-specific diet advice
- View general nutrition guidelines
- Calculate BMI and get health tips

### ✅ **Emergency Help**
- Set up emergency contacts
- Send emergency alerts (demo mode)
- Access emergency numbers worldwide

### ✅ **Health Tips**
- Daily wellness advice
- Seasonal health recommendations
- Lifestyle improvement tips

---

## 🔧 Optional Setup (For Full Features)

### **Google Maps API** (For Hospital Locations)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable Maps JavaScript API
3. Get API key and add to `.env` file:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### **Twilio API** (For SMS Alerts)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID, Auth Token, and phone number
3. Add to `.env` file:
```
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=your_twilio_number
```

---

## 🧪 Test Everything Works

Run the test suite:
```bash
python test_app.py
```

You should see: `🎉 All tests passed!`

---

## 📱 Example Usage

### **Case 1: Fever & Body Pain**
**Input**: "I have high fever and severe body pain"
**Output**: 
- Predicted: Dengue
- First Aid: Rest, hydration, acetaminophen
- Emergency Signs: Severe abdominal pain, bleeding
- Diet: Fluids, vitamin C, avoid fried foods

### **Case 2: Headache & Nausea**
**Input**: "I have intense headache with nausea"
**Output**:
- Predicted: Migraine
- First Aid: Rest in dark room, cold compress
- Emergency Signs: Worst headache, vision problems
- Diet: Avoid triggers, stay hydrated

---

## 🆘 Troubleshooting

### **Import Errors**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Model Training Issues**
```bash
python model/train_model.py
```

### **Streamlit Not Starting**
```bash
streamlit run app.py --server.port 8501
```

### **Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Next Steps

1. **Customize**: Add your own symptoms and diseases to `data/symptoms.csv`
2. **Enhance**: Integrate real APIs for Google Maps and Twilio
3. **Deploy**: Deploy to Streamlit Cloud or your own server
4. **Extend**: Add more features like medication tracking, appointment scheduling

---

## ⚠️ Important Notes

- **Not Medical Advice**: This app is for informational purposes only
- **Emergency Situations**: Always call emergency services for serious conditions
- **Professional Consultation**: Consult healthcare professionals for medical decisions
- **Demo Mode**: Some features work in demonstration mode without API keys

---

**🎉 You're all set! Your Smart Health Companion is ready to help!** 