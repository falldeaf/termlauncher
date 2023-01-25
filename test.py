import asyncio
import json

async def get_console_output() -> None:

	command = "Get-ChildItem -Path c:\project\* -Include *.py -Recurse -ErrorAction SilentlyContinue | Select-Object -First 10 @{Name='name';Expression={$_.Name}}, @{Name='action';Expression={'start explorer'}}, @{Name='description';Expression={'Open the folder in explorer'}} | ConvertTo-Json -Compress"

	process = await asyncio.create_subprocess_shell('powershell.exe -Command "' + command + '"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
	output, stderr = await process.communicate()
		
	if(stderr):
		print("command_error: " + str(stderr, 'utf-8'))
	else:
		print("command_output: " + str(output, 'utf-8'))

	try:
		current_object = json.loads(str(output, 'utf-8'))
		#print(current_object)
	except json.decoder.JSONDecodeError as e:
		print(f'Error decoding JSON: {e}')
		return

	for i in range(len(current_object)):
		print(type(current_object[i]))
		print(current_object[i]['name'])
		#try: 
		#	print(current_object[i]['name'])
		#except Exception as e:
		#	# code that will be executed if any exception is raised
		#	print("Error: ", e)
		#	continue
	
asyncio.run(get_console_output())
