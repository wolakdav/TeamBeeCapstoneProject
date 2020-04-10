## Usage (in Python)


### Load config
```
from config import config
from config import BoundsResult

config.load('path_to_config.json')
```

### Set value
```
try:
    user = os.environ["PIPELINE_USER"]
    config.set_value('user', user)
except KeyError as err:
    print("Could not read environment data.")
```

### Get value
```
email = config.get_value('email', email)
```

### Column bounds checking
```
result = config.check_bounds('id', 22)

if result == BoundsResult.VALID:
    print("it's valid!")
elif result == BoundsResult.MIN_ERROR:
    print("it's too low!")
elif result == BoundsResult.MAX_ERROR:
    print("it's too high!")
```

## Usage (Command Line)

(currently unclear what this is for)

```
$ python3 Config.py load

Loaded config data.
```
