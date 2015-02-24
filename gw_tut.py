__author__ = 'kiruba'
import sys
# import flopy.modflow as fmf
import flopy.modflow as fmf
import flopy.utils as fut
import numpy as np
import matplotlib.pyplot as plt
import fortranfile as ff
import flopy
print flopy.__version__

# from numpy import array
# h = array([[4., 5., 6., 7.],
#           [4., 0., 0., 7,],
#           [4., 0., 0., 7.],
#           [4., 5., 6., 7.]])
# dummy = h.shape
# nrow = dummy[0]
# ncol = dummy[1]
#
# print 'Head matrix is a ', nrow, 'by', ncol, 'matrix'
#
# ni = 1
# conv_crit = 1e-3
# converged = False
# w = 1.1
#
# while (not converged):
#     # max_err = 0
#     for r in range(1, nrow-1):
#         for c in range(1, ncol-1):
#             h_old = h[r, c]
#             print h_old
#             h[r, c] = (h[r-1, c] + h[r+1, c] + h[r, c-1] + h[r, c+1])/4
#             print h[r, c]
#             c_1 = h[r, c] - h_old
#             print c_1
#             h[r, c] += (w * c_1)
#             print h[r, c]
#             diff = h[r, c] - h_old
#             print diff
#             if diff < conv_crit:
#                 converged = True
#     ni = ni +1
#
# # while (not converged):
# #     max_err = 0
# #     for r in range(1, nrow-1):
# #         for c in range(1, ncol-1):
# #             h_old = h[r, c]
# #             h[r, c] = (h[r-1, c] + h[r+1, c] + h[r, c-1] + h[r, c+1])/4
# #             diff = h[r, c] - h_old
# #             if (diff > max_err):
# #                 max_err = diff
# #     if (max_err < conv_crit):
# #         converged = True
# #     ni += 1
# print 'Number of iterations = ', ni-1
# print h



name = 'lake_example'
h1 = 100
h2 = 90
Nlay = 10
N = 101
L = 400.0
H = 50.0
k = 1.0

ml = fmf.Modflow(modelname=name, exe_name='/home/kiruba/Downloads/Unix/src/mf2005', version='mf2005', model_ws='mf_files/')



bot = np.linspace(-H/Nlay,-H,Nlay)
delrow = delcol = L/(N-1)
dis = fmf.ModflowDis(ml,nlay=Nlay,nrow=N,ncol=N,delr=delrow,delc=delcol,top=0.0,botm=bot,laycbd=0)

Nhalf = (N-1)/2
ibound = np.ones((Nlay,N,N), 'int32')
ibound[:,0,:] = -1; ibound[:,-1,:] = -1; ibound[:,:,0] = -1; ibound[:,:,-1] = -1
ibound[0,Nhalf,Nhalf] = -1
start = h1 * np.ones((N,N))
start[Nhalf,Nhalf] = h2
bas = fmf.ModflowBas(ml,ibound=ibound,strt=start)
print "o"
lpf = fmf.ModflowLpf(ml, hk=k)
pcg = fmf.ModflowPcg(ml)
oc = fmf.ModflowOc(ml)
ml.write_input()
ml.run_model()

hds = fut.HeadFile(ml.model_ws+name+'.hds')
h = hds.get_data(kstpker=(1,1))
x = y = np.linspace(0, L, N)
a = ff.FortranFile("lake_example.hds",mode='r')
head = a.readReals()
xx = a.readInts()
c = plt.contour(x, y, head , np.arange(90, 100.1, 0.2))
plt.show()
print len(x)
print len(xx)
# # a = ff.FortranFile("lake_example.hds",mode='w')
# # a.writeReals(np.linspace(0,1,10))
# # a.close()
# # hds = fut.HeadFile('lake_example.hds')