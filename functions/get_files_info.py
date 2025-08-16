import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_full = os.path.abspath(working_directory)

    # print(f'{full_path=}, {working_directory=}')

    if working_directory_full not in full_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    res = ''
    # print(os.listdir(full_path))

    for dir_elem in os.listdir(full_path):
        dir_elem_path = os.path.join(full_path, dir_elem)
        if os.path.isfile(dir_elem_path):
            res += f"- {dir_elem}: file_size={os.path.getsize(dir_elem_path)} bytes, is_dir=False\n"
        else: 
            res += f"- {dir_elem}: file_size={os.path.getsize(dir_elem_path)} bytes, is_dir=True\n"
    
    return res
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)