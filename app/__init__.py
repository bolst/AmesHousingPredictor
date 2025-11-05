from types import ModuleType
import sys

from .custom_transformers import FeatureEngineer, LogTransformer


def _register_custom_modules() -> None:
    """Expose custom transformers under the `models` namespace for joblib unpickling."""
    models_pkg = sys.modules.get("models")
    if models_pkg is None:
        models_pkg = ModuleType("models")
        sys.modules["models"] = models_pkg

    custom_transformers = ModuleType("models.custom_transformers")
    custom_transformers.FeatureEngineer = FeatureEngineer  # type: ignore[attr-defined]
    custom_transformers.LogTransformer = LogTransformer  # type: ignore[attr-defined]

    models_pkg.custom_transformers = custom_transformers  # type: ignore[attr-defined]
    sys.modules["models.custom_transformers"] = custom_transformers


_register_custom_modules()

__all__ = ["FeatureEngineer", "LogTransformer"]
