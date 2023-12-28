import json
import copy

def VScode_export(command_input, output_file):
    command = copy.deepcopy(command_input)
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
    command = "CUDA_VISIBLE_DEVICES=0 python ./src/train.py --cuda --data data/ --dataset wt103 --adaptive --n_layer 16 --d_model 128 --n_head 8 --d_head 16 --d_inner 2048 --dropout 0.1 --dropatt 0.0 --optim adam --lr 0.00025 --warmup_step 2000 --max_step 500000 --attn_type 2 --tgt_len 256 --mem_len 0 --eval_tgt_len 256 --batch_size 96 --multi_gpu --use_wandb --project_name 'mgk' --seed 1111 --job_name softmax-seed-1111 --work_dir checkpoints/softmax-seed-1111"
    VScode_export(command, output_file = "configurations.json")


