from importlib import import_module
import sys

# Make app.models importable as top-level "models" to satisfy pickled pipelines.
app_models = import_module("app.models")
sys.modules.setdefault("models", app_models)
sys.modules.setdefault("models.custom_transformers", import_module("app.models.custom_transformers"))
