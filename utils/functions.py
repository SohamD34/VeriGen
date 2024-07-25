from pynvml import *
from functools import partial
import re
import random

def print_gpu_utilization():
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    print(f"GPU memory occupied: {info.used//1024**2} MB.")


def create_prompt_formats(sample):
    """
    Format various fields of the sample ('instruction','output')
    Then concatenate them using two newline characters 
    :param sample: Sample dictionnary
    """
    INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
    INSTRUCTION_KEY = "### Instruct: Summarize the below conversation."
    RESPONSE_KEY = "### Output:"
    END_KEY = "### End"
    
    blurb = f"\n{INTRO_BLURB}"
    instruction = f"{INSTRUCTION_KEY}"
    input_context = f"{sample['dialogue']}" if sample["dialogue"] else None
    response = f"{RESPONSE_KEY}\n{sample['summary']}"
    end = f"{END_KEY}"
    
    parts = [part for part in [blurb, instruction, input_context, response, end] if part]

    formatted_prompt = "\n\n".join(parts)
    sample["text"] = formatted_prompt

    return sample



# SOURCE https://github.com/databrickslabs/dolly/blob/master/training/trainer.py
def get_max_length(model):
    conf = model.config
    max_length = None
    for length_setting in ["n_positions", "max_position_embeddings", "seq_length"]:
        max_length = getattr(model.config, length_setting, None)
        if max_length:
            print(f"Found max lenth: {max_length}")
            break
    if not max_length:
        max_length = 1024
        print(f"Using default max length: {max_length}")
    return max_length



def preprocess_batch(batch, tokenizer, max_length):
    """
    Tokenizing a batch
    """
    return tokenizer(
        batch["text"],
        max_length=max_length,
        truncation=True,
    )


# SOURCE https://github.com/databrickslabs/dolly/blob/master/training/trainer.py
def preprocess_dataset(tokenizer, max_length: int, seed, dataset):
    """Format & tokenize it so it is ready for training
    :param tokenizer (AutoTokenizer): Model Tokenizer
    :param max_length (int): Maximum number of tokens to emit from tokenizer
    """
    
    # Add prompt to each sample
    print("Preprocessing dataset...")
    dataset = dataset.map(create_prompt_formats)#, batched=True)
    
    _preprocessing_function = partial(preprocess_batch, max_length=max_length, tokenizer=tokenizer)
    dataset = dataset.map(
        _preprocessing_function,
        batched=True,
        remove_columns=['id', 'topic', 'dialogue', 'summary'],
    )

    dataset = dataset.filter(lambda sample: len(sample["input_ids"]) < max_length)
    dataset = dataset.shuffle(seed=seed)

    return dataset



def randomize_variable_names(verilog_code, change_probability=0.5):
    variables = re.findall(r'\b\w+\b', verilog_code)

    keywords = {'module', 'input', 'output', 'wire', 'reg', 'assign', 'always', 'begin', 'end'}
    variables = [var for var in variables if var not in keywords and not var.isdigit()]
    unique_variables = set(variables)

    changed_variables = {}
    for var in unique_variables:
        new_var = var + str(random.randint(0, 9))
        changed_variables[var] = new_var

    def random_replace(match):
        var = match.group(0)
        if var in changed_variables and random.random() < change_probability:
            return changed_variables[var]
        return var

    randomized_verilog_code = re.sub(r'\b\w+\b', random_replace, verilog_code)

    return randomized_verilog_code



def randomize_operators(verilog_code, change_probability=0.5):
    operators = ['\+', '-', '\*', '/', '%', '&', '\|', '\^', '!', '~', '&&', '\|\|', '==', '!=', '<', '<=', '>', '>=']
    operator_replacements = {
        '+': ['-', '*', '/', '%', '&&', '^'],
        '-': ['+', '*', '/', '%', '&&', '^'],
        '*': ['+', '-', '/', '%', '&&', '^'],
        '/': ['+', '-', '*', '%', '&&', '^'],
        '%': ['+', '-', '*', '/', '&&', '^'],
        '&': ['&', '|', '+', '*', '/', '-'],
        '|': ['&', '|', '+', '*', '/', '-'],
        '^': ['&', '|', '+', '*', '/', '-'],
        '!': ['&', '|', '+', '*', '/', '-'],
        '~': ['&', '|', '+', '*', '/', '-'],
        '&&': ['||', '%%'],
        '||': ['&&', '%%'],
        '==': ['!=', '<', '<=', '>', '>='],
        '!=': ['==', '<', '<=', '>', '>='],
        '<': ['<=', '>', '>='],
        '<=': ['<', '>', '>='],
        '>': ['<', '<=', '>='],
        '>=': ['<', '<=', '>']
    }

    def random_replace_operator(match):
        op = match.group(0)
        if random.random() < change_probability:
            possible_replacements = operator_replacements.get(op, [])
            if possible_replacements:
                return random.choice(possible_replacements)
        return op

    pattern = re.compile('|'.join(operators))
    randomized_verilog_code = pattern.sub(random_replace_operator, verilog_code)
    return randomized_verilog_code



def comment_lines(input_string):
    """
    Adds '//' at the beginning of random lines in the input string
    """
    lines = input_string.split('\n')
    total_lines = len(lines)
    
    num_comments = random.randint(0, total_lines//2)
    
    for i in range(num_comments):
        line_no = random.randint(0, total_lines-1)
        lines[line_no] = '//' + lines[line_no]
    
    commented_string = '\n'.join(lines)    
    return commented_string
