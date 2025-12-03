@echo off
REM Set PYTHONPATH to include the src directory
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"

REM Run pytest, letting it discover tests automatically
pytest
