from importlib import import_module
import os
from pathlib import Path
import sys


def _ensure_models_on_path() -> None:
    """Ensure the directory containing the pickled models package is importable."""

    candidates: list[Path] = []

    env_dir = os.getenv("MODEL_DIR")
    if env_dir:
        candidates.append(Path(env_dir))

    # Fallback to the repo's models directory when running outside Docker.
    candidates.append(Path(__file__).resolve().parent.parent / "models")

    for directory in candidates:
        if not directory.exists():
            continue

        directory_str = str(directory)
        if directory_str not in sys.path:
            sys.path.append(directory_str)
        break


def _ensure_pickled_modules_available() -> None:
    """
    Pipelines were serialized referencing `models.*`. Import and register those modules
    so joblib.load can resolve the original paths when the API runs inside the app pkg.
    """

    _ensure_models_on_path()

    models_pkg = import_module("models")
    sys.modules.setdefault("models", models_pkg)
    sys.modules.setdefault("models.custom_transformers", import_module("models.custom_transformers"))


def _patch_sklearn_backward_compat() -> None:
    """
    Provide the legacy `_RemainderColsList` symbol if sklearn no longer exposes it.
    This avoids AttributeError when loading older ColumnTransformer pickles.
    """

    try:
        from sklearn.compose import _column_transformer  # type: ignore
    except Exception:  # pragma: no cover - optional dependency
        return

    if hasattr(_column_transformer, "_RemainderColsList"):
        return

    class _RemainderColsList(list):
        """Lightweight placeholder for backward compatibility."""

    _column_transformer._RemainderColsList = _RemainderColsList  # type: ignore[attr-defined]


_ensure_pickled_modules_available()
_patch_sklearn_backward_compat()
