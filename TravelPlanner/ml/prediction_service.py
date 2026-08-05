import os
import pickle
import numpy as np
import pandas as pd
from services.ml.budget_predictor import BudgetPredictor

class PredictionService:
    _model = None
    _encoder = None
    _feature_columns = None
    _loaded = False

    @classmethod
    def _load_model(cls):
        """
        Loads the budget predictor dependencies for legacy compatibility.
        """
        BudgetPredictor._load_model()
        cls._model = BudgetPredictor._model
        cls._encoder = BudgetPredictor._encoder
        cls._loaded = True

    @classmethod
    def predict_cost(cls, destination, travelers, days, package_type, season):
        """
        Predicts total trip cost based on inputs by delegating to BudgetPredictor.
        """
        return BudgetPredictor.predict_cost(
            destination=destination,
            travelers=travelers,
            days=days,
            package_type=package_type,
            season=season
        )
