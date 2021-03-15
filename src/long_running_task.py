import time
from typing import Dict

def long_running_task() -> Dict[str, str]:
    time.sleep(10)
    return {
        "foo": "bar"
    }