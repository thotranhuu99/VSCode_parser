# VSCode parser
This simple repo is to extract program name, arguments, environment variables from python command inside bash script into .json file for usage with VS code.
# Bash script usage
```
python create_configs_bash.py --input_file unify.sh --output_file configs.json
```
# Single command usage
Replace $python_command with your python script:
```
python create_configs.py --command "$python_command" --output_file configs.json
```
# Note
Loop is not tested, if-else is not support.
# Todo
Support for python module.