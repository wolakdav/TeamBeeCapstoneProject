from .flagger import Flagger, Flags, flaggers

#data is a row of data from the db: parsed JSON
class Null(Flagger):
  name = 'Null'
  def flag(self, data):
    null_flags = []     #all null flags will be appended to the list

    #Checks if service_date is Null
    if (hasattr(data, "service_date") or 'service_date' in data) and data["service_date"] is None: 
      null_flags.append(Flags.SERVICE_DATE_NULL)

    #Checks if vehicle_number is Null
    if (hasattr(data, "vehicle_number") or 'vehicle_number' in data) and data["vehicle_number"] is None:
      null_flags.append(Flags.VEHICLE_NUMBER_NULL)

    #Checks if leave_time is Null
    if (hasattr(data, "leave_time") or 'leave_time' in data) and data["leave_time"] is None:
      null_flags.append(Flags.LEAVE_TIME_NULL)

    #Checks if train is Null
    if (hasattr(data, "train") or 'train' in data) and data["train"] is None:
      null_flags.append(Flags.TRAIN_NULL)

    #Checks if badge is Null
    if (hasattr(data, "badge") or 'badge' in data) and data["badge"] is None:
      null_flags.append(Flags.BADGE_NULL)

    #Checks if route_number is Null
    if (hasattr(data, "route_number") or 'route_number' in data) and data["route_number"] is None:
      null_flags.append(Flags.ROUTE_NUMBER_NULL)

    #Checks if direction is Null
    if (hasattr(data, "direction") or 'direction' in data) and data["direction"] is None:
      null_flags.append(Flags.DIRECTION_NULL)

    #Checks if service_key is Null
    if (hasattr(data, "service_key") or 'service_key' in data) and data["service_key"] is None:
      null_flags.append(Flags.SERVICE_KEY_NULL)

    #Checks if trip_number is Null
    if (hasattr(data, "trip_number") or 'trip_number' in data) and data["trip_number"] is None:
      null_flags.append(Flags.TRIP_NUMBER_NULL)

    #Checks if stop_time is Null
    if (hasattr(data, "stop_time") or 'stop_time' in data) and data["stop_time"] is None:
      null_flags.append(Flags.STOP_TIME_NULL)

    #Checks if arrive_time is Null
    if (hasattr(data, "arrive_time") or 'arrive_time' in data) and data["arrive_time"] is None:
      null_flags.append(Flags.ARRIVE_TIME_NULL)

    #Checks if dwell is Null
    if (hasattr(data, "dwell")or 'dwell' in data) and data["dwell"] is None:
      null_flags.append(Flags.DWELL_NULL)

    #Checks if location_id is Null
    if (hasattr(data, "location_id") or 'location_id' in data) and data["location_id"] is None:
      null_flags.append(Flags.LOCATION_ID_NULL)

    #Checks if door is Null
    if (hasattr(data, "door") or 'door' in data) and data["door"] is None:
      null_flags.append(Flags.DOOR_NULL)

    #Checks if ons is Null
    if (hasattr(data, "ons") or 'ons' in data) and data["ons"] is None:
      null_flags.append(Flags.ONS_NULL)

    #Checks if offs is Null
    if (hasattr(data, "offs") or 'offs' in data) and data["offs"] is None:
      null_flags.append(Flags.OFFS_NULL)

    #Checks if estimated_load is Null
    if (hasattr(data, "estimated_load") or 'estimated_load' in data) and data["estimated_load"] is None:
      null_flags.append(Flags.ESTIMATED_LOAD_NULL)

    #Checks if lift is Null
    if (hasattr(data, "lift") or 'lift' in data) and data["lift"] is None:
      null_flags.append(Flags.LIFT_NULL)

    #Checks if maximum_speed is Null
    if (hasattr(data, "maximum_speed") or 'maximum_speed' in data) and data["maximum_speed"] is None:
      null_flags.append(Flags.MAXIMUM_SPEED_NULL)

    #Checks if train_mileage is Null
    if (hasattr(data, "train_mileage") or 'train_mileage' in data) and data["train_mileage"] is None:
      null_flags.append(Flags.TRAIN_MILEAGE_NULL)

    #Checks if pattern_distance is Null
    if (hasattr(data, "pattern_distance") or 'pattern_distance' in data) and data["pattern_distance"] is None:
      null_flags.append(Flags.PATTERN_DISTANCE_NULL)

    #Checks if location_distance is Null
    if (hasattr(data, "location_distance") or 'location_distance' in data) and data["location_distance"] is None:
      null_flags.append(Flags.LOCATION_DISTANCE_NULL)

    #Checks if x_coordinate is Null
    if (hasattr(data, "x_coordinate") or 'x_coordinate' in data) and data["x_coordinate"] is None:
      null_flags.append(Flags.X_COORDINATE_NULL)

    #Checks if y_coordinate is Null
    if (hasattr(data, "y_coordinate") or 'y_coordinate' in data) and data["y_coordinate"] is None:
      null_flags.append(Flags.Y_COORDINATE_NULL)

    #Checks if data_source is Null
    if (hasattr(data, "data_source") or 'data_source' in data) and data["data_source"] is None:
      null_flags.append(Flags.DATA_SOURCE_NULL)

    #Checks if schedule_status is Null
    if (hasattr(data, "schedule_status") or 'schedule_status' in data) and data["schedule_status"] is None:
      null_flags.append(Flags.SCHEDULE_STATUS_NULL)

    #Checks if trip_id is Null
    if (hasattr(data, "trip_id") or 'trip_id' in data) and data["trip_id"] is None:
      null_flags.append(Flags.TRIP_ID_NULL)
     
flaggers.append(Null())
