# Importar las funciones necesarias del archivo difussionH2_stress_DF.py
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


# Importar las funciones necesarias del archivo principal
from .difussionH2_stress_DF import (
    inicializar_parametros,
    inicializar_arreglos,
    configurar_matriz_difusion,
    resolver_difusion,
    resolver_esfuerzos,
    post_procesar_esfuerzos
)

# Llamar a los valores y cálculos
Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = inicializar_parametros()
Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = inicializar_arreglos(n, nt, C0, Ri, Ro)
configurar_matriz_difusion(A, ADisp, n, dr, D, S, dt, r, nu)
resolver_difusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Hflux, n)
resolver_esfuerzos(ADisp, rhsDisp, Disp, H, HDisp, n, nt, dr, Omega, pin, E, nu)
post_procesar_esfuerzos(HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t, r, n, E, nu, Omega, H, dr)

