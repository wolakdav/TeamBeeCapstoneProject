from .flagger import Flagger, Flags, flaggers

#Class that implements unopened door check:
#That is if the bus stopped but door hasn't been opened
class UnopenedDoor(Flagger):
	name = 'UnopenedDoor'

	def flag(self, data):
		"""
		Checks if bus had stopped but door haven't opened (perhaps no passengers getting on/off?).
		To check, we check door field:
		door: The number of times the door was opened at the stop.

		Args:
			data (Object): data row from full dataset fetched from the db

		Returns: 
			list: either empty or containing UNOPENED_DOOR Flag
		"""

	flag = []

	if('door' in data) and (data.door == 0):
		flag.append(Flags.UNOPENED_DOOR)

	return flag

flaggers.append(UnopenedDoor())