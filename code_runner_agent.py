# from llama_index.core.tools import function_tool
from llama_index.core.tools import FunctionTool
import subprocess
import os

def run_code(code):
    try:
        temp_file_path = 'temp_script.py'
        with open(temp_file_path, 'w') as f:
            f.write(code)

        process = subprocess.run(['python3', temp_file_path], check=True, text=True, capture_output=True)

        os.remove(temp_file_path)
        output = process.stdout
        return output
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e.stderr}"





code_runner_engine = FunctionTool.from_defaults(fn=run_code
                                                       ,name='code_runner',
                                                       description='this run the generated code which is {code} in terminal and save outputs into {output} ',
                                                    )




# code_syntax = """
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd 
# # assume you have the data for world population and growth rate

# data=pd.read_csv("WorldPopulation2023.csv")

# net_change = data["NetChange"]
# years = np.arange(2020, 2020+len(net_change))
# plt.plot(years, net_change)
# plt.xlabel('Year')
# plt.ylabel('Net Change')
# plt.title('Net Change in World Population')
# plt.show()
# """

# output = run_code(code_syntax)
# print(output)

#this is my note this part is creating code runner Queryagent to pass as toolagent to agent_sytem
# Define the FunctionTool for the code runner
code_runner_engine = FunctionTool.from_defaults(
    fn=run_code,
    name='code_runner',
    description='This runs the generated code which is code in the terminal and saves outputs into output.'
)
