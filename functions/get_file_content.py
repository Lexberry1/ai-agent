import os
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
	joined_path = os.path.join(working_directory, file_path)
	if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	if not os.path.isfile(joined_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'
	try:
		with open(joined_path, "r") as f:
			chars = os.path.getsize(joined_path)
			file_content_string = f.read(MAX_CHARS)
			if chars > MAX_CHARS:
				total_string = file_content_string + f'[...File "{joined_path}" truncated at {MAX_CHARS} characters]'
				return total_string
			else:
				return file_content_string
	except Exception as e:
		return f"Error: {str(e)}"

