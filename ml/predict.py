import os
import pickle
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

_model = None

def get_model():
    """Lazy load or train model if not present."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        from ml.train import build_and_train
        _model = build_and_train()
    else:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict_market(price: float, volume: float = 1000.0, trades: int = 20):
    """
    Predict binary resolution outcome and model confidence for a prediction contract.

    Args:
        price: Implied Yes probability (between 0.00 and 1.00)
        volume: Total trading volume in USD
        trades: Estimated or discrete number of trades

    Returns:
        pred (int): 1 if model expects "Yes", 0 if "No"
        prob (float): Model-estimated probability of resolving to Yes (0.0 to 1.0)
        edge (float): Discrepancy between model confidence and current price (prob - price)
    """
    model = get_model()

    price_clean  = max(0.01, min(0.99, float(price)))
    volume_clean = max(1.0, float(volume))
    trades_clean = max(1, int(trades))

    import pandas as pd
    X = pd.DataFrame([{
        "price": price_clean,
        "volume": volume_clean,
        "num_trades": trades_clean
    }])
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])
    edge = round(prob - price_clean, 4)

    return pred, round(prob, 4), edge


if __name__ == "__main__":
    # Quick sanity check
    sample_price = 0.42
    pred, prob, edge = predict_market(sample_price, volume=50000, trades=150)
    print(f"Sample Prediction for Yes Price ${sample_price:.2f}:")
    print(f"  Predicted Outcome: {'Yes (1)' if pred == 1 else 'No (0)'}")
    print(f"  Model Probability: {prob * 100:.1f}%")
    print(f"  Estimated Edge:    {edge * 100:+.1f}%")