import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for name in os.listdir(target_dir):
            full = os.path.join(target_dir, name)
            entries.append(
                f"- {name}: file_size={os.path.getsize(full)} bytes, "
                f"is_dir={os.path.isdir(full)}"
            )
        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"
