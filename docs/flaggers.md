# Flags 

## Setup
To create a new flagger:
Copy the boilerplate class, change the class name, the name field, the flag
method, and add the class to the flaggers list. The flag class must return a 
list of flag, or an empty list.

## Flags
There are different types of flags used to represent different types of things 
present in a row data (object):

## Null Flags
Flag is turned on when particular field is None:

  - `ROW_ID_NULL`                         ['row_id' field is Null]
  - `SERVICE_DATE_NULL`                   ['service_date' field is Null]
  - `VEHICLE_NUMBER_NULL`                 ['vehicle_number' field is Null]
  - `LEAVE_TIME_NULL`                     ['leave_time' field is Null]
  - `TRAIN_NULL`                          ['train' field is Null]
  - `ROUTE_NUMBER_NULL`                   ['route_number' field is Null]
  - `DIRECTION_NULL`                      ['direction' field is Null]
  - `SERVICE_KEY_NULL`                    ['service_key' field is Null]
  - `TRIP_NUMBER_NULL`                    ['trip_number' field is Null]
  - `STOP_TIME_NULL`                      ['stop_time' field is Null]
  - `ARRIVE_TIME_NULL`                    ['arrive_time' field is Null]
  - `DWELL_NULL`                          ['dwell' field is Null]
  - `LOCATION_ID_NULL`                    ['location_id' field is Null]
  - `DOOR_NULL`                           ['door' field is Null]
  - `ONS_NULL`                            ['ons' field is Null]
  - `OFFS_NULL`                           ['offs' field is Null]
  - `ESTIMATED_LOAD_NULL`                 ['estimated_load' field is Null]
  - `LIFT_NULL`                           ['lift' field is Null]
  - `MAXIMUM_SPEED_NULL`                  ['maximum_speed' field is Null]
  - `TRAIN_MILEAGE_NULL`                  ['train_mileage' field is Null]
  - `PATTERN_DISTANCE_NULL`               ['pattern_distance' field is Null]
  - `LOCATION_DISTANCE_NULL`              ['location_distance' field is Null]
  - `X_COORDINATE_NULL`                   ['x_coordinate' field is Null]
  - `Y_COORDINATE_NULL`                   ['y_coordinate' field is Null]
  - `DATA_SOURCE_NULL`                    ['data_source' field is Null]
  - `SCHEDULE_STATUS_NULL`                ['schedule_status' field is Null]
  - `TRIP_ID_NULL`                        ['trip_id' field is Null]

## Unobserved stop Flag
Flag is turned on when bus stops at a certain distance away from the stop, meaning that bus stopped where it should not have stopped:

  - `UNOBSERVED_STOP`                     ['location_distance' is above some specific number (threshold)]

## Unopened door Flag
Flag is turned on when door is not opened during stop (perhaps no passengers getting on/off, or test drive of the bus, or any other reason):

  - `UNOPENED_DOOR`                       ['door' is 0 (door field specifies number of time door has been opened)]

## Duplicate Flag
Flag is turned on when there is a duplicate row exists in the dataset:

  - `DUPLICATE`                           [Checks full dataset for another identical row]
