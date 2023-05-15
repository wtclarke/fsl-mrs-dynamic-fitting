Parameters = {
   'conc'     : {
        'MM_WT_': {'dynamic': 'model_exp',   'params': ['c_amp', 'c_mono_adc']},
        'other' : {'dynamic': 'model_biexp', 'params': ['c_amp', 'c_adc_slow', 'c_adc_fast', 'c_frac_slow']}
        },
   'baseline' : {'dynamic': 'model_exp_offset', 'params': ['b_amp', 'b_adc', 'b_off']}
}


Bounds = {
    'c_amp'       : (0, None),
    'c_mono_adc'  : (0, None),
    'c_adc_slow'  : (0, .1),
    'c_adc_fast'  : (.1, 4),
    'c_frac_slow' : (0, 1),
    'gamma'       : (0, None),
    'sigma'       : (0, None),
    'b_amp'       : (None, None),
    'b_adc'       : (1E-5, 3),
}

# Dynamic models
from numpy import exp
from numpy import asarray
from numpy import ones_like

# Mono-exponential
def model_exp(p, t):
    # p = [amp,adc]
    return p[0]*exp(-p[1]*t)

# Mono-exponential model with offset
def model_exp_offset(p, t):
    # p = [amp,adc,off]
    return p[2]+p[0]*exp(-p[1]*t)

# Bi-exponential model
def model_biexp(p, t):
    # p = [amp,adc1,adc2,frac]
    return p[0]*(p[3]*exp(-p[1]*t)+(1-p[3])*exp(-p[2]*t))

# Gradients
# For each of the models defined above, specify the gradient
def model_exp_grad(p,t):
    e1 = exp(-p[1]*t)
    g0 = e1
    g1 = -t*p[0]*e1
    return asarray([g0,g1], dtype=object)

def model_biexp_grad(p,t):
    e1 = exp(-p[1]*t)
    e2 = exp(-p[2]*t)
    g0 = p[3]*e1+(1-p[3])*e2
    g1 = p[0]*(-p[3]*t*e1)
    g2 = p[0]*(-(1-p[3])*t*e2)
    g3 = p[0]*(e1-e2)
    return asarray([g0,g1,g2,g3])

def model_exp_offset_grad(p,t):
    e1 = exp(-p[1]*t)
    g0 = e1
    g1 = -t*p[0]*e1
    g2 = ones_like(t)
    return asarray([g0,g1,g2], dtype=object)