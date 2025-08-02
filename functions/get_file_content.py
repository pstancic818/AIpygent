import os
from google.genai import types
#from config import char_limit
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieve the content of a file from the file_path provided so long as it is in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

char_limit = 10000  # Assuming char_limit is defined here for simplicity

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, 'r') as file:
            content = file.read()
        if len(content) > char_limit:
            return f'{content[:char_limit]}[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'