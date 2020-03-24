#! /usr/bin/env python

import os, sys, math
import subprocess
import common as c
import xml.etree.ElementTree as ET
import json
import ROOT

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Script to create the list of output trees"

    parser = OptionParser(usage)
    parser.add_option("-d","--dir",default="jobs/",help="input directory with processed ntuples [default: %default]")
    parser.add_option("-s","--samples",default="samples.xml",help="list of samples [default: %default]")
    parser.add_option("-y","--year",default="2016",help="year of data taking [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    fout = open('info.xml',"w+")
    fout.write('<data>\n')

    samples = next(os.walk(options.dir))[1]
    
    submitList = eval('c.submit'+options.year)
    
    os.system('rm -f '+options.dir+'/*/merged*')
    
    print 'Getting info'
    for s in samples:
        found = False
        for s0, tag, sig, lep, process, channel, train, test in submitList:
            sname = s0+'_'+tag
            if sname == s:
                
                if train+test > 1.0:
                    print 'Requested train and test stats exceed the available data'
                    sys.exit()
                    
                found = True
                
                if sig == '': continue
                
                print sname
                
                filesTrain = []
                filesTest = []

                for r, d, f in os.walk(options.dir+s):
                    filesROOT = [x for x in f if 'root' in x]
                    files2train = int(math.ceil(train*len(filesROOT)))
                    for ff in range(files2train):
                        if '.root' in filesROOT[ff]:
                            fname = options.dir+s+'/'+filesROOT[ff]
                            filesTrain.append(fname)
                    files2test = int(math.ceil(test*len(filesROOT)))
                    testmax = files2train+files2test
                    if len(filesROOT) == 2: testmax += 1
                    if testmax > 0:
                        for ff in range(files2train,testmax-1):
                            if '.root' in filesROOT[ff]:
                                fname = options.dir+s+'/'+filesROOT[ff]
                                filesTest.append(fname)
                            
                elecPromptStatsTrain, elecNonPromptStatsTrain, muonPromptStatsTrain, muonNonPromptStatsTrain = 0, 0, 0, 0
                elecPromptStatsTest, elecNonPromptStatsTest, muonPromptStatsTest, muonNonPromptStatsTest = 0, 0, 0, 0
                
                filelistTrain = []
                for f in filesTrain:
                    inFile = ROOT.TFile.Open(f,"OPEN")
                    elecPromptStatsTrain += inFile.Get('elecPrompt').GetEntries()
                    elecNonPromptStatsTrain += inFile.Get('elecNonPrompt').GetEntries()
                    muonPromptStatsTrain += inFile.Get('muonPrompt').GetEntries()
                    muonNonPromptStatsTrain += inFile.Get('muonNonPrompt').GetEntries()
                    filelistTrain.append('        <file>'+f+'</file>\n')

                filelistTest = []
                for f in filesTest:
                    inFile = ROOT.TFile.Open(f,"OPEN")
                    elecPromptStatsTest += inFile.Get('elecPrompt').GetEntries()
                    elecNonPromptStatsTest += inFile.Get('elecNonPrompt').GetEntries()
                    muonPromptStatsTest += inFile.Get('muonPrompt').GetEntries()
                    muonNonPromptStatsTest += inFile.Get('muonNonPrompt').GetEntries()
                    filelistTest.append('        <file>'+f+'</file>\n')

                if len(filelistTrain) > 0:
                    fout.write('    <sample id="'+s+'" sig="'+sig+'" lep="'+lep+'" elecPrompt="'+str(elecPromptStatsTrain)+'" elecNonPrompt="'+str(elecNonPromptStatsTrain)+'" muonPrompt="'+str(muonPromptStatsTrain)+'" muonNonPrompt="'+str(muonNonPromptStatsTrain)+'" process="'+process+'" channel="'+channel+'" target="train">\n')
                    for f in filelistTrain:
                        fout.write(f)                    
                    fout.write('    </sample>\n')

                if len(filelistTest) > 0:
                    fout.write('    <sample id="'+s+'" sig="'+sig+'" lep="'+lep+'" elecPrompt="'+str(elecPromptStatsTest)+'" elecNonPrompt="'+str(elecNonPromptStatsTest)+'" muonPrompt="'+str(muonPromptStatsTest)+'" muonNonPrompt="'+str(muonNonPromptStatsTest)+'" process="'+process+'" channel="'+channel+'" target="test">\n')
                    for f in filelistTest:
                        fout.write(f)                    
                    fout.write('    </sample>\n')
                
                print '>>> Train : elecPrompt=\033[;1m' + str(elecPromptStatsTrain) + '\033[0;0m elecNonPrompt=\033[;1m' + str(elecNonPromptStatsTrain) + '\033[0;0m muonPrompt=\033[;1m' + str(muonPromptStatsTrain) + '\033[0;0m muonNonPrompt=\033[;1m' + str(muonNonPromptStatsTrain) + '\033[0;0m'
                print '>>> Test  : elecPrompt=\033[;1m' + str(elecPromptStatsTest) + '\033[0;0m elecNonPrompt=\033[;1m' + str(elecNonPromptStatsTest) + '\033[0;0m muonPrompt=\033[;1m' + str(muonPromptStatsTest) + '\033[0;0m muonNonPrompt=\033[;1m' + str(muonNonPromptStatsTest) + '\033[0;0m'

        if not found:
            print 'Not found sample '+s
            exit

    fout.write('</data>\n')
    fout.close()
