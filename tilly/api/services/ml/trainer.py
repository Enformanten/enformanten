from pandas import DataFrame

from api.services.ml.model import update_model, ModelRegistry


async def train_models(
    training_data: dict[str, DataFrame]
) -> list[dict[str, DataFrame]]:
    """Trains a new model with the given training data and updates the dashboard."""
    # Simulate model training
    model = ModelRegistry()
    results: dict[str, tuple[list[float], list[int]]] = model.train(training_data)

    # Update the global model
    update_model(model)

    return results
