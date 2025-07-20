import os

def write_file(working_directory, file_path, content):

	total_path = os.path.join(working_directory, file_path)
	if not os.path.abspath(total_path).startswith(os.path.abspath(working_directory)):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	try:
		new_dir = os.path.dirname(total_path)
		os.makedirs(new_dir, exist_ok=True)
		with open(total_path, "w") as f:
			f.write(content)
			message = f'Successfully wrote to "{file_path}" ({len(content)} characters written)' 
			return message
	except Exception as e:
		return f"Error: {str(e)}"
