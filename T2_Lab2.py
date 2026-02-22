#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCreated on Sun Feb 22 10:58:17 2026

@author: inez

2: Randvärdesproblem - Temperatur i stav
Finita differensmetoden för: k*d²T/dx² = q(x)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve


# HJÄLPFUNKTIONER

def q(x):
    """
    Källterm för värmetillförsel.
    
    Parameters:
        x : float eller array - position
    
    Returns:
        float eller array - q(x) = 50*x³*ln(x+1)
    """
    return 50 * x**3 * np.log(x + 1)


def diskretisering_temperatur(N, q, k, TL, TR, L=1.0):
    """
    T2.b) och T2.c) Diskretiserar randvärdesproblemet med finita differenser.
    
    Centrala differenser: d²T/dx² ≈ (T_{j-1} - 2*T_j + T_{j+1}) / h²
    
    Ger systemet: k/h² * [-2T_j + T_{j-1} + T_{j+1}] = q(x_j)
    
    Med randvillkor: T_0 = TL, T_N = TR
    
    Parameters:
        N : int - antal delintervall
        q : function - källterm q(x)
        k : float - värmeledningsförmåga
        TL : float - temperatur vid x=0
        TR : float - temperatur vid x=L
        L : float - stavens längd (default 1.0)
    
    Returns:
        A : sparse matrix - systemmatris
        HL : array - högerled (med randvillkor)
    """
    h = L / N
    
    # Inre punkter: x_j för j = 1, 2, ..., N-1
    n_inner = N - 1
    x_inner = np.array([h * j for j in range(1, N)])
    
    # Systemmatris: tridiagonal med -2 på diagonalen, 1 på över/underdiagonal
    # Multiplicera med k/h²
    diagonals = [
        np.ones(n_inner - 1),      # överdiagonal
        -2 * np.ones(n_inner),     # huvuddiagonal
        np.ones(n_inner - 1)       # underdiagonal
    ]
    offsets = [1, 0, -1]
    
    A = (k / h**2) * diags(diagonals, offsets, shape=(n_inner, n_inner), format='csr')
    
    # Högerled
    HL = q(x_inner)
    
    # Lägg till randvillkor i högerledet
    HL[0] -= (k / h**2) * TL      # Första ekvationen
    HL[-1] -= (k / h**2) * TR     # Sista ekvationen
    
    return A, HL


def solve_temperature(N, q, k, TL, TR, L=1.0):
    """
    Löser temperaturproblemet för givet N.
    
    Parameters:
        N : int - antal delintervall
        q : function - källterm
        k : float - värmeledningsförmåga
        TL : float - vänster randvillkor
        TR : float - höger randvillkor
        L : float - stavens längd
    
    Returns:
        x : array - alla punkter (inkl. randpunkter)
        T : array - temperaturen i alla punkter
    """
    h = L / N
    
    # Diskretisera
    A, HL = diskretisering_temperatur(N, q, k, TL, TR, L)
    
    # Lös systemet
    T_inner = spsolve(A, HL)
    
    # Lägg till randvillkor
    x = np.linspace(0, L, N + 1)
    T = np.zeros(N + 1)
    T[0] = TL
    T[1:-1] = T_inner
    T[-1] = TR
    
    return x, T


# DELFRÅGOR

def test_T2a():
    """
    T2.a) Testa diskretisering för N=4.
    """
    N = 4
    k = 2.0
    TL = 2.0
    TR = 2.0
    L = 1.0
    
    A, HL = diskretisering_temperatur(N, q, k, TL, TR, L)
    
    print("\n T2.a) Diskretisering för N=4")
    print(f"Steglängd h = L/N = {L/N}")
    print(f"\nSystemmatris A (k/h² = {k/(L/N)**2}):")
    print(A.toarray())
    print(f"\nHögerled HL:")
    print(HL)
    
    # Verifiera mot förväntade värden
    A_expected = 32 * np.array([
        [-2, 1, 0],
        [1, -2, 1],
        [0, 1, -2]
    ])
    HL_expected = np.array([-63.826, 2.534, -52.196])
    
    print(f"\nFörväntat A:")
    print(A_expected)
    print(f"\nFörväntad HL:")
    print(HL_expected)
    print(f"\nVerifiering A: {np.allclose(A.toarray(), A_expected, atol=1)}")
    print(f"Verifiering HL: {np.allclose(HL, HL_expected, atol=1)}")


def solve_T2d():
    """
    T2.d) Lös för N=100 och plotta.
    """
    N = 100
    k = 2.0
    TL = 2.0
    TR = 2.0
    L = 1.0
    
    x, T = solve_temperature(N, q, k, TL, TR, L)
    
    # Temperatur vid x = 0.2
    idx_02 = int(0.2 / (L / N))
    T_02 = T[idx_02]
    
    print(f"\n T2.d) Lösning för N={N}")
    print(f"Temperatur vid x = 0.2: T ≈ {T_02:.6f}")
    
    # Plotta
    plt.figure(figsize=(10, 6))
    plt.plot(x, T, 'b-', linewidth=2)
    plt.plot(0.2, T_02, 'ro', markersize=10, label=f'T(0.2) ≈ {T_02:.4f}')
    plt.xlabel('Position x (m)')
    plt.ylabel('Temperatur T (°C)')
    plt.title(f'Temperaturfördelning i stav (N={N})')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return T_02


def solve_T2e():
    """
    T2.e) Konvergensstudie - temperatur vid x = 0.7.
    """
    k = 2.0
    TL = 2.0
    TR = 2.0
    L = 1.0
    x_target = 0.7
    T_converged = 1.6379544  # Konvergensvärde
    
    N_values = [50, 100, 200, 400, 800]
    T_values = []
    h_values = []
    errors = []
    
    print(f"\n T2.e) Konvergensstudie vid x = {x_target} ")
    print(f"{'N':<6} {'h':<10} {'T(0.7)':<15} {'Fel':<15}")
    print("-" * 50)
    
    for N in N_values:
        h = L / N
        x, T = solve_temperature(N, q, k, TL, TR, L)
        
        # Hitta närmaste punkt till x = 0.7
        idx = np.argmin(np.abs(x - x_target))
        T_07 = T[idx]
        error = np.abs(T_07 - T_converged)
        
        T_values.append(T_07)
        h_values.append(h)
        errors.append(error)
        
        print(f"{N:<6} {h:<10.5f} {T_07:<15.8f} {error:<15.6e}")
    
    # Beräkna noggrannhetsordning
    print("\n Noggrannhetsordning ")
    print(f"{'N':<6} {'N*2':<6} {'e(h)':<15} {'e(h/2)':<15} {'p':<10}")
    print("-" * 60)
    
    errors = np.array(errors)
    orders = []
    
    for i in range(len(N_values) - 1):
        N1 = N_values[i]
        N2 = N_values[i + 1]
        e1 = errors[i]
        e2 = errors[i + 1]
        
        # p ≈ log(e(h)/e(h/2)) / log(2)
        p = np.log(e1 / e2) / np.log(2)
        orders.append(p)
        
        print(f"{N1:<6} {N2:<6} {e1:<15.6e} {e2:<15.6e} {p:<10.3f}")
    
    print(f"\nMedel noggrannhetsordning: {np.mean(orders):.3f}")
    print(f"Teoretisk ordning för centrala differenser: 2")
    
    # Plotta konvergens
    plt.figure(figsize=(10, 6))
    plt.loglog(h_values, errors, 'bo-', label='Beräknade fel', markersize=8)
    plt.loglog(h_values, np.array(h_values)**2 * errors[0] / h_values[0]**2, 
               'r--', label='h² (ordning 2)', linewidth=2)
    plt.xlabel('Steglängd h')
    plt.ylabel('Fel vid x = 0.7')
    plt.title('Konvergens för finita differensmetoden')
    plt.grid(True, which='both', alpha=0.3)
    plt.legend()
    plt.show()


def solve_T2f():
    """
    T2.f) Testa olika randvillkor.
    """
    N = 100
    k = 2.0
    L = 1.0
    
    # Olika fall
    cases = [
        (2.0, 2.0, "TL = TR = 2°C"),
        (2.0, 10.0, "TL = 2°C, TR = 10°C"),
        (10.0, 2.0, "TL = 10°C, TR = 2°C"),
        (0.0, 20.0, "TL = 0°C, TR = 20°C")
    ]
    
    plt.figure(figsize=(12, 8))
    
    for i, (TL, TR, label) in enumerate(cases, 1):
        x, T = solve_temperature(N, q, k, TL, TR, L)
        
        plt.subplot(2, 2, i)
        plt.plot(x, T, 'b-', linewidth=2)
        plt.xlabel('Position x (m)')
        plt.ylabel('Temperatur T (°C)')
        plt.title(label)
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\nT2.f) Analys av randvillkor ")
    print("Randvillkoren har stor påverkan på temperaturfördelningen.")
    print("När TL ≠ TR skapas en gradient längs staven.")


# HUVUDFUNKTION

def main():
    """Huvudfunktion - kör alla delfrågor"""
    
    # T2.a) Test för N=4
    test_T2a()
    
    # T2.d) Lösning för N=100
    solve_T2d()
    
    # T2.e) Konvergensstudie
    solve_T2e()
    
    # T2.f) Olika randvillkor
    solve_T2f()


if __name__ == "__main__":
    main()
