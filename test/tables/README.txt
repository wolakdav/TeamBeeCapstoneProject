
Be aware that Table is the ABC of these tests. Currently, Duplicated_Data,
Flagged_Data, and Flags all set the abstract member data and do not change
anything else. Since testing every method for all of them would be redundant,
Flags will be tested fully in their place. CTran_Data overrides a single
method, so that method will be tested in addition to the basic subclass test.
