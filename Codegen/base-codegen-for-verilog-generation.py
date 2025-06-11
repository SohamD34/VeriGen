from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_verilog(prompt, max_length=256, temperature=0.7, top_p=0.9):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            num_return_sequences=1,
        )
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_code


if __name__=="__main__":
 
 model_name = "Salesforce/codegen-16B-multi"
 
 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).cuda()
 
 prompt = """// Verilog module for a 4-bit adder
module adder4bit(
     input [3:0] a,
     input [3:0] b,
     output [4:0] sum
);
"""
 
 generated_verilog = generate_verilog(prompt)
 print(generated_verilog)
