import json
import os
import subprocess
import argparse

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
                if "python " in line: 
                    f.write("dryrun " + line + "\n")
                else:
                    f.write(line + "\n")

def VScode_export_bashscript(input_file, output_file="configurations.json"):
    # Create and run dryrun file
    dryrun = DryrunScript(input_file)
    dryrun.create_dryrun_script()

    result = subprocess.check_output(["bash", f"{dryrun.dryrun_file}"])

    result = result.decode().splitlines()

    # Remove dryrun file
    os.remove(f"{dryrun.dryrun_file}") 

    # Process output from dryrun
    python_command_list = []

    for line in result:
        # Detect python
        if "python " in line:
            python_command_list.append(line)

    configurations_dict = {}

    for i, _ in enumerate(python_command_list):
        python_command_list[i] = python_command_list[i].replace("\"", "").replace("\'", "")
        all_elements = python_command_list[i].split()

        configurations_dict[f"script_{i}"] = {}
        configurations_dict[f"script_{i}"]["program"] = all_elements[all_elements.index("python")+1]
        configurations_dict[f"script_{i}"]["args"] = all_elements[all_elements.index("python")+2:]

        env_variables = all_elements[:all_elements.index("python")]
        configurations_dict[f"script_{i}"]["env"] = {}

        for variable in env_variables:
            name, value = variable.split("=")
            configurations_dict[f"script_{i}"]["env"][name] = value

    with open(output_file, "w") as file:
        json.dump(configurations_dict, file, sort_keys=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="unify.sh")
    parser.add_argument('--output_file', type=str, default="configurations.json")
    args = parser.parse_args() 
    VScode_export_bashscript(args.input_file, args.output_file)
