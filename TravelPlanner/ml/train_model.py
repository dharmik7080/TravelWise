import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # run without UI window
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

def train():
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(ml_dir, 'datasets', 'trip_cost_dataset.csv')
    df = pd.read_csv(dataset_path)

    # Separate features and target
    X = df[['Destination', 'Number of Travelers', 'Number of Days', 'Package Type', 'Season']]
    y = df['Estimated Cost']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # OneHotEncoder for categorical columns
    categorical_cols = ['Destination', 'Package Type', 'Season']
    numerical_cols = ['Number of Travelers', 'Number of Days']

    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_train_cat = encoder.fit_transform(X_train[categorical_cols])
    X_test_cat = encoder.transform(X_test[categorical_cols])

    # Column names for one-hot encoded categories
    encoded_cat_cols = encoder.get_feature_names_out(categorical_cols).tolist()

    # Concatenate numerical and encoded categorical features
    X_train_preprocessed = np.hstack([X_train[numerical_cols].values, X_train_cat])
    X_test_preprocessed = np.hstack([X_test[numerical_cols].values, X_test_cat])

    all_feature_cols = numerical_cols + encoded_cat_cols

    # Log transform target to model the multiplicative relationship linearly
    y_train_log = np.log1p(y_train)

    # Train model
    model = LinearRegression()
    model.fit(X_train_preprocessed, y_train_log)

    # Predict & Convert back using expm1
    y_pred_log = model.predict(X_test_preprocessed)
    y_pred = np.expm1(y_pred_log)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("=== Model Evaluation (with Log Transform) ===")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    # Save models and metadata
    models_dir = os.path.join(ml_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    with open(os.path.join(models_dir, 'trip_cost_model.pkl'), 'wb') as f:
        pickle.dump(model, f)

    with open(os.path.join(models_dir, 'encoder.pkl'), 'wb') as f:
        pickle.dump(encoder, f)

    with open(os.path.join(models_dir, 'feature_columns.pkl'), 'wb') as f:
        pickle.dump(all_feature_cols, f)

    # Plots
    # 1. Actual vs Predicted Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, color='blue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Cost (₹)')
    plt.ylabel('Predicted Cost (₹)')
    plt.title('Actual vs Predicted Trip Cost')
    plt.grid(True)
    plt.savefig(os.path.join(models_dir, 'actual_vs_predicted.png'), dpi=300)
    plt.close()

    # 2. Residual Plot
    plt.figure(figsize=(8, 6))
    residuals = y_test - y_pred
    plt.scatter(y_pred, residuals, alpha=0.5, color='purple')
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Predicted Cost (₹)')
    plt.ylabel('Residuals (₹)')
    plt.title('Residual Plot')
    plt.grid(True)
    plt.savefig(os.path.join(models_dir, 'residual_plot.png'), dpi=300)
    plt.close()

    print(f"Model saved and evaluation graphs generated in: {models_dir}")

if __name__ == '__main__':
    train()
