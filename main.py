import argparse
import os
import sys
import uuid
from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def get_client_and_model():
    load_dotenv()
    provider = (os.environ.get("LLM_PROVIDER") or "openrouter").lower().strip()

    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY not found. Create one at https://openrouter.ai/keys "
                "and put it in .env as OPENROUTER_API_KEY='your_key_here'"
            )
        base_url = "https://openrouter.ai/api/v1"
        model = os.environ.get("OPENROUTER_MODEL") or "openrouter/free"
        extra_headers = None
    elif provider in ("opencode-go", "opencode_go", "go"):
        api_key = os.environ.get("OPENCODE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENCODE_API_KEY not found. Copy it from https://opencode.ai/console "
                "(Go subscription) and put it in .env as OPENCODE_API_KEY='your_key_here'"
            )
        base_url = "https://opencode.ai/inference/go/openai/v1"
        model = os.environ.get("OPENCODE_MODEL") or "muse-spark-1.3-contributor"
        extra_headers = {"x-opencode-session": f"ses_{uuid.uuid4().hex}"}
    elif provider == "opencode":
        api_key = os.environ.get("OPENCODE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENCODE_API_KEY not found. Copy it from https://opencode.ai/console "
                "and put it in .env as OPENCODE_API_KEY='your_key_here'"
            )
        base_url = "https://opencode.ai/inference/openai/v1"
        model = os.environ.get("OPENCODE_MODEL") or "muse-spark-1.3-contributor"
        extra_headers = {"x-opencode-session": f"ses_{uuid.uuid4().hex}"}
    else:
        raise RuntimeError(
            f'Unknown LLM_PROVIDER={provider!r}. Use "openrouter", "opencode-go", or "opencode".'
        )

    return OpenAI(base_url=base_url, api_key=api_key), model, extra_headers


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    load_dotenv()
    client, model, extra_headers = get_client_and_model()

    for _ in range(20):
        kwargs = {"model": model, "messages": messages}
        if extra_headers:
            kwargs["extra_headers"] = extra_headers
        response = client.chat.completions.create(
            **kwargs,
            tools=available_functions,
            temperature=0,
        )

        if response.usage is None:
            raise RuntimeError("API request failed: response.usage is None")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                if not result_message.get("content"):
                    raise Exception("Function call returned no content")
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            break
    else:
        print("Max iterations reached without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
