import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import joblib

class CareerPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.model_path = 'model.joblib'
        self.le_path = 'label_encoder.joblib'
        self._initialize_model()

    def _initialize_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.le_path):
            self.model = joblib.load(self.model_path)
            self.label_encoder = joblib.load(self.le_path)
            print("Loaded structured career prediction model.")
        else:
            print("Training initial model on synthetic dataset...")
            self._train_dummy_model()

    def _train_dummy_model(self):
        # Generate some synthetic data emphasizing logic:
        # High Academics + Co-curricular (projects/coding) -> Software Engineer / Data Scientist
        # High Extra-curricular (leadership/sports) + decents Academics -> Product Manager / HR
        # High All -> Entrepreneur / CEO track
        
        np.random.seed(42)
        n_samples = 500
        
        cgpa = np.random.uniform(5.0, 10.0, n_samples)
        co_curricular = np.random.uniform(1.0, 10.0, n_samples)
        extra_curricular = np.random.uniform(1.0, 10.0, n_samples)
        
        careers = []
        for i in range(n_samples):
            c_g = cgpa[i]
            c_c = co_curricular[i]
            e_c = extra_curricular[i]
            
            if c_g > 8.5 and c_c > 8.0:
                careers.append("Data Scientist")
            elif c_g > 7.5 and c_c > 7.0:
                careers.append("Software Engineer")
            elif e_c > 8.0 and c_g > 7.0:
                careers.append("Product Manager")
            elif c_g < 7.0 and e_c > 7.0:
                careers.append("Sales & Marketing")
            elif c_g > 9.0 and c_c < 5.0 and e_c < 5.0:
                careers.append("Research Scholar")
            else:
                careers.append("Business Analyst")
                
        df = pd.DataFrame({
            'cgpa': cgpa,
            'co_curricular': co_curricular,
            'extra_curricular': extra_curricular,
            'career': careers
        })

        X = df[['cgpa', 'co_curricular', 'extra_curricular']]
        y = self.label_encoder.fit_transform(df['career'])
        
        self.model.fit(X, y)
        
        # Save models for faster startup next time
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.label_encoder, self.le_path)

    def predict_career(self, cgpa, co_curricular, extra_curricular):
        features = np.array([[cgpa, co_curricular, extra_curricular]])
        pred_encoded = self.model.predict(features)
        pred_probs = self.model.predict_proba(features)[0]
        
        career = self.label_encoder.inverse_transform(pred_encoded)[0]
        
        # Get top 3 careers instead for a richer UI
        top_3_idx = np.argsort(pred_probs)[-3:][::-1]
        top_3_careers = self.label_encoder.inverse_transform(top_3_idx)
        top_3_probs = pred_probs[top_3_idx]
        
        return [
            {"career": top_3_careers[0], "confidence": round(top_3_probs[0] * 100, 1)},
            {"career": top_3_careers[1], "confidence": round(top_3_probs[1] * 100, 1)},
            {"career": top_3_careers[2], "confidence": round(top_3_probs[2] * 100, 1)}
        ]

# A global instance to use throughout the app
predictor = CareerPredictor()
