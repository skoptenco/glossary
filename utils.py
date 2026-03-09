from typing import Any

def concat_objects(obj1: Any, obj2: Any) -> Any:
    for key, value in obj2:
        obj1[key] = value
    return obj1