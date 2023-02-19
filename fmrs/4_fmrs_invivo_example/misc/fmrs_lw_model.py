from numpy import dot

param_names = ['STIM0', 'STIM1', 'STIM2', 'STIM3', 'linear', 'constant']

Parameters = {
    'Phi_0'    : 'fixed',
    'Phi_1'    : 'fixed',
    'conc'     : {'dynamic': 'model_glm', 'params': param_names},
    'eps'      : 'fixed',
    'gamma'    : {'dynamic': 'model_glm', 'params': param_names},
    'sigma'    : 'fixed',
    'baseline' : 'fixed'
}

Bounds = {
    'sigma': (0, None),
    'constant': (0, None),
}


# --------- Dynamic models ---------
def model_glm(p, t):
    return dot(t, p)


# --------- Gradients --------------
def model_glm_grad(p, t):
    return t.T
