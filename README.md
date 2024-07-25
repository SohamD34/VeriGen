# VeriGen

This is an attempt to fine tune SOTA Large Language Models so as to generate Verilog (VHDL) programmes, detect syntax, logic and human errors in codes and rectify them.

## Directory Guide

```
├── .gitignore
├── LICENSE
├── README.md
├── environment.yaml
├── requirements.txt
├── data
│     └── df_small.csv
│     └── formatted_small_df.csv
├── preprocessing
│     └── data_preprocessing.py
│     └── small_df_preprocessing.py        // generates .csv file with base prompt, instructions, error code and correct (expected) output
├── CodeGen
|     └── base-codegen-for-verilog-generation.ipynb            
├── Llama2
|     └── base_llama.ipynb
|     └── finetuning-llama2-7b-on-verilog-code-data.ipynb
├── ref
|     └── RTLFixerAutomatically Fixing RTL Syntax Errors with LargeLanguage Models.pdf
|     └── Phi2-LoRA
|           └── finetuning-phi2-using-lora-on-dialogsum-dataset.ipynb
└──  utils
      └── functions.py

```

Dataset Link - [[Link](https://drive.google.com/drive/folders/1kE3Rr6AFidkoaZG_risZXP7fSGhw1vCR?usp=drive_link)]
