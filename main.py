import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_files_info import schema_get_file_content
from functions.get_files_info import schema_run_python_file
from functions.get_files_info import schema_write_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

available_functions = types.Tool(
	function_declarations=[
		schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
	]
)

function_executor_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwite files
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
def generate_content(user_prompt, verbose):
	messages = [
		types.Content(role="user", parts=[types.Part(text=user_prompt)]),
	]
	for i in range(20):
		try:
			response = client.models.generate_content(
				model = 'gemini-2.0-flash-001', 
				contents = messages,
				config=types.GenerateContentConfig(
					tools=[available_functions], 
					system_instruction=system_prompt
				)
		)
			for candidate in response.candidates:
				messages.append(candidate.content)


			if "--verbose" in sys.argv:
				print(f"User prompt: {user_prompt}")
				print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
				print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

			if response.function_calls:
				for function_call_part in response.function_calls:
					function_call_result = call_function(function_call_part, verbose)
					messages.append(function_call_result)
			elif response.text:
				print(f"Final response:\n{response.text}")
				break
		except Exception as e: # This is the missing part!
                        print(f"An error occurred during agent execution: {e}")
                        break # As per lesson 2.2, handle errors and stop the loop
def call_function(function_call_part, verbose=False):
	function_name = function_call_part.name
	if verbose == True:
		print(f"Calling function: {function_name}({function_call_part.args})")
	else:
		print(f" - Calling function: {function_name}")
	try:
		function_to_call = function_executor_map[function_name]
		combined_args = function_call_part.args.copy()
		combined_args['working_directory'] = "./calculator"
		function_result = function_to_call(**combined_args)
		return types.Content(
	role="tool",
	parts=[
		types.Part.from_function_response(
			name=function_name,
			response={"result": function_result},
		)
	],
)

	except KeyError:
		return types.Content(
	role="tool",
	parts=[
	types.Part.from_function_response(
	name=function_name,
	response={"error": f"Unknown function: {function_name}"},
		)
	],
)

def main():
	if len(sys.argv) > 1:
		is_verbose = False
		if "--verbose" in sys.argv:
			is_verbose= True
		generate_content(sys.argv[1], is_verbose)
	else:
		print("error")
		sys.exit (1)



if __name__ == "__main__":
	main()

