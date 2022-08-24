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
    parser.add_option("-d","--dir",default="jobs_train_UL17_all/",help="input directory with processed ntuples [default: %default]")
    parser.add_option("-s","--samples",default="samples_UL17.xml",help="list of samples [default: %default]")
    parser.add_option("-y","--year",default="2017",help="year of data taking [default: %default]")
    parser.add_option("--split", action="store_true", help="split into prompt and nonprompt trees [default: %default]")

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
                filesAll = []

                if options.split:
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
                else:
                    for r, d, f in os.walk(options.dir+s):
                        filesROOT = [x for x in f if 'root' in x]
                        for ff, fil in enumerate(filesROOT):
                            fname = options.dir+s+'/'+filesROOT[ff]
                            filesAll.append(fname)
                            
                elecPromptStatsTrain, elecNonPromptStatsTrain, muonPromptStatsTrain, muonNonPromptStatsTrain = 0, 0, 0, 0
                elecPromptStatsTest, elecNonPromptStatsTest, muonPromptStatsTest, muonNonPromptStatsTest = 0, 0, 0, 0
                elecAllStats, muonAllStats = 0, 0
                
                if options.split:
                    filelistTrain = []
                    for f in filesTrain:
                        inFile = ROOT.TFile.Open(f,"OPEN")
                        elecPromptStatsTrain += inFile.Get('elecPrompt').GetEntries()
                        elecNonPromptStatsTrain += inFile.Get('elecNonprompt').GetEntries()
                        muonPromptStatsTrain += inFile.Get('muonPrompt').GetEntries()
                        muonNonPromptStatsTrain += inFile.Get('muonNonprompt').GetEntries()
                        filelistTrain.append('        <file>'+home+'/'+f+'</file>\n')

                    filelistTest = []
                    for f in filesTest:
                        inFile = ROOT.TFile.Open(f,"OPEN")
                        elecPromptStatsTest += inFile.Get('elecPrompt').GetEntries()
                        elecNonPromptStatsTest += inFile.Get('elecNonprompt').GetEntries()
                        muonPromptStatsTest += inFile.Get('muonPrompt').GetEntries()
                        muonNonPromptStatsTest += inFile.Get('muonNonprompt').GetEntries()
                        filelistTest.append('        <file>'+home+'/'+f+'</file>\n')
                else:
                    filelistAll = []
                    for f in filesAll:
                        inFile = ROOT.TFile.Open(f,"OPEN")
                        elecAllStats += inFile.Get('elecAll').GetEntries()
                        muonAllStats += inFile.Get('muonAll').GetEntries()
                        filelistAll.append('        <file>'+home+'/'+f+'</file>\n')                    

                if options.split:
                    if len(filelistTrain) > 0:
                        fout.write('    <sample id="'+s+'" sig="'+sig+'" lep="'+lep+'" elecPrompt="'+str(elecPromptStatsTrain)+'" elecNonprompt="'+str(elecNonPromptStatsTrain)+'" muonPrompt="'+str(muonPromptStatsTrain)+'" muonNonprompt="'+str(muonNonPromptStatsTrain)+'" process="'+process+'" channel="'+channel+'" target="train">\n')
                        for f in filelistTrain:
                            fout.write(f)
                        fout.write('    </sample>\n')

                    if len(filelistTest) > 0:
                        fout.write('    <sample id="'+s+'" sig="'+sig+'" lep="'+lep+'" elecPrompt="'+str(elecPromptStatsTest)+'" elecNonprompt="'+str(elecNonPromptStatsTest)+'" muonPrompt="'+str(muonPromptStatsTest)+'" muonNonprompt="'+str(muonNonPromptStatsTest)+'" process="'+process+'" channel="'+channel+'" target="test">\n')
                        for f in filelistTest:
                            fout.write(f)
                        fout.write('    </sample>\n')
                else:
                    if len(filelistAll) > 0:
                        fout.write('    <sample id="'+s+'" sig="all" lep="'+lep+'" elec="'+str(elecAllStats)+'" muon="'+str(muonAllStats)+'" process="'+process+'" channel="'+channel+'" target="all">\n')
                        for f in filelistAll:
                            fout.write(f)
                        fout.write('    </sample>\n')
                        
                if options.split:
                    print '>>> Train : elecPrompt=\033[;1m' + str(elecPromptStatsTrain) + '\033[0;0m elecNonPrompt=\033[;1m' + str(elecNonPromptStatsTrain) + '\033[0;0m muonPrompt=\033[;1m' + str(muonPromptStatsTrain) + '\033[0;0m muonNonPrompt=\033[;1m' + str(muonNonPromptStatsTrain) + '\033[0;0m'
                    print '>>> Test  : elecPrompt=\033[;1m' + str(elecPromptStatsTest) + '\033[0;0m elecNonPrompt=\033[;1m' + str(elecNonPromptStatsTest) + '\033[0;0m muonPrompt=\033[;1m' + str(muonPromptStatsTest) + '\033[0;0m muonNonPrompt=\033[;1m' + str(muonNonPromptStatsTest) + '\033[0;0m'
                else: print '>>> elec=\033[;1m' + str(elecAllStats) + '\033[0;0m muon=\033[;1m' + str(muonAllStats) + '\033[0;0m'

        if not found:
            print 'Not found sample '+s
            continue

    fout.write('</data>\n')
    fout.close()
