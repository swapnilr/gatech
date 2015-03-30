from lk_flow import lk_flow
import pyramid
import warp
import numpy as np

def hierarchical_lk(init, final, levels=4):
    Lk = pyramid.gaussPyramid(init,levels)
    Rk = pyramid.gaussPyramid(final, levels)
    #for i in range(levels):
    #    Lk = pyramid.reduce(Lk)
    #    Rk = pyramid.reduce(Rk)
    U = np.zeros(Lk[-1].shape, dtype=np.float32)
    V = np.zeros(Lk[-1].shape, dtype=np.float32)
    for i in range(levels,-1,-1):
        print U.shape, V.shape, Lk[i].shape
        Wk = warp.warp(Lk[i], -U, -V).astype(np.float32)
        print Wk.dtype, Rk[i].dtype
        Dx, Dy = lk_flow(Wk, Rk[i].astype(np.float32))
        U = U + Dx
        V = V + Dy
        U = pyramid.expand(U) * 2
        V = pyramid.expand(V) * 2
    return U,V
