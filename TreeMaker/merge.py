#! /usr/bin/env python

import os, sys
import subprocess
import common as c
import xml.etree.ElementTree as ET
import json
import ROOT

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Script to merge output trees"

    parser = OptionParser(usage)
    parser.add_option("--files", default="info.xml", help="input xml file list [default: %default]")
    parser.add_option("--dir", default="srm://maite.iihe.ac.be/pnfs/iihe/cms/store/user/kskovpen/TopLeptonMVATrain/", help="output directory for the merged file on pnfs [default: %default]")
    parser.add_option("--out", default="2017.root", help="output file name [default: %default]")
    parser.add_option("--year", default="2017", help="year of data taking [default: %default]")
    parser.add_option("--mode", default="train", help="only use for training or testing [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    xmlTree = ET.parse(options.files)

    promptTrain, promptProcTrain, promptTest, promptProcTest = [], [], [], []
    nonpromptTrain, nonpromptProcTrain, nonpromptTest, nonpromptProcTest = [], [], [], []

    elecPromptTrain, elecNonpromptTrain, elecPromptTest, elecNonpromptTest = {}, {}, {}, {}
    muonPromptTrain, muonNonpromptTrain, muonPromptTest, muonNonpromptTest = {}, {}, {}, {}
    
    print 'Merge and trim per dataset:\n'
    for s in xmlTree.findall('sample'):
        
        sname = s.get('id')
        ssig = s.get('sig')
        slep = s.get('lep')
        sproc = s.get('process')
        schannel = s.get('channel')
        starget = s.get('target')

        if options.mode == 'test' and starget == 'train': continue
        if options.mode == 'train' and starget == 'test': continue
        
        if schannel != '': sproc += '_'+schannel
        
        if ssig not in ['prompt', 'nonprompt', 'all']:
            continue
        
        sys.stdout.write(sname)
        
        tr = []
        for ch in s:
            tr.append(ch.text)
            
        outdir = tr[0].replace(sname,' ').split()[0]
        filestomerge = ' '.join(tr)
        if starget == 'train':
            outfile = outdir+sname+'/merged_train.root'
        else:
            outfile = outdir+sname+'/merged_test.root'
        os.system('rm -rf '+outfile)

        col = ''
        if ssig == 'all':
            if starget == 'train':
                promptTrain.append(outfile)
                promptProcTrain.append(sproc)
                nonpromptTrain.append(outfile)
                nonpromptProcTrain.append(sproc)
            else:
                promptTest.append(outfile)
                promptProcTest.append(sproc)
                nonpromptTest.append(outfile)
                nonpromptProcTest.append(sproc)                
            col = '\033[1;32m'
        elif ssig == 'prompt':
            if starget == 'train':
                promptTrain.append(outfile)
                promptProcTrain.append(sproc)
            else:
                promptTest.append(outfile)
                promptProcTest.append(sproc)
            col = '\033[1;31m'
        elif ssig == 'nonprompt':
            if starget == 'train':
                nonpromptTrain.append(outfile)
                nonpromptProcTrain.append(sproc)
            else:
                nonpromptTest.append(outfile)
                nonpromptProcTest.append(sproc)
            col = '\033[1;34m'
            
        sys.stdout.write(col+' --> '+ssig+' ('+starget+')\033[0;0m\n')

        os.system('hadd -f '+outfile+' '+filestomerge+' > /dev/null')
        f = ROOT.TFile(outfile,"UPDATE")
        if ssig == 'prompt':
            ROOT.gDirectory.Delete("elecNonprompt;*")
            ROOT.gDirectory.Delete("muonNonprompt;*")
            if slep == 'all':
                nElecPrompt = f.Get('elecPrompt').GetEntries()
                nMuonPrompt = f.Get('muonPrompt').GetEntries()
                if starget == 'train':
                    if sproc in elecPromptTrain.keys():
                        elecPromptTrain[sproc] += nElecPrompt
                        muonPromptTrain[sproc] += nMuonPrompt
                    else:
                        elecPromptTrain[sproc] = nElecPrompt
                        muonPromptTrain[sproc] = nMuonPrompt                
                else:
                    if sproc in elecPromptTest.keys():
                        elecPromptTest[sproc] += nElecPrompt
                        muonPromptTest[sproc] += nMuonPrompt
                    else:
                        elecPromptTest[sproc] = nElecPrompt
                        muonPromptTest[sproc] = nMuonPrompt                
                print 'nElecPrompt=\033[;1m'+str(nElecPrompt)+'\033[0;0m nMuonPrompt=\033[;1m'+str(nMuonPrompt)+'\033[0;0m\n'
            elif slep == 'elec':
                nElecPrompt = f.Get('elecPrompt').GetEntries()
                ROOT.gDirectory.Delete("muonPrompt;*")
                if starget == 'train':
                    if sproc in elecPromptTrain.keys():
                        elecPromptTrain[sproc] += nElecPrompt
                    else:
                        elecPromptTrain[sproc] = nElecPrompt
                else:
                    if sproc in elecPromptTest.keys():
                        elecPromptTest[sproc] += nElecPrompt
                    else:
                        elecPromptTest[sproc] = nElecPrompt                    
                print 'nElecPrompt=\033[;1m'+str(nElecPrompt)+'\033[0;0m\n'
            elif slep == 'muon':
                nMuonPrompt = f.Get('muonPrompt').GetEntries()
                ROOT.gDirectory.Delete("elecPrompt;*")
                if starget == 'train':
                    if sproc in elecPromptTrain.keys():
                        muonPromptTrain[sproc] += nMuonPrompt
                    else:
                        muonPromptTrain[sproc] = nMuonPrompt
                else:
                    if sproc in elecPromptTest.keys():
                        muonPromptTest[sproc] += nMuonPrompt
                    else:
                        muonPromptTest[sproc] = nMuonPrompt                    
                print 'nMuonPrompt=\033[;1m'+str(nMuonPrompt)+'\033[0;0m\n'
        if ssig == 'nonprompt':
            ROOT.gDirectory.Delete("elecPrompt;*")
            ROOT.gDirectory.Delete("muonPrompt;*")
            if slep == 'all':
                nElecNonprompt = f.Get('elecNonprompt').GetEntries()
                nMuonNonprompt = f.Get('muonNonprompt').GetEntries()
                if starget == 'train':
                    if sproc in elecNonpromptTrain.keys():
                        elecNonpromptTrain[sproc] += nElecNonprompt
                        muonNonpromptTrain[sproc] += nMuonNonprompt
                    else:
                        elecNonpromptTrain[sproc] = nElecNonprompt
                        muonNonpromptTrain[sproc] = nMuonNonprompt
                else:
                    if sproc in elecNonpromptTest.keys():
                        elecNonpromptTest[sproc] += nElecNonprompt
                        muonNonpromptTest[sproc] += nMuonNonprompt
                    else:
                        elecNonpromptTest[sproc] = nElecNonprompt
                        muonNonpromptTest[sproc] = nMuonNonprompt
                print 'nElecNonprompt=\033[;1m'+str(nElecNonprompt)+'\033[0;0m nMuonNonprompt=\033[;1m'+str(nMuonNonprompt)+'\033[0;0m\n'
            if slep == 'elec':
                nElecNonprompt = f.Get('elecNonprompt').GetEntries()
                ROOT.gDirectory.Delete("muonNonprompt;*")
                if starget == 'train':
                    if sproc in elecNonpromptTrain.keys():
                        elecNonpromptTrain[sproc] += nElecNonprompt
                    else:
                        elecNonpromptTrain[sproc] = nElecNonprompt
                else:
                    if sproc in elecNonpromptTest.keys():
                        elecNonpromptTest[sproc] += nElecNonprompt
                    else:
                        elecNonpromptTest[sproc] = nElecNonprompt                    
                print 'nElecNonprompt=\033[;1m'+str(nElecNonprompt)+'\033[0;0m\n'
            elif slep == 'muon':
                nMuonNonprompt = f.Get('muonNonprompt').GetEntries()
                ROOT.gDirectory.Delete("elecNonprompt;*")
                if starget == 'train':
                    if sproc in muonNonpromptTrain.keys():
                        muonNonpromptTrain[sproc] += nMuonNonprompt
                    else:
                        muonNonpromptTrain[sproc] = nMuonNonprompt
                else:
                    if sproc in muonNonpromptTest.keys():
                        muonNonpromptTest[sproc] += nMuonNonprompt
                    else:
                        muonNonpromptTest[sproc] = nMuonNonprompt                    
                print 'nMuonNonprompt=\033[;1m'+str(nMuonNonprompt)+'\033[0;0m\n'                
        f.Write()
        f.Close()
        sys.stdout.flush()

    print 'Merge datasets'
    
    for idx, s in enumerate([promptTrain,nonpromptTrain,promptTest,nonpromptTest]):
        filestomerge = ' '.join(s)
        
        if len(s) == 0: continue
        
        target = 'Train'
        if idx == 0: outfile = 'prompt_train.root'
        elif idx == 1: outfile = 'nonprompt_train.root'
        elif idx == 2: 
            outfile = 'prompt_test.root'
            target = 'Test'
        elif idx == 3: 
            outfile = 'nonprompt_test.root'
            target = 'Test'
        
        os.system('hadd -f '+outfile+' '+filestomerge+' > /dev/null')

        f = ROOT.TFile(outfile,"OPEN")
        if idx == 0 or idx == 2: 
            ROOT.gDirectory.Delete("elecNonprompt;*")
            ROOT.gDirectory.Delete("muonNonprompt;*")
            nElecPrompt = f.Get('elecPrompt').GetEntries()
            nMuonPrompt = f.Get('muonPrompt').GetEntries()            
            print target+': '+'nElecPrompt=\033[;1m'+str(nElecPrompt)+'\033[0;0m nMuonPrompt=\033[;1m'+str(nMuonPrompt)+'\033[0;0m'
        elif idx == 1 or idx == 3:
            ROOT.gDirectory.Delete("elecPrompt;*")
            ROOT.gDirectory.Delete("muonPrompt;*")
            nElecNonprompt = f.Get('elecNonprompt').GetEntries()
            nMuonNonprompt = f.Get('muonNonprompt').GetEntries()
            print target+': '+'nElecNonprompt=\033[;1m'+str(nElecNonprompt)+'\033[0;0m nMuonNonprompt=\033[;1m'+str(nMuonNonprompt)+'\033[0;0m'

    for idx, s in enumerate([promptTrain,nonpromptTrain,promptTest,nonpromptTest]):

        for f in s:
            if os.path.exists(f):
                os.system('rm '+f)

    if os.path.exists('prompt_train.root'):
        os.system('hadd -f train_'+options.year+'.root prompt_train.root nonprompt_train.root > /dev/null')
        os.system('rm prompt_train.root nonprompt_train.root')

    if os.path.exists('prompt_test.root'):
        os.system('hadd -f test_'+options.year+'.root prompt_test.root nonprompt_test.root > /dev/null')
        os.system('rm prompt_test.root nonprompt_test.root')
    
#    print 'Copy over to pnfs'
#    os.system('gfal-rm -r '+options.dir)
#    os.system('gfal-mkdir '+options.dir)
#    os.system('gfal-copy input.root '+options.dir+options.out)
#    os.system('rm input.root')
    
#    print 'Produce plots'

#    for res in ['elecPrompt','elecNonPrompt','muonPrompt','muonNonPrompt']:
#        fig1, ax1 = plt.subplots()
#        ax1.pie(eval(res+'.values()'), labels=eval(res+'.keys()'), autopct='%1.1f%%', shadow=True, startangle=90)
#        ax1.axis('equal')
#        stat = 'Prompt = '+str(nElecPrompt)
#        if res == 'elecNonPrompt': stat = 'NonPrompt = '+str(nElecNonPrompt)
#        elif res == 'muonPrompt': stat = 'Prompt = '+str(nMuonPrompt)
#        elif res == 'muonNonPrompt': stat = 'NonPrompt = '+str(nMuonNonPrompt)
#        plt.text(0.8, 0.5, stat, bbox=dict(facecolor='red', alpha=0.5))
#        plt.savefig(res+'.pdf')
#        plt.close()
    
    print '\033[92mDone\033[0;0m'
