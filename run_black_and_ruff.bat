pip install --upgrade black~=25.1 ruff~=0.8.0 && ^
black --config pyproject.toml . asammdf.spec && ^
ruff check --fix
