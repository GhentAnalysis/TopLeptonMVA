treeName = "blackJackAndHookers/blackJackAndHookersTree"
proxy = "x509up_u20657"
proxydir = "/user/kskovpen/proxy/"
arch = "slc6_amd64_gcc700"
batchqueue = "localgrid"
walltime = "01:00:00"

variables = [ 'pt', 'eta', 'jetNDauChargedMVASel', 'miniRelIsoCharged', 'miniRelIsoNeutral', \
'jetPtRelv2', 'jetPtRatio', 'jetBTag', 'sip3d', 'dxy', 'dz', 'relIso0p3', 'mvaIDsegComp' ]

# process, tag, label

submit2016 = [\
('TTGamma_Dilept_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3-v1_leptonMVA_2016', ''),\
('TTGamma_Hadronic_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',           'crab_MiniAOD2016v3-v1_leptonMVA_2016', ''),\
('TTGamma_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8',    'crab_MiniAOD2016v3-v2_leptonMVA_2016', ''),\
('TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8',      'crab_MiniAOD2016v3-v1_leptonMVA_2016', ''),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',                     'crab_MiniAOD2016v3-v1_leptonMVA_2016', ''),\
('ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',    'crab_MiniAOD2016v3-v2_leptonMVA_2016', ''),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3_ext1-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',             'crab_MiniAOD2016v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',          'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'nonprompt'),\
('TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 'crab_MiniAOD2016v3_ext1-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3_ext1-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',    'crab_MiniAOD2016v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',                    'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'nonprompt'),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_MiniAOD2016v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8',                 'crab_RunIISummer16MiniAODv3-PUMoriond17_backup_94X_mcRun2_asymptotic_v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                 'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'nonprompt'),\
('TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',          'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'nonprompt'),\
('TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8',     'crab_MiniAOD2016v3-v2_leptonMVA_2016', 'nonprompt'),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext1-v2_leptonMVA_2016', ''),\
('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',     'crab_MiniAOD2016v3_ext2-v1_leptonMVA_2016', ''),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext1-v2_leptonMVA_2016', 'prompt'),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext2-v1_leptonMVA_2016', 'prompt'),\
('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',             'crab_MiniAOD2016v3_ext3-v1_leptonMVA_2016', 'prompt'),\
('tZq_ll_4f_13TeV-amcatnlo-herwigpp',                                'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'prompt'),\
('tZq_ll_4f_PSweights_13TeV-amcatnlo-pythia8',                       'crab_MiniAOD2016v3-v1_leptonMVA_2016', 'prompt')\
]

submit2017 = [\
]

submit2018 = [\
]
