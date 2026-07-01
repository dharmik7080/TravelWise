import os
import pickle
import numpy as np
import pandas as pd

class PredictionService:
    _model = None
    _encoder = None
    _feature_columns = None
    _loaded = False

    @classmethod
    def _load_model(cls):
        if cls._loaded:
            return
        
        ml_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(ml_dir, 'models')
        
        model_path = os.path.join(models_dir, 'trip_cost_model.pkl')
        encoder_path = os.path.join(models_dir, 'encoder.pkl')
        feature_cols_path = os.path.join(models_dir, 'feature_columns.pkl')
        
        if not (os.path.exists(model_path) and os.path.exists(encoder_path) and os.path.exists(feature_cols_path)):
            raise FileNotFoundError("Trained model files not found. Please run train_model.py first.")
            
        with open(model_path, 'rb') as f:
            cls._model = pickle.load(f)
            
        with open(encoder_path, 'rb') as f:
            cls._encoder = pickle.load(f)
            
        with open(feature_cols_path, 'rb') as f:
            cls._feature_columns = pickle.load(f)
            
        cls._loaded = True

    @classmethod
    def predict_cost(cls, destination, travelers, days, package_type, season):
        """
        Predicts total trip cost based on inputs.
        """
        cls._load_model()
        
        # 1. Create a single-row DataFrame for the input features
        input_df = pd.DataFrame([{
            'Destination': destination,
            'Number of Travelers': travelers,
            'Number of Days': days,
            'Package Type': package_type,
            'Season': season
        }])
        
        # 2. Transform categorical features using the saved encoder
        categorical_cols = ['Destination', 'Package Type', 'Season']
        numerical_cols = ['Number of Travelers', 'Number of Days']
        
        try:
            cat_encoded = cls._encoder.transform(input_df[categorical_cols])
            
            # Combine numerical and categorical features
            num_features_values = input_df[numerical_cols].values
            X_input = np.hstack([num_features_values, cat_encoded])
            
            # 3. Predict (the model was trained on log-transformed costs)
            pred_log = cls._model.predict(X_input)
            predicted_cost = np.expm1(pred_log)[0]
            
            return round(float(predicted_cost), 2)
        except Exception:
            return None
