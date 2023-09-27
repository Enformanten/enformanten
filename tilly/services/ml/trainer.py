from pandas import DataFrame
from loguru import logger

from tilly.services.ml.model import update_model, ModelRegistry


def train_models(training_data: dict[str, DataFrame]) -> list[dict[str, DataFrame]]:
    """Trains a new model with the given training data and updates the dashboard."""
    # Simulate model training
    model = ModelRegistry()
    results: dict[str, tuple[list[float], list[int]]] = model.train(training_data)

    # Update the global model
    update_model(model)

    logger.info("Training flow completed")
    return results
