"""Machine Learning Services for Tilly

This package provides a comprehensive suite of tools for managing 
room-specific machine learning models in Tilly. It includes 
functionalities for preprocessing, training, and postprocessing,
as well as maintaining a global model registry.

Main Components:
    - ModelRegistry: A singleton class that serves as an in-memory registry for
        trained machine learning models. 
        Each model is room-specific and is used for batch predictions. 
        This class also takes care of model training, fitting, and predictions.

    - Model: A wrapper class around the scikit-learn Isolation Forest model. Each
        instance of this class represents a trained model for a specific room, 
        and it provides functionalities to fit new data, make predictions, and
        calculate anomaly scores.

    - Transformations: A collection of modules for pre- and post-processing steps. 
        This includes feature extraction, normalization, and any 
        other transformations required 
        before and after model training or predictions.

    - Trainer: A script responsible for orchestrating the model training flow. 
        It takes in new data, triggers model training, and updates the
        global model registry.
               
The package is designed to be robust, scalable, and thread-safe.

Examples:
    >>> from tilly.services.ml import ModelRegistry
    >>> registry = ModelRegistry()
    >>> training_data = {...}
    >>> registry.train(training_data)

    >>> from tilly.services.ml import train_models
    >>> train_models(training_data)

"""
