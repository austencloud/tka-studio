# Update your test_model.py with this code:
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_id = "meta-llama/Llama-4-Maverick-17B-128E-Instruct"
bnb_cfg = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="bfloat16",
    llm_int8_enable_fp32_cpu_offload=True,  # Enable CPU offloading
)

tok = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_cfg,
    torch_dtype="bfloat16",
    low_cpu_mem_usage=True,  # Additional memory optimization
)

print("Model loaded successfully!")
