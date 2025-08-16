from google.genai import types
from functions.run_python import run_python_file
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.get_file_content import get_file_content


def call_function(function_call_part: types.FunctionCall, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    
    fname = function_call_part.name
    args = function_call_part.args
    working_directory = "./calculator"

    if fname == "get_file_content":
        fres = get_file_content(working_directory=working_directory, **args)
    elif fname == "write_file":
        fres = write_file(working_directory=working_directory, **args)
    elif fname == "get_files_info":
        fres = get_files_info(working_directory=working_directory, **args)
    elif fname == "run_python_file":
        fres = run_python_file(working_directory=working_directory, **args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fname,
                    response={"error": f"Unknown function: {fname}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fname,
                response={"result": fres},
            )
        ],
    )