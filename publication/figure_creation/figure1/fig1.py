import numpy as np
import matplotlib.pyplot as plt
RED='#99261E'
BLUE='#253999'
x = np.linspace(-20,20,300)
y1 = np.exp(-(x+5)**2/2/3)
y2 = np.exp(-(x-10)**2/2/3)
noise = np.random.randn(len(x))/20.
fig, ax = plt.subplots(nrows=3, ncols=1, sharey=True,sharex=True,figsize=(4,10))
ax[0].plot(x,y1+y2/2+noise,'.',c=[.5,.5,.5],markersize=2)
ax[1].plot(x,.5*(y1+y2/2)+noise,'.',c=[.5,.5,.5],markersize=2)
ax[2].plot(x,.1*(y1+y2/2)+noise,'.',c=[.5,.5,.5],markersize=2)

# ax[0].plot(x,y1+y2/2,'-',c=BLUE,linewidth=3)
# ax[1].plot(x,.5*(y1+y2/2),'-',c=BLUE,linewidth=3)
# ax[2].plot(x,.1*(y1+y2/2),'-',c=BLUE,linewidth=3)

ax[0].plot(x,y1+y2/2,'-',c=RED,linewidth=3)
ax[1].plot(x,.5*(y1+y2/2),'-',c=RED,linewidth=3)
ax[2].plot(x,.1*(y1+y2/2),'-',c=RED,linewidth=3)

fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0, top=0.9)
for i in [0,1,2]:
    fig.axes[i].set_axis_off() 
fig.savefig('fig1_component.pdf')
plt.show()