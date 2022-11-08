import numpy as np

Parameters = {
    'Phi_0'    : 'fixed',
    'Phi_1'    : 'fixed',
    'conc'     : {'dynamic': 'ball2sticks',
                  'params': ['s0', 'd', 'th1', 'ph1', 'f1', 'th2', 'ph2', 'f2']},
    'eps'      : 'fixed',
    'gamma'    : 'fixed',
    'sigma'    : 'fixed',
    'baseline' : 'fixed'
}

Bounds = {
    's0'       : (0, None),
    'd'        : (0, 3.),
    'f1'       : (0, 1.),
    'f2'       : (0, .5),
}


# forward model is ball and stick
def ball2sticks(p, t):
    bvals = np.linalg.norm(t, axis=1)
    bvecs = np.asarray([tt/bb if bb > 0 else tt for tt, bb in zip(t, np.linalg.norm(t, axis=1))])
    s0, d, th1, ph1, f1, th2, ph2, f2 = p
    s = (1-f1-f2)*np.exp(-bvals*d)
    for th, ph, f in zip([th1, th2], [ph1, ph2], [f1, f2]):        
        x = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
        ang = np.sum(x[np.newaxis, :] * bvecs, axis=1)**2
        s += f*np.exp(-bvals*d*ang)
    return s0*s


def ball2sticks_grad(p, t):
    bvals = np.linalg.norm(t, axis=1)
    bvecs = np.asarray([tt/bb if bb > 0 else tt for tt, bb in zip(t, np.linalg.norm(t, axis=1))])
    s0,d,th1,ph1,f1,th2,ph2,f2 = p
    Eiso = np.exp(-bvals*d)
    s    = (1-f1-f2)*Eiso
    dsdd = -bvals*s
    
    th_ph_f = zip([th1,th2],[ph1,ph2],[f1,f2])
    dsdth,dsdph,dsdf = [],[],[]
    for i,(th,ph,f) in enumerate(th_ph_f):        
        st,ct = np.sin(th),np.cos(th)
        sp,cp = np.sin(ph),np.cos(ph)
        x     = np.array([st*cp,st*sp,ct])
        dp    = np.sum(x[np.newaxis,:]*bvecs,axis=1)
        ang   = dp**2
        
        EXP     = np.exp(-bvals*d*ang)
        dsdang  = -bvals*f*d*EXP
        dangdth = 2.*dp*( ct*cp*bvecs[:,0]+ct*sp*bvecs[:,1]-st*bvecs[:,2]) 
        dangdph = 2.*dp*(-st*sp*bvecs[:,0]+st*cp*bvecs[:,1]) 
                
        dsdth.append(dsdang*dangdth)
        dsdph.append(dsdang*dangdph)
        dsdf.append(EXP)
        
        dsdd += -bvals*f*ang*EXP
        
        s += f*EXP

    dsds0  = s
    dsdd  *= s0
    dsdth1 = dsdth[0]*s0
    dsdph1 = dsdph[0]*s0
    dsdf1  = (dsdf[0]-Eiso)*s0
    dsdth2 = dsdth[1]*s0
    dsdph2 = dsdph[1]*s0
    dsdf2  = (dsdf[1]-Eiso)*s0
    
    return np.array([dsds0,dsdd,dsdth1,dsdph1,dsdf1,dsdth2,dsdph2,dsdf2])
    
