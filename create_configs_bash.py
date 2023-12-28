import json
import os
import subprocess

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
        print("test")

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
    # 
    dryrun = DryrunScript(input_file)
    dryrun.create_dryrun_script()

    result = subprocess.check_output(["bash", f"{dryrun.dryrun_file}"])

    result = result.decode().splitlines()

    for line in result:
        if "python " in line:
            command = line

    command = command.replace("\"", "")
    command = command.replace("\'", "")
    all_elements = command.split()

    args = all_elements[all_elements.index("python")+2:]
    program = all_elements[all_elements.index("python")+1]

    env_variables = all_elements[:all_elements.index("python")]
    variable_dict = {}
    for variable in env_variables:
        name, value = variable.split("=")
        variable_dict[name] = value

    configurations_dict = {"program": program, "args": args, 
                        "env": variable_dict}
    with open(output_file, "w") as file:
        json.dump(configurations_dict, file)

if __name__ == "__main__":
    input_file = "unify.sh"
    output_file = "configurations.json"
    VScode_export_bashscript(input_file, output_file)
