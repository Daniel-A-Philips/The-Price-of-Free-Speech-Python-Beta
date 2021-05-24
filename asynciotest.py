import asyncio

async def count(d):
	for i in range(d,100):
		print(i)
		await asyncio.sleep(.005)

async def main():
	task1 = asyncio.create_task(count(10))
	task2 = asyncio.create_task(count(5))
	await task1
	await task2

def test():
	asyncio.run(main())

test()
