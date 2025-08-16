import os 
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_full = os.path.abspath(working_directory)

    # print(f'{full_path=}, {working_directory=}')

    if working_directory_full not in full_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    cmd_lst = ['python', full_path, *args]

    # print(f'{cmd_lst=}')

    comp_proc = subprocess.run(cmd_lst,
                   timeout=30,
                   capture_output=True)
                
    # print(comp_proc)

    res = ''

    if comp_proc.stdout:
        res += f'STDOUT: {comp_proc.stdout}\n' 
    if comp_proc.stderr:
        res += f'STDERR: {comp_proc.stderr}\n' 

    if comp_proc.returncode != 0:
        res += f'Process existed with code {comp_proc.returncode}\n'

    if not res:
        return "No output produced"


    return res

# FunctionDeclaration for Gemini
from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file.",
            ),
        },
    ),
)