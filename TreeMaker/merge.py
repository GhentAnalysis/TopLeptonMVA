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

    usage = "usage: %prog [options]\n Script to merge output trees"

    parser = OptionParser(usage)
    parser.add_option("-f","--files",default="info.xml",help="input xml file list [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    xmlTree = ET.parse(options.files)

    prompt = []
    nonprompt = []

    print 'Merge and trim per dataset:\n'
    for s in xmlTree.findall('sample'):
        
        sname = s.get('id')
        ssig = s.get('sig')
        
        if ssig not in ['prompt','nonprompt']:
            continue
        
        sys.stdout.write(sname)
        
        tr = []
        for ch in s:
            tr.append(ch.text)
        outdir = tr[0].replace(sname,' ').split()[0]
        filestomerge = ' '.join(tr)
        outfile = outdir+sname+'/merged.root'

        col = ''
        if ssig == 'prompt':
            prompt.append(outfile)
            col = '\033[1;31m'
        elif ssig == 'nonprompt':
            nonprompt.append(outfile)
            col = '\033[1;34m'
            
        sys.stdout.write(col+' --> '+ssig+'\033[0;0m\n')
        
        os.system('hadd -f '+outfile+' '+filestomerge+' > /dev/null')
        f = ROOT.TFile(outfile,"UPDATE")
        if ssig == 'prompt':
            ROOT.gDirectory.Delete("elecNonPrompt;*")
            ROOT.gDirectory.Delete("muonNonPrompt;*")
            nElecPrompt = f.Get('elecPrompt').GetEntries()
            nMuonPrompt = f.Get('muonPrompt').GetEntries()
            print 'nElecPrompt=\033[;1m'+str(nElecPrompt)+'\033[0;0m nMuonPrompt=\033[;1m'+str(nMuonPrompt)+'\033[0;0m\n'
        else:
            ROOT.gDirectory.Delete("elecPrompt;*")
            ROOT.gDirectory.Delete("muonPrompt;*")            
            nElecNonPrompt = f.Get('elecNonPrompt').GetEntries()
            nMuonNonPrompt = f.Get('muonNonPrompt').GetEntries()
            print 'nElecNonPrompt=\033[;1m'+str(nElecNonPrompt)+'\033[0;0m nMuonNonPrompt=\033[;1m'+str(nMuonNonPrompt)+'\033[0;0m\n'
        f.Write()
        f.Close()
        sys.stdout.flush()

    print 'Merge datasets'
    for idx, s in enumerate([prompt,nonprompt]):
        filestomerge = ' '.join(s)
        if idx == 0: outfile = 'prompt.root'
        else: outfile = 'nonprompt.root'
        os.system('hadd -f '+outfile+' '+filestomerge+' > /dev/null')        
        for f in s:
            os.system('rm '+f)
        f = ROOT.TFile(outfile,"OPEN")
        if idx == 0: 
            nElecPrompt = f.Get('elecPrompt').GetEntries()
            nMuonPrompt = f.Get('muonPrompt').GetEntries()
            print 'nElecPrompt=\033[;1m'+str(nElecPrompt)+'\033[0;0m nMuonPrompt=\033[;1m'+str(nMuonPrompt)+'\033[0;0m'
        else:
            nElecNonPrompt = f.Get('elecNonPrompt').GetEntries()
            nMuonNonPrompt = f.Get('muonNonPrompt').GetEntries()
            print 'nElecNonPrompt=\033[;1m'+str(nElecNonPrompt)+'\033[0;0m nMuonNonPrompt=\033[;1m'+str(nMuonNonPrompt)+'\033[0;0m'

    os.system('hadd -f input.root prompt.root nonprompt.root > /dev/null')
    os.system('rm prompt.root nonprompt.root')
    
    print '\033[92mDone\033[0;0m'
