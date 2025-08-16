import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    # print(sys.argv)

    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

    if len(sys.argv) == 1:
        print('Should provide prompt as commandline argument')
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    VERBOSE_FLAG_SET = ('--verbose' in sys.argv)

    print(resp.text)
    if VERBOSE_FLAG_SET:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {resp.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {resp.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
