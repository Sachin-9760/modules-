# Module 5: Local Models, Ollama, DeepSeek, Hugging Face, and Colab

This mini-project compares two inference workflows on the same sentiment task set:

1. **Ollama**: a local model called through the Ollama HTTP API.
2. **Hugging Face**: a pretrained text-classification pipeline.

The main artifact is `module5_compare_workflows.ipynb`.

## Quick start

### 1. Hugging Face workflow

Create a Python environment and install the notebook dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Open the notebook in VS Code or Jupyter and run all cells. The first Hugging Face run downloads `distilbert-base-uncased-finetuned-sst-2-english` from the Hub.

### 2. Ollama workflow

Install Ollama from https://ollama.com/download, start it, and pull a model:

```powershell
ollama pull llama3.2:3b
```

Then run the notebook. To try a DeepSeek variant when your hardware supports it, change `OLLAMA_MODEL` to a model shown at https://ollama.com/search?q=deepseek, for example `deepseek-r1:7b`, and pull that model first.

The notebook checks `http://localhost:11434` before making calls. If Ollama is not running, its results are marked unavailable and the Hugging Face experiment still completes.

## Colab

Upload the notebook to Google Colab. Run the setup cell, then run the Hugging Face cells. Colab does not automatically provide a local Ollama daemon, so the Ollama side is expected to be unavailable unless you deliberately configure a reachable Ollama endpoint.

## What to report

Use the final comparison table to discuss:

- accuracy on the shared labeled examples;
- average latency and total runtime;
- model size, hardware, and network requirements;
- output reliability and how much prompt handling each workflow needs;
- why stable inference and evaluation should come before fine-tuning.

This is a learning experiment, not a production benchmark. The task set is intentionally small and should be expanded before making model-selection decisions.
