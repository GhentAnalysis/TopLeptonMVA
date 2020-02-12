#! /usr/bin/env python

import os
import sys
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
    parser.add_option("-o","--output",default="info.xml",help="output file name [default: %default]")
    parser.add_option("-s","--samples",default="samples.xml",help="list of samples [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    fout = open(options.output,"w+")
    fout.write('<data>\n')

    samples = next(os.walk(options.dir))[1]
    
    submitList = c.submit2016 + c.submit2017 + c.submit2018
    
    print 'Getting info'
    for s in samples:
        found = False
        for s0, tag, sig in submitList:
            sname = s0+'_'+tag
            if sname == s:
                print sname
                found = True
                files = []
                
                for r, d, f in os.walk(options.dir+'/'+s):
                    for file in f:
                        if '.root' in file:
                            fname = options.dir+'/'+s+'/'+file
                            files.append(home+'/'+fname)
                            
                fout.write('    <sample id="'+s+'" sig="'+sig+'">\n')
                elecPromptStats, elecNonPromptStats, muonPromptStats, muonNonPromptStats = 0, 0, 0, 0
                for f in files:
                    inFile = ROOT.TFile.Open(f,"OPEN")
                    elecPromptStats += inFile.Get('elecPrompt').GetEntries()
                    elecNonPromptStats += inFile.Get('elecNonPrompt').GetEntries()
                    muonPromptStats += inFile.Get('muonPrompt').GetEntries()
                    muonNonPromptStats += inFile.Get('muonNonPrompt').GetEntries()
                    fout.write('        <file>'+f+'</file>\n')
                fout.write('    </sample>\n')
                print '>>> elecPrompt=' + str(elecPromptStats) + ' elecNonPrompt=' + str(elecNonPromptStats) + ' muonPrompt=' + str(muonPromptStats) + ' muonNonPrompt=' + str(muonNonPromptStats)

        if not found and not isdata:
            print 'Not found sample '+s
            exit

    fout.write('</data>\n')
    fout.close()
