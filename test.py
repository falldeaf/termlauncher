

import asyncio

async def get_console_output(command: str) -> None:
	try:
		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()
		print(output)
		print(stderr)
	except asyncio.exceptions.CancelledError as e:
		print("cancelled: " + str(e))
		print(stderr)
		return

async def main():
	await get_console_output("dir")

asyncio.run(main())