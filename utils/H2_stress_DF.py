#método de diferencias Finitas implícitas

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded

radio_exterior=2.0e-2
radio_interior=radio_exterior-3.0e-3
concentracion_entrada=0.1
concentracion_salida=0.0
difusividad=1.0e-8
modulo_elasticidad=10e9 #Pa
coef_poisson=0.3
frecuencia=5.0e-3
concentracion_inicial=0.0
presion_entrada=400.0e3 #Pa
nodos=2000 #nodes
d_r=(radio_exterior-radio_interior)/(nodos-1)
#dt=0.083
#S=31536000 # seconds in a year
segundos=60*60 # seconds per hour
tiempo_final=5.0
#nt=int(tiempo_final/dt)
n_tiempos=1000
dt=tiempo_final/(n_tiempos-1)

concentracion_anterior=np.zeros(nodos)
concentracion=np.zeros(nodos)
desplazamiento=np.zeros(nodos)
esfuerzo_radial=np.zeros(nodos)
esfuerzo_tangencial=np.zeros(nodos)
deformacion_radial=np.zeros(nodos)
deformacion_tangencial=np.zeros(nodos)
matriz_A=np.zeros((3,nodos))
matriz_ADisp=np.zeros((5,nodos))
rhs=np.zeros(nodos)
rhs_desplazamiento=np.zeros(nodos)
r=np.linspace(radio_interior,radio_exterior,nodos)
t=np.linspace(0,n_tiempos*dt,n_tiempos+1)
historial=np.zeros((nodos,n_tiempos+1))
flujo_concentracion=np.zeros(nodos)
flujo_historial=np.zeros((nodos,n_tiempos+1))
flujo_desplazamiento=np.zeros((nodos,n_tiempos+1))
historial_esfuerzo_radial=np.zeros((nodos,n_tiempos+1))
historial_esfuerzo_tangencial=np.zeros((nodos,n_tiempos+1))
historial_deformacion_radial=np.zeros((nodos,n_tiempos+1))
historial_deformacion_tangencial=np.zeros((nodos,n_tiempos+1))

concentracion_anterior[:]=concentracion_inicial
historial[:,0]=concentracion_anterior
flujo_historial[:,0]=0

# modelo de difusión y matrices para ambos problemas
for i in range(1,nodos-1):
    matriz_A[1+i-i,i]=-2*segundos*difusividad/d_r**2-1/dt
    matriz_A[1+i-(i+1),i+1]=segundos*difusividad/d_r**2+segundos*difusividad/(2*r[i]*d_r)
    matriz_A[1+i-(i-1),i-1]=segundos*difusividad/d_r**2-segundos*difusividad/(2*r[i]*d_r)
    matriz_ADisp[2+i-(i+1),i+1]=1/d_r**2+1/(2*r[i]*d_r)
    matriz_ADisp[2+i-(i-1),i-1]=1/d_r**2-1/(2*r[i]*d_r)
    matriz_ADisp[2+i-i,i]=-2/d_r**2-1./r[i]**2
matriz_A[1+0-0,0]=1 
matriz_A[1+nodos-1-(nodos-1),nodos-1]=1
matriz_ADisp[2+0-0,0]=-3*(coef_poisson-1.)/(2*d_r)-coef_poisson/r[0]
matriz_ADisp[2+0-1,1]=4*(coef_poisson-1.)/(2*d_r)
matriz_ADisp[2+0-2,2]=-(coef_poisson-1.)/(2*d_r)
matriz_ADisp[2+nodos-1-(nodos-3),nodos-3]=(coef_poisson-1.)/(2*d_r)
matriz_ADisp[2+nodos-1-(nodos-2),nodos-2]=-4*(coef_poisson-1.)/(2*d_r)
matriz_ADisp[2+nodos-1-(nodos-1),nodos-1]=3*(coef_poisson-1.)/(2*d_r)-coef_poisson/r[nodos-1]

for j in range(n_tiempos):
    for i in range(1,nodos-1):
        rhs[i]=-concentracion_anterior[i]/dt
    rhs[0]=concentracion_entrada
    rhs[nodos-1]=concentracion_salida
    concentracion=solve_banded((1,1),matriz_A,rhs)
    for i in range(1,nodos-1): # post procesamiento de flujos
        flujo_concentracion[i]=-2.0*np.pi*r[i]*difusividad*(concentracion[i+1]-concentracion[i-1])/(2*d_r)
    flujo_concentracion[0]=-2.0*np.pi*r[0]*difusividad*(-3*concentracion[0]+4*concentracion[1]-concentracion[2])/(2*d_r)  
    flujo_concentracion[nodos-1]=-2.0*np.pi*r[nodos-1]*difusividad*(3*concentracion[nodos-1]-4*concentracion[nodos-2]+concentracion[nodos-3])/(2*d_r)
    historial[:,j+1]=concentracion
    flujo_historial[:,j+1]=flujo_concentracion
    concentracion_anterior[:]=concentracion

# post procesamiento de flujos totales    
flujo_total_entrada=0
flujo_total_salida=0
for i in range(n_tiempos):
    flujo_total_entrada+=0.5*(flujo_historial[0,i]+flujo_historial[0,i+1])*segundos*dt
    flujo_total_salida+=0.5*(flujo_historial[nodos-1,i]+flujo_historial[nodos-1,i+1])*segundos*dt

# modelo de esfuerzos    
for j in range(n_tiempos+1):
    concentracion[:]=historial[:,j]
    for i in range(1,nodos-1):
        rhs_desplazamiento[i]=-(1.0/3.0)*(frecuencia/(coef_poisson-1.0))*(concentracion[i+1]-concentracion[i-1])/(2.*d_r)
    rhs_desplazamiento[0]=-presion_entrada*(1.+coef_poisson)*(2*coef_poisson-1.)/modulo_elasticidad-(1./3.)*frecuencia*concentracion[0]
    rhs_desplazamiento[nodos-1]=-(1./3.)*frecuencia*concentracion[nodos-1]
    desplazamiento=solve_banded((2,2),matriz_ADisp,rhs_desplazamiento)
    flujo_desplazamiento[:,j]=desplazamiento

# post procesamiento de esfuerzos y deformaciones    
    deformacion_tangencial=desplazamiento/r
    for i in range(nodos):
        if i>0 and i<nodos-1:
            deformacion_radial[i]=(desplazamiento[i+1]-desplazamiento[i-1])/(2*d_r)
        if i==0:
            deformacion_radial[i]=(-3*desplazamiento[i]+4*desplazamiento[i+1]-desplazamiento[i+2] )/(2*d_r)
        if i==nodos-1:    
            deformacion_radial[i]=(3*desplazamiento[i]-4*desplazamiento[i-1]+desplazamiento[i-2] )/(2*d_r)
        esfuerzo_radial[i]=(modulo_elasticidad/((1.+coef_poisson)*(2.*coef_poisson-1.))) * \
        ((coef_poisson-1.)*deformacion_radial[i]-coef_poisson*deformacion_tangencial[i]+(1./3.)*frecuencia*concentracion[i])
        esfuerzo_tangencial[i]=(modulo_elasticidad/((1.+coef_poisson)*(2.*coef_poisson-1.))) * \
        ((coef_poisson-1.)*deformacion_tangencial[i]-coef_poisson*deformacion_radial[i]+(1./3.)*frecuencia*concentracion[i])
    historial_esfuerzo_radial[:,j]=esfuerzo_radial
    historial_esfuerzo_tangencial[:,j]=esfuerzo_tangencial
    historial_deformacion_radial[:,j]=deformacion_radial
    historial_deformacion_tangencial[:,j]=deformacion_tangencial

# función para retornar las figuras
def generar_graficas(r, historial_esfuerzo_radial, historial_esfuerzo_tangencial, dt, n_tiempos):
    figuras = []
    
    # Figura de esfuerzo radial
    fig_radial = plt.figure()
    for i in range(0, n_tiempos+1, 100):
        plt.plot(r * 1e3, historial_esfuerzo_radial[:, i], label=f't={i * dt:.1f} años') 
    plt.xlabel('r [mm]')
    plt.ylabel('$\sigma_r$ [Pa]')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    figuras.append(fig_radial)
    
    # Figura de esfuerzo tangencial
    fig_tangencial = plt.figure()
    for i in range(0, n_tiempos+1, 100):
        plt.plot(r * 1e3, historial_esfuerzo_tangencial[:, i], label=f't={i * dt:.1f} años')
    plt.xlabel('r [mm]')
    plt.ylabel(r'$\sigma_\theta$ [Pa]')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    figuras.append(fig_tangencial)
    
    return figuras