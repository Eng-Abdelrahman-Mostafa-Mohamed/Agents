from llama_index.core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
)



# instruction_str = """\
#     1. Convert the query to executable Python code using Pandas.
#     2. The final line of code should be a Python expression that can be called with the `eval()` function.
#     3. The code should represent a solution to the query.
#     4. PRINT ONLY THE EXPRESSION.
#     5. Do not quote the expression.
#     6. data is the local data stored in the bath that you know
#     7. you must run code to find the columns of data to know its and match the input columns name from user to correct column name in data to generate correct code 
#     """
    
instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. Ensure the final line of code is a Python expression that can be executed with the `eval()` function.
    3. The code should accurately represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION without any additional text or formatting.
    5. Do not enclose the expression in quotes.
    6. The variable `data` refers to the local dataset stored at the specified path.
    7. Before generating the code, run a preliminary script to identify the columns in the dataset.
    8. Match the input column names provided by the user to the correct column names in the dataset to ensure the generated code is accurate.
    9. If the query involves plotting or visualizing data, ensure the code includes the necessary import statements and plotting commands.
    10. If the query cannot be resolved with the local data, indicate that a web search will be performed to find the best possible response.
    11. Generate the code but do not execute it in the terminal. Instead, provide the code as output for review.
    12. If the user requests to run the code, use the `code_runner_agent` to execute it and display the results.
    """


new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is worledPobulation2023.csv which stord in {data}.
    This is the result of `print(data.head())`:
    {data_str}
    the generated code full with imports in python is {code} and please 
    Follow these instructions:
    {instruction_str}
    and if i asked you run code and find  results  not find result directly to check that generated code is correct run code in terminal and 
    output of code using {code_runner_engine} which i add into agent as function_engin_tool  
    is {output} and the output of responce is {responce} 
    if you didnt find the answer from given data search on web and give me the best responces and before that tell me iam searching  
    
    Query: {query_str}

    Expression: """
)
# new_prompt = f"{new_prompt} /n the path of local data is {local_data_path}"
context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about world population statistics and details about a country and have abillity to generate full python 
            code that give the answer of query from data (full code with imports)  {generated_code} but if i didnt ask you to give me code --> give me result directly or my query 
             
. """

# from llama_index.core.prompts import (
#     ChatPromptTemplate,
#     PromptTemplate,
# )

# instruction_str = """\
#     1. Convert the query to executable Python code using Pandas.
#     2. The final line of code should be a Python expression that can be called with the `eval()` function.
#     3. The code should represent a solution to the query.
#     4. PRINT ONLY THE EXPRESSION.
#     5. Do not quote the expression.
#     """
    

# new_prompt = PromptTemplate(
#     """\
#     You are working with a pandas dataframe in Python.
#     The name of the dataframe is `df`.
#     This is the result of `print(df.head())`:
#     {df_str}
    
#     The generated code (with all necessary imports) in Python is: {generated_code_from_agents}.
    
#     Follow these instructions:
#     {instruction_str}
    
#     If asked to run the code and check the results, execute the generated code in the terminal and return the output.
#     Hint the path of data is "/home/abdelrahman/Documents/learning_RAG/WorldPopulation2023.csv"

#     The result of running the code is: {output}
    
#     Query: {query_str}

#     Expression: """
# )

# context = """Purpose: The primary role of this agent is to assist users by providing accurate 
#             information about world population statistics and details about a country, and has the ability to generate full Python 
#             code that gives the answer to a query from data (including imports). The generated code is {generated_code_from_agents}. 
#             It can also execute the code and provide the output using a function tool named `code_runner_engine`."""

# print(new_prompt)
