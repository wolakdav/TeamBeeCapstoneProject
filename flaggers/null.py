from .flagger import Flagger, Flags, flaggers

#data is a row of data from the db: parsed JSON
class Null(Flagger):
  def flag(self, data):
    #all null flags will be appended to the list
    null_flags = []

    #Checks if service_date is Null
    if data["service_date"] is None: 
      null_flags.append(Flags.SERVICE_DATE_NULL)

    #Checks if vehicle_number is Null
    if data["vehicle_number"] is None:
      null_flags.append(Flags.VEHICLE_NUMBER_NULL)

    #Checks if leave_time is Null
    if data["leave_time"] is None:
      null_flags.append(Flags.LEAVE_TIME_NULL)

    #Checks if train is Null
    if data["train"] is None:
      null_flags.append(Flags.TRAIN_NULL)

    #Checks if badge is Null
    if data["badge"] is None:
      null_flags.append(Flags.BADGE_NULL)

    #Checks if route_number is Null
    if data["route_number"] is None:
      null_flags.append(Flags.ROUTE_NUMBER_NULL)

    #Checks if direction is Null
    if data["direction"] is None:
      null_flags.append(Flags.DIRECTION_NULL)

    #Checks if service_key is Null
    if data["service_key"] is None:
      null_flags.append(Flags.SERVICE_KEY_NULL)

    #Checks if trip_number is Null
    if data["trip_number"] is None:
      null_flags.append(Flags.TRIP_NUMBER_NULL)

    #Checks if stop_time is Null
    if data["stop_time"] is None:
      null_flags.append(Flags.STOP_TIME_NULL)

    #Checks if arrive_time is Null
    if data["arrive_time"] is None:
      null_flags.append(Flags.ARRIVE_TIME_NULL)

    #Checks if dwell is Null
    if data["dwell"] is None:
      null_flags.append(Flags.DWELL_NULL)

    #Checks if location_id is Null
    if data["location_id"] is None:
      null_flags.append(Flags.LOCATION_ID_NULL)

    #Checks if door is Null
    if data["door"] is None:
      null_flags.append(Flags.DOOR_NULL)

    #Checks if ons is Null
    if data["ons"] is None:
      null_flags.append(Flags.ONS_NULL)

    #Checks if offs is Null
    if data["offs"] is None:
      null_flags.append(Flags.OFFS_NULL)

    #Checks if estimated_load is Null
    if data["estimated_loan"] is None:
      null_flags.append(Flags.ESTIMATED_LOAD_NULL)

    #Checks if lift is Null
    if data["lift"] is None:
      null_flags.append(Flags.LIFT_NULL)

    #Checks if maximum_speed is Null
    if data["maximum_speed"] is None:
      null_flags.append(Flags.MAXIMUM_SPEED_NULL)

    #Checks if train_mileage is Null
    if data["train_mileage"] is None:
      null_flags.append(Flags.TRAIN_MILEAGE_NULL)

    #Checks if pattern_distance is Null
    if data["pattern_distance"] is None:
      null_flags.append(Flags.PATTERN_DISTANCE_NULL)

    #Checks if location_distance is Null
    if data["location_distance"] is None:
      null_flags.append(Flags.LOCATION_DISTANCE_NULL)

    #Checks if x_coordinate is Null
    if data["x_coordinate"] is None:
      null_flags.append(Flags.X_COORDINATE_NULL)

    #Checks if y_coordinate is Null
    if data["y_coordinate"] is None:
      null_flags.append(Flags.Y_COORDINATE_NULL)

    #Checks if data_source is Null
    if data["data_source"] is None:
      null_flags.append(Flags.DATA_SOURCE_NULL)

    #Checks if schedule_status is Null
    if data["schedule_status"] is None:
      null_flags.append(Flags.SCHEDULE_STATUS_NULL)

    #Checks if trip_id is Null
    if data["trip_id"] is None:
      null_flags.append(Flags.TRIP_ID_NULL)
     
flaggers.append(Null())
