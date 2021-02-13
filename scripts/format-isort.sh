# should be run from root of project.
# e.g.
# ./scripts/format-isort.sh

source $(poetry env info --path)/bin/activate

isort app

deactivate
