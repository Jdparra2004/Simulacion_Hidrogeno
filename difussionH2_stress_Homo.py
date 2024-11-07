import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.integrate import solve_ivp

class DiffusionH2StressHomotopy:
    def __init__(self):
        # Parámetros físicos
        self.Ro = 2.0e-2  # Radio externo [m]
        self.Ri = self.Ro - 3.0e-3  # Radio interno [m]
        self.D = 1.0e-8  # Coeficiente de difusión [m²/s]
        self.Cin = 0.1  # Concentración inicial en r = Ri
        self.Cout = 0.0  # Concentración inicial en r = Ro
        
        # Parámetros de estrés
        self.E = 200e9  # Módulo de Young [Pa]
        self.nu = 0.3   # Coeficiente de Poisson
        self.VH = 2e-6  # Volumen molar parcial del hidrógeno [m³/mol]
        
        # Parámetros de homotopía
        self.p = 0.0  # Parámetro de homotopía
        self.p_steps = 100  # Número de pasos para p de 0 a 1
        
        # Malla espacial
        self.Nr = 100
        self.r = np.linspace(self.Ri, self.Ro, self.Nr)
        self.dr = self.r[1] - self.r[0]
        
        # Coeficientes de la solución de difusión pura
        self.pure_diffusion_coeffs = None
        
    def load_pure_diffusion_coeffs(self):
        """Carga los coeficientes obtenidos del caso de difusión pura"""
        # Aquí cargaríamos los coeficientes desde difusion_pura_homo.py
        # Por ahora, usaremos una solución analítica simplificada
        A = (self.Cout - self.Cin) / np.log(self.Ro/self.Ri)
        B = self.Cin - A * np.log(self.Ri)
        self.pure_diffusion_coeffs = {'A': A, 'B': B}
        
    def pure_diffusion_solution(self, r):
        """Calcula la solución de difusión pura"""
        A = self.pure_diffusion_coeffs['A']
        B = self.pure_diffusion_coeffs['B']
        return A * np.log(r) + B
    
    def stress_term(self, C, r):
        """Calcula el término de estrés"""
        # Gradiente de concentración
        dC_dr = np.gradient(C, self.dr)
        
        # Término de estrés hidrostático
        sigma_h = -self.E * self.VH / (3 * (1 - self.nu)) * dC_dr
        
        # Término completo de estrés
        stress_contribution = self.D * self.VH / (self.E * r) * np.gradient(r * sigma_h, self.dr)
        
        return stress_contribution
    
    def homotopy_operator(self, C, r, p):
        """Define el operador de homotopía"""
        # Operador lineal (difusión pura)
        L_u = self.D * (np.gradient(np.gradient(C, self.dr), self.dr) + 
                        np.gradient(C, self.dr) / r)
        
        # Operador no lineal (término de estrés)
        N_u = self.stress_term(C, r)
        
        # Operador de homotopía
        return L_u + p * N_u
    
    def solve_homotopy_step(self, p):
        """Resuelve un paso del método de homotopía"""
        # Sistema de ecuaciones para el paso actual
        def system(r, C):
            return self.homotopy_operator(C, r, p)
        
        # Condiciones iniciales (usando la solución de difusión pura)
        C_init = self.pure_diffusion_solution(self.r)
        
        # Resolver el sistema
        sol = solve_ivp(
            system,
            [self.Ri, self.Ro],
            C_init,
            method='RK45',
            t_eval=self.r
        )
        
        return sol.y[:, -1]
    
    def solve_complete(self):
        """Resuelve el problema completo usando homotopía"""
        # Cargar coeficientes de difusión pura
        self.load_pure_diffusion_coeffs()
        
        # Iterar sobre p de 0 a 1
        p_values = np.linspace(0, 1, self.p_steps)
        solutions = []
        
        for p in p_values:
            self.p = p
            solution = self.solve_homotopy_step(p)
            solutions.append(solution)
            
            # Mostrar progreso
            print(f"Progreso: {p*100:.1f}%")
            
        return np.array(solutions)
    
    def plot_results(self, solutions):
        """Visualiza los resultados de la homotopía"""
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Perfiles de concentración
        plt.subplot(2, 1, 1)
        p_to_plot = [0, 0.5, 1.0]
        for p in p_to_plot:
            idx = int(p * (self.p_steps - 1))
            plt.plot(self.r*1000, solutions[idx], 
                    label=f'p = {p:.1f}')
        
        plt.xlabel('Radio [mm]')
        plt.ylabel('Concentración')
        plt.title('Perfiles de concentración para diferentes valores de p')
        plt.grid(True)
        plt.legend()
        
        # Subplot 2: Evolución de la solución
        plt.subplot(2, 1, 2)
        plt.imshow(solutions, aspect='auto', 
                    extent=[self.Ri*1000, self.Ro*1000, 0, 1])
        plt.colorbar(label='Concentración')
        plt.xlabel('Radio [mm]')
        plt.ylabel('Parámetro de homotopía (p)')
        plt.title('Evolución de la solución con el parámetro de homotopía')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Crear instancia del solver
    solver = DiffusionH2StressHomotopy()
    
    # Resolver el problema
    solutions = solver.solve_complete()
    
    # Visualizar resultados
    solver.plot_results(solutions)