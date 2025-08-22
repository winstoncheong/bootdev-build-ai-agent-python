import os
import sys
from icecream import ic
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
When asked to run a file without optional arguments supplied, just run the file.
Use the available function calls to answer the user's question.
Do not write to main.py.

If the user mentions any bugs, it pertains to the calculator program located at ./calculator/. 
You should try to fix the specified bugs.
"""

def main():

    # print(sys.argv)


    if len(sys.argv) == 1:
        print('Should provide prompt as commandline argument')
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    VERBOSE_FLAG_SET = ('--verbose' in sys.argv)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        resp = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # ic(resp)

        for candidate in resp.candidates:
            messages.append(candidate.content)

        if resp.text:
            print(resp.text)
        
        if resp.function_calls: # wants to execute a function call
            # print(resp.function_calls)
            for fcall in resp.function_calls:
                print(f"Calling function: {fcall.name}({fcall.args})")
                res = call_function(fcall, verbose=VERBOSE_FLAG_SET)
                if not res.parts[0].function_response.response:
                    raise Exception('Issue with function call response')
                response = res.parts[0].function_response.response
                print(f"-> {response}")

                msg = types.Content(role='user', parts=[types.Part(function_response=res.parts[0].function_response)])
                messages.append(msg)


        if VERBOSE_FLAG_SET:
            print(f'User prompt: {user_prompt}')
            print(f'Prompt tokens: {resp.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {resp.usage_metadata.candidates_token_count}')

        if resp.text and not resp.function_calls: # no more work to perform.
            break


if __name__ == "__main__":
    main()
