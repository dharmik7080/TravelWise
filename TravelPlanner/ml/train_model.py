import os
import sys

# Ensure project root is in path
ml_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(ml_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from services.ml.budget_predictor import BudgetPredictor

def train():
    """
    Delegates training to the central BudgetPredictor service.
    """
    BudgetPredictor.train_and_save_best_model()

if __name__ == '__main__':
    train()
