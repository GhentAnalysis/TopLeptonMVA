import os
import sys
import math
from array import array
import utils
import common as c
import xgboost as xgb

class mva():

    def __init__(self, tree, model):

        self.isValid = False
        
        if model != '':
            
            self.mod = xgb.Booster()
            self.mod.load_model(model)
            self.isValid = True
            
    def predict(self, x):

        return self.mod.predict(x)
