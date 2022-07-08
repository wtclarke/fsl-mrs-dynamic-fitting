# --------------------------------------------------------
# User file for defining a model

# Parameter behaviour
# 'variable' : one per time point
# 'fixed'    : same for all time points
# 'dynamic'  : model-based change across time points

Parameters = {
   'conc'    : 'fixed',
   'eps'     : 'fixed',
   'Phi_0'   : 'fixed',
   'Phi_1'   : 'fixed',
   'gamma'   : 'fixed',
   'sigma'   : 'fixed',
   'baseline': 'fixed',
}

Bounds = {
}
