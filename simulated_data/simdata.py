import numpy
from scipy.stats import skewnorm
import matplotlib.pylab as plt
import seaborn as sns

def create_normal_flux(mu=1.0,std = 0.1,npts=100000):
    """create flux distributed normally

    Args:
        mu (float, optional): mean of the gaussian. Defaults to 1.0.
        std (float, optional): standard deviation of the gaussian. Defaults to 0.1.
        npts (int, optional): number of observation points. Defaults to 100000.

    Returns:
        _type_: normally distributed simulated flux
    """    
    norm_flux = numpy.random.normal(mu, std, npts)
    return norm_flux

def create_skewed_flux(mu=1.0,std=0.1,npts=100000,a=-1.0):
    """skew a normally distributed flux

    Args:
        mu (float, optional): mean of the gaussian. Defaults to 1.0.
        std (float, optional): standard deviation of the gaussian. Defaults to 0.1.
        npts (int, optional): number of observation points. Defaults to 100000.
        a (float, optional): skew (negative for left skewed, positive for right skewed). Defaults to -1.0.

    Returns:
        _type_: _description_
    """    
    norm_flux = create_normal_flux(mu=mu,std=std,npts=npts)
    skew_flux = skewnorm.pdf(norm_flux,a=a)
    return skew_flux


    