from pandas import DataFrame
from loguru import logger

from tilly.services.ml import update_registry, ModelRegistry


def train_models(training_data: dict[str, DataFrame]) -> list[dict[str, DataFrame]]:
    """Trains a new model with the given training data and updates the dashboard."""

    # Create a new model registry
    model_registry = ModelRegistry()

    results: dict[str, tuple[list[float], list[int]]] = model_registry.train(
        training_data
    )

    # Update the global model
    update_registry(model_registry)

    logger.info("Training flow completed")
    return results
