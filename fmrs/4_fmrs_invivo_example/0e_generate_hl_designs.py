import numpy as np
import subprocess
import tempfile

des_mat = np.zeros((26, 14), int)
des_mat[:13, 0] = 1
des_mat[13:, 0] = -1
des_mat[:13, 1:] = np.eye(13)
des_mat[13:, 1:] = np.eye(13)
print(des_mat)

with tempfile.NamedTemporaryFile() as tmp:
    np.savetxt(tmp.name, des_mat)
    subprocess.run(['Text2Vest', str(tmp.name), 'misc/design.mat'])

con_mat = np.zeros((2, 14), int)
con_mat[0, 0] = 1
con_mat[1, 0] = -1
print(con_mat)

with tempfile.NamedTemporaryFile() as tmp2:
    np.savetxt(tmp2.name, con_mat)
    subprocess.run(['Text2Vest', str(tmp2.name), 'misc/design.con'])

# Group average designs
des_mat = np.zeros((26, 2), int)
des_mat[:13, 0] = 1
des_mat[13:, 1] = 1
print(des_mat)

with tempfile.NamedTemporaryFile() as tmp:
    np.savetxt(tmp.name, des_mat)
    subprocess.run(['Text2Vest', str(tmp.name), 'misc/design_ga.mat'])

con_mat = np.zeros((4, 2), int)
con_mat[0, 0] = 1
con_mat[1, 0] = -1
con_mat[2, 1] = 1
con_mat[3, 1] = -1
print(con_mat)

with tempfile.NamedTemporaryFile() as tmp2:
    np.savetxt(tmp2.name, con_mat)
    subprocess.run(['Text2Vest', str(tmp2.name), 'misc/design_ga.con'])
