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
from random import shuffle
mine_list = ['co', 'ra', 'qu', 'ex', 'cu', 'li']
shuffle(mine_list)

# a = random.choice(mine_list)
print mine_list