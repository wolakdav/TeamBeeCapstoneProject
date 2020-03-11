from .flagger import Flagger, Flags, flaggers

class Invalid(Flagger):
	name = 'Invalid'
	def flag(data):
	# YOUR DATA IS PURE GARBAGE.
		return 1 
	#[Flags.INVALID]
     
#flaggers.append(Invalid())
