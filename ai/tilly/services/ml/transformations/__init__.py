"""
ML Transformations Module Initializer

This initializer script in the `tilly/services/ml/transformations` folder
imports and combines the `Preprocessor` and `Postprocessor` classes into a single
`Transformer` class, inheriting the methods and attributes of both.
"""

from tilly.services.ml.transformations.postprocessing import Postprocessor
from tilly.services.ml.transformations.preprocessing import Preprocessor


class Transformer(Preprocessor, Postprocessor):
    """
    Transformer Class

    This class inherits from both `Preprocessor` and `Postprocessor` classes,
    effectively combining their functionalities. Instances of this class can
    be used for both preprocessing and postprocessing steps in a machine learning
    pipeline.

    Inherits:
        - `Preprocessor`: Class containing methods and attributes for data
            preprocessing.
        - `Postprocessor`: Class containing methods and attributes for data
            postprocessing.
    """

    pass
