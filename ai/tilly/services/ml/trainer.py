from pandas import DataFrame
from loguru import logger
from tilly.services.ml import update_registry, ModelRegistry


def train_models(training_data: dict[str, DataFrame]) -> list[dict[str, DataFrame]]:
    """Trains new models based on the given training data and updates the global
    model registry.

    This function performs the following steps:
    1. Create a new instance of ModelRegistry.
    2. Train the models using the training data.
    3. Update the global model registry with the newly trained models.

    Args:
        training_data (dict[str, DataFrame]): A dictionary containing the training data
            for each room, keyed by room name.

    Returns:
        list[dict[str, DataFrame]]: A list of dictionaries, each containing the
        predicted DataFrame and anomaly scores for each room.

    """
    # Create a new model registry
    model_registry = ModelRegistry()

    # Train models and receive the results
    results: dict[str, tuple[list[float], list[int]]] = model_registry.train(
        training_data
    )

    # Update the global model registry
    update_registry(model_registry)

    logger.info("Training flow completed")
    return results
