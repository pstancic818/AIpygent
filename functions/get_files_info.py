import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), directory))
    tmp_string = ""
    #if directory == ".":
    #    print(f'Result for current directory:')
    #else:
    #    print(f'Result for \'{directory}\' directory:')
    try:
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        for i in os.listdir(full_path):
            tmp_string += f'- {i}: file_size={os.path.getsize(full_path + "/" + i)} is_dir={os.path.isdir(full_path + "/" + i)}\n'
        return tmp_string
    except Exception as e:
        return f'Error: {str(e)}'