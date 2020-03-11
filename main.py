from flaggers.flagger import flaggers
from flaggers.dataRow import dataRow

# These structures are only to demosntrate that flaggers work,
# and not a final say on what our data should look like.
data_dict = {"Placeholder" : [], "Data" : []}

# for data in data_dict.keys():
#   for flagger in flaggers:
#     flags = flagger.flag(data)
#     data_dict[data] += flags

# print(data_dict)

#Helper function that tests all Null flags individually (one at a time)
#@positive=true, tests so that flags 'fire'
#@positive=false, test so that flags don't 'fire'
def testNullFlagsIndividual(positive):
	corr_cnt = 0  #count for correct null flag checks
	inc_cnt = 0	  #count for incorrect null flag checks
	#Step 1: Transform Nulls class fields into dict, and then transform into keys and vals lists
	nulls = Nulls()  					#create Nulls object
	nulls_flags = vars(nulls)			#create dict from object
	flag_names = list(nulls_flags.keys())		#create keys list from dict
	flag_vals = list(nulls_flags.values())	#create vals list from dict

	#Step 2: Check for each flag and its value
	for i in range(len(nulls_flags)):
		if(positive): json_obj = '{"' + flag_names[i] + '":null}'	#create JSON object with 1 value: current flag
		else: json_obj = '{"' + flag_names[i] + '":"good"}'
		
		python_obj = json.loads(json_obj)				#create Python object from JSON object

		ret_flag = null_check(python_obj)		#check Python object with 1 value for a flag

		#Testing positive: should fire
		if(positive and len(ret_flag) > 0): 
			correct = ret_flag[0] == flag_vals[i]
			if(correct): corr_cnt += 1
			else: inc_cnt += 1
			#print('NULL CHECK -', flag_names[i], ':', correct)
		#Testing negative: shouldn't fire
		else:
			if(len(ret_flag) == 0): corr_cnt += 1
			else: inc_cnt += 1

	print('-------------------------------------------------------------------------------')
	if(positive): print('Testing INDIVIDUAL for Positives [null flags should fire = return null_flag]')
	else: print('Testing INDIVIDUAL for Negatives [null flags shouldn\'t fire = not return null flag]')
	print('Correct:', corr_cnt)
	print('Incorrect:', inc_cnt)
	print('Success Rate:', (corr_cnt / len(nulls_flags)) * 100, '%')
	print('-------------------------------------------------------------------------------')


#Tests full object (not one flag at a time)
def testNullFlagsFull(positive):
	#Step 1: Transform Nulls class fields into dict, and then transform into keys and vals lists
	nulls = Nulls()  					#create Nulls object
	nulls_vars = vars(nulls)			#create dict from object, to import all the fields
	flag_names = list(nulls_vars.keys())		#create keys list from dict
	flag_vals = list(nulls_vars.values())	#create vals list from dict
	incorrect = 0

	#positive = must return a list of flags
	if(positive):
		#Change every value in the nulls_vars to None (to return a flag)
		for i in range(len(flag_names)):
			nulls_vars[flag_names[i]] = None

		ret_flags = null_check(nulls_vars)
		if(len(ret_flags) == len(nulls_vars)): correct = len(ret_flags)
		else: incorrect = len(nulls_vars) - len(ret_flags)
	#Negative = must return empty list
	else: 
		ret_flags = null_check(nulls_vars)
		if(len(ret_flags) == 0): correct = len(nulls_vars)
		else: incorrect = len(null_vars) - len(ret_flags)

	print('-------------------------------------------------------------------------------')
	if(positive): print('Testing  FULL for Positives [null flags should fire = return ret_flag list]')
	else: print('Testing FULL for Negatives [null flags shouldn\'t fire = empty ret_flag list]')
	print('Correct:', correct)
	print('Incorrect:', incorrect)
	print('Success rate:', (correct / len(nulls_vars)) * 100, '%')
	print('-------------------------------------------------------------------------------')

def runNullTests():
	#Calling Individual test functions
	testNullFlagsIndividual(True)
	testNullFlagsIndividual(False)

	#Calling Full test functions
	testNullFlagsFull(True)
	testNullFlagsFull(False)

for flagger in flaggers:
	#currently on a null flagger
	#if(flagger.name == 'Null')

data = dataRow()

print(data)