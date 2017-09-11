#!/usr/bin/env python3
import core, dictionary
input1 = input()
f = core.frequencyList(input1)
sortedShiftList = core.sortLinear(lambda x, a, b: a*x + b, input1, range(1,12), range(26), f)
print(dictionary.filterIgnoreSpace(lambda x, a, b: a*x + b,input1.replace(" ",""),sortedShiftList))
