from .flagger import Flagger, Flags, flaggers

#Class implements duplicate check
class Duplicate(Flagger):
	name = 'Duplicate'

	def flag(self, row, data):
		"""
		Checks if bus had stopped but door haven't opened (perhaps no passengers getting on/off?).
		To check, we check door field:
		door: The number of times the door was opened at the stop.

		Args:
			row (Object): data row from full dataset fetched from the db
			data (Matrix/List of Objects): full dataset fetched from db

		Returns: 
			list: either empty or containing DUPLICATE Flag
		"""

		flag = []

		for dataRow in data:
			if(vars(row) == vars(dataRow)):
				flag.append(Flags.DUPLICATE)
				break	

		return flag

flaggers.append(Duplicate())