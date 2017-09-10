#!/usr/bin/env python3
import core
input1 = input()
f = core.frequencyList(input1)
shift = core.sort(lambda a, b: a + b, range(26), range(26), f)
print(core.dictionaryFilter(lambda x, a, b: a*x + b,input1,zip([1]*26,shift)))
