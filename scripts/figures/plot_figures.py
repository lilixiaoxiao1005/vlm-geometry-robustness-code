"""Portable transcriptions of the final manuscript figure scripts; Agg/CPU only."""
from pathlib import Path
import argparse, csv, hashlib, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'config' / 'plotting_style'))
from style import apply_readable

EXPECTED = {
 'stage31_condition_results_corrected.csv': 'd46ee44764b7611b7277dc83e6412b55d398a084b2a5fb55062c5b54dbdd8ca9',
 'stage30_four_group_metrics.csv': 'd7c316bd043ddcca38dbd92e1c69e341a6a5ccf27a464742ac6ee07dbe4979d4',
 'stage30_selective_risk.csv': 'c92fe9932d72f77243cf949be6aa78990080096875000773537d230fa80aaa7b',
}
def checked_file(path):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.name not in EXPECTED or digest != EXPECTED[path.name]:
        raise ValueError(f'Unexpected input or SHA-256: {path.name}: {digest}')
    return path

def load(path):
    with checked_file(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def save(fig,name):
    fig.savefig(HERE/(name+'.png'),dpi=300)
    fig.savefig(HERE/(name+'.svg'))
    plt.close(fig)

def figure4():
    groups=[('Oxford-IIIT Pet','ViT-B/32','Oxford B/32'),('Oxford-IIIT Pet','ViT-L/14','Oxford L/14'),('CIFAR-10','ViT-B/32','CIFAR-10 B/32'),('CIFAR-10','ViT-L/14','CIFAR-10 L/14')]
    colors={'ViT-B/32':'#51999F','ViT-L/14':'#ED8D5A'}
    fig,axs=plt.subplots(3,1,figsize=(3.14,5.65))
    fig.subplots_adjust(left=.30,right=.97,top=.91,bottom=.095,hspace=.68)
    for ax,(title,key) in zip(axs,[('NLL','nll'),('15-bin ECE','ece_15_equal_width'),('Multiclass Brier','brier_multiclass')]):
     for i,(dataset,model,label) in enumerate(groups):
      def value(state):
       found=[r for r in metrics if r['dataset']==dataset and r['model']==model and r['probability_state']==state and r['metric']==key]
       assert len(found)==1; return float(found[0]['value'])
      raw,cal=value('raw'),value('calibrated'); c=colors[model]
      ax.plot([raw,cal],[i,i],c=c,lw=1.7,zorder=1)
      ax.scatter(raw,i,s=34,facecolors='white',edgecolors=c,lw=1.2,zorder=2)
      ax.scatter(cal,i,s=25,marker='D',c=c,zorder=3)
     ax.set_yticks(range(4),[g[2] for g in groups]); ax.invert_yaxis(); ax.set_title(title,weight='bold',pad=4)
     ax.grid(axis='x',color='#dddddd',lw=.5); ax.tick_params(axis='y',length=0)
    ax.set_xlabel('Lower is better')
    handles=[Line2D([],[],marker='o',color='#52676B',markerfacecolor='white',ls='None',label='Raw'),Line2D([],[],marker='D',color='#52676B',ls='None',label='Temperature-scaled')]
    fig.legend(handles=handles,loc='upper center',ncol=2,bbox_to_anchor=(.57,.995),frameon=False)
    save(fig,'fig4_calibration_readable')

def figure10():
    groups=[('Oxford-IIIT Pet','ViT-B/32','Oxford B/32'),('Oxford-IIIT Pet','ViT-L/14','Oxford L/14'),('CIFAR-10','ViT-B/32','CIFAR-10 B/32'),('CIFAR-10','ViT-L/14','CIFAR-10 L/14')]
    colors={'ViT-B/32':'#51999F','ViT-L/14':'#ED8D5A'}
    labels=['Clean','R−10','R−5','R+5','R+10','Tx−10','Tx−5','Tx+5','Tx+10','Ty−10','Ty−5','Ty+5','Ty+10','S0.8','S0.9','S1.11','S1.25','Crop90','Crop80']
    base=[r for r in rows if r['dataset']==groups[0][0] and r['model']==groups[0][1] and r['probability_state']=='raw']
    conds=[r['condition'] for r in base]; assert len(conds)==19 and len(set(conds))==19
    lookup={(r['dataset'],r['model'],r['probability_state'],r['condition']):r for r in rows};assert len(lookup)==152
    fig,axes=plt.subplots(2,2,figsize=(6.46,7.15),sharex=True)
    fig.subplots_adjust(left=.12,right=.98,top=.965,bottom=.075,wspace=.48,hspace=.32)
    for ax,(d,m,title) in zip(axes.flat,groups):
     vals=sorted([(float(lookup[d,m,'raw',c]['error_auroc']),labels[i]) for i,c in enumerate(conds)])
     ax.scatter([v for v,_ in vals],range(19),s=17,c=colors[m]);ax.set_yticks(range(19),[label for _,label in vals]);ax.set_ylim(-.8,18.8)
     ax.axvline(.5,c='#52676B',ls='--',lw=.8);ax.set_xlim(.48,1.0);ax.set_title(title,weight='bold',pad=4)
     ax.grid(axis='x',alpha=.15);ax.tick_params(axis='y',length=0);ax.set_xlabel('Raw error AUROC')
    save(fig,'fig10_auroc_readable')

def figure_heat(selected):
    D=['Oxford-IIIT Pet','CIFAR-10'];M=['ViT-B/32','ViT-L/14'];G=[(d,m) for d in D for m in M];names=['Oxford B/32','Oxford L/14','CIFAR-10 B/32','CIFAR-10 L/14']
    base=[r for r in rows if r['dataset']==D[0] and r['model']==M[0] and r['probability_state']=='raw'];cond=[r['condition'] for r in base];assert len(cond)==19 and len(set(cond))==19
    labels=['Clean','R−10','R−5','R+5','R+10','Tx−10','Tx−5','Tx+5','Tx+10','Ty−10','Ty−5','Ty+5','Ty+10','S0.8','S0.9','S1.11','S1.25','Crop90','Crop80']
    lookup={(r['dataset'],r['model'],r['probability_state'],r['condition']):r for r in rows};assert len(lookup)==152
    teal='#51999F';orange='#ED8D5A'; famcols={'rotation':'#86B6A3','translation':'#4198AC','scaling':'#D8A258','crop':'#ED8D5A'}
    def matrix(field,state):return np.array([[float(lookup[d,m,state,c][field]) for c in cond] for d,m in G])
    def heat(values,name,diverging):
     fig,ax=plt.subplots(figsize=(6.46,3.0));fig.subplots_adjust(left=.16,right=.86,bottom=.32,top=.96)
     cm=LinearSegmentedColormap.from_list('ocean',[teal,'#ffffff',orange] if diverging else ['#EFF8F5','#86B6A3','#4198AC','#236978'])
     if diverging:
      bound=max(abs(float(values.min())),abs(float(values.max()))); im=ax.imshow(values,aspect='auto',cmap=cm,norm=TwoSlopeNorm(vmin=-bound,vcenter=0,vmax=bound))
     else:im=ax.imshow(values,aspect='auto',cmap=cm,vmin=float(values.min()),vmax=float(values.max()))
     ax.set_xticks(range(19),labels,rotation=90);ax.set_yticks(range(4),names)
     ax.set_xticks(np.arange(-.5,19,1),minor=True);ax.set_yticks(np.arange(-.5,4,1),minor=True);ax.grid(which='minor',color='white',lw=.6);ax.tick_params(which='minor',bottom=False,left=False)
     cb=fig.colorbar(im,ax=ax,pad=.02,shrink=.85);cb.set_label('Calibrated − raw' if diverging else 'Accuracy')
     save(fig,name)
    if selected in ('5', 'all'): heat(matrix('accuracy','raw'),'fig5_accuracy_readable',False)
    if selected in ('9', 'all'): heat(matrix('brier_multiclass','calibrated')-matrix('brier_multiclass','raw'),'fig8_brier_readable',True)

def figure7():
    D=['Oxford-IIIT Pet','CIFAR-10'];M=['ViT-B/32','ViT-L/14'];G=[(d,m) for d in D for m in M];names=['Oxford B/32','Oxford L/14','CIFAR-10 B/32','CIFAR-10 L/14']
    base=[r for r in rows if r['dataset']==D[0] and r['model']==M[0] and r['probability_state']=='raw'];cond=[r['condition'] for r in base];assert len(cond)==19 and len(set(cond))==19
    labels=['Clean','R−10','R−5','R+5','R+10','Tx−10','Tx−5','Tx+5','Tx+10','Ty−10','Ty−5','Ty+5','Ty+10','S0.8','S0.9','S1.11','S1.25','Crop90','Crop80']
    lookup={(r['dataset'],r['model'],r['probability_state'],r['condition']):r for r in rows};assert len(lookup)==152
    teal='#51999F';orange='#ED8D5A'; famcols={'rotation':'#86B6A3','translation':'#4198AC','scaling':'#D8A258','crop':'#ED8D5A'}
    families=['rotation','translation','scaling','crop'];fig,axes=plt.subplots(2,2,figsize=(6.46,4.35),sharex=True);fig.subplots_adjust(left=.09,right=.98,top=.95,bottom=.14,wspace=.34,hspace=.40)
    for ax,(d,m),title in zip(axes.flat,G,names):
     vals=[[float(r['nll']) for r in rows if r['dataset']==d and r['model']==m and r['probability_state']=='raw' and r['family']==fam] for fam in families];assert list(map(len,vals))==[4,8,4,2]
     bp=ax.boxplot(vals,positions=range(4),widths=.55,patch_artist=True,showfliers=False,medianprops={'color':'#253C45','linewidth':1.2})
     for patch,fam in zip(bp['boxes'],families):patch.set_facecolor(famcols[fam]);patch.set_alpha(.55);patch.set_edgecolor('#52676B')
     for j,(fam,v) in enumerate(zip(families,vals)):ax.scatter(j+np.linspace(-.12,.12,len(v)),v,c=famcols[fam],edgecolors='white',linewidth=.5,s=18,zorder=3)
     ax.set_title(title,weight='bold');ax.set_ylabel('Raw NLL');ax.set_xticks(range(4),['R','T','S','C']);ax.grid(axis='y',alpha=.15)
    fig.supxlabel('Rotation (R)   Translation (T)   Scaling (S)   Crop (C)',fontsize=8,y=.01)
    save(fig,'fig7_nll_readable')

def figure6():
    fig, axes = plt.subplots(1, 2, figsize=(6.46, 2.9), sharex=True, sharey=True)
    fig.subplots_adjust(left=.115, right=.98, bottom=.20, top=.73, wspace=.13)
    colors = {'ViT-B/32': '#51999F', 'ViT-L/14': '#ED8D5A'}
    for ax, dataset in zip(axes, ['Oxford-IIIT Pet', 'CIFAR-10']):
        for model, color in colors.items():
            for coverage, marker in [('0.8', 'o'), ('0.9', 'D')]:
                match = [r for r in rows if r['dataset'] == dataset and r['model'] == model and r['target_coverage'] == coverage]
                assert len(match) == 1
                ax.scatter(float(match[0]['actual_coverage']), float(match[0]['selective_risk']), marker=marker, color=color, s=35, edgecolors='white', linewidth=.5)
        ax.set_title(dataset, weight='bold')
        ax.set_xlim(.76, .93)
        ax.set_ylim(0, .13)
        ax.grid(alpha=.15)
        ax.set_xlabel('Actual Test coverage')
    axes[0].set_ylabel('Selective risk')
    handles = [Line2D([], [], marker='o', color=c, ls='None', label=m) for m, c in zip(['B/32', 'L/14'], colors.values())]
    handles += [Line2D([], [], marker=k, color='#52676B', ls='None', label=l) for k, l in [('o', '80% target'), ('D', '90% target')]]
    fig.legend(handles=handles, loc='upper center', ncol=4, bbox_to_anchor=(.5, .99), frameon=False)
    save(fig, 'fig6_selective_horizontal')
def main():
    global HERE, rows, metrics
    p=argparse.ArgumentParser(description='Rebuild final quantitative figures from verified aggregate files.')
    p.add_argument('--input-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--figures', nargs='+', choices=['4','5','6','7','9','10'], default=['4','5','6','7','9','10'])
    args=p.parse_args(); HERE=args.output_dir; HERE.mkdir(parents=True,exist_ok=True)
    wanted=set(args.figures)
    if wanted & {'5','7','9','10'}:
        rows=load(args.input_dir/'stage31_condition_results_corrected.csv')
        if len(rows)!=152: raise ValueError('Expected 152 condition records')
    if '4' in wanted: metrics=load(args.input_dir/'stage30_four_group_metrics.csv')
    if '6' in wanted:
        selective=load(args.input_dir/'stage30_selective_risk.csv')
        if len(selective)!=8: raise ValueError('Expected 8 selective operating points')
    for key in ['4','5','6','7','9','10']:
        if key not in wanted: continue
        apply_readable(8.3 if key in ('5','7','9') else 8.5)
        if key=='4': figure4()
        elif key in ('5','9'): figure_heat(key)
        elif key=='6': rows=selective; figure6()
        elif key=='7': figure7()
        elif key=='10': figure10()
        if key=='6' and wanted & {'7','9','10'}: rows=load(args.input_dir/'stage31_condition_results_corrected.csv')
        print('Generated figure',key)
if __name__=='__main__': main()
