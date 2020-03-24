treeName = "blackJackAndHookers/blackJackAndHookersTree"
proxy = "x509up_u20657"
proxydir = "/user/kskovpen/proxy/"
arch = "slc6_amd64_gcc700"
batchqueue = "localgrid"
batchqueueHighMem = "highmem"
walltime = "12:00:00"

variables = {}

variables['Muon'] = {}
variables['Elec'] = {}

variables['Muon']['TTH'] = {}
variables['Muon']['TTH']['pt'] = 'LepGood_pt'
variables['Muon']['TTH']['eta'] = 'LepGood_eta'
variables['Muon']['TTH']['trackMultClosestJet'] = 'LepGood_jetNDauChargedMVASel'
variables['Muon']['TTH']['miniIsoCharged'] = 'LepGood_miniRelIsoCharged'
variables['Muon']['TTH']['miniIsoNeutral'] = 'LepGood_miniRelIsoNeutral'
variables['Muon']['TTH']['pTRel'] = 'LepGood_jetPtRelv2'
variables['Muon']['TTH']['ptRatio'] = 'LepGood_jetPtRatio'
variables['Muon']['TTH']['relIso'] = ''
variables['Muon']['TTH']['bTagClosestJet'] = 'LepGood_jetDF'
variables['Muon']['TTH']['sip3d'] = 'LepGood_sip3d'
variables['Muon']['TTH']['dxy'] = 'LepGood_dxy'
variables['Muon']['TTH']['dz'] = 'LepGood_dz'
variables['Muon']['TTH']['idSeg'] = 'LepGood_segmentComp'

variables['Elec']['TTH'] = {}
variables['Elec']['TTH']['pt'] = 'LepGood_pt'
variables['Elec']['TTH']['eta'] = 'LepGood_eta'
variables['Elec']['TTH']['trackMultClosestJet'] = 'LepGood_jetNDauChargedMVASel'
variables['Elec']['TTH']['miniIsoCharged'] = 'LepGood_miniRelIsoCharged'
variables['Elec']['TTH']['miniIsoNeutral'] = 'LepGood_miniRelIsoNeutral'
variables['Elec']['TTH']['pTRel'] = 'LepGood_jetPtRelv2'
variables['Elec']['TTH']['ptRatio'] = 'LepGood_jetPtRatio'
variables['Elec']['TTH']['relIso'] = ''
variables['Elec']['TTH']['bTagClosestJet'] = 'LepGood_jetDF'
variables['Elec']['TTH']['sip3d'] = 'LepGood_sip3d'
variables['Elec']['TTH']['dxy'] = 'LepGood_dxy'
variables['Elec']['TTH']['dz'] = 'LepGood_dz'
variables['Elec']['TTH']['idSeg'] = 'LepGood_mvaFall17V2noIso'

variables['Muon']['TZQ'] = {}
variables['Muon']['TZQ']['pt'] = 'pt'
variables['Muon']['TZQ']['eta'] = 'eta'
variables['Muon']['TZQ']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Muon']['TZQ']['miniIsoCharged'] = 'miniIsoCharged'
variables['Muon']['TZQ']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Muon']['TZQ']['pTRel'] = 'pTRel'
variables['Muon']['TZQ']['ptRatio'] = 'ptRatio'
variables['Muon']['TZQ']['relIso'] = 'relIso'
variables['Muon']['TZQ']['bTagClosestJet'] = 'deepCsvClosestJet'
variables['Muon']['TZQ']['sip3d'] = 'sip3d'
variables['Muon']['TZQ']['dxy'] = 'dxy'
variables['Muon']['TZQ']['dz'] = 'dz'
variables['Muon']['TZQ']['idSeg'] = 'segmentCompatibility'
variables['Muon']['TZQ']['idSeg17'] = 'segmentCompatibility'

variables['Elec']['TZQ'] = {}
variables['Elec']['TZQ']['pt'] = 'pt'
variables['Elec']['TZQ']['eta'] = 'eta'
variables['Elec']['TZQ']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Elec']['TZQ']['miniIsoCharged'] = 'miniIsoCharged'
variables['Elec']['TZQ']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Elec']['TZQ']['pTRel'] = 'pTRel'
variables['Elec']['TZQ']['ptRatio'] = 'ptRatio'
variables['Elec']['TZQ']['relIso'] = 'relIso'
variables['Elec']['TZQ']['bTagClosestJet'] = 'deepCsvClosestJet'
variables['Elec']['TZQ']['sip3d'] = 'sip3d'
variables['Elec']['TZQ']['dxy'] = 'dxy'
variables['Elec']['TZQ']['dz'] = 'dz'
variables['Elec']['TZQ']['idSeg'] = 'electronMvaSpring16GP'
variables['Elec']['TZQ']['idSeg17'] = 'electronMvaFall17NoIso'

variables['Muon']['TOP'] = {}
variables['Muon']['TOP']['pt'] = 'pt'
variables['Muon']['TOP']['eta'] = 'etaAbs'
variables['Muon']['TOP']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Muon']['TOP']['miniIsoCharged'] = 'miniIsoCharged'
variables['Muon']['TOP']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Muon']['TOP']['pTRel'] = 'pTRel'
variables['Muon']['TOP']['ptRatio'] = 'ptRatio'
variables['Muon']['TOP']['relIso'] = 'relIso'
variables['Muon']['TOP']['bTagClosestJet'] = 'bTagDeepJetClosestJet'
variables['Muon']['TOP']['sip3d'] = 'sip3d'
variables['Muon']['TOP']['dxy'] = 'dxylog'
variables['Muon']['TOP']['dz'] = 'dzlog'
variables['Muon']['TOP']['idSeg'] = 'segmentCompatibility'

variables['Elec']['TOP'] = {}
variables['Elec']['TOP']['pt'] = 'pt'
variables['Elec']['TOP']['eta'] = 'etaAbs'
variables['Elec']['TOP']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Elec']['TOP']['miniIsoCharged'] = 'miniIsoCharged'
variables['Elec']['TOP']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Elec']['TOP']['pTRel'] = 'pTRel'
variables['Elec']['TOP']['ptRatio'] = 'ptRatio'
variables['Elec']['TOP']['relIso'] = 'relIso'
variables['Elec']['TOP']['bTagClosestJet'] = 'bTagDeepJetClosestJet'
variables['Elec']['TOP']['sip3d'] = 'sip3d'
variables['Elec']['TOP']['dxy'] = 'dxylog'
variables['Elec']['TOP']['dz'] = 'dzlog'
variables['Elec']['TOP']['idSeg'] = 'mvaIdFall17v2noIso'

var = {}

var['Muon'] = {}
var['Elec'] = {}

for lep in ['Muon','Elec']:
    
    v = variables[lep]['TZQ']
    var[lep]['TZQ'] = {'pt':v['pt'], 'eta':v['eta'], 'trackMultClosestJet':v['trackMultClosestJet'], 'miniIsoCharged':v['miniIsoCharged'], 'miniIsoNeutral':v['miniIsoNeutral'],\
    'pTRel':v['pTRel'], 'ptRatio':v['ptRatio'], 'relIso':v['relIso'], 'bTagClosestJet':v['bTagClosestJet'], 'sip3d':v['sip3d'], 'dxy':v['dxy'], 'dz':v['dz'], 'idSeg':v['idSeg'], 'idSeg17':v['idSeg17']}

    v = variables[lep]['TTH']
    var[lep]['TTH'] = {'pt':v['pt'], 'eta':v['eta'], 'trackMultClosestJet':v['trackMultClosestJet'], 'miniIsoCharged':v['miniIsoCharged'], 'miniIsoNeutral':v['miniIsoNeutral'],\
    'pTRel':v['pTRel'], 'bTagClosestJet':v['bTagClosestJet'], 'ptRatio':v['ptRatio'], 'dxy':v['dxy'], 'sip3d':v['sip3d'], 'dz':v['dz'], 'idSeg':v['idSeg']}

    v = variables[lep]['TOP']
    var[lep]['TOP'] = {'pt':v['pt'], 'eta':v['eta'], 'trackMultClosestJet':v['trackMultClosestJet'], 'miniIsoCharged':v['miniIsoCharged'], 'miniIsoNeutral':v['miniIsoNeutral'],\
    'pTRel':v['pTRel'], 'ptRatio':v['ptRatio'], 'relIso':v['relIso'], 'bTagClosestJet':v['bTagClosestJet'], 'sip3d':v['sip3d'], 'dxy':v['dxy'], 'dz':v['dz'], 'idSeg':v['idSeg']}
    
# process, tag, label, prompt/nonprompt, elec/muon/all, process, channel, fraction of stats to train, fraction of stats to test

submit2016 = [\
('QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8',                'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'QCD', 'Inclusive', 0.5, 0.5),\
('TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',          'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', '', '', 'TTGamma', 'Inclusive', 0.5, 0.5),\
('TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8',          'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'Dilept', 0.5, 0.5),\
('TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'Dilept', 0.5, 0.5),\
('TTGamma_Hadronic_TuneCP5_PSweights_13TeV-madgraph-pythia8',        'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'Hadronic', 0.0, 0.0),\
('TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',           'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'Hadronic', 0.0, 0.0),\
('TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8',      'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix',   'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',                     'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',          'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'Dilept', 0.25, 0.25),\
('TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_MiniAOD2016v3_backup-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TT_TuneCUETP8M2T4_PSweights_13TeV-powheg-pythia8',                 'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',              'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'Hadronic', 0.25, 0.25),\
('TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',                    'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_RunIISummer16MiniAODv3-PUMoriond17_backup_94X_mcRun2_asymptotic_v3-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', '', 0.25, 0.25),\
('TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                 'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'Dilept', 0.25, 0.25),\
('TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'muon', 'TTJets', 'Dilept', 0.25, 0.25),\
('TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',     'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'prompt', 'all', 'TTW', 'LNu', 0.25, 0.25),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTW', 'LNu', 0.25, 0.25),\
#('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', '', '', 'TTW', 'LNu', 0.5, 0.5),\
#('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', '', '', 'TTW', 'LNu', 0.5, 0.5),\
('TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',      'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'TTW', 'QQ', 0.0, 0.0),\
('ttWJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTW', 'LNu', 0.25, 0.25),\
#('ttWJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', '', '', 'TTW', 'LNu', 0.5, 0.5),\
('WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',               'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', '', '', 'WJets', 'LNu', 0.5, 0.5),\
('WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',               'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'WJets', 'LNu', 0.5, 0.5),\
('WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',                'crab_MiniAOD2016v3_ext2-v2_TopLeptonMVA_2016', '', '', 'WJets', 'LNu', 0.5, 0.5),\
('WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',                'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'WJets', 'LNu', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'prompt', 'all', 'TTZ', 'LLNuNu', 0.25, 0.25),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTZ', 'LLNuNu', 0.25, 0.25),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext3-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTZ', 'LLNuNu', 0.25, 0.25),\
#('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.5, 0.5),\
#('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.5, 0.5),\
#('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext3-v1_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.5, 0.5),\
('TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',           'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.0, 0.0),\
('TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',                      'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', '', 'TTZ', 'QQ', 0.0, 0.0),\
('ttZJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTZ', 'LLNuNu', 0.25, 0.25),\
('ttZJets_13TeV_madgraphMLM-pythia8',                                'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'all', 'TTZ', 'LLNuNu', 0.25, 0.25),\
#('ttZJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.5, 0.5),\
#('ttZJets_13TeV_madgraphMLM-pythia8',                                'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'TTZ', 'LLNuNu', 0.5, 0.5),\
('tZq_ll_4f_13TeV-amcatnlo-herwigpp',                                'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'tZq', 'LL', 0.0, 0.0),\
('tZq_ll_4f_13TeV-amcatnlo-pythia8',                                 'crab_MiniAOD2016v3_ext1-v1_TopLeptonMVA_2016', 'prompt', 'all', 'tZq', 'LL', 0.25, 0.25),\
('tZq_ll_4f_PSweights_13TeV-amcatnlo-pythia8',                       'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'all', 'tZq', 'LL', 0.25, 0.25),\
#('tZq_ll_4f_13TeV-amcatnlo-pythia8',                                 'crab_MiniAOD2016v3_ext1-v1_TopLeptonMVA_2016', '', '', 'tZq', 'LL', 0.5, 0.5),\
#('tZq_ll_4f_PSweights_13TeV-amcatnlo-pythia8',                       'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', '', 'tZq', 'LL', 0.5, 0.5),\
('tZq_nunu_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1',                  'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', '', '', 'tZq', 'nunu', 0.0, 0.0)\
]

submit2017 = [\
('QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8',                               'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'QCD', 'Inclusive', 0.5, 0.5),\
('TT_DiLept_TuneCP5_13TeV-amcatnlo-pythia8',                                 'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.5, 0.5),\
('TTGamma_Dilept_TuneCP5_PSweights_13TeV_madgraph_pythia8',                  'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'DiLept', 0.5, 0.5),\
('TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8',                  'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'DiLept', 0.5, 0.5),\
('TTGamma_Hadronic_TuneCP5_PSweights_13TeV_madgraph_pythia8',                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'Hadronic', 0.5, 0.5),\
('TTGamma_Hadronic_TuneCP5_PSweights_13TeV-madgraph-pythia8',                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'Hadronic', 0.5, 0.5),\
('TTGamma_SingleLeptFromTbar_TuneCP5_PSweights_13TeV_madgraph_pythia8',      'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLeptFromT_TuneCP5_PSweights_13TeV_madgraph_pythia8',         'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8',              'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                       'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', '', '', 'TTGamma', 'Inclusive', 0.5, 0.5),\
('ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8',            'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',                             'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8',                          'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8',              'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8',                 'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',                                'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', 'nonprompt', 'muon', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',                                 'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'nonprompt', 'muon', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                         'crab_MiniAOD2017v2NewPMX-v2_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',                      'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', 'nonprompt', 'muon', 'TTJets', 'Hadronic', 0.5, 0.5),\
('TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',                  'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',        'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', 'prompt', 'all', 'TTWJets', 'ToLNu', 0.25, 0.25),\
#('TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',        'crab_MiniAOD2017v2NewPMX-v1_TopLeptonMVA_2017', '', '', 'TTWJets', 'ToLNu', 0.5, 0.5),\
('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2_ext1-v2_TopLeptonMVA_2017', 'prompt', 'all', 'TTWJets', 'Inclusive', 0.25, 0.25),\
('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'prompt', 'all', 'TTWJets', 'Inclusive', 0.25, 0.25),\
#('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2_ext1-v2_TopLeptonMVA_2017', '', '', 'TTWJets', 'Inclusive', 0.5, 0.5),\
#('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTWJets', 'Inclusive', 0.5, 0.5),\
('TTZJetsToQQ_Dilept_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',              'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'TTZJets', 'DiLept', 0.5, 0.5),\
('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2_ext1-v3_TopLeptonMVA_2017', 'prompt', 'all', 'ttZJets', 'Inclusive', 0.25, 0.25),\
('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', 'prompt', 'all', 'ttZJets', 'Inclusive', 0.25, 0.25),\
#('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2_ext1-v3_TopLeptonMVA_2017', '', '', 'ttZJets', 'Inclusive', 0.5, 0.5),\
#('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'ttZJets', 'Inclusive', 0.5, 0.5),\
('TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',                           'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', '', '', 'ttZJets', 'DiLept', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                          'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', 'prompt', 'all', 'ttZJets', 'DiLept', 0.5, 0.5),\
#('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                          'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', '', '', 'ttZJets', 'DiLept', 0.5, 0.5),\
('TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',                                   'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', '', '', 'ttZJets', 'ToQQ', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',               'crab_MiniAOD2017v2NewPMX-v2_TopLeptonMVA_2017', 'prompt', 'all', 'tZq', 'll', 0.5, 0.5),\
#('tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',               'crab_MiniAOD2017v2NewPMX-v2_TopLeptonMVA_2017', '', '', 'tZq', 'll', 0.5, 0.5),\
('tZq_nunu_4f_ckm_NLO_TuneCP5_PSweights_13TeV-madgraph-pythia8',             'crab_MiniAOD2017v2-v2_TopLeptonMVA_2017', '', '', 'tZq', 'nunu', 0.5, 0.5),\
('tZq_W_lept_Z_hadron_4f_ckm_NLO_13TeV_amcatnlo_pythia8',                    'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'tZq', 'W_lept_Z_hadron', 0.5, 0.5),\
('tZq_Zhad_Wlept_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',       'crab_MiniAOD2017v2-v1_TopLeptonMVA_2017', '', '', 'tZq', 'Zhad_Wlept', 0.5, 0.5)\
]

submit2018 = [\
('TT_DiLept_TuneCP5_13TeV-amcatnlo-pythia8',                                   'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.5, 0.5),\
('TTGamma_Dilept_TuneCP5_13TeV_madgraph_pythia8',                              'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTGamma', 'DiLept', 0.5, 0.5),\
('TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8',                              'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTGamma', 'DiLept', 0.5, 0.5),\
('TTGamma_Hadronic_TuneCP5_13TeV_madgraph_pythia8',                            'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTGamma', 'Hadronic', 0.5, 0.5),\
('TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8',                            'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTGamma', 'Hadronic', 0.5, 0.5),\
('TTGamma_SingleLeptFromTbar_TuneCP5_13TeV_madgraph_pythia8',                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLeptFromT_TuneCP5_13TeV_madgraph_pythia8',                     'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8',                          'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTGamma', 'SingleLept', 0.5, 0.5),\
('TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                         'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTGamma', 'Inclusive', 0.5, 0.5),\
('ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8',              'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',                               'crab_MiniAOD2018-v2_TopLeptonMVA_2018', '', '', 'ttH', 'ToNonbb', 0.5, 0.5),\
('TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8',                            'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8',                'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'muon', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8',                   'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'muon', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',                                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTJets', 'Inclusive', 0.25, 0.25),\
('TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',                                   'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTJets', 'Inclusive', 0.25, 0.25),\
('TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',                                     'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'all', 'TTJets', 'DiLept', 0.25, 0.25),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8',                                  'crab_MiniAOD2018_ext2-v2_TopLeptonMVA_2018', 'nonprompt', 'muon', 'TTJets', 'Hadronic', 0.5, 0.5),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8',                                  'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'muon', 'TTJets', 'Hadronic', 0.5, 0.5),\
('TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',                              'crab_MiniAOD2018_ext3-v2_TopLeptonMVA_2018', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',                              'crab_MiniAOD2018-v1_TopLeptonMVA_2018', 'nonprompt', 'all', 'TTJets', 'SingleLept', 0.25, 0.25),\
('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                    'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'prompt', 'all', 'TTWJets', 'ToLNu', 0.25, 0.25),\
#('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                    'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTWJets', 'ToLNu', 0.5, 0.5),\
('TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                     'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTWJets', 'ToQQ', 0.5, 0.5),\
('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'prompt', 'all', 'TTWJets', 'Inclusive', 0.25, 0.25),\
#('ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTWJets', 'Inclusive', 0.5, 0.5),\
('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'prompt', 'all', 'TTZ', 'Inclusive', 0.25, 0.25),\
#('ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8',                                  'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTZ', 'Inclusive', 0.5, 0.5),\
('TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',                             'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTZ', 'ToLL', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                            'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'prompt', 'all', 'TTZ', 'ToLL', 0.25, 0.25),\
#('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                            'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'TTZ', 'ToLL', 0.5, 0.5),\
('TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',                                     'crab_MiniAOD2018_ext1-v1_TopLeptonMVA_2018', '', '', 'TTZ', 'ToQQ', 0.5, 0.5),\
('TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',                                     'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'TTZ', 'ToQQ', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-madgraph-pythia8',                           'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', 'prompt', 'all', 'tZq', 'll', 0.5, 0.5),\
#('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-madgraph-pythia8',                           'crab_MiniAOD2018_ext1-v2_TopLeptonMVA_2018', '', '', 'tZq', 'll', 0.5, 0.5),\
('tZq_nunu_4f_ckm_NLO_TuneCP5_PSweights_13TeV-mcatnlo-pythia8',                'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'tZq', 'nunu', 0.5, 0.5),\
('tZq_Zhad_Wlept_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',         'crab_MiniAOD2018-v1_TopLeptonMVA_2018', '', '', 'tZq', 'Zhad_Wlept', 0.5, 0.5)\
]
