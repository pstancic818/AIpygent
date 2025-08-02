import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the specified working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python script.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
    
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ['python3', full_path]
        if args:
            command.extend(args)
        print(f'Running command: "{" ".join(command)}"')
        completed_process = subprocess.run(command, timeout=30, capture_output=True, cwd=os.path.abspath(working_directory))
        output = []
        if completed_process.stdout:
            output.append(f'STDOUT:\n{completed_process.stdout.decode()}')
        if completed_process.stderr:
            output.append(f'STDERR:\n{completed_process.stderr.decode()}')
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        return '\n'.join(output) if output else 'No output produced.'
    except Exception as e:
        return f'Error: executing Python file: {str(e)}'