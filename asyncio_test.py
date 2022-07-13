import asyncio

async def main():
    task = asyncio.create_task(second())
    print("Hi")
    await asyncio.sleep(1)
    print("Ho")
    return_value = await task
    print(return_value)

async def second():
    print("1")
    await asyncio.sleep(2)
    print("2")
    return 10

asyncio.run(main())
