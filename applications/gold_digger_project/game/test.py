from yieldgen import RandomYieldGenerator, ConstantYieldGenerator, LinearYieldGenerator
from mine import Mine
import pickle


# gen = ConstantYieldGenerator(depth=10, max=42, min=0)
# m = Mine(gen, 0.8)
#
# a = m.blocks
#
# for al in a:
#     print al
#
#
# file_Name = "testfile"
# # open the file for writing
# fileObject = open(file_Name, 'wb')
#
# # this writes the object a to the
# # file named 'testfile'
# pickle.dump(a, fileObject)
#
# # here we close the fileObject
# fileObject.close()
# # we open the file for reading
# fileObject = open(file_Name, 'r')
# # load the object from the file into var b
# b = pickle.load(fileObject)
# print "------------------"
# for bl in b:
#     print bl
#
# if a == b:
#     print "a and b are equal"
# else:
#     print "a and b are different"
# import random
# a =26
# b =34
# c = 6
#
# cue_range = []
#
# r = random.randint(a,b)
#
# print r
#
# gold = 30
# span = 4
# upper_limit = gold+span
# lower_limit = gold-span
# print upper_limit
# print lower_limit
#
# cue = random.randint(lower_limit, upper_limit)
#
# print cue
#
# for x in range(c):
#     cue_range.append(a)
#     print x
#
# array = Yieldgen.constant_yield(10)
#
# print "Yield array"
#
# for c in array:
#     print c
#
# arraycue = Cuegen.make_cue(array, 0.8)
#
# print "arraycue"
#
# for p in arraycue:
#     print p
#
#
# yield_array = Yi
# accuracy = [0.8, 0.6, 0.4, 0.3, 0.2]
#
# for a in accuracy:
#     span = Cuegen.cue_function(a)
#     upper_limit = yield_array[0]+span
#     lower_limit = yield_array[0]-span
#
#     Cuegen.make_cue(yield_array, a)
#
#     print "-----------"
#     print span
#     print "-----------"
#     print upper_limit
#     print lower_limit


#array = [25, 25, 25, 25, 25, 25, 25, 25]
#c = Cuegen.make_cue(array, 0.9)
#print c


#max = 10
#for d in range(max, 0):
#    print d


### CUETEST #####################################

# max = yieldgen.b
# rangecue = int(float(round(cuegen.cue_range)))
# patterns = cuegen.cue_patterns
#
# array_list = []
#
# count = 1
#
#
#
# for r in range(rangecue):
#     cue_list = []
#     array_list.append(cue_list)
#     if len(array_list) <= rangecue:
#         for x in range(max, 0, -1):
#             cue_list.append(x)
#
#             if count == rangecue:
#                 count = 1
#                 max -= rangecue
#                 break
#             else:
#                 count += 1
#
# print rangecue
#
# array_list.remove([])
# a = array_list[patterns-1]
# a.append(0)
# print a
# print array_list
#
import random
# from random import shuffle
# mine_list = ['co', 'ra', 'qu', 'ex', 'cu', 'li']
# shuffle(mine_list)
#
# # a = random.choice(mine_list)
# print mine_list

#BEGINNING#######################################

# users = []
#
# file = open('../log_file.log')
#
#
#
# for line in file:
#
#     a = line.split(" ")
#     count = 0
#     for token in a:
#         if token == "USER":
#             user = a[count+1]
#
#             if user not in users:
#                 users.append(user)
#
#         else:
#             count += 1
# print users
# print len(users)


# for u in users:
#     file = open('../log_file.log')
#     log = open("../users_log/"+u+".txt", "w")
#     for linea in file:
#         if u in linea:
#             log.write(linea)
#
#     log.close()
#
# print "--------------------- SMOVE -------------------------"
#
# for u in users:
#     print u, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#     log = open("../users_log/"+u+".txt", "r")
#     log_a = open("../user_performance/"+u+".txt", "a")
#     checking = False
#     for line in log:
#
#         a = line.split(" ")
#         index = 0
#
#         for token in a:
#             if token == "SMOVE" and checking == True:
#                 log_a.write(" " + '\n')
#
#             if token == "SMOVE":
#                 smove = a[index+1]
#                 log_a.write(smove.rstrip('\n') + " ")
#                 checking = True
#
#
#             if token == "MOVE" and checking == True:
#                 move = a[index+1]
#                 log_a.write(move)
#                 checking = False
#
#             else:
#                 index += 1
#
# for u in users:
#     log_p = open("../user_performance/"+u+".txt", "r")
#     log_pw = open("../user_performance/"+u+"_clean.txt", "w")
#     print u, "USERRRRRRRRRRR"
#     for line in log_p:
#         l = line.split()
#         if len(l) == 2:
#
#               # TOGGLE FOR +1 ON MOVE
#             l[1] = int(l[1])
#             l[1] += 1
#             l[1] = str(l[1])
#             for token_l in l:
#                 log_pw.write(token_l + " ")

######################

# smove_arr = []
# move_arr = []
# for u in users:
#     log_pw = open("../user_performance/"+u+"_clean.txt", "r")
#     for line in log_pw:
#         l = line.split(" ")
#         index = 0
#         print u, "visited ", float(len(l)-1)/2, " mines"
#         for tok in l:
#             if index % 2 == 0 and tok != '':
#                 smove_arr.append(int(tok))
#                 index += 1
#             elif index % 2 != 0 and tok != '':
#                 move_arr.append(int(tok))
#                 index += 1
#
# print "smove: ", smove_arr
# print len(smove_arr)
# print "move: ", move_arr
# print len(move_arr)
#
# print " "
#
# print "sum smove ", sum(smove_arr)
# print "sum move ", sum(move_arr)
#
# print reduce(lambda x, y: x + y, smove_arr) / float(len(smove_arr))
# print reduce(lambda x, y: x + y, move_arr) / float(len(move_arr))
#
# diff_arr = []
# for i in range(len(smove_arr)):
#     diff = smove_arr[i] - move_arr[i]
#     diff_arr.append(diff)
#
# print reduce(lambda x, y: x + y, diff_arr) / float(len(diff_arr))
#
# for u in users:
#     log_pw = open("../user_performance/"+u+"_clean.txt", "r")
#     log_pw2 = open("../user_ordered/"+u+"_ordered.txt", "a")
#     for line in log_pw:
#         l = line.split(" ")
#         index = 0
#         for tok in l:
#             if index % 2 == 0 and tok != '':
#                 print tok,
#                 log_pw2.write(tok.rstrip('\n') + " ")
#                 index += 1
#             elif index % 2 != 0 and tok != '':
#                 print tok
#                 log_pw2.write(tok + '\n')
#                 index += 1

###############################################################################

# print a
# TO GET ARRAYS
#
# example = string[string.find("["):]
#
# print example
#
# trad = eval(example)
#
# print trad

class ModelTest(TestCase):

    user_info = {'username': 'guybrush',
                 'email': 'guy@monkey.island',
                 'password': 'secret'}


    def test_user_profile_data(self):
        """
        Check if UserProfile object is created with appropriate  data
        """

        new_user = User.objects.create_user(**self.user_info)
        user_profile = UserProfile()
        user_profile.user = new_user

        scan = ScanningEquipment.objects.get_or_create(name="Oil Lamp", modifier=0.2, image='icons/Scan/Oil Lamp.png', price=1, description="It won't allow you to see much but it's better than going in blind!", store_val=20)[0]
        dig = DiggingEquipment.objects.get_or_create(name='Spoon', modifier=0.3, time_modifier=5, image='icons/Tools/Spoon.png', price=1, description="What am I supposed to do with this?", store_val=30)[0]
        move = Vehicle.objects.get_or_create(name='Boots', modifier=10, image='icons/Vehicle/Boots.png', price=1, description="Two boots is better than no boots!")[0]
        user_profile.equipment = scan
        user_profile.tool = dig
        user_profile.vehicle = move

        self.assertEqual(user_profile.user.username, 'guybrush')
        self.assertEqual(new_user.email, 'guy@monkey.island')
        self.failUnless(new_user.check_password('secret'))
        self.failIf(not new_user.is_active)
        self.failIf(not user_profile.equipment)
        self.failIf(not user_profile.tool)
        self.failIf(not user_profile.vehicle)
        self.assertEqual(user_profile.gold, 100)
        self.assertEqual(user_profile.games_played, 0)
        self.assertEqual(user_profile.game_overs, 0)
        self.assertEqual(user_profile.mines, 0)

        user_profile.delete()