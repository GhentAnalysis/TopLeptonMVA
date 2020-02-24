treeName = "blackJackAndHookers/blackJackAndHookersTree"
proxy = "x509up_u20657"
proxydir = "/user/kskovpen/proxy/"
arch = "slc6_amd64_gcc700"
batchqueue = "localgrid"
walltime = "06:00:00"

variables = [ 'pt', 'eta', 'jetNDauChargedMVASel', 'miniRelIsoCharged', 'miniRelIsoNeutral', \
'jetPtRelv2', 'jetPtRatio', 'jetBTag', 'sip3d', 'dxy', 'dz', 'relIso0p3', 'mvaIDsegComp' ]

# process, tag, label, process, channel, fraction of files to use

submit2016 = [\
('TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', 'TTGamma', 'Dilept', 1.0),\
('TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',           'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', 'TTGamma', 'Hadronic', 1.0),\
('TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', '', 'TTGamma', 'SingleLept', 1.0),\
('TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8',      'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', 'TTGamma', 'SingleLept', 1.0),\
('ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix',   'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'prompt', 'ttH', 'ToNonbb', 1.0),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',                     'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'ttH', 'ToNonbb', 1.0),\
('ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'prompt', 'ttH', 'ToNonbb', 1.0),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'DiLept', 1.0),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'DiLept', 1.0),\
('TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',          'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'Dilept', 1.0),\
('TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'SingleLept', 1.0),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'SingleLept', 1.0),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'SingleLept', 1.0),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',                           'crab_MiniAOD2016v3_backup-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TT_TuneCUETP8M2T4_PSweights_13TeV-powheg-pythia8',                 'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',              'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', '', 'TTJets', 'Hadronic', 1.0),\
('TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',                    'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_RunIISummer16MiniAODv3-PUMoriond17_backup_94X_mcRun2_asymptotic_v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', '', 1.0),\
('TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                 'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'Dilept', 1.0),\
('TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'Dilept', 1.0),\
('TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'SingleLept', 1.0),\
('TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',     'crab_MiniAOD2016v3-v2_TopLeptonMVA_2016', 'nonprompt', 'TTJets', 'SingleLept', 1.0),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'prompt', 'TTW', 'LNu', 1.0),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', 'prompt', 'TTW', 'LNu', 1.0),\
('ttWJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'prompt', 'TTW', 'LNu', 1.0),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016', 'prompt', 'TTZ', 'LLNuNu', 1.0),\
#('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext2-v1_TopLeptonMVA_2016', 'prompt', 'TTZ', 'LLNuNu', 0.1),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext3-v1_TopLeptonMVA_2016', 'prompt', 'TTZ', 'LLNuNu', 1.0),\
('ttZJets_13TeV_madgraphMLM',                                        'crab_RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1_TopLeptonMVA_2016', 'prompt', 'TTZ', 'LLNuNu', 1.0),\
('ttZJets_13TeV_madgraphMLM-pythia8',                                'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'TTZ', 'LLNuNu', 1.0),\
('tZq_ll_4f_13TeV-amcatnlo-herwigpp',                                'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'tZq', 'LL', 1.0),\
('tZq_ll_4f_13TeV-amcatnlo-pythia8',                                 'crab_MiniAOD2016v3_ext1-v1_TopLeptonMVA_2016', 'prompt', 'tZq', 'LL', 1.0),\
('tZq_ll_4f_PSweights_13TeV-amcatnlo-pythia8',                       'crab_MiniAOD2016v3-v1_TopLeptonMVA_2016', 'prompt', 'tZq', 'LL', 1.0)\
]

submit2017 = [\
]

submit2018 = [\
]
