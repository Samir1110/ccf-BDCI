#!/bin/bash

# 获取当前脚本所在的路径
CURRENT_DIR=$(pwd)

# 输出路径（可选调试）
echo "当前路径为: $CURRENT_DIR"

# 替换所有路径为动态获取的当前路径
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 llamafactory-cli train \
    --stage sft \
    --do_predict \
    --model_name_or_path "$CURRENT_DIR/620ccf/Qwen2___5-Coder-32B-Instruct" \
    --adapter_name_or_path "$CURRENT_DIR/620ccf/saves/train_qwen_32b/checkpoint-300" \
    --eval_dataset adgen_local_correct \
    --dataset_dir "$CURRENT_DIR/620ccf/data" \
    --template llama3 \
    --finetuning_type lora \
    --output_dir "$CURRENT_DIR/620ccf/output/error" \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 1024 \
    --preprocessing_num_workers 16 \
    --per_device_eval_batch_size 1 \
    --max_samples 2000 \
    --predict_with_generate
