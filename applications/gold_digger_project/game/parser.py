__author__ = '2108535R'

### PARSER V.1 ############################################################

# file = open('../clean_log', 'r')
# file_a = open('../clean_log_ordered', 'a')
#
#
# switch = True
#
# for line in file:
#     split_log_line = line.split(" ")
#     index = 0
#     ordered_line = []
#
#     for s in split_log_line:
#         if s == 'SMOVE' and switch == True:
#             beta_i = int(split_log_line[18])/int(split_log_line[16])
#             beta = str(beta_i)
#
#             file_a.write(split_log_line[4].rstrip('\n') + " ")
#             file_a.write(split_log_line[index+1].rstrip('\n') + " ")
#             file_a.write(split_log_line[16].rstrip('\n') + " ")
#             file_a.write(split_log_line[18].rstrip('\n') + " ")
#             file_a.write(beta.rstrip('\n') + " ")
#
#
#             switch = False
#
#         if s == 'MOVE' and switch == False:
#             file_a.write(split_log_line[index+1])
#             switch = True
#
#         index += 1

### PARSER V.2 ############################################################

"""
This parser extracts data from the log file. The Log file has already been sorted and trimmed
using 'grep' and 'sort' statements in a linux based terminal.
"""

# Open file for editing
file = open('../log_NLOC2', 'r')
# Append to file
file_a = open('../ordered_log_NLOC', 'a')
loc = ''

# The 'switch' variable is used to determine whether to a SMOVE value (when the user should move)
# corresponds a MOVE value (when the user did actually move). The lines containing SMOVE which are not
# followed by a MOVE are not printed to the file.
switch = True

#read every line from the file
for line in file:
    # Split the line using spaces as delimiter
    split_log_line = line.split(" ")
    index = 0

    for s in split_log_line:

        # Extract the value of the scanning equipment
        if s == 'SCAN':
            loc = split_log_line[index+1]

        # If SMOVE is found, harvest the appropriate data from the line
        if s == 'SMOVE' and switch is True:
            beta_i = int(split_log_line[18])/int(split_log_line[16])    # calculate beta (move cost / dig cost)
            beta = str(beta_i)
                                                                        # Append to file:
            file_a.write(split_log_line[4].rstrip('\n') + " ")          # - user
            file_a.write(split_log_line[index+1].rstrip('\n') + " ")    # - SMOVE
            file_a.write(split_log_line[16].rstrip('\n') + " ")         # - dig cost
            file_a.write(split_log_line[18].rstrip('\n') + " ")         # - move cost
            file_a.write(beta.rstrip('\n') + " ")                       # - beta
            file_a.write(loc.rstrip('\n') + " ")                        # - scanning equipment
            file_a.write(split_log_line[8].rstrip('\n') + " ")          # - mine number
            switch = False

        if s == 'MOVE' and switch is False:
            file_a.write(split_log_line[index+1])                       # - MOVE
            switch = True

        index += 1
