## Usage (in Python)

Config file is set using an absolute path CONFIG_FILE in Config.py



```

from config import config
from config import BoundsResult

config.load()
result = config.check_bounds('id', 22)

if result == BoundsResult.VALID:
    print("it's valid!")
elif result == BoundsResult.MIN_ERROR:
    print("it's too low!")
elif result == BoundsResult.MAX_ERROR:
    print("it's too high!")
```