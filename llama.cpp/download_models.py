import os
import sys
from huggingface_hub import hf_hub_download

# Base directory for models
base_dir = r"D:\Docker\llama.cpp\models"

downloads = [
    {
        "repo_id": "unsloth/Qwen3.6-35B-A3B-MTP-GGUF",
        "filename": "Qwen3.6-35B-A3B-UD-IQ4_NL.gguf",
        "local_dir": os.path.join(base_dir, "Qwen3.6-35B-A3B-MTP-GGUF")
    },
    {
        "repo_id": "unsloth/Qwen3.6-35B-A3B-MTP-GGUF",
        "filename": "mmproj-F16.gguf",
        "local_dir": os.path.join(base_dir, "Qwen3.6-35B-A3B-MTP-GGUF")
    },
    {
        "repo_id": "unsloth/Qwen3.5-9B-MTP-GGUF",
        "filename": "Qwen3.5-9B-UD-Q4_K_XL.gguf",
        "local_dir": os.path.join(base_dir, "Qwen3.5-9B-MTP-GGUF")
    },
    {
        "repo_id": "unsloth/Qwen3.5-9B-MTP-GGUF",
        "filename": "mmproj-F16.gguf",
        "local_dir": os.path.join(base_dir, "Qwen3.5-9B-MTP-GGUF")
    }
]

print("Starting downloads...", flush=True)

for dl in downloads:
    repo_id = dl["repo_id"]
    filename = dl["filename"]
    local_dir = dl["local_dir"]
    
    print(f"\nDownloading {filename} from {repo_id} to {local_dir}...", flush=True)
    try:
        os.makedirs(local_dir, exist_ok=True)
        # Download and put in local_dir with the same structure
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"Successfully downloaded: {filename} to {path}", flush=True)
    except Exception as e:
        print(f"Error downloading {filename} from {repo_id}: {e}", flush=True)

print("\nAll downloads finished!", flush=True)
