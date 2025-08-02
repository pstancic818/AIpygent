from google.genai import types

schema_call_function = types.FunctionDeclaration(
    name="call_function",
    description="Call a function with the specified arguments in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "function_call_part": types.Schema(
                type=types.Type.OBJECT,
                description="The function call part containing the function name and arguments.",
            ),
            "verbose": types.Schema(
                type=types.Type.BOOLEAN,
                description="Whether to print verbose output.",
            ),
        },
    ),
)

def call_function(function_call_part, verbose=False):
    function_call_part.args["working_directory"] = "./calculator"
    function_name = function_call_part.name
    if verbose:
        print(f'- Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f'- Calling function: {function_call_part.name}')
    match function_call_part.name:
        case "get_files_info":
            from .get_files_info import get_files_info
            function_result = get_files_info(**function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ]
            )
        case "get_file_content":
            from .get_file_content import get_file_content
            function_result = get_file_content(**function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ]
            )
        case "write_file":
            from .write_file import write_file
            function_result = write_file(**function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ]
            )
        case "run_python_file":
            from .run_python_file import run_python_file
            function_result = run_python_file(**function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ]
            )
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f'Unknown function: {function_name}'}
                    )
                ]
            )