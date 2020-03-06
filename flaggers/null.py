from .flagger import Flagger, Flags, flaggers

#In Python there is no Null, but there is None, need to check individually for None and return particular flag num

class Null(Flagger):
  def flag(self, data):
    # DUDE YOUR DATA HAS A NULL IN IT!!!!
    return [Flags.CONTAINS_NULL]

  #Checks if service_date is Null
  def service_date(data)
  	return [Flags.SERVICE_DATE_NULL]

  #Checks if vehicle_number is Null
  def vehicle_number(data)
  	return [Flags.VEHICLE_NUMBER_NULL]

  #Checks if leave_time is Null
  def leave_time(data)
  	return [Flags.LEAVE_TIME_NULL]

  #Checks if train is Null
  def train(data)
  	return [Flags.TRAIN_NULL]

  #Checks if badge is Null
  def badge(data)
  	return [Flags.BADGE_NULL]

  #Checks if route_number is Null
  def route_number(data)
  	return [Flags.ROUTE_NUMBER_NULL]

  #Checks if direction is Null
  def direction(data)
  	return [Flags.DIRECTION_NULL]

  #Checks if service_key is Null
  def service_key(data)
  	return [Flags.SERVICE_KEY_NULL]

  #Checks if trip_number is Null
  def trip_number(data)
  	return [Flags.TRIP_NUMBER_NULL]

  #Checks if stop_time is Null
  def stop_time(data)
  	return [Flags.STOP_TIME_NULL]

  #Checks if arrive_time is Null
  def arrive_time(data)
  	return [Flags.ARRIVE_TIME_NULL]

  #Checks if dwell is Null
  def dwell(data)
  	return [Flags.DWELL_NULL]

  #Checks if location_id is Null
  def location_id(data)
  	return [Flags.LOCATION_ID_NULL]

  #Checks if door is Null
  def door(data)
  	return [Flags.DOOR_NULL]

  #Checks if ons is Null
  def ons(data)
  	return [Flags.ONS_NULL]

  #Checks if offs is Null
  def offs(data)
  	return [Flags.OFFS_NULL]

  #Checks if estimated_load is Null
  def estimated_load(data)
  	return [Flags.ESTIMATED_LOAD_NULL]

  #Checks if lift is Null
  def lift(data)
  	return [Flags.LIFT_NULL]

  #Checks if maximum_speed is Null
  def maximum_speed(data)
  	return [Flags.MAXIMUM_SPEED_NULL]

  #Checks if train_mileage is Null
  def train_mileage(data)
  	return [Flags.TRAIN_MILEAGE_NULL]

  #Checks if pattern_distance is Null
  def pattern_distance(data)
  	return [Flags.PATTERN_DISTANCE_NULL]

  #Checks if location_distance is Null
  def location_distance(data)
  	return [Flags.LOCATION_DISTANCE_NULL]

  #Checks if x_coordinate is Null
  def x_coordinate(data)
  	return [Flags.X_COORDINATE_NULL]

  #Checks if y_coordinate is Null
  def y_coordinate(data)
  	return [Flags.Y_COORDINATE_NULL]

  #Checks if data_source is Null
  def data_source(data)
  	return [Flags.DATA_SOURCE_NULL]

  #Checks if schedule_status is Null
  def schedule_status(data)
  	return [Flags.SCHEDULE_STATUS_NULL]

  #Checks if trip_id is Null
  def trip_id(data)
  	return [Flags.TRIP_ID_NULL]
     
flaggers.append(Null())
