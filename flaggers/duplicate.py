from .flagger import Flagger, Flags, flaggers

#Class implements duplicate check
class Duplicate(Flagger):
	name = 'Duplicate'

	def flag(self, row, data):
		"""
		Checks passed row/dict/object and passed full dataset, to see if there are duplicates.

		Args:
			row (Object): data row from full dataset fetched from the db
			data (Matrix/List of Objects): full dataset fetched from db

		Returns: 
			list: either empty or containing DUPLICATE Flag
		"""

		flag = []

		#Count number of occurances in the list, and if occurs more than once append Flag to flag list.
		if(data.count(row)) > 1:
			flag.append(Flags.DUPLICATE)

		return flag

flaggers.append(Duplicate())