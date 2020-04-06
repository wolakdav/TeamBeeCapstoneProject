from .flagger import Flagger, Flags, flaggers

#Class that implements unobserved stop check:
#That is is bus stops at a certain distance away from the stop, we mark it as an unobserved stop.
class UnobservedStop(Flagger):
	name = 'Unobserved Stop'

	def flag(self, data):
		"""Checks if stop happened at a certain distance away from the actual stop to mark it as an unobserved stop

		Args:
			data (Object): data row from full dataset fetched from the db

		Returns: 
			list: either empty or containing UNOBSERVED_FLAG 

		"""

		#maxDistance specifies max distance away from the stop at which we start marking stop as an unobserved
		#Instead of being hardcoded, in the future substitute to .env variable
		maxDistance = 50

		flag = []
		if ('location_distance' in data) and (data.location_distance > maxDistance):
			flag.append(Flags.UNOBSERVED_FLAG);
		return flag

flaggers.append(UnobservedStop())