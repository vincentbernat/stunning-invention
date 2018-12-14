import pytest
import asyncio


@pytest.mark.asyncio
async def test_follow_inexistent(httpmonitor):
    with pytest.raises(RuntimeError):
        async for line in httpmonitor.follow_file("/i_should_not_exist"):
            assert line is None


@pytest.mark.asyncio
async def test_follow_existing(httpmonitor, tmpdir):
    queue = asyncio.Queue()
    logfile = tmpdir.join("log.txt")
    logfile.write("line 1\n", "w")

    async def follow():
        async for line in httpmonitor.follow_file(str(logfile.realpath())):
            await queue.put(line)

    asyncio.ensure_future(follow())
    await asyncio.sleep(1)      # let tail be ready
    logfile.write("line 2\n", "a")
    logfile.write("line 3\n", "a")
    first = await asyncio.wait_for(queue.get(), 1)
    assert first == "line 2\n"
    second = await asyncio.wait_for(queue.get(), 1)
    assert second == "line 3\n"


@pytest.mark.asyncio
async def test_follow_rotate(httpmonitor, tmpdir):
    queue = asyncio.Queue()
    logfile = tmpdir.join("log.txt")
    logfile.write("line 1\n", "w")

    async def follow():
        async for line in httpmonitor.follow_file(str(logfile.realpath())):
            await queue.put(line)

    asyncio.ensure_future(follow())
    await asyncio.sleep(1)      # let tail be ready
    logfile.write("line 2\n", "a")
    await asyncio.sleep(1)      # let tail catchup
    logfile.write("line 3\n", "w")
    first = await asyncio.wait_for(queue.get(), 1)
    assert first == "line 2\n"
    second = await asyncio.wait_for(queue.get(), 1)
    assert second == "line 3\n"
