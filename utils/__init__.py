# Importar las funciones necesarias del archivo difussionH2_stress_DF.py
from .difussionH2_stress_DF import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

# Importar los calculos necesarios del archivo difussionH2_stress_DF.py
from .difussionH2_stress_DF import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

# Llamar los valores y calculos
Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = initialize_parameters()
Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = initialize_arrays(n, nt, C0, Ri, Ro)
A, ADisp = setup_diffusion_matrix(A, ADisp, n, dr, D, S, dt, r, nu)
solve_diffusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Hflux, n)
solve_disp(ADisp, rhsDisp, Disp, H, HDisp, n, nt, dt, dr, Omega, pin, E, nu)
post_processing(n, nt, r, H, Cflux, Disp, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t, dt)