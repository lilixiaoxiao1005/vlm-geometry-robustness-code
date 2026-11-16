"""Explicit rcParams matching the manuscript plotting styles."""
import matplotlib as mpl

def apply_readable(secondary=8.5):
    mpl.rcdefaults()
    mpl.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans','DejaVu Sans'], 'font.size':9, 'axes.labelsize':9, 'axes.titlesize':9, 'legend.fontsize':secondary, 'xtick.labelsize':8, 'ytick.labelsize':8, 'axes.linewidth':.6, 'xtick.direction':'out', 'ytick.direction':'out', 'xtick.major.size':3, 'ytick.major.size':3, 'xtick.major.width':.6, 'ytick.major.width':.6, 'axes.spines.top':False, 'axes.spines.right':False, 'axes.spines.left':True, 'axes.spines.bottom':True, 'axes.grid':False, 'legend.frameon':False, 'figure.dpi':200, 'savefig.dpi':300, 'savefig.bbox':None, 'axes.titleweight':'normal', 'axes.titlelocation':'left', 'axes.labelweight':'normal', 'lines.linewidth':1.2, 'patch.linewidth':.6, 'svg.fonttype':'none', 'pdf.fonttype':42, 'ps.fonttype':42, 'figure.facecolor':'white'})

def apply_ocean():
    mpl.rcdefaults()
    mpl.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'axes.titlesize':10.5,'legend.fontsize':8.5,'xtick.labelsize':8,'ytick.labelsize':8,'axes.linewidth':.8,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
