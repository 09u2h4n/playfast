import time
from functools import wraps
from fastapi.responses import JSONResponse

def dummy_function():
    return {"key1":"value1", "key2":"value2", "key3":"value3", "key4":"value4", "key5":"value5"}

def measure_time():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            if isinstance(result, dict):
                result['execution_time'] = f"{execution_time:.4f} seconds"
            else:
                return JSONResponse(content={
                    "result": result,
                    "execution_time": f"{execution_time:.4f} seconds"
                })
            
            return result
        return wrapper
    return decorator