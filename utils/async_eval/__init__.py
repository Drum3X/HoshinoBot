#python modules
from asyncio import wait_for, exceptions
from io import StringIO
from contextlib import redirect_stdout
from textwrap import indent

async def async_eval(
    code: str, 
    env: dict = {},
    timeout: float = 60.0
):
    stdout = StringIO()
    
    try:
        with redirect_stdout(stdout):
            exec(
                f"async def function():\n{indent(code, '    ')}", 
                env
            )    
            await wait_for(env["function"](), timeout = timeout)
            
        dict = {
            "error": False, 
            "output": stdout.getvalue()
        }        
               
    except Exception as err:
        if isinstance(err, exceptions.TimeoutError):
            raise err
            
        dict = {
            "error": True, 
            "output": err
        }
        
    return dict    