#!/bin/bash

set -e

this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $this_dir/../

# Run lint
pylint --rcfile $this_dir/pylint.rc gitmetheurl

# Run static type checking
cd $this_dir
mypy $this_dir/../gitmetheurl
