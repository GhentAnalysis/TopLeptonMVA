from collections import OrderedDict

treeName = "ntuple/nt"
proxy = "/user/kskovpen/proxy/x509up_u20657"
arch = "slc6_amd64_gcc700"

variables = {}

variables['Muon'] = {}
variables['Elec'] = {}

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

variables['Muon']['TOP-UL'] = {}
variables['Muon']['TOP-UL']['pt'] = 'pt'
variables['Muon']['TOP-UL']['eta'] = 'etaAbs'
variables['Muon']['TOP-UL']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Muon']['TOP-UL']['miniIsoCharged'] = 'miniIsoCharged'
variables['Muon']['TOP-UL']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Muon']['TOP-UL']['pTRel'] = 'pTRel'
variables['Muon']['TOP-UL']['ptRatio'] = 'ptRatio'
variables['Muon']['TOP-UL']['relIso'] = 'relIso'
variables['Muon']['TOP-UL']['bTagClosestJet'] = 'bTagDeepJetClosestJet'
variables['Muon']['TOP-UL']['sip3d'] = 'sip3d'
variables['Muon']['TOP-UL']['dxy'] = 'dxylog'
variables['Muon']['TOP-UL']['dz'] = 'dzlog'
variables['Muon']['TOP-UL']['idSeg'] = 'segmentCompatibility'

variables['Elec']['TOP-UL'] = {}
variables['Elec']['TOP-UL']['pt'] = 'pt'
variables['Elec']['TOP-UL']['eta'] = 'etaAbs'
variables['Elec']['TOP-UL']['trackMultClosestJet'] = 'trackMultClosestJet'
variables['Elec']['TOP-UL']['miniIsoCharged'] = 'miniIsoCharged'
variables['Elec']['TOP-UL']['miniIsoNeutral'] = 'miniIsoNeutral'
variables['Elec']['TOP-UL']['pTRel'] = 'pTRel'
variables['Elec']['TOP-UL']['ptRatio'] = 'ptRatio'
variables['Elec']['TOP-UL']['relIso'] = 'relIso'
variables['Elec']['TOP-UL']['bTagClosestJet'] = 'bTagDeepJetClosestJet'
variables['Elec']['TOP-UL']['sip3d'] = 'sip3d'
variables['Elec']['TOP-UL']['dxy'] = 'dxylog'
variables['Elec']['TOP-UL']['dz'] = 'dzlog'
variables['Elec']['TOP-UL']['idSeg'] = 'mvaIdFall17v2noIso'

mnames = {'v1': [], 'v2': []}
for v in ['TOP_', '4TOP_', 'TOP_PUP', '4TOP_PUP', 'TOP_TAUFLIP', '4TOP_TAUFLIP']:
    
    ver = 'v1'
    mname = 'TOP-UL.'+v+ver
    mnames['v1'].append(mname)
    
    variables['Muon'][mname] = {}
    variables['Muon'][mname]['pt'] = 'pt'
    variables['Muon'][mname]['eta'] = 'eta'
    variables['Muon'][mname]['trackMultClosestJet'] = 'trackMultClosestJet'
    variables['Muon'][mname]['miniIsoCharged'] = 'miniIsoCharged'
    variables['Muon'][mname]['miniIsoNeutral'] = 'miniIsoNeutral'
    variables['Muon'][mname]['pTRel'] = 'pTRel'
    variables['Muon'][mname]['ptRatio'] = 'ptRatio'
    variables['Muon'][mname]['relIso'] = 'relIso'
    variables['Muon'][mname]['bTagClosestJet'] = 'bTagDeepJetClosestJet'
    variables['Muon'][mname]['sip3d'] = 'sip3d'
    variables['Muon'][mname]['dxy'] = 'dxylog'
    variables['Muon'][mname]['dz'] = 'dzlog'
    variables['Muon'][mname]['idSeg'] = 'segmentCompatibility'
    
    variables['Elec'][mname] = {}
    variables['Elec'][mname]['pt'] = 'pt'
    variables['Elec'][mname]['eta'] = 'eta'
    variables['Elec'][mname]['trackMultClosestJet'] = 'trackMultClosestJet'
    variables['Elec'][mname]['miniIsoCharged'] = 'miniIsoCharged'
    variables['Elec'][mname]['miniIsoNeutral'] = 'miniIsoNeutral'
    variables['Elec'][mname]['pTRel'] = 'pTRel'
    variables['Elec'][mname]['ptRatio'] = 'ptRatio'
    variables['Elec'][mname]['relIso'] = 'relIso'
    variables['Elec'][mname]['bTagClosestJet'] = 'bTagDeepJetClosestJet'
    variables['Elec'][mname]['sip3d'] = 'sip3d'
    variables['Elec'][mname]['dxy'] = 'dxylog'
    variables['Elec'][mname]['dz'] = 'dzlog'
    variables['Elec'][mname]['idSeg'] = 'mvaIdFall17v2noIso'

    ver = 'v2'
    mname = 'TOP-UL.'+v+ver
    mnames['v2'].append(mname)
    
    variables['Muon'][mname] = {}
    variables['Muon'][mname]['pt'] = 'pt'
    variables['Muon'][mname]['eta'] = 'eta'
    variables['Muon'][mname]['trackMultClosestJet'] = 'trackMultClosestJet'
    variables['Muon'][mname]['miniIsoCharged'] = 'miniIsoCharged'
    variables['Muon'][mname]['miniIsoNeutral'] = 'miniIsoNeutral'
    variables['Muon'][mname]['pTRel'] = 'pTRel'
    variables['Muon'][mname]['ptRatio'] = 'ptRatio'
    variables['Muon'][mname]['relIso'] = 'relIso'
    variables['Muon'][mname]['bTagClosestJet'] = 'bTagDeepJetClosestJet'
    variables['Muon'][mname]['sip3d'] = 'sip3d'
    variables['Muon'][mname]['dxy'] = 'dxylog'
    variables['Muon'][mname]['dz'] = 'dzlog'
    variables['Muon'][mname]['idSeg'] = 'segmentCompatibility'
    
    variables['Elec'][mname] = {}
    variables['Elec'][mname]['pt'] = 'pt'
    variables['Elec'][mname]['eta'] = 'eta'
    variables['Elec'][mname]['trackMultClosestJet'] = 'trackMultClosestJet'
    variables['Elec'][mname]['miniIsoCharged'] = 'miniIsoCharged'
    variables['Elec'][mname]['miniIsoNeutral'] = 'miniIsoNeutral'
    variables['Elec'][mname]['pTRel'] = 'pTRel'
    variables['Elec'][mname]['ptRatio'] = 'ptRatio'
    variables['Elec'][mname]['relIso'] = 'relIso'
    variables['Elec'][mname]['bTagClosestJet'] = 'bTagDeepJetClosestJet'
    variables['Elec'][mname]['sip3d'] = 'sip3d'
    variables['Elec'][mname]['dxy'] = 'dxylog'
    variables['Elec'][mname]['dz'] = 'dzlog'
    variables['Elec'][mname]['idSeg'] = 'mvaIdFall17v2noIso'
    variables['Elec'][mname]['medHit'] = 'missHits'
    
var = {}
var['Muon'] = {}
var['Elec'] = {}

for lep in ['Muon','Elec']:
    
    v = variables[lep]['TOP']
    var[lep]['TOP'] = OrderedDict([('pt',v['pt']), ('eta',v['eta']), ('trackMultClosestJet',v['trackMultClosestJet']), ('miniIsoCharged',v['miniIsoCharged']), ('miniIsoNeutral',v['miniIsoNeutral']),\
    ('pTRel',v['pTRel']), ('ptRatio',v['ptRatio']), ('relIso',v['relIso']), ('bTagClosestJet',v['bTagClosestJet']), ('sip3d',v['sip3d']), ('dxy',v['dxy']), ('dz',v['dz']), ('idSeg',v['idSeg'])])

    v = variables[lep]['TOP-UL']
    var[lep]['TOP-UL'] = OrderedDict([('pt',v['pt']), ('eta',v['eta']), ('trackMultClosestJet',v['trackMultClosestJet']), ('miniIsoCharged',v['miniIsoCharged']), ('miniIsoNeutral',v['miniIsoNeutral']),\
    ('pTRel',v['pTRel']), ('ptRatio',v['ptRatio']), ('relIso',v['relIso']), ('bTagClosestJet',v['bTagClosestJet']), ('sip3d',v['sip3d']), ('dxy',v['dxy']), ('dz',v['dz']), ('idSeg',v['idSeg'])])

    for mname in mnames['v1']:
        v = variables[lep][mname]
        var[lep][mname] = OrderedDict([('pt',v['pt']), ('eta',v['eta']), ('trackMultClosestJet',v['trackMultClosestJet']), ('miniIsoCharged',v['miniIsoCharged']), ('miniIsoNeutral',v['miniIsoNeutral']),\
        ('pTRel',v['pTRel']), ('ptRatio',v['ptRatio']), ('relIso',v['relIso']), ('bTagClosestJet',v['bTagClosestJet']), ('sip3d',v['sip3d']), ('dxy',v['dxy']), ('dz',v['dz']), ('idSeg',v['idSeg'])])
    for mname in mnames['v2']:
        v = variables[lep][mname]
        if lep == 'Elec':
            var[lep][mname] = OrderedDict([('pt',v['pt']), ('eta',v['eta']), ('trackMultClosestJet',v['trackMultClosestJet']), ('miniIsoCharged',v['miniIsoCharged']), ('miniIsoNeutral',v['miniIsoNeutral']),\
            ('pTRel',v['pTRel']), ('ptRatio',v['ptRatio']), ('relIso',v['relIso']), ('bTagClosestJet',v['bTagClosestJet']), ('sip3d',v['sip3d']), ('dxy',v['dxy']), ('dz',v['dz']), ('idSeg',v['idSeg']), ('medHit',v['medHit'])])
        else:
            var[lep][mname] = OrderedDict([('pt',v['pt']), ('eta',v['eta']), ('trackMultClosestJet',v['trackMultClosestJet']), ('miniIsoCharged',v['miniIsoCharged']), ('miniIsoNeutral',v['miniIsoNeutral']),\
            ('pTRel',v['pTRel']), ('ptRatio',v['ptRatio']), ('relIso',v['relIso']), ('bTagClosestJet',v['bTagClosestJet']), ('sip3d',v['sip3d']), ('dxy',v['dxy']), ('dz',v['dz']), ('idSeg',v['idSeg'])])
    
submit2016 = [\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTTT_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016-v2_UL16', 'all', 'all', 'TTTT', 'Inclusive', 0.5, 0.5),\
('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'TTW', 'Inclusive', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'TTZ', 'Inclusive', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'tZq', 'Inclusive', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016-v2_UL16', 'all', 'all', 'ttH', 'Inclusive', 0.5, 0.5),\
('TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016-v1_UL16', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
]

submit2016APV = [\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'crab_MiniAOD2016APV-v1_UL16APV', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTTT_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016APV-v2_UL16APV', 'all', 'all', 'TTTT', 'Inclusive', 0.5, 0.5),\
('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 'crab_MiniAOD2016APV-v2_UL16APV', 'all', 'all', 'TTW', 'Inclusive', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016APV-v1_UL16APV', 'all', 'all', 'TTZ', 'Inclusive', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2016APV-v1_UL16APV', 'all', 'all', 'tZq', 'Inclusive', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016APV-v2_UL16APV', 'all', 'all', 'ttH', 'Inclusive', 0.5, 0.5),\
('TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016APV-v1_UL16APV', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2016APV-v1_UL16APV', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
]

submit2017 = [\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'crab_MiniAOD2017-v2_UL17', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTTT_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2017-v2_UL17', 'all', 'all', 'TTTT', 'Inclusive', 0.5, 0.5),\
('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 'crab_MiniAOD2017-v1_UL17', 'all', 'all', 'TTW', 'Inclusive', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2017-v1_UL17', 'all', 'all', 'TTZ', 'Inclusive', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2017-v1_UL17', 'all', 'all', 'tZq', 'Inclusive', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2017-v2_UL17', 'all', 'all', 'ttH', 'Inclusive', 0.5, 0.5),\
('TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2017-v1_UL17', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2017-v2_UL17', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
]

submit2018 = [\
('TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'crab_MiniAOD2018-v2_UL18', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
('TTTT_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2018-v2_UL18', 'all', 'all', 'TTTT', 'Inclusive', 0.5, 0.5),\
('TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 'crab_MiniAOD2018-v1_UL18', 'all', 'all', 'TTW', 'Inclusive', 0.5, 0.5),\
('TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2018-v2_UL18', 'all', 'all', 'TTZ', 'Inclusive', 0.5, 0.5),\
('tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8', 'crab_MiniAOD2018-v2_UL18', 'all', 'all', 'tZq', 'Inclusive', 0.5, 0.5),\
('ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2018-v2_UL18', 'all', 'all', 'ttH', 'Inclusive', 0.5, 0.5),\
('TTToHadronic_TuneCP5_13TeV-powheg-pythia8', 'crab_MiniAOD2018-v1_UL18', 'all', 'all', 'TTJets', 'Inclusive', 0.5, 0.5),\
]
