# augustus



A simple plug-n-play threat intel tool to quickly enrich IOCs.

## Installation (Dev)
Installation instructions for `augustus` dev mode

Poetry
1. `poetry lock`
2. `poetry install`
3. `poetry build`
4. `poetry run augustus`

## Developing

Run `make` for help

    make install             # Run `poetry install`
    make showdeps            # run poetry to show deps
    make lint                # Runs bandit and black in check mode
    make format              # Formats you code with Black
    make test                # run pytest with coverage
    make build               # run `poetry build` to build source distribution and wheel
make pyinstaller # Create a binary executable using pyinstaller
