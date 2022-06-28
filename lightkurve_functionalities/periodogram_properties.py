import lightkurve as lk


def searchNstitch(ticid: int):
    """returns lightkurve.LightCurve object from ticid
    
    searches and downloads for TESS SPOC 2 minute light curves 

    Args:
        ticid (int): 16 digit code of object
    """    
    ticstr = 'TIC '+str(ticid) 
    search_results = lk.search_lightcurve(ticstr, radius=None, 
                                      exptime='short', cadence=None, 
                                      mission='TESS', author='SPOC', 
                                      quarter=None, month=None, 
                                      campaign=None, 
                                      sector=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), 
                                      limit=None)
    lc = search_results.download_all(quality_bitmask='default', download_dir=None, cutout_size=None)
    lc = lc.stitch()    
    return(lc)

def genp(lk_obg: object):
    """lomb scargle and BLS periodograms from lightkurve.LightCurve

    Args:
        lk_obg (object): lightkurve.LightCurve object

    Returns:
        _type_: ls and bls periodogram
    """    
    ls_pg = lk_obg.to_periodogram()
    bls_pg = lk_obg.to_periodogram(method='bls',frequency_factor=100)
    return ls_pg,bls_pg

def getLSparams(ls_obj: object,bls_obj: object):
    """returns transit properties

    Args:
        ls_obj (object): lomb-scargle periodogram
        bls_obj (object): bls periodogram

    Returns:
        _type_: _description_
    """    
    ls_period = ls_obj.period_at_max_power
    bls_period = bls_obj.period_at_max_power
    bls_t0 = bls_obj.transit_time_at_max_power
    bls_dur = bls_obj.duration_at_max_power
    return ls_period,bls_period,bls_t0,bls_dur

