import os
import sys
import math
from array import array
import utils
import common as c
import xgboost as xgb

mod = xgb.Booster()
mod.load_model('weights/elec2016.bin')

print 'test1:start'
for i in range(100000):
    data = [[eval('1') for v in c.variables]]
    x = xgb.DMatrix(data, feature_names=c.variables)
    mod.predict(x)
print 'test1:end'
print 'test2:start'
data = []
for i in range(100000):
    data.append([eval('1') for v in c.variables])
x = xgb.DMatrix(data, feature_names=c.variables)
print 'test2:end'
