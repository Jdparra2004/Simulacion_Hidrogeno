# utils/__init__.py

# Importar las funciones necesarias del archivo difussionH2_stress_DF.py
from utils.difussionH2_stress_DF import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

# Llamar los valores y cálculos
Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = initialize_parameters()
Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = initialize_arrays(n, nt, C0, Ri, Ro)
A, ADisp = setup_diffusion_matrix(A, ADisp, n, dr, D, S, dt, r, nu)
solve_diffusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Hflux, n)
solve_disp(ADisp, rhsDisp, Disp, H, HDisp, n, nt, dt, dr, Omega, pin, E, nu)
post_processing(n, nt, r, H, Cflux, Disp, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t, dt)

# Importar la función de generar gráficas
from utils.H2_stress_DF import generar_graficas

# Importar las variables y funciones necesarias del archivo H2_stress_DF.py
from utils.H2_stress_DF import (
    radio_exterior,
    radio_interior,
    concentracion_entrada,
    concentracion_salida,
    difusividad,
    modulo_elasticidad,
    coef_poisson,
    frecuencia,
    concentracion_inicial,
    presion_entrada,
    nodos,
    d_r,
    segundos,
    tiempo_final,
    n_tiempos,
    dt,
    r,
    historial_esfuerzo_radial,
    historial_esfuerzo_tangencial,
    generar_graficas  
)


# funciones para cada interfaz
from gui.difussion_window import DifussionWindow
from gui.radial_stress_window import RadialStressWindow
from gui.tangential_stress_window import TangentialStressWindow
from gui.comparison_window import ComparisonWindow
from gui.main_window import MainWindow
from simulations.difussion import simulate_difussion 