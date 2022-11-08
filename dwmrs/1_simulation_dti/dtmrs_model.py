# ------------------------------------------------------------------------
# User file for defining a model

# Parameter behaviour
# 'variable' : one per time point
# 'fixed'    : same for all time points
# 'dynamic'  : model-based change across time points

# Each parameter of the spectral fitting gets a specific behaviour
# The default behaviour is 'fixed'
Parameters = {
   'Phi_0'    : 'fixed',
   'Phi_1'    : 'fixed',
   'conc'     : {'dynamic': 'model_dti', 
                 'params': ['c_amp', 'c_Dxx', 'c_Dyy', 'c_Dzz', 'c_Dxy', 'c_Dxz', 'c_Dyz']},
   'eps'      : 'fixed',
   'gamma'    : 'fixed',
   'sigma'    : 'fixed',
   'baseline' : 'fixed'
}

# Optionally define bounds on the parameters
Bounds = {
    'c_amp'   : (0, None),
    'c_Dxx'   : (0, None),
    'c_Dyy'   : (0, None),
    'c_Dzz'   : (0, None),
    'gamma'   : (0, None),
    'sigma'   : (0, None)
}

# Dynamic models here
# These define how the parameters of the dynamic models change as a function 
# of the time variable (in dwMRS, that is the bvalue)
from numpy import exp
from numpy import asarray
from numpy import ones_like
from numpy.linalg import norm


# dti model
#[Dxx, Dxy Dxz]
#[Dxy, Dyy Dyz]
#[Dxz, Dyz Dzz]
def model_dti(p, t):
    # p = [conc, Dxx, Dyy, Dzz, Dxy, Dxz, Dyz]
    # p = [p[0], p[1], p[2], p[3], p[4], p[5], p[6]]
    b = norm(t, axis=1)
    bvec = asarray([tt/bb if bb > 0 else tt for tt, bb in zip(t, norm(t, axis=1))])
    D = asarray([[[p[1], p[4], p[5]], [p[4], p[2], p[6]], [p[5], p[6], p[3]]]])

    return [p[0]*exp(-bb * tt.T @ D @ tt) for bb, tt in zip(b, bvec)]


# ------------------------------------------------------------------------
# Gradients
# For each of the models defined above, specify the gradient
# And call these functions using the same names as above with 
# '_grad' appended in the end
def model_dti_grad(p, t):
    bv = norm(t, axis=1)
    bvec = asarray([tt/bb if bb > 0 else tt for tt, bb in zip(t, norm(t, axis=1))]).T
    a = bvec[0]
    b = bvec[1]
    c = bvec[2]
    s = p[0]
    Dxx, Dyy, Dzz, Dxy, Dxz, Dyz = p[1], p[2], p[3], p[4], p[5], p[6]

    g0 = exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g1 = -a**2*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g2 = -b**2*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g3 = -c**2*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g4 = -2*a*b*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g5 = -2*a*c*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    g6 = -2*b*c*s*bv*exp(-bv*(Dxx*a**2 + 2*Dxy*a*b + 2*Dxz*a*c + Dyy*b**2 + 2*Dyz*b*c + Dzz*c**2))
    return asarray([g0, g1, g2, g3, g4, g5, g6])
