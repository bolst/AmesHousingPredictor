# Ames Housing Predictor

## Using notebooks

This project uses [uv](https://github.com/astral-sh/uv) for package management. You can install it by running

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv self update
```

Once [uv](https://github.com/astral-sh/uv) is installed you just need to create a virtual environment, activate it, and sync

```bash
uv venv
source .venv/bin/activate
uv sync
```