## Config Usage (in Python)


### Config JSON file
Can set config data in a JSON file that is passed to the config.load() as the first parameter.

Any arbitrary variables can be set at the top level of the object. There is also a "columns" attribute that contains a column name, and a "max" and "min" that can be an integer, date, float, or "NA" if it is not bounded in that direction.

```
{
  "email": "test@test.com",
  "something_else" : "some_value", 
  "columns": {
    "vehicle_number": { "max": "NA", "min": 0 },
    "maximum_speed": { "max": 150, "min": 0 },
    "service_date": { "max": "NA", "min": "1990-01-01" }
  }
}
```


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
email = config.get_value('email')
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

#also works for dates
result = config.check_bounds('service_date', '1990-01-01')

```
