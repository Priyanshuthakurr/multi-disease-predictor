"""
Train disease prediction model using symptoms data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def load_and_prepare_data():
    """
    Load symptoms data and prepare for training
    """
    # Load the symptoms dataset
    data = pd.read_csv('data/symptoms.csv')
    
    # Separate features (symptoms) and targets (diseases)
    symptoms = data['symptom'].values
    diseases = data.columns[1:].values  # All columns except 'symptom'
    
    # Create feature matrix (symptoms as features)
    X = data.iloc[:, 1:].T  # Transpose to get diseases as rows, symptoms as columns
    y = diseases  # Disease names as labels
    
    return X, y, symptoms

def train_model(X, y):
    """
    Train Random Forest model for disease prediction
    """
    # Split data for training (in this case, we have limited data, so we'll use all for training)
    # In a real scenario, you'd have more data and proper train/test split
    
    # Create and train the model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )
    
    # Train the model
    model.fit(X, y)
    
    return model

def evaluate_model(model, X, y):
    """
    Evaluate the trained model
    """
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y, y_pred))
    
    return accuracy

def save_model(model, symptoms, filepath='model/disease_model.pkl'):
    """
    Save the trained model and symptoms list
    """
    # Create model directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save model and symptoms
    model_data = {
        'model': model,
        'symptoms': symptoms
    }
    
    with open(filepath, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved to {filepath}")

def create_symptom_mapping():
    """
    Create a mapping of symptoms to their indices for easy lookup
    """
    data = pd.read_csv('data/symptoms.csv')
    symptoms = data['symptom'].values
    
    symptom_mapping = {symptom: i for i, symptom in enumerate(symptoms)}
    
    return symptom_mapping

def main():
    """
    Main function to train and save the model
    """
    print("Loading and preparing data...")
    X, y, symptoms = load_and_prepare_data()
    
    print(f"Training data shape: {X.shape}")
    print(f"Number of diseases: {len(y)}")
    print(f"Number of symptoms: {len(symptoms)}")
    
    print("\nTraining Random Forest model...")
    model = train_model(X, y)
    
    print("\nEvaluating model...")
    accuracy = evaluate_model(model, X, y)
    
    print("\nSaving model...")
    save_model(model, symptoms)
    
    # Create symptom mapping
    symptom_mapping = create_symptom_mapping()
    
    # Save symptom mapping
    with open('model/symptom_mapping.pkl', 'wb') as f:
        pickle.dump(symptom_mapping, f)
    
    print("Model training completed successfully!")
    print(f"Model accuracy: {accuracy:.2f}")
    print("Files created:")
    print("- model/disease_model.pkl")
    print("- model/symptom_mapping.pkl")

if __name__ == "__main__":
    main() 