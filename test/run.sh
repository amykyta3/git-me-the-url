#!/bin/bash

set -e

cd "$(dirname "$0")"

python3.13 -m venv .venv
source .venv/bin/activate

# Install test dependencies
pip install -r requirements.txt

# Install dut
pip install -e ".."

# Run lint
pylint --rcfile pylint.rc ../src/gitmetheurl

# Run static type checking
mypy ../src/gitmetheurl
