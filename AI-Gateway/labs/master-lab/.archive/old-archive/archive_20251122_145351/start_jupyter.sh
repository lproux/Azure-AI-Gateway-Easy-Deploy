#!/bin/bash
source .venv-py311/Scripts/activate 2>/dev/null || . .venv-py311/bin/activate
jupyter notebook --no-browser --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.disable_check_xsrf=True
