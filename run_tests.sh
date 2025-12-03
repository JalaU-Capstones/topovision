#!/bin/bash
# Set PYTHONPATH to include the src directory
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# Run pytest, letting it discover tests automatically
pytest
