#!/usr/bin/env python3
import core
input1 = input()
f = core.frequencyList(input1)
sortedShiftList = core.sortLinear(lambda x, a, b: a*x + b, input1, range(1,26), range(26), f)
print(core.dictionaryFilter(lambda x, a, b: a*x + b,input1,sortedShiftList))