import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
	name="get_files_info",
	description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"directory": types.Schema(
				type=types.Type.STRING,
				description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
			),
		},
	),
)

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets the contents of a specified file and reads the file.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path to the file to read, relative to the working directory"
			),
		},
	),
)

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the file.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The path to the file to run, relative to the working directory"
                        ),
                },
        ),
)

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwites the file.",
        parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                        "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The path to the file to write, relative to the working directory"
                        ),
                        "content": types.Schema(
                                type=types.Type.STRING,
                                description="The content to write to the file"
			),
                },
        ),
)
def get_files_info(working_directory, directory="."):
	full_path = os.path.join(working_directory, directory)
	if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	if not os.path.isdir(full_path):
		return f'Error: "{directory}" is not a directory'
	try:
		directory_contents_list = os.listdir(full_path)
		total = ""
		for file in directory_contents_list:
			file_fullpath = os.path.join(full_path, file)
			file_size = os.path.getsize(file_fullpath)
			is_dir = os.path.isdir(file_fullpath)
			total += f' - {file}: file_size={file_size} bytes, is_dir={is_dir}\n'
		return total
	except Exception as e:
		return f"Error: {str(e)}"

