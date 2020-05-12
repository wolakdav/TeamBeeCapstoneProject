from .flagger import Flagger, Flags, flaggers

#data is a row of data from the db: parsed JSON
class Null(Flagger):
  name = 'Null'
  columns_flag_dict = {
    'row_id': Flags.ROW_ID_NULL,
    'service_date' : Flags.SERVICE_DATE_NULL,
    'vehicle_number' : Flags.VEHICLE_NUMBER_NULL,
    'leave_time' : Flags.LEAVE_TIME_NULL,
    'train' : Flags.TRAIN_NULL,
    'route_number' : Flags.ROUTE_NUMBER_NULL,
    'direction' : Flags.DIRECTION_NULL,
    'service_key' : Flags.SERVICE_KEY_NULL,
    'trip_number' : Flags.TRIP_NUMBER_NULL,
    'stop_time' : Flags.STOP_TIME_NULL,
    'arrive_time' : Flags.ARRIVE_TIME_NULL,
    'dwell' : Flags.DWELL_NULL,
    'location_id' : Flags.LOCATION_ID_NULL,
    'door' : Flags.DOOR_NULL,
    'ons' : Flags.ONS_NULL,
    'offs' : Flags.OFFS_NULL,
    'estimated_load' : Flags.ESTIMATED_LOAD_NULL,
    'lift' : Flags.LIFT_NULL,
    'maximum_speed' : Flags.MAXIMUM_SPEED_NULL,
    'train_mileage' : Flags.TRAIN_MILEAGE_NULL,
    'pattern_distance' : Flags.PATTERN_DISTANCE_NULL,
    'location_distance' : Flags.LOCATION_DISTANCE_NULL,
    'x_coordinate' : Flags.X_COORDINATE_NULL,
    'y_coordinate' : Flags.Y_COORDINATE_NULL,
    'data_source' : Flags.DATA_SOURCE_NULL,
    'schedule_status' : Flags.SCHEDULE_STATUS_NULL,
    'trip_id' : Flags.TRIP_ID_NULL
  }

  def flag(self, data):
    #all null flags will be appended to the list
    null_flags = []
    for col in self.columns_flag_dict:
      if (col in data) and (data[col] is None):
        null_flags.append(self.columns_flag_dict[col])

    return null_flags
     
flaggers.append(Null())
