import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # print(f'{full_path=}, {working_directory=}')

    if working_directory not in full_path:
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
    

# print(get_files_info("calculator", "."))
# print(get_files_info("calculator", "pkg"))
# print(get_files_info("calculator", "/bin"))
# print(get_files_info("calculator", "../"))

