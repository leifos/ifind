__author__ = '2108535R'

file = open('../clean_log', 'r')
file_a = open('../clean_log_ordered', 'a')


switch = True

for line in file:
    split_log_line = line.split(" ")
    index = 0
    ordered_line = []

    for s in split_log_line:
        if s == 'SMOVE' and switch == True:
            beta_i = int(split_log_line[18])/int(split_log_line[16])
            beta = str(beta_i)

            file_a.write(split_log_line[4].rstrip('\n') + " ")
            file_a.write(split_log_line[index+1].rstrip('\n') + " ")
            file_a.write(split_log_line[16].rstrip('\n') + " ")
            file_a.write(split_log_line[18].rstrip('\n') + " ")
            file_a.write(beta.rstrip('\n') + " ")


            switch = False

        if s == 'MOVE' and switch == False:
            file_a.write(split_log_line[index+1])
            switch = True

        index += 1
