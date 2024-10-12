from llama_index.core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
)



instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""

new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is `data`.
    This is the result of `print(data.head())`:
    {df_str}
    the generated code full with imports in python is {code} and please 
    Follow these instructions:
    {instruction_str}
    and if i asked you run code and find results not fin results result directly to check that generated code is correct run code in terminal and output of code  
    is {output}
      
    
    Query: {query_str}

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about world population statistics and details about a country and have abillity to generate full python 
            code that give the answer of query from data (full code with imports) the generated code is {generated_code_from_agents} but if ididnt ask you to give me code --> give me result directly or my query 

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
