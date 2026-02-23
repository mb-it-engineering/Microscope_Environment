from fastapi import FastAPI, Body, HTTPException
from edge.simulation.microscope_environment import MicroscopeEnv

FUNCTION_REGISTRY = {}
app = FastAPI()
env = MicroscopeEnv()

def register(name):
    def decorator(func):
        FUNCTION_REGISTRY[name] = func
        return func
    return decorator

@register("capture")
def capture():
    img, metrics = env.capture()
    return {"image": img.tolist(), "metrics": metrics}

@register("set_parameter")
def set_parameter(name, value):
    env.set_parameter(name, value)
    return {"status": "ok"}

@register("get_parameters")
def get_parameters():
    return env.get_parameters()

@register("reset")
def reset():
    env.reset()
    return {"status": "ok"}

@app.post("/execute/{function_name}")
def execute_function(function_name: str, payload: dict = Body(default={})):
    if function_name not in FUNCTION_REGISTRY:
        raise HTTPException(status_code=404, detail="Function not found")
    
    func = FUNCTION_REGISTRY[function_name]
    try:
        result = func(**payload)
        return {"result": result}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")   
