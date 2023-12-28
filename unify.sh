output_dir="/home/rog/CGPT-appendix/CIFAR10/checkpoints" 
run_name="CGPT_BASE"
batch_size=4
batch_size_test=4
lr_ini=1e-5
lr_min=1e-5
lr_base=5e-4
warmup=0
decay=495
depth=5
num_class=10
hdim=128
num_heads=4
sample_size=1
jitter=1e-7
drop_rate=0.1
keys_len=32
kernel_type="std"
flag_cgp="True"
epochs=500
use_wandb="False"

flag_mle_100="False"
flag_mle_100_only_kernel="False"
flag_mle_best="False"

anneal_kl="1.0"
flag_adaptive_anneal="True"
anneal_kl_ini=0.0

cuda=0
seed=0

CUDA_VISIBLE_DEVICES=0 python train_cifar_cgp2.py \
    --output_dir ${output_dir} \
    --run_name ${run_name} \
    --seed ${seed} \
    --batch_size ${batch_size} \
    --batch_size_test  ${batch_size_test} \
    --lr_ini  ${lr_ini} \
    --lr_min  ${lr_min} \
    --lr_base  ${lr_base} \
    --warmup  ${warmup} \
    --decay  ${decay} \
    --depth  ${depth} \
    --num_class  ${num_class} \
    --hdim  ${hdim} \
    --num_heads  ${num_heads} \
    --sample_size  ${sample_size} \
    --jitter  ${jitter} \
    --drop_rate  ${drop_rate} \
    --keys_len  ${keys_len} \
    --kernel_type  ${kernel_type} \
    --flag_cgp  ${flag_cgp} \
    --epochs  ${epochs} \
    --use_wandb  ${use_wandb} \
    --flag_mle_100  ${flag_mle_100} \
    --flag_mle_100_only_kernel  ${flag_mle_100_only_kernel} \
    --flag_mle_best  ${flag_mle_best} \
    --anneal_kl  ${anneal_kl} \
    --flag_adaptive_anneal  ${flag_adaptive_anneal} \
    --anneal_kl_ini  ${anneal_kl_ini} \
    --cuda  ${cuda}

CUDA_VISIBLE_DEVICES=0 python ./src/train.py --cuda --data data/ --dataset wt103 --adaptive --n_layer 16 --d_model 128 --n_head 8 --d_head 16 --d_inner 2048 --dropout 0.1 --dropatt 0.0 --optim adam --lr 0.00025 --warmup_step 2000 --max_step 500000 --attn_type 2 --tgt_len 256 --mem_len 0 --eval_tgt_len 256 --batch_size 96 --multi_gpu --use_wandb --project_name 'mgk' --seed 1111 --job_name softmax-seed-1111 --work_dir checkpoints/softmax-seed-1111