import os 

def write_file(working_directory, file_path, content):

    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # print(f'{full_path=}, {working_directory=}')

    if working_directory not in full_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    

    try:
        with open(full_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")

# FunctionDeclaration for Gemini
from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the provided content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)