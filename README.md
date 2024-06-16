# VeriGen

This is an attempt to fine tune SOTA Large Language Models so as to generate Verilog (VHDL) programmes, detect syntax, logic and human errors in codes and rectify them.

## Directory Guide

```
├── .gitignore
├── LICENSE
├── README.md
├── data
│     └── df_small.csv
├── Llama2
|     └── llama2-on-verilog-code-data.ipynb
├── Phi2-LoRA
|     └── finetuning-phi2-using-lora-on-dialogsum-dataset.ipynb
├── ref
|     └── RTLFixerAutomatically Fixing RTL Syntax Errors with LargeLanguage Models.pdf
└──  utils
      └── functions.py

```

Dataset Link - !(https://drive.google.com/drive/folders/1kE3Rr6AFidkoaZG_risZXP7fSGhw1vCR?usp=drive_link)[Link]