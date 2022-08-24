#!/bin/env python3

import os, sys, glob, pickle, uproot4
import pandas as pd
import numpy as np
import ROOT as r
import xgboost as xgb
import seaborn as sb
import plotly.express as px
import plotly.offline as po
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.colors as pycol
plt.switch_backend('agg')
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.covariance import EllipticEnvelope
from optparse import OptionParser

def set_xgbc(conf):
    
    xgbc = xgb.XGBClassifier(use_label_encoder = False,
                             booster           = conf['booster'],
                             tree_method       = conf['tree_method'], 
                             sampling_method   = conf['sampling_method'],
                             base_score        = float(conf['base_score']),
                             colsample_bylevel = float(conf['colsample_bylevel']),
                             colsample_bytree  = float(conf['colsample_bytree']),
                             colsample_bynode  = float(conf['colsample_bynode']),
                             gamma             = float(conf['gamma']),
                             learning_rate     = float(conf['learning_rate']),
                             max_delta_step    = int(conf['max_delta_step']),
                             min_child_weight  = float(conf['min_child_weight']),
                             missing           = conf['missing'],
                             objective         = conf['objective'],
                             reg_alpha         = float(conf['reg_alpha']),
                             reg_lambda        = float(conf['reg_lambda']),
                             scale_pos_weight  = float(conf['scale_pos_weight']),
                             seed              = int(conf['seed']),
                             subsample         = int(conf['subsample']),
                             eval_metric       = conf['eval_metric'],
                             n_estimators      = int(conf['n_estimators']),
                             eta               = float(conf['eta']),
                             max_depth         = int(conf['max_depth']),
                             n_jobs            = 8)
                             
    return xgbc
    
def norm(x):
    
    return (x-min(x))/(max(x)-min(x))

def reweight(X_train, y_train):
    
    weights = np.ones(len(X_train))
    
    if options.reweight:

        y_train = list(y_train)
        x_train = list(X_train['pt'])
        sig = [x for ix, x in enumerate(x_train) if y_train[ix] == 1]
        bkg = [x for ix, x in enumerate(x_train) if y_train[ix] == 0]
        
        # calculate per bin weights
        bins = [10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 30., 35., 40., 45., 50., 70., 100., 150., 200., 300., 10000.]
        nbins = len(bins)-1
        sigtot, bkgtot = float(len(sig)), float(len(bkg))
        sigw, bkgw, ratw = np.zeros(nbins), np.zeros(nbins), np.ones(nbins)
        for iv, v in enumerate([sig, bkg]):
            for s in v:
                bin = -1
                for ib in range(nbins):
                    if (s > bins[ib]) and (s <= bins[ib+1]):
                        bin = ib
                        if iv == 0: sigw[bin] += 1./sigtot
                        else: bkgw[bin] += 1./bkgtot
                        break
                if bin < 0:
                    print('Please adjust the pT range for reweighting, found pt =', s)
                    sys.exit()
        for ib in range(nbins):
            ratw[ib] = sigw[ib]/bkgw[ib] if (bkgw[ib] > 0 and sigw[ib] > 0) else 1.

        # calculate per event weights
        for iv, v in enumerate(x_train):
            if y_train[iv] == 0:
                pt = x_train[iv]
                sf = 1.
                for ib in range(nbins):
                    if pt > bins[ib] and pt <= bins[ib+1]:
                        sf = ratw[ib]
                        break
                weights[iv] = sf
        
        # produce validation plot
        dsig, dbkg, weights_sig, weights_bkg = [], [], [], []
        for iv, v in enumerate(x_train):
            if y_train[iv] == 0:
                dbkg.append(x_train[iv])
                weights_bkg.append(weights[iv])
            else: 
                dsig.append(x_train[iv])
                weights_sig.append(weights[iv])
        fig, ax = plt.subplots()
        ax.hist(dsig, bins=70, histtype='step', alpha=0.7, linewidth=2, color='r', label='Prompt (Test)', weights=weights_sig)
        ax.hist(dbkg, bins=70, histtype='step', alpha=0.7, linewidth=2, color='b', label='Nonprompt (Test)', weights=weights_bkg)
        ax.legend(loc='best')
        ax.set_xlabel(xlabel='$\mathrm{p_{T}}$ [GeV]', fontsize=14)
        ax.set_ylabel(ylabel='Normalized to unity', fontsize=14)
        fig = ax.get_figure()
        fig.savefig(options.path+'pics/reweight.pdf')
        
    return weights

def plot_roc(rocs, tagname, cv = False):
    
    fig, ax = plt.subplots()
    
    plt.title(tagname)
    dfs, names = [], []
    for roc in rocs:
        name, fpr, tpr, roc_auc, ths = roc[0], roc[1], roc[2], roc[3], roc[6]
        names.append(name)
        ax.plot(fpr, tpr, linewidth=3, label=name.capitalize()) if not cv else ax.plot(fpr, tpr, linewidth=3, label='CV '+name.split('testcv')[1])
        dfs.append(pd.DataFrame(zip(fpr, tpr, ths), columns=['Nonprompt', 'Prompt', 'Cut']))
        
    legend = ax.legend(loc='lower right', fontsize=12, scatterpoints=1, frameon=False, numpoints=1)
    legend.get_frame().set_linewidth(0.0)
    
    ax.set_xlabel(xlabel='Nonprompt lepton efficiency', fontsize=14)
    ax.set_ylabel(ylabel='Prompt lepton efficiency', fontsize=14)
    ax.set_xticks(np.arange(0.001, 1., 0.005))
    ax.set_yticks(np.arange(0.7, 1., 0.05))
    ax.grid(which='both')
    
    ax.set_xscale('log')
    ax.set_xlim(0.001, 1)
    ax.set_ylim(0.7, 1)
    
    fig.savefig(options.path+'pics/roc.pdf' if not cv else options.path+'pics/roccv.pdf')
    plt.close()
    
    for i, d in enumerate(dfs):
        figt = px.line(d, x='Nonprompt', y='Prompt', hover_data=['Nonprompt', 'Prompt', 'Cut'])
        figt.update_xaxes(type='log')
        figt.update_yaxes(title_text="Prompt lepton efficiency")
        figt.update_xaxes(title_text="Nonprompt lepton efficiency")
        po.plot(figt, filename = options.path+'pics/roc_'+names[i]+'.html', auto_open=False)

def plot_overtrain(rocs, tagname):

    fig, ax = plt.subplots()
    plt.title(tagname)
    for roc in rocs:
        name, sigresp, bkg1resp = roc[0], roc[4], roc[5]
        min_sig, max_sig = min(sigresp), max(sigresp)
        min_bkg1, max_bkg1 = min(bkg1resp), max(bkg1resp)
        xmin = min(min_sig, min_bkg1)
        xmax = max(max_sig, max_bkg1)
        weights_sig = np.ones_like(sigresp) / len(sigresp)
        weights_bkg = np.ones_like(bkg1resp) / len(bkg1resp)        
        if name in ['test']:
            ax.hist(sigresp, bins=70, histtype='step', alpha=0.7, linewidth=2, color='r', label='Prompt (Test)', weights=weights_sig, range=[xmin,xmax])
            ax.hist(bkg1resp, bins=70, histtype='step', alpha=0.7, linewidth=2, color='b', label='Nonprompt (Test)', weights=weights_bkg, range=[xmin,xmax])
        else:            
            n, bins, patches = ax.hist(sigresp, bins=70, histtype='step', alpha=0.0, weights=weights_sig, range=[xmin,xmax])
            plt.scatter(bins[:-1]+0.5*(bins[1:]-bins[:-1]), n, marker='o', c='r', s=20, alpha=1.0, label='Prompt (Train)')
            n, bins, patches = ax.hist(bkg1resp, bins=70, histtype='step', alpha=0.0, weights=weights_bkg, range=[xmin,xmax])
            plt.scatter(bins[:-1]+0.5*(bins[1:]-bins[:-1]), n, marker='^', c='b', s=20, alpha=1.0, label='Nonprompt (Train)')
    ax.legend(loc='best')
    ax.set_xlabel(xlabel='Predicted score', fontsize=14)
    ax.set_ylabel(ylabel='Normalized to unity', fontsize=14)
    fig = ax.get_figure()
    fig.savefig(options.path+'pics/res.pdf')
    
def plot_learning_curve(results, epochs, tagname):
    x_axis = range(0, epochs)
    fig, ax = plt.subplots()
    plt.title(tagname)
    ax.plot(x_axis, results['validation_0']['logloss'], label='Logloss (Train)')
    ax.plot(x_axis, results['validation_1']['logloss'], label='Logloss (Test)')
    ax.plot(x_axis, results['validation_0']['auc'], label='AUC (Train)')
    ax.plot(x_axis, results['validation_1']['auc'], label='AUC (Test)')
    ax.legend(loc='best')
    plt.xlabel('Number of boosting rounds')
    plt.ylabel('Log Loss/AUC')
    fig.savefig(options.path+'pics/learn.pdf')
    plt.close()
    
def plot_classification_error(results, epochs, tagname):
    x_axis = range(0, epochs)
    fig, ax = plt.subplots()
    plt.title(tagname)
    ax.plot(x_axis, results['validation_0']['error'], label='Train')
    ax.plot(x_axis, results['validation_1']['error'], label='Test')
    ax.legend(loc='best')
    plt.xlabel('Number of boosting rounds')
    plt.ylabel('Classification error')
    fig.savefig(options.path+'pics/error.pdf')
    plt.close()

def plot_importance(xgbc):
    plt.figure(figsize = (16, 12))
    xgb.plot_importance(xgbc)
    plt.savefig(options.path+'pics/importance.pdf')
    plt.close()
    
def plot_correlation(X, tagname):
    corr = X.corr()
    f, ax = plt.subplots(figsize=(11, 9))
    plt.title(tagname)
    cmap = pycol.LinearSegmentedColormap.from_list(name='test', colors=['red', 'white', 'red'])
    sb.heatmap(corr, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5)
    plt.savefig(options.path+'pics/correlation.pdf')
    plt.close()    

def plot_features(X_sig, X_bkg):    
    for p in X_sig.columns:
        f, ax = plt.subplots()
        min_sig, max_sig = min(X_sig[p]), max(X_sig[p])
        min_bkg, max_bkg = min(X_bkg[p]), max(X_bkg[p])
        xmin = min(min_sig, min_bkg)
        xmax = min(max_sig, max_bkg)
        weights_sig = np.ones_like(X_sig[p])/len(X_sig[p])
        weights_bkg = np.ones_like(X_bkg[p])/len(X_bkg[p])
        ax.hist(X_sig[p], bins=70, histtype='step', alpha=1.0, linewidth=3, color='r', label='Prompt', weights=weights_sig, range=[xmin,xmax])
        ax.hist(X_bkg[p], bins=70, histtype='step', alpha=1.0, linewidth=3, color='b', label='Nonprompt', weights=weights_bkg, range=[xmin,xmax])
        print(p+':', '['+str(max_sig)+',', str(max_bkg)+']')
        if p in ['mvaIdFall17v2noIso', 'miniIsoCharged', 'miniIsoNeutral', 'pTRel', 'relIso']:
            ax.set_yscale('log')
        ax.legend(loc='best')
        plt.xlabel(p)
        plt.ylabel('Normalized to unity')
        plt.savefig(options.path+'pics/feature_'+p+'.pdf')
        plt.close()

def getconf(custom):

    defs = {'booster':'gbtree', 'tree_method':'auto', 'sampling_method':'uniform', \
    'base_score':'0.5', 'colsample_bylevel':'1', 'colsample_bytree':'1', \
    'colsample_bynode':'1', 'gamma':'0', 'learning_rate':'0.1', \
    'max_delta_step':'0', 'min_child_weight':'1', 'missing':np.nan, \
    'objective':'binary:'+options.objective, 'reg_alpha':'0', 'reg_lambda':'1', \
    'scale_pos_weight':'1.', 'seed':'0', 'subsample':'1', \
    'eval_metric':'logloss', 'n_estimators':'1000', 'eta':'0.1', \
    'max_depth':'4'}
    
    for ik, k in enumerate(custom.keys()):
        if k in defs.keys():
            defs[k] = list(custom.values())[ik]
            
    return defs

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Train xgboost"

    parser = OptionParser(usage)
    parser.add_option("--cv", action="store_true", help="Perform cross validation [default: %default]")
    parser.add_option("--reweight", action="store_true", help="Reweight in lepton pT [default: %default]")
    parser.add_option("--presel", action="store_true", help="Apply preselection [default: %default]")
    parser.add_option("--outliers", action="store_true", help="Filter outliers [default: %default]")
    parser.add_option("--lowstats", action="store_true", help="Use only a handful of files [default: %default]")
    parser.add_option("--chan", default="elec", help="Lepton type [default: %default]")
    parser.add_option("--year", default="UL16APV", help="Year of data taking [default: %default]")
    parser.add_option("--path", default="/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/", help="Output path [default: %default]")
    parser.add_option("--definition", default="n_estimators-2000__max_depth-4__eta-0.1__gamma-5__min_child_weight-500", help="Configuration of BDT [default: %default]")
    parser.add_option("--iterations", type=int, default=1000, help="Number of iterations in the cross validation [default: %default]")
    parser.add_option("--test", type=float, default=0.5, help="Fraction of events to be used for testing the model [default: %default]")
    parser.add_option("--nmax", type=int, default=100000, help="Maximum number of events to be used either for training or testing [default: %default]")
    parser.add_option("--njob", type=int, default=16, help="Number of parallel jobs [default: %default]")
    parser.add_option("--metrics", default="aucdiff", help="Scoring metrics in cross validation (auc, aucdiff) [default: %default]")
    parser.add_option("--selection", default="pt10toInf", help="Lepton selection (pt10toInf, pt10to25, pt25toInf) [default: %default]")
    parser.add_option("--version", default="v2", help="Version to train (v1, v2, FLIPv1, FLIPv2, PUPv1, PUPv2, TAUv1, TAUv2, TAUPUPv1, TAUPUPv2) [default: %default]")
    parser.add_option("--objective", default="logistic", help="Logistic response (logistic, logitraw) [default: %default]")
    parser.add_option("--stop", type=int, default=10, help="Early stopping rounds in final fit [default: %default]")
    parser.add_option("--config", default="TOP", help="Training configuration (TOP, 4TOP) [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':
    
    options = main()

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 150)
    
    year = 'UL'+options.year[2:]
    
    params = {'legend.fontsize': 'x-large', 'axes.titlesize': 72, 'figure.titlesize': 'small', 'legend.frameon': False, 'figure.constrained_layout.use': True}
    pylab.rcParams.update(params)
    
    sb.set(style="white")
    
    var = ['pt', 'eta', 'trackMultClosestJet', \
    'miniIsoCharged', 'miniIsoNeutral', 'pTRel', \
    'ptRatio', 'relIso', 'bTagDeepJetClosestJet', 'sip3d', \
    'dxylog', 'dzlog', 'mvaIdFall17v2noIso', 'missHits' \
    ]
    if 'PUP' in options.version: var = ['puppiCombIso' if v=='relIso' else v for v in var]
    if 'v1' in options.version: var.remove('missHits')
    if options.chan == 'muon':
        var = [v if (v != 'mvaIdFall17v2noIso') else 'segmentCompatibility' for v in var]
        if 'missHits' in var: var.remove('missHits')
    print('Input features:', var)
    
    varout = ['pt', 'eta', 'trackMultClosestJet', \
    'miniIsoCharged', 'miniIsoNeutral', 'pTRel', \
    'ptRatio', 'relIso', 'bTagClosestJet', 'sip3d', \
    'dxylog', 'dzlog', 'idSeg', 'medHit' \
    ]
    if options.chan == 'muon' or 'v1' in options.version: varout.remove('medHit')
    if 'PUP' in options.version: varout = ['puppiCombIso' if v=='relIso' else v for v in varout]
    print('Output features:', varout)
    
    os.system('rm -rf '+options.path+'pics; mkdir '+options.path+'pics')
    config = {}
    dcus = options.definition.split('__')
    for d in dcus:
        name = d.split('-')[0]
        val = d.split('-')[1]
        config[name] = val
    conf = getconf(config)

    prompt = ['Prompt']
    if 'FLIP' in options.version: prompt += ['PromptFlip']
    if 'TAU' in options.version: prompt += ['PromptTau']
    if options.chan == 'elec': nonprompt = ['NonpromptHF', 'NonpromptLF', 'NonpromptConv', 'NonpromptPileup']
    else: nonprompt = ['NonpromptHF', 'NonpromptLF', 'NonpromptPileup']
    
    tagname = options.config+'-UL' if 'v1' in options.version else options.config+'-UL ('+options.version+')'

    print('Read data ..')
    ffsig, ffbkg = [], []
    fdir = '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/jobs_train_'+year+'_splitfine'
    mini = 'MiniAOD2017'
    if year == 'UL16': mini = 'MiniAOD2016'
    elif year == 'UL16APV': mini = 'MiniAOD2016APV'
    elif year == 'UL18': mini = 'MiniAOD2018'
    fs = "2" if options.lowstats else "*"
    if options.config == 'TOP':
        print('Configure TOP training')
        if year == 'UL17':
            ffsig.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        elif year == 'UL18':
            ffsig.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        elif year == 'UL16':
            ffsig.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        elif year == 'UL16APV':
            ffsig.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v2_"+year+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
            ffsig.append(glob.glob(fdir+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
    elif options.config == '4TOP':
        print('Configure 4TOP training')
        ffsig.append(glob.glob(fdir+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
    else:
        print('Unknown config:', options.config)
        sys.exit()
    if year == 'UL17':
        ffbkg.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
    elif year == 'UL18':
        ffbkg.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v2_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
    elif year == 'UL16':
        ffbkg.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
    elif year == 'UL16APV':
        ffbkg.append(glob.glob(fdir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
        ffbkg.append(glob.glob(fdir+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_crab_"+mini+"-v1_"+year+"_"+fs+".root"))
    fsig, fbkg = [], []
    for ff in ffsig:
        fsig.append([])
        for p in prompt:
            fsig[-1] += [f+':'+options.chan+p for f in ff]
    for ff in ffbkg:
        fbkg.append([])
        for p in nonprompt:
            fbkg[-1] += [f+':'+options.chan+p for f in ff]
    sig = [uproot4.lazy(f) for f in fsig]
    nsig = min(min([len(f) for f in sig]), int(options.nmax/len(fsig)))
    sig = [f[:nsig] for f in sig]
    bkg = [uproot4.lazy(f) for f in fbkg]
    nbkg = min(min([len(f) for f in bkg]), int(options.nmax/len(fbkg)))
    bkg = [f[:nbkg] for f in bkg]
    nsig = sum([len(s) for s in sig])
    nbkg = sum([len(b) for b in bkg])
    print('Initial statistics: Signal='+str(nsig)+', Background='+str(nbkg))
    
    if options.selection != "":
        for it, t in enumerate([sig, bkg]):
            for itt, tt in enumerate(t):
                if options.selection == 'pt10toInf': cut = np.array(tt['pt'] > 10)
                elif options.selection == 'pt25toInf': cut = np.array(tt['pt'] > 25)
                elif options.selection == 'pt10to25': cut = np.array(tt['pt'] > 10) & np.array(tt['pt'] < 25)
                else:
                    print('Uknown selection specified')
                    sys.exit()
                if options.presel or 'v1' in options.version: cut &= np.array(tt['passedPresel'] == 1)
                if 'v2' in options.version:
                    if options.chan == 'muon': cut &= np.array(tt['POGMedium'] == 1)
                    cut &= np.array(np.abs(tt['sip3d']) < 15.)
                    cut &= np.array(tt['relIso'] < 1.)
                if it == 0: sig[itt] = tt[cut]
                else: bkg[itt] = tt[cut]
    nsig = sum([len(s) for s in sig])
    nbkg = sum([len(b) for b in bkg])
    print('Selected: Signal='+str(nsig)+', Background='+str(nbkg))
    
    datasig, databkg = [], []
    
    for s in sig:
        datasig.append({})
        for iv, v in enumerate(var):
            datasig[-1][var[iv]] = s[v]
    dfsig = pd.concat([pd.DataFrame(data) for data in datasig], ignore_index=True, sort=False)

    for s in bkg:
        databkg.append({})
        for iv, v in enumerate(var):
            databkg[-1][var[iv]] = s[v]
    dfbkg = pd.concat([pd.DataFrame(data) for data in databkg], ignore_index=True, sort=False)
    
    dfsig['flag'] = 1
    dfbkg['flag'] = 0
    df = pd.concat([dfsig, dfbkg], ignore_index=True)
    missval = list(df.isnull().sum())
    for ic, c in enumerate(df.columns.values.tolist()):
        if missval[ic] > 0:
            print('Found missing values in '+c)
            sys.exit()
    
    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=options.test, random_state=int(conf['seed']))
    print('train+validation='+str(len(y_train))+', test='+str(len(y_test)))
    if options.outliers:
        ee = EllipticEnvelope(contamination=0.001, support_fraction=0.5)
        yhat = ee.fit_predict(X_train)
        mask = (yhat != -1)
        X_train, y_train = X_train[mask], y_train[mask]
        print('train+validation(cleaned)='+str(len(y_train))+', test='+str(len(y_test)))
    plot_correlation(X_train, tagname)
    X_train_sig = X_train[y_train == 1]
    X_train_bkg = X_train[y_train == 0]    
    plot_features(X_train_sig, X_train_bkg)
    
    conf['scale_pos_weight'] = sum(np.ones(len(X_train_bkg)))/sum(np.ones(len(X_train_sig)))

    if options.cv:
        kfold = 3
        cv = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=int(conf['seed']))
        cvtestb = []
        for _, test_index in cv.split(X_test, y_test):
            cvtestb.append([X_test.values[test_index], y_test.values[test_index]])
    
    if options.reweight:
        print('Reweight ..')
        weights = reweight(X_train, y_train)
        print('train+validation(reweight)='+str(len(y_train))+', test='+str(len(y_test)))
    
    print('Train ..')
    xgbc = set_xgbc(conf)

    if options.cv:
        param_dist = {}
        param_dist['all'] = {'max_depth': [3, 4, 5, 6], \
        'n_estimators': [100, 250, 500, 1000], \
        'min_child_weight': [1., 50., 100.], \
        'gamma': [0., 5., 10.] \
        }
        metrics = 'AUC'
        scoring = {'LogLoss': 'neg_log_loss', 'AUC': 'roc_auc', 'ACC': 'balanced_accuracy'}
        for p in param_dist:
            xgbcv = RandomizedSearchCV(xgbc, param_distributions=param_dist[p], \
            cv=cv, scoring=scoring, refit=False, n_iter=options.iterations, verbose=10, return_train_score=True)
            xgbcv.fit(X_train, y_train)
            print('##### Tuning: '+p+' #####')
            scores = []
            for it in range(len(xgbcv.cv_results_['mean_test_AUC'])):
                mean_test_AUC = xgbcv.cv_results_['mean_test_AUC']
                mean_train_AUC = xgbcv.cv_results_['mean_train_AUC']
                diffauc = abs(mean_test_AUC[it]-mean_train_AUC[it])/mean_train_AUC[it]
                if options.metrics == 'auc': score = mean_test_AUC[it]
                elif options.metrics == 'aucdiff': score = mean_test_AUC[it]*(1.-diffauc)
                else:
                    print('Unknown metrics:', options.metrics)
                    sys.exit()
                scores.append(score)
            restbest = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
            for m in restbest:
                diffauc = abs(xgbcv.cv_results_['mean_test_AUC'][m]-xgbcv.cv_results_['mean_train_AUC'][m])/xgbcv.cv_results_['mean_train_AUC'][m]
                print('Model #'+str(m))
                print('Scoring =', scores[m])
                print('Mean AUC =', xgbcv.cv_results_['mean_test_AUC'][m])
                print('Diff AUC =', diffauc)
                print('Mean ACC =', xgbcv.cv_results_['mean_test_ACC'][m])
                print('Mean LogLoss =', xgbcv.cv_results_['mean_test_LogLoss'][m])
                print('Mean fit time =', xgbcv.cv_results_['mean_fit_time'][m])
                print('Parameters =', xgbcv.cv_results_['params'][m])
                print('-----')
            parambest = xgbcv.cv_results_['params'][restbest[0]]
            for c in conf.keys():
                if c in parambest.keys(): conf[c] = str(parambest[c])
            xgbc = set_xgbc(conf)

    eval_set = [(X_train, y_train), (X_test, y_test)]
    
    xgbc.fit(X_train, y_train,
             eval_metric=['auc', 'error', 'logloss'],
             eval_set=eval_set,
             early_stopping_rounds=options.stop, # on logloss (last element in eval_metric)
             verbose=True)

    results = xgbc.evals_result()
    epochs = len(results['validation_0']['error'])
    plot_learning_curve(results, epochs, tagname)
    plot_classification_error(results, epochs, tagname)
    plot_importance(xgbc)
    
    bst = xgbc.get_booster()
    bst.save_model(options.path+'xgb.bin')
    bst.dump_model(options.path+'xgb.txt')
    pickle.dump(xgbc, open(options.path+'xgb.pkl', "wb"), protocol=2) # dump in python2

    print('Test ..')
    
    xgbc = xgb.Booster()
    xgbc.load_model(options.path+'xgb.bin')
        
    #        columns=["dxy", "miniIsoCharged", "miniIsoNeutral", "pTRel", "sip3d", "idSeg", "ptRatio", "bTagClosestJet", "pt", "trackMultClosestJet", "eta", "dz", "relIso"]
    #        df = pd.DataFrame(\
    #        columns=columns, \
    #        data=[[0.001100,0.000000,0.0,14.459858,0.991693,0.978643,0.971481,0.005874,52.270103,1,2.204103,-0.004022,0.000000]])
    #        x = xgb.DMatrix(df, feature_names=varout)
    #        x = xgb.DMatrix(df, feature_names=columns)
    #        res = xgbc.predict(x)
    #        print(res)
    #        sys.exit()

    #r.TMVA.Experimental.SaveXGBoost(xgbc, "model", "tmva.root")
        
#    xtt = X_test.loc[[0]]
#    x = xgb.DMatrix(xtt, feature_names=varout)

    x = xgb.DMatrix(X_test, feature_names=varout)
    y_test_pred = xgbc.predict(x)
    if options.objective == 'logitraw': y_test_pred = norm(y_test_pred)
    x = xgb.DMatrix(X_train, feature_names=varout)
    y_train_pred = xgbc.predict(x)
    if options.objective == 'logitraw': y_train_pred = norm(y_train_pred)
    if options.cv:
        ycv_test_pred = []
        for icv in range(len(cvtestb)):
            xcv = xgb.DMatrix(cvtestb[icv][0], feature_names=varout)
            ycv_test_pred.append(xgbc.predict(xcv))
            if options.objective == 'logitraw': ycv_test_pred = norm(ycv_test_pred)
        
    sig_test, bkg1_test, sig_train, bkg1_train = ([] for _ in range(4))
    sigresp_test, bkg1resp_test, sigresp_train, bkg1resp_train = ([] for _ in range(4))
    
    for iy, y in enumerate(y_test):
        if y == 1:
            sig_test.append(y)
            sigresp_test.append(y_test_pred[iy])
        else:
            bkg1_test.append(y)
            bkg1resp_test.append(y_test_pred[iy])

    for iy, y in enumerate(y_train):
        if y == 1:
            sig_train.append(y)
            sigresp_train.append(y_train_pred[iy])
        else:
            bkg1_train.append(y)
            bkg1resp_train.append(y_train_pred[iy])
            
    rocs = []
    data = [['train', y_train, y_train_pred, sigresp_train, bkg1resp_train], ['test', y_test, y_test_pred, sigresp_test, bkg1resp_test]]
    
    for d in data:
        fpr, tpr, ths = roc_curve(d[1], d[2])
        roc_auc = auc(fpr, tpr)
        rocs.append([d[0], fpr, tpr, roc_auc, d[3], d[4], ths])
        
    plot_roc(rocs, tagname)
    plot_overtrain(rocs, tagname)
    
    if options.cv:
        
        sig_cvtest, bkg1_cvtest = [], []
        sigresp_cvtest, bkg1resp_cvtest = [], []
        rocscv = []

        for icv in range(len(cvtestb)):
            sig_cvtest.append([])
            bkg1_cvtest.append([])
            sigresp_cvtest.append([])
            bkg1resp_cvtest.append([])
        
            for iy, y in enumerate(cvtestb[icv][1]):
                if y == 1:
                    sig_cvtest[-1].append(y)
                    sigresp_cvtest[-1].append(ycv_test_pred[icv][iy])
                else:
                    bkg1_cvtest[-1].append(y)
                    bkg1resp_cvtest[-1].append(ycv_test_pred[icv][iy])
            
            d = ['testcv'+str(icv), cvtestb[icv][1], ycv_test_pred[icv], sigresp_cvtest[icv], bkg1resp_cvtest[icv]]
            fpr, tpr, _ = roc_curve(d[1], d[2])
            roc_auc = auc(fpr, tpr)
            rocscv.append([d[0], fpr, tpr, roc_auc, d[3], d[4]])
            
        plot_roc(rocscv, tagname, cv=True)
    
#        mod = xgb.Booster()
#        mod.load_model('xgb.bin')
#        df = pd.DataFrame(\
#        columns=["dxy", "miniIsoCharged", "miniIsoNeutral", "pTRel", "sip3d", "idSeg", "ptRatio", "bTagClosestJet", "pt", "trackMultClosestJet", "eta", "dz", "relIso"], \
#        data=[[0.0005832,0.0100824,0.0230920,8.3642292,0.8218691,1,0.8491282,0.0467907,44.239578,1,-0.658110,0.0021321,0.0323947]])
#        x = xgb.DMatrix(df, feature_names=varout)
#        res = mod.predict(x)
#        print(res)
