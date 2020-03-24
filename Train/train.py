#!/usr/bin/env python

from subprocess import call
from os.path import isfile
import os, math

from optparse import OptionParser
from ROOT import TMVA, TFile, TCut

TreeMaker = '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/'

import sys
sys.path.append(TreeMaker)
import common as c

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Train BDT with TMVA"

    parser = OptionParser(usage)
    parser.add_option("-m","--mva",default="TOPJETSPL",help="MVA name to train [default: %default]")
    parser.add_option("-t","--train",default=0.8,help="fraction of input data to be used for training [default: %default]")
    parser.add_option("-c","--chan",default="muon",help="lepton type [default: %default]")
    parser.add_option("-p","--path",default="jobs",help="output path [default: %default]")
    parser.add_option("-i","--input",default="train.root",help="input file name [default: %default]")
    parser.add_option("-d","--definition",default="cuts100_depth3_trees100_shrinkage0p1",help="BDT definition [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()

    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()

    output = TFile.Open(options.path+'/output.root', 'RECREATE')
    
    factory = TMVA.Factory('TMVAClassification', 
                           output,
                           '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

    data = TFile.Open(TreeMaker+options.input)
    signal = data.Get(options.chan+'Prompt')
    background = data.Get(options.chan+'NonPrompt')
    
    nSignal = signal.GetEntries()
    nBackground = background.GetEntries()

    chan = options.chan.capitalize()
    mva = options.mva
    
    os.chdir(options.path)
    
    dataloader = TMVA.DataLoader('dataset')
    for k, v in c.var[chan][mva].iteritems():
        dataloader.AddVariable(c.var[chan][mva][k], 'F')

    dataloader.AddSignalTree(signal, 1.0)
    dataloader.AddBackgroundTree(background, 1.0)

    sigTrain = math.floor(float(options.train)*float(nSignal))
    bkgTrain = math.floor(float(options.train)*float(nBackground))

    sigTest = math.floor((1-float(options.train))*float(nSignal))
    bkgTest = math.floor((1-float(options.train))*float(nBackground))

    print 'sig = ', nSignal, ' bkg = ', nBackground
    print 'sigTrain =', sigTrain, ' bkgTrain =', bkgTrain
    print 'sigTest =', sigTest, ' bkgTest =', bkgTest

    dataloader.PrepareTrainingAndTestTree(TCut(''),
                                          'nTrain_Signal='+str(sigTrain)+\
                                          ':nTrain_Background='+str(bkgTrain)+\
                                          ':nTest_Signal='+str(sigTest)+\
                                          ':nTest_Background='+str(bkgTest)+\
                                          ':SplitMode=Random:NormMode=None:!V')

    opt = options.definition.split('_')
    
    cuts = [s for s in opt if 'cuts' in s]
    trees = [s for s in opt if 'trees' in s]
    depth = [s for s in opt if 'depth' in s]
    shrinkage = [s for s in opt if 'shrinkage' in s]
    
    if len(cuts) == 0: print 'No cuts specified'
    else: cutsOpt = cuts[0].replace('cuts','')
    if len(trees) == 0: print 'No trees specified'
    else: treesOpt = trees[0].replace('trees','')
    if len(depth) == 0: print 'No depth specified'
    else: depthOpt = depth[0].replace('depth','')
    if len(shrinkage) == 0: print 'No shrinkage specified'
    else: 
        shrinkageOpt = shrinkage[0].replace('p','.') if 'p' in shrinkage[0] else shrinkage[0]
        shrinkageOpt = shrinkageOpt.replace('shrinkage','') 
    
    print '-----------------------------------'
    print 'Run MVA training with:'
    print '        cuts = ', cutsOpt
    print '        trees = ', treesOpt
    print '        depth = ', depthOpt
    print '        shrinkage = ', shrinkageOpt
    print '-----------------------------------'
                                          
    factory.BookMethod(dataloader,
                       TMVA.Types.kBDT,
                       'BDTG_'+options.definition+'_'+options.chan,
                       '!H:!V:NTrees='+str(treesOpt)+':MinNodeSize=2.5%:BoostType=Grad:Shrinkage='+str(shrinkageOpt)+':nCuts='+str(cutsOpt)+':MaxDepth='+str(depthOpt)+':IgnoreNegWeightsInTraining:UseBaggedBoost=True:DoBoostMonitor=True');

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()    
