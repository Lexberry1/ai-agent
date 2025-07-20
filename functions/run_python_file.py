import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
	joined_path = os.path.join(working_directory, file_path)
	if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	if not os.path.abspath(joined_path).endswith('.py'):
		return f'Error: "{file_path}" is not a Python file.'
	if not os.path.exists(joined_path):
		return f'Error: File "{file_path}" not found.'
	try:
		result = subprocess.run(['python', file_path] + args, capture_output=True, timeout=30, cwd=working_directory)
		stdout = f'STDOUT: {result.stdout.decode()}'
		stderr =f'STDERR: {result.stderr.decode()}'
		output = stdout + '\n' + stderr
		if not result.stdout.strip() and not result.stderr.strip():
			return f"No output produced."
		if result.returncode != 0:
			output +=  f'\nProcess exited with code {result.returncode}'
		return output
	except Exception as e:
		return f"Error: executing Python file: {e}"
