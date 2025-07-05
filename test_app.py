#!/usr/bin/env python3
"""
Test script for Smart Health Companion
"""

import sys
import os
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'folium',
        'requests',
        'plotly'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All packages imported successfully")
        return True

def test_data_files():
    """Test if data files exist"""
    print("\n📊 Testing data files...")
    
    required_files = [
        'data/symptoms.csv',
        'utils/helpers.py',
        'model/train_model.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All data files found")
        return True

def test_model_training():
    """Test model training functionality"""
    print("\n🤖 Testing model training...")
    
    try:
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        
        # Load data
        data = pd.read_csv('data/symptoms.csv')
        print(f"✅ Loaded symptoms data: {data.shape}")
        
        # Test model creation
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        print("✅ Created Random Forest model")
        
        # Test with sample data
        X = data.iloc[:, 1:].T
        y = data.columns[1:].values
        
        if len(X) > 0 and len(y) > 0:
            model.fit(X, y)
            print("✅ Model training successful")
            return True
        else:
            print("❌ No data for training")
            return False
            
    except Exception as e:
        print(f"❌ Model training failed: {e}")
        return False

def test_utility_functions():
    """Test utility functions"""
    print("\n🔧 Testing utility functions...")
    
    try:
        sys.path.append('utils')
        from helpers import clean_symptoms_text, extract_symptoms_from_text
        
        # Test text cleaning
        test_text = "I have FEVER and Headache!!!"
        cleaned = clean_symptoms_text(test_text)
        if cleaned == "i have fever and headache":
            print("✅ Text cleaning works")
        else:
            print("❌ Text cleaning failed")
            return False
        
        # Test symptom extraction
        symptoms = extract_symptoms_from_text(test_text)
        if 'fever' in symptoms and 'headache' in symptoms:
            print("✅ Symptom extraction works")
        else:
            print("❌ Symptom extraction failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Utility functions failed: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("\n🌐 Testing Streamlit app...")
    
    try:
        # Test if app.py exists and can be imported
        if os.path.exists('app.py'):
            print("✅ app.py found")
            
            # Try to import main function
            import importlib.util
            spec = importlib.util.spec_from_file_location("app", "app.py")
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            
            if hasattr(app_module, 'main'):
                print("✅ main() function found")
                return True
            else:
                print("❌ main() function not found")
                return False
        else:
            print("❌ app.py not found")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 Smart Health Companion - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Data Files", test_data_files),
        ("Model Training", test_model_training),
        ("Utility Functions", test_utility_functions),
        ("Streamlit App", test_streamlit_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your Smart Health Companion is ready to use.")
        print("\nTo run the app:")
        print("streamlit run app.py")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 