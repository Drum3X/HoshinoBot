#python modules
from asyncio import wait_for, exceptions, subprocess, create_subprocess_shell

async def async_exec(
    code: str, 
    timeout: float = 60.0
):
    proc = await create_subprocess_shell(
        code,
        stderr = subprocess.PIPE,
        stdout = subprocess.PIPE
    )
    
    stdout, stderr = await wait_for(proc.communicate(), timeout = timeout)
    
    dict = {
        "return": proc.returncode,
        "output": stdout.decode("utf-8"),
        "error": stderr.decode("utf-8")
    }
    
    return dict