from gettext import dpgettext
from matplotlib.pyplot import title
import periodogram_properties as pprop
import matplotlib.pylab as plt
import numpy as np

def get_lc(ticid: int,zoom=0,save=False):
    lc = pprop.searchNstitch(ticid=ticid)
    lc.plot(color='k')

def lc_plot_sector_by_sector(ticid: int):
    ticstr = 'TIC '+str(ticid) 
    search_results = lk.search_lightcurve(ticstr, radius=None, 
                                      exptime='short', cadence=None, 
                                      mission='TESS', author='SPOC', 
                                      quarter=None, month=None, 
                                      campaign=None, 
                                      sector=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), 
                                      limit=None)
    lc = search_results.download_all(quality_bitmask='default', download_dir=None, cutout_size=None)
    
    

def automator(ticid: int,save=False,period='None'):
    """automates the plotter

    Args:
        ticid (int): 16 digit TESS target id
    """    
    fig = plt.subplots()
    
    lc = pprop.searchNstitch(ticid=ticid)
    ls,bls = pprop.genp(lc.flatten())
    
    lc.plot(title='Light curve')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_lc.eps')
    
    fig2,ax = plt.subplots(2)
    ls.plot(scale='log',title='LS periodogram',ax=ax[0],color='k')
    bls.plot(scale='log',title='BLS periodogram',ax=ax[1],color='k',view='frequency')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_per.eps')

    ls_period,bls_period,t0,dur = pprop.getLSparams(ls,bls)
    print("LS Period : {}\nBLS Period : {}\nT0 : {}\nTransit duration : {}".format(ls_period,bls_period,t0,dur))

    fig3,ax = plt.subplots(2)
    lc.fold(period=ls_period,normalize_phase=True).plot(ax=ax[0],color='k')
    if period=='None':
        lc.fold(period=bls_period,epoch_time=t0,normalize_phase=True).plot(ax=ax[1],color='k')
    else:
        lc.fold(period=period,epoch_time=t0,normalize_phase=True).plot(ax=ax[1],color='k')
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_fold.eps')

    fig4,ax = plt.subplots()
    lc.fold(period=ls_period,epoch_time=t0).plot_river()
    if save:
        plt.savefig('TIC'+str(ticid)+'_ls_riverplot.eps',dpi=200)
            
    fig5,ax = plt.subplots()
    lc.fold(period=bls_period,epoch_time=t0).plot_river()
    plt.tight_layout()
    if save:
        plt.savefig('TIC'+str(ticid)+'_bls_riverplot.eps',dpi=200)
        
def lc_plot_sector_by_sector(ticid: int,sigma_plot = 0.1):
    ticstr = 'TIC '+str(ticid) 
    search_results = lk.search_lightcurve(ticstr, radius=None, 
                                      exptime='short', cadence=None, 
                                      mission='TESS', author='SPOC', 
                                      quarter=None, month=None, 
                                      campaign=None, 
                                      sector=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), 
                                      limit=None)
    lc = search_results.download_all(quality_bitmask='default', download_dir=None, cutout_size=None)
    len_sector = len(lc.sector)

    Tot = len_sector
    Cols = 2

    Rows = Tot // Cols 
    Rows += Tot % Cols

    Position = range(Tot)    
    
    mins = []
    maxs = []
    for i in range(Tot):
        mins.append(np.nanmin(np.array(lc[i].flux)))
        maxs.append(np.nanmax(np.array(lc[i].flux)))
    
    minY = np.nanmin(np.array(mins)) - sigma_plot*np.nanstd(np.array(mins))
    maxY = np.nanmax(np.array(maxs)) + sigma_plot*np.nanstd(np.array(maxs))
    
    print("Row : %d\nCol : %d\nTot : %d"%(Rows,Cols,Tot))
    print()
    fig = plt.figure(1)
    fig.suptitle('TIC '+str(ticid))
    for k in range(Tot):
        if (k!=Tot):
            pos = k+1
        else:
            pos = k
        ax = fig.add_subplot(Rows,Cols,pos)
        lc[k].plot(color='k',ax=ax,label='')
        ax.set_ylabel('S' + str(lc.sector[k]).zfill(2))
        ax.set_ylim(minY,maxY)
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))