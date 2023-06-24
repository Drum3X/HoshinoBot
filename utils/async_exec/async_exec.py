#python modules
import asyncio
from asyncio import subprocess, create_subprocess_exec

async def async_exec(code: str):
    proc = await create_subprocess_exec(
        code,
        stderr = subprocess.PIPE,
        stdout = subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    
    dict = {
        "input": code,
        "output": stdout.decode("utf-8"),
        "error": stderr.decode("utf-8")
    }

    return dict

print(asyncio.run(async_exec("a")))