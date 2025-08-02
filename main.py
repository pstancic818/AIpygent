import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.config import model_name, system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import write_file, schema_write_file
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.call_function import call_function, schema_call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if not api_key:
        print("GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
    if len(sys.argv) <= 1:
        print("ERROR: No prompt provided.")
        print("USAGE: uv run main.py <prompt>")
        sys.exit(1)
    #print("Hello from AIpygent!")
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content, 
            schema_write_file, 
            schema_run_python_file, 
            schema_call_function
        ]
    )
    messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]
    for i in range(20):
        try:
            response = client.models.generate_content(
                model=model_name, 
                contents=messages, 
                config=types.GenerateContentConfig(
                    tools=[available_functions],system_instruction=system_prompt
                )
            )
            if response.candidates:
                for j in response.candidates:
                    messages.append(j.content)
            if response.function_calls:
                for j in response.function_calls:
                    if "--verbose" in sys.argv:
                        function_response = call_function(j, verbose=True)
                        function_response_part = types.Part(function_response=function_response.parts[0].function_response)
                        messages.append(types.Content(role="tool", parts=[function_response_part]))
                    else:
                        function_response = call_function(j)
                        function_response_part = types.Part(function_response=function_response.parts[0].function_response)
                        messages.append(types.Content(role="tool", parts=[function_response_part]))
                    if not function_response.parts[0].function_response.response:
                        raise Exception("Function response is empty")
                    if "--verbose" in sys.argv:
                        print(f'f-> {function_response.parts[0].function_response.response}')
            elif response.text:
                print("Final response:")
                print(response.text)
                break
        except Exception as e:
            print(f'Error: {str(e)}')
            break


if __name__ == "__main__":
    main()
