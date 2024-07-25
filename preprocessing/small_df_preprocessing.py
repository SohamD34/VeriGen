import os
import pandas as pd
import numpy as np
import random
from utils.functions import comment_lines, randomize_operators, randomize_variable_names

os.chdir('E:/Binod Sir Internship/VeriGen')

half_adder_1_bit = """
module half_adder (
    input a, b,
    output sum, carry
);
    assign sum = a ^ b;
    assign carry = a & b;
endmodule
"""

full_adder_1_bit = """
module full_adder (
    input a, b, cin,
    output sum, carry
);
    assign sum = a ^ b ^ cin;
    assign carry = (a & b) | (b & cin) | (a & cin);
endmodule
"""

full_adder_32_bit = """
module full_adder_32 (
    input [31:0] a, b,
    input cin,
    output [31:0] sum,
    output carry
);
    wire [31:0] carry_out;
    assign carry_out[0] = cin;

    genvar i;
    generate
        for (i = 0; i < 32; i = i + 1) begin: full_adders
            full_adder fa (
                .a(a[i]),
                .b(b[i]),
                .cin(carry_out[i]),
                .sum(sum[i]),
                .carry(carry_out[i + 1])
            );
        end
    endgenerate
    assign carry = carry_out[32];
endmodule
"""

subtractor_32_bit = """
module subtractor_32 (
    input [31:0] a, b,
    output [31:0] diff,
    output borrow
);
    wire [31:0] b_complement = ~b + 1; // 2's complement of b
    wire [31:0] temp_sum;
    full_adder_32 fa32 (
        .a(a),
        .b(b_complement),
        .cin(1'b0),
        .sum(temp_sum),
        .carry(borrow)
    );
    assign diff = temp_sum;
endmodule
"""

multiplier_1_bit = """
module multiplier_1 (
    input a, b,
    output product
);
    assign product = a & b;
endmodule
"""

multiplier_32_bit = """
module multiplier_32 (
    input [31:0] a, b,
    output [63:0] product
);
    assign product = a * b;
endmodule
"""

and_gate = """
module and_1 (
    input a, b,
    output result
);
    assign result = a & b;
endmodule
"""

or_gate = """
module or_1 (
    input a, b,
    output result
);
    assign result = a | b;
endmodule
"""

not_gate = """
module not_1 (
    input a,
    output result
);
    assign result = ~a;
endmodule
"""

xor_gate = """
module xor_1 (
    input a, b,
    output result
);
    assign result = a ^ b;
endmodule
"""

nand_gate = """
module nand_1 (
    input a, b,
    output result
);
    assign result = ~(a & b);
endmodule
"""

nor_gate = """
module nor_1 (
    input a, b,
    output result
);
    assign result = ~(a | b);
endmodule
"""

mux_1to2 = """
module mux_1to2 (
    input d0, d1, sel,
    output y
);
    assign y = sel ? d1 : d0;
endmodule
"""

mux_1to4 = """
module mux_4to1 (
    input [3:0] d,
    input [1:0] sel,
    output y
);
    assign y = d[sel];
endmodule
"""

mux_1to8 = """
module mux_8to1 (
    input [7:0] d,
    input [2:0] sel,
    output y
);
    assign y = d[sel];
endmodule
"""

mux_1to16 = """
module mux_16to1 (
    input [15:0] d,
    input [3:0] sel,
    output y
);
    assign y = d[sel];
endmodule
"""

mux_1to32 = """
module mux_32to1 (
    input [31:0] d,
    input [4:0] sel,
    output y
);
    assign y = d[sel];
endmodule
"""

mux_1to64 = """
module mux_64to1 (
    input [63:0] d,
    input [5:0] sel,
    output y
);
    assign y = d[sel];
endmodule
"""

demux_2to1 = """
module demux_1to2 (
    input d, sel,
    output y0, y1
);
    assign y0 = ~sel & d;
    assign y1 = sel & d;
endmodule
"""

demux_4to1 = """
module demux_1to4 (
    input d,
    input [1:0] sel,
    output [3:0] y
);
    assign y = (1 << sel) & {4{d}};
endmodule
"""

demux_8to1 = """
module demux_1to8 (
    input d,
    input [2:0] sel,
    output [7:0] y
);
    assign y = (1 << sel) & {8{d}};
endmodule
"""

demux_16to1 = """
module demux_1to16 (
    input d,
    input [3:0] sel,
    output [15:0] y
);
    assign y = (1 << sel) & {16{d}};
endmodule
"""

demux_32to1 = """
module demux_1to32 (
    input d,
    input [4:0] sel,
    output [31:0] y
);
    assign y = (1 << sel) & {32{d}};
endmodule
"""

demux_64to1 = """
module demux_1to64 (
    input d,
    input [5:0] sel,
    output [63:0] y
);
    assign y = (1 << sel) & {64{d}};
endmodule
"""


#---------------------------------------------ADDING COMMENTS---------------------------------------------#

data = pd.read_csv('../VeriGen/data/df_small.csv')
print(len(data))

L = [half_adder_1_bit, full_adder_1_bit, full_adder_32_bit, subtractor_32_bit, multiplier_1_bit, multiplier_32_bit, and_gate, or_gate, not_gate, 
     xor_gate, nand_gate, nor_gate, mux_1to2, mux_1to4, mux_1to8, mux_1to16, mux_1to32, mux_1to64, demux_2to1, demux_4to1, demux_8to1, demux_16to1, demux_32to1, 
     demux_64to1]

for i in range(2):
    for string in L:
        for j in range(10):
            new_string = comment_lines(string)
            new_df = pd.DataFrame(columns=['Correct','Error'])
            new_df['Correct'] = [string]
            new_df['Error'] = [new_string]
            data = pd.concat([data, new_df], ignore_index=True)
        
print(len(data))
data = data.sample(frac=1).reset_index(drop=True)
# data.to_csv('commented.csv', index=False)


#---------------------------------------------CHANGING VARIABLE NAMES---------------------------------------------#

L = [half_adder_1_bit, full_adder_1_bit, full_adder_32_bit, subtractor_32_bit, multiplier_1_bit, multiplier_32_bit, and_gate, or_gate, not_gate, 
     xor_gate, nand_gate, nor_gate, mux_1to2, mux_1to4, mux_1to8, mux_1to16, mux_1to32, mux_1to64, demux_2to1, demux_4to1, demux_8to1, demux_16to1, demux_32to1, 
     demux_64to1]

for i in range(2):
    for string in L:
        for j in range(10):
            new_string = randomize_variable_names(string)
            new_df = pd.DataFrame(columns=['Correct','Error'])
            new_df['Correct'] = [string]
            new_df['Error'] = [new_string]
            data = pd.concat([data, new_df], ignore_index=True)
        
print(len(data))
data = data.sample(frac=1).reset_index(drop=True)
# data.to_csv('commented.csv', index=False)


#---------------------------------------------OPERATOR ERRORS---------------------------------------------#


L = [half_adder_1_bit, full_adder_1_bit, full_adder_32_bit, subtractor_32_bit, multiplier_1_bit, multiplier_32_bit, and_gate, or_gate, not_gate, 
     xor_gate, nand_gate, nor_gate, mux_1to2, mux_1to4, mux_1to8, mux_1to16, mux_1to32, mux_1to64, demux_2to1, demux_4to1, demux_8to1, demux_16to1, demux_32to1, 
     demux_64to1]

for i in range(2):
    for string in L:
        for j in range(10):
            new_string = randomize_operators(string)
            new_df = pd.DataFrame(columns=['Correct','Error'])
            new_df['Correct'] = [string]
            new_df['Error'] = [new_string]
            data = pd.concat([data, new_df], ignore_index=True)
        
print(len(data))
data = data.sample(frac=1).reset_index(drop=True)
# data.to_csv('small_df.csv', index=False)



#---------------------------------------------FORMATTING DATASET---------------------------------------------#


# data = pd.read_csv('../VeriGen/data/small_df.csv')
print(len(data))
data.head(2)

base_prompt = """\nBASE PROMPT: You are an expert in Verilog code generation and code correction. Below is an instruction that describes a task. Write a response that appropriately completes the request. Do not write any explanation after the code."""

instruction = """\nINSTRUCT: Correct the logic and syntax of the following Verilog code. Check and correct any instances of wrong or missing commented lines, variable names, module names, and operators."""

end = """CODE: \n"""


data['Base Prompt'] = [base_prompt for i in range(len(data))]
data['Instruction'] = [instruction for i in range(len(data))]
data['End'] = [end for i in range(len(data))]

data = data[['Base Prompt', 'Instruction', 'Error', 'End', 'Correct']]
# data.head(2)

data.to_csv('../VeriGen/data/formatted_small_df.csv', index=False)