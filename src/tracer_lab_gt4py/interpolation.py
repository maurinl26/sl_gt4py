from gt4py.cartesian.gtscript import stencil, Field, GlobalTable, function, IJ
from tracer_lab_gt4py.gt4py_config import backend, externals, nx, ny
from tracer_lab_gt4py.boundaries import bc_1d
import numpy as np

@function
def p0_lagrange(l: Field[np.float64]):
    return l
    
@function
def p1_lagrange(l: Field[np.float64]):
    return 1 - l

@stencil(backend=backend, externals=externals)
def elarmes_1d_linear(
    tracer: GlobalTable[np.float64, (nx, ny)], 
    tracer_e: Field[np.float64],
    weight_x: Field[np.float64],
    weight_y: Field[np.float64],
    idx_dep: Field[IJ, int],
    idy_dep: Field[IJ, int],    
):
    """Computes a linear interpolation

    Args:
        tracer (Field[np.float64]): tracer at dep
        tracer_e (Field[np.float64]): tracer at arrival
        weight_x (Field[np.float64]): coordinate of dep point in departure cell (x)
        weight_y (Field[np.float64]): coordinate of dep point in dep cell (y)
        idx_dep (Field[np.float64]): index of the point in lower left corner of departure cell
        idy_dep (Field[np.float64]): index of the point in lower left corner of departure cell
    """
    
    from __externals__ import (
        bcx_kind, 
        bcy_kind, 
        nx, 
        ny
    )
    
    with computation(PARALLEL), interval(...):

        # Boundary treatment of indexes
        idx_0 = bc_1d(idx_dep, nx, bcx_kind)
        idx_1 = bc_1d(idx_dep + 1, nx, bcx_kind)
    
        idy_0 = bc_1d(idy_dep, ny, bcy_kind)
        idy_1 = bc_1d(idy_dep + 1, ny, bcy_kind)
        
        # Linear interpolation       
        first_line = p0_lagrange(weight_x) * tracer.A[1, 1] + p1_lagrange(weight_x) * tracer.A[2, 1]
        sec_line = p0_lagrange(weight_x) * tracer.A[1, 2] + p1_lagrange(weight_x) * tracer.A[2, 2]

        # first_line = p0_lagrange(weight_x) * tracer.A[idx_0[0, 0, 0], idy_0[0, 0, 0]] + p1_lagrange(weight_x) * tracer.A[idx_1[0, 0, 0], idy_0[0, 0, 0]]
        # sec_line = p0_lagrange(weight_x) * tracer.A[idx_0[0, 0, 0], idy_1[0, 0, 0]] + p1_lagrange(weight_x) * tracer.A[idx_1[0, 0, 0], idy_1[0, 0, 0]]
        tracer_e = p0_lagrange(weight_y) * first_line + p1_lagrange(weight_y) * sec_line
    


