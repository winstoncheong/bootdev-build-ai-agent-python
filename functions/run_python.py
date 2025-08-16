import os 
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # print(f'{full_path=}, {working_directory=}')

    if working_directory not in full_path:
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