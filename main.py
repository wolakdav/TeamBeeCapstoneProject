from flaggers.flagger import flaggers

# These structures are only to demosntrate that flaggers work,
# and not a final say on what our data should look like.
data_dict = {"Placeholder" : [], "Data" : []}

<<<<<<< Updated upstream
# for data in data_dict.keys():
#   for flagger in flaggers:
#     flags = flagger.flag(data)
#     data_dict[data] += flags

# print(data_dict)

for flagger in flaggers: 
	print(flagger.name)

