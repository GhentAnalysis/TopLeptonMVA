import numpy as np

WPNames = {}
#WPNames['elec'] = ['VLoose', 'Loose', 'MediumL', 'Medium', 'Tight']
#WPNames['muon'] = ['VLoose', 'Loose', 'MediumL', 'Medium', 'Tight']
WPNames['elec'] = ['VLoose', 'Loose', 'Medium', 'Tight']
WPNames['muon'] = ['VLoose', 'Loose', 'Medium', 'Tight']

WPs = {}
for d in ['TOP', 'TOPULTOPv1', 'TOPULTOPv2', 'TOPUL4TOPv1', 'TOPUL4TOPv2', \
'TOPULTOPPUPv1', 'TOPULTOPPUPv2', 'TOPUL4TOPPUPv1', 'TOPUL4TOPPUPv2']: WPs[d] = {}

#WPs['TOP']['elec'] = [-0.55, 0.00, 0.40 ,0.60, 0.90]
#WPs['TOP']['muon'] = [-0.45, 0.05, 0.40 ,0.65, 0.90]
WPs['TOP']['elec'] = [-0.55, 0.00, 0.40, 0.90]
WPs['TOP']['muon'] = [-0.45, 0.05, 0.40, 0.90]

#WPs['TOPULTOPv1']['elec'] = [0.20, 0.30, 0.41 ,0.58, 0.81] # 98, 97, 96, 94, 89 (preselection not included)
#WPs['TOPULTOPv1']['muon'] = [0.20, 0.30, 0.41 ,0.58, 0.81]
#WPs['TOPULTOPv2']['elec'] = [0.59, 0.68, 0.81 ,0.87, 0.94] # 96, 95, 93, 91, 87
#WPs['TOPULTOPv2']['muon'] = [0.59, 0.68, 0.81 ,0.87, 0.94]
WPs['TOPULTOPv1']['elec'] = [0.20, 0.41, 0.64, 0.81] # 98, 96, 93, 89 (preselection not included)
WPs['TOPULTOPv1']['muon'] = [0.20, 0.41, 0.64, 0.81]
WPs['TOPULTOPv2']['elec'] = [0.59, 0.81, 0.90, 0.94] # 96, 93, 90, 87
WPs['TOPULTOPv2']['muon'] = [0.59, 0.81, 0.90, 0.94]

#WPs['TOPUL4TOPv1']['elec'] = [0.20, 0.30, 0.41 ,0.58, 0.81]
#WPs['TOPUL4TOPv1']['muon'] = [0.20, 0.30, 0.41 ,0.58, 0.81]
#WPs['TOPUL4TOPv2']['elec'] = [0.59, 0.68, 0.81 ,0.87, 0.94]
#WPs['TOPUL4TOPv2']['muon'] = [0.59, 0.68, 0.81 ,0.87, 0.94]
WPs['TOPUL4TOPv1']['elec'] = [0.20, 0.41, 0.64, 0.81]
WPs['TOPUL4TOPv1']['muon'] = [0.20, 0.41, 0.64, 0.81]
WPs['TOPUL4TOPv2']['elec'] = [0.59, 0.81, 0.90, 0.94]
WPs['TOPUL4TOPv2']['muon'] = [0.59, 0.81, 0.90, 0.94]

Bins = {}
Bins['pt'] = [0., 10.] + list(np.arange(11., 50., 5.)) + list(np.arange(50., 100., 10.))
Bins['eta'] = list(np.arange(-2.5, 2.75, 0.5))
Bins['nvertex'] = list(np.arange(0., 65., 5.))
