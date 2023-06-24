#python modules
import asyncio
from asyncio import run
from async_timeout import timeout
from io import StringIO
from contextlib import redirect_stdout
from textwrap import indent

async def async_eval(code: str, env: dict = {}):
        
    stdout = StringIO()
    
    try:
        with redirect_stdout(stdout):
            exec(
                f"async def func():\n{indent(code, '    ')}", 
                env
            )    
            
            await asyncio.wait_for(env["func"](), timeout=1)
            
            dict = {
                "error": 0, 
                "output": stdout.getvalue()
            }        
               
    except Exception as err:
        dict = {
            "error": 1, 
            "output": err
        }
        
    return dict  
    
res = run(async_eval("""
i = 1; 
while True: i = i + i
"""))
print(res)