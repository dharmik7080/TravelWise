import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

class BudgetPredictor:
    _model = None
    _encoder = None
    _scaler = None
    _loaded = False

    @classmethod
    def _get_models_dir(cls):
        """
        Dynamically resolves the path to the ml/models directory.
        """
        services_ml_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.dirname(services_ml_dir))
        return os.path.join(project_dir, 'ml', 'models')

    @classmethod
    def _load_model(cls):
        """
        Bypassed model loader.
        """
        cls._loaded = True

    @classmethod
    def predict_cost(cls, destination, travelers, days, package_type, season):
        """
        Predicts total trip cost based on inputs deterministically.
        """
        try:
            breakdown = cls.calculate_breakdown(destination, travelers, days, package_type, season)
            if not breakdown:
                return 1000.0
            return round(sum(breakdown.values()), 2)
        except Exception:
            return 1000.0

    @classmethod
    def calculate_breakdown(cls, destination, travelers, days, package_type, season):
        """
        Returns a dict of estimated stay, transport, meals, and activities costs.
        """
        try:
            # 1. Stay (Accommodation) Cost
            stay_rate = 1200.0 if package_type == 'Budget' else (2500.0 if package_type == 'Standard' else 6000.0)
            rooms = (int(travelers) + 1) // 2
            stay_cost = rooms * int(days) * stay_rate

            # 2. Transport Cost
            transport_rate = 500.0 if package_type == 'Budget' else (1500.0 if package_type == 'Standard' else 4000.0)
            transport_cost = int(travelers) * transport_rate

            # 3. Meals Cost
            meal_rate = 250.0 if package_type == 'Budget' else (600.0 if package_type == 'Standard' else 1800.0)
            meals_cost = int(travelers) * int(days) * meal_rate

            # 4. Activities Cost
            from destinations.models import Destination
            try:
                dest_obj = Destination.objects.get(destination_name=destination)
                att_fees = sum(float(attr.entry_fee) for attr in dest_obj.attractions.all())
            except Exception:
                att_fees = 100.0
            activities_cost = int(travelers) * att_fees

            return {
                'stay': round(stay_cost, 2),
                'transport': round(transport_cost, 2),
                'meals': round(meals_cost, 2),
                'activities': round(activities_cost, 2)
            }
        except Exception:
            return {}

    @classmethod
    def train_and_save_best_model(cls):
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        services_ml_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.dirname(services_ml_dir))
        
        dataset_path = os.path.join(project_dir, 'ml', 'datasets', 'trip_cost_dataset.csv')
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found at {dataset_path}")

        df = pd.read_csv(dataset_path)

        X = df[['Destination', 'Number of Travelers', 'Number of Days', 'Package Type', 'Season']]
        y = df['Estimated Cost']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        categorical_cols = ['Destination', 'Package Type', 'Season']
        numerical_cols = ['Number of Travelers', 'Number of Days']

        # Preprocessing: Encoder and Scaler
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        X_train_cat = encoder.fit_transform(X_train[categorical_cols])
        X_test_cat = encoder.transform(X_test[categorical_cols])

        scaler = StandardScaler()
        X_train_num = scaler.fit_transform(X_train[numerical_cols])
        X_test_num = scaler.transform(X_test[numerical_cols])

        # Combine numerical and categorical features
        X_train_preprocessed = np.hstack([X_train_num, X_train_cat])
        X_test_preprocessed = np.hstack([X_test_num, X_test_cat])

        # Log transform target variable
        y_train_log = np.log1p(y_train)

        # Models to evaluate
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest Regressor': RandomForestRegressor(random_state=42),
            'Decision Tree Regressor': DecisionTreeRegressor(random_state=42)
        }

        best_model_name = None
        best_model = None
        best_r2 = -float('inf')
        best_metrics = {}

        print("=== Training & Evaluating Models ===")
        for name, model in models.items():
            model.fit(X_train_preprocessed, y_train_log)
            
            y_pred_log = model.predict(X_test_preprocessed)
            y_pred = np.expm1(y_pred_log)

            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)

            print(f"{name} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}")

            if r2 > best_r2:
                best_r2 = r2
                best_model_name = name
                best_model = model
                best_metrics = {
                    'model_name': name,
                    'r2': round(r2, 4),
                    'mae': round(mae, 2),
                    'rmse': round(rmse, 2),
                    'last_trained': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        # Save best model artifacts
        models_dir = cls._get_models_dir()
        os.makedirs(models_dir, exist_ok=True)

        print(f"\nChampion Model: {best_model_name} (R²: {best_r2:.4f})")

        # Save encoder, scaler, and the champion model
        with open(os.path.join(models_dir, 'trained_model.pkl'), 'wb') as f:
            pickle.dump(best_model, f)
            
        with open(os.path.join(models_dir, 'trip_cost_model.pkl'), 'wb') as f:
            pickle.dump(best_model, f)

        with open(os.path.join(models_dir, 'encoder.pkl'), 'wb') as f:
            pickle.dump(encoder, f)

        with open(os.path.join(models_dir, 'scaler.pkl'), 'wb') as f:
            pickle.dump(scaler, f)

        # Save metrics JSON
        with open(os.path.join(models_dir, 'model_metrics.json'), 'w') as f:
            json.dump(best_metrics, f)

        # Save feature columns lists for legacy compatibility
        encoded_cat_cols = encoder.get_feature_names_out(categorical_cols).tolist()
        all_feature_cols = numerical_cols + encoded_cat_cols
        with open(os.path.join(models_dir, 'feature_columns.pkl'), 'wb') as f:
            pickle.dump(all_feature_cols, f)

        # Reset class cache
        cls._loaded = False

        print("Trained model files saved successfully to:", models_dir)
