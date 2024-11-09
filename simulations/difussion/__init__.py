# Importar las funciones necesarias del módulo simulations
from simulations import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

# Inicializar parámetros
Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = initialize_parameters()

# Inicializar arreglos
Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = initialize_arrays(n, nt, C0, Ri, Ro)

# Configurar la matriz de difusión
A, ADisp = setup_diffusion_matrix(A, ADisp, n, dr, D, S, dt, r, nu)

# Resolver la difusión
solve_diffusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Cflux, n)

# Resolver el desplazamiento
solve_disp(ADisp, rhsDisp, Disp, H, HDisp, n, nt, dt, dr, Omega, pin, E, nu)

# Procesamiento posterior
post_processing(n, nt, r, H, Cflux, Disp, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t, dt)
