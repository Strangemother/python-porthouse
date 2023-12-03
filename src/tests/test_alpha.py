import asyncio
import pytest

from porthouse import run

@pytest.mark.asyncio
async def test_an_async_function():
    task =  run.main(await_task=False)
    print('Run task.', task)
    await task
    print('Ran task.', task)

    await asyncio.sleep(3)
    # result = await call_to_my_async_function()
    assert 1 == 1
