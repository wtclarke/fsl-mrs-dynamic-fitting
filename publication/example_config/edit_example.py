# Parameter behaviour
# 'variable' : one per time point
# 'fixed'    : same for all time points
# 'dynamic'  : model-based change across time points

Parameters = {
   'conc'    : 'fixed',
   'eps'     : 'fixed',
   'gamma'   : 'fixed',
   'Phi_0'   : 'fixed',
   'Phi_1'   : 'fixed',
   'baseline': 'fixed',
}

Bounds = {
    'conc' : (0, None),
    'gamma': (0, None)
}
