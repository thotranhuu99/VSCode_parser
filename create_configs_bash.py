import json
import os
import subprocess
import argparse
import copy
import sys

class DryrunScript():
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.file_lines = []
        with open(file_name, "r") as f:
            for line in f.readlines():
                self.file_lines.append(line.strip())

        self.decorator = []
        self.command = []
        for line in self.file_lines:
            if len(line) > 0:
                if line[0] == "#":
                    self.decorator.append(line)
                else:
                    self.command.append(line)
        self.command_merged = []
        line_temp = ""
        for i, line in enumerate(self.command):
            if line[-1] == "\\":
                line_temp += line[:-1].strip() + " "
                # In case last line also has "\\"
                if i == len(self.command) - 1:
                    self.command_merged.append(line_temp)
            else:
                line_temp += line
                self.command_merged.append(line_temp)
                line_temp = ""

        self.dryrun_config = """dryrun() {
    if [[ ! -t 0 ]]
    then
        cat
    fi
    printf -v cmd_str '%q ' "$@"; echo "$cmd_str"
}"""
    
    def create_dryrun_script(self):
        self.dryrun_file = os.path.splitext(self.file_name)[0] + "_dryrun" + ".sh"
        with open(self.dryrun_file, "w") as f:
            for line in self.decorator:
                f.write(line + "\n")

            f.write(self.dryrun_config + "\n")

            for line in self.command_merged:
                python_prefixes = ["python", "python3"]
                if any(prefix + " " in line for prefix in python_prefixes):
                    f.write("dryrun " + line + "\n")
                elif line.startswith("export"):
                    f.write("dryrun " + line + "\n")
                else:
                    f.write(line + "\n")

class ExportVSConfigBash():
    def export(self, input_file, output_file="config.json"):
        # Create and run dryrun file
        dryrun = DryrunScript(input_file)
        dryrun.create_dryrun_script()

        result = subprocess.check_output(["bash", f"{dryrun.dryrun_file}"])

        result = result.decode().splitlines()

        # Remove dryrun file
        os.remove(f"{dryrun.dryrun_file}") 

        # Process output from dryrun
        env_list = []
        env_buffer = {}
        python_command_list = []

        for line in result:
            # Detect python
            python_prefixes = ["python", "python3"]
            if any(prefix + " " in line for prefix in python_prefixes):
                python_command_list.append(line)
                env_list.append(copy.deepcopy(env_buffer))
            # Dectect environment variable
            elif line.startswith("export"):
                name, value = line.split()[-1].split("=")
                env_buffer[name] = value

        configurations_dict = {}

        for i, _ in enumerate(python_command_list):

            python_command_separated = python_command_list[i].split()
            python_prefixes = ["python", "python3"]
            for prefix in python_prefixes:
                if prefix in python_command_separated:
                    python_index = python_command_separated.index(prefix)

            python_args_joined = " ".join(python_command_separated[python_index+2:])
            self.write_args_to_json(python_args_joined)
            with open('vsargs.json') as file:
                args = json.load(file)
            os.remove('vsargs.json')

            configurations_dict[f"script_{i}"] = {}
            configurations_dict[f"script_{i}"]["program"] = python_command_separated[python_index+1]
            configurations_dict[f"script_{i}"]["args"] = args
            configurations_dict[f"script_{i}"]["env"] = env_list[i]

            env_variables = python_command_separated[:python_index]

            for variable in env_variables:
                name, value = variable.split("=")
                configurations_dict[f"script_{i}"]["env"][name] = value

        with open(output_file, "w") as file:
            json.dump(configurations_dict, file, sort_keys=False, indent=4)

    @staticmethod
    def write_args_to_json(args_str):
        full_path = os.path.realpath(__file__)
        print(full_path)
        python_command = f"{full_path} {args_str} --mode_vsparser export_arg"
        os.system(f"python {python_command}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode_vsparser', type=str, default="run")
    args, unkown_args = parser.parse_known_args()
    VS_exporter = ExportVSConfigBash()
    if args.mode_vsparser == "run":
        parser.add_argument('--input', type=str, default="quan.sh")
        parser.add_argument('--output', type=str, default="config.json")
        args, unkown_args = parser.parse_known_args()
        VS_exporter.export(args.input, args.output)
    if args.mode_vsparser == "export_arg":
        with open("vsargs.json", "w") as file:
            json.dump(unkown_args, file, sort_keys=False, indent=4)