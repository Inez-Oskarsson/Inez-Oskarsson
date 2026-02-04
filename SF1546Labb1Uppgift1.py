#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 19:06:10 2026

Uppgift 1: Numerisk beräkning av nollställen
Metoder: Fixpunktsiteration och Newtons metod

Ekvation: f(x) = (8/3)*(x/L) - 3*(x/L)^2 + (1/3)*(x/L)^3 - (2/3)*sin(πx/L) = 0

@author: inez
"""
import numpy as np
import matplotlib.pyplot as plt
import os


def console_clear():
    """Rensar konsolen"""
    os.system('clear' if os.name != 'nt' else 'cls')


# KONSTANTER OCH FUNKTIONSDEFINITIONER
L = 1.0                 # Längd på intervallet
tol = 1e-10            # Tolerans för konvergens
max_iter = 300         # Max antal iterationer

# Originalfunktionen f(x) vars nollställen vi söker
f = lambda x: (8/3)*(x/L) - 3*(x/L)**2 + (1/3)*(x/L)**3 - (2/3)*np.sin(np.pi*x/L)

# Derivatan av f(x), behövs för Newtons metod
df = lambda x: (8/3)*(1/L) - 6*(x/L)*(1/L) + (x/L)**2*(1/L) - (2/3)*(np.pi/L)*np.cos(np.pi*x/L)

# Fixpunktfunktionen g(x) där x = g(x) vid fixpunkter
g = lambda x: (3*L/8)*(3*(x/L)**2 - (1/3)*(x/L)**3 + (2/3)*np.sin(np.pi*x/L))

# Derivatan av g(x), behövs för konvergensanalys
dg = lambda x: (3*L/8)*(6*(x/L)*(1/L) - (x/L)**2*(1/L) + (2/3)*(np.pi/L)*np.cos(np.pi*x/L))


# UPPGIFT 1a: PLOTTA FUNKTIONEN OCH IDENTIFIERA NOLLSTÄLLEN
def plot_function():
    """
    Plottar funktionen f(x) för att visualisera nollställena.
    Returnerar ungefärliga positioner för nollställena.
    """
    x = np.linspace(0, L, 1000)
    y = f(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='f(x)')
    plt.axhline(0, color='r', linestyle='--', linewidth=1, label='y = 0')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title('Funktionen f(x) - Identifiering av nollställen', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, L)
    
    # Hitta nollställen genom teckenbyte
    zeros_approx = []
    for i in range(len(y)-1):
        if y[i] * y[i+1] < 0:
            zeros_approx.append((x[i] + x[i+1]) / 2)
    
    # Markera nollställena med vertikala linjer
    for zero in zeros_approx:
        plt.axvline(zero, color='g', linestyle=':', alpha=0.5, linewidth=2)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\nAntal nollställen hittade: {len(zeros_approx)}")
    for i, z in enumerate(zeros_approx, 1):
        print(f"  Nollställe {i}: x ~ {z:.4f}")
    
    return zeros_approx


# UPPGIFT 1b: KONVERGENSANALYS FÖR FIXPUNKTSMETODEN
def analyze_convergence(zeros_approx):
    """
    Analyserar var fixpunktsmetoden kan konvergera genom att plotta |g'(x)|.
    """
    x = np.linspace(0, L, 1000)
    dg_vals = np.abs(dg(x))
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, dg_vals, 'purple', linewidth=2, label="|g'(x)|")
    plt.axhline(1, color='r', linestyle='--', linewidth=1.5, label="|g'(x)| = 1")
    plt.xlabel('x', fontsize=12)
    plt.ylabel("|g'(x)|", fontsize=12)
    plt.title('Konvergensanalys för fixpunktsmetoden', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, L)
    plt.ylim(0, 2)
    
    # Markera konvergensområde
    convergent_mask = dg_vals < 1
    plt.fill_between(x, 0, 2, where=convergent_mask, alpha=0.2, 
                     color='green', label='Konvergensområde')
    
    # Markera nollställena
    for i, z in enumerate(zeros_approx, 1):
        dg_val = np.abs(dg(z))
        color = 'green' if dg_val < 1 else 'red'
        plt.scatter(z, dg_val, s=100, color=color, zorder=5)
    
    plt.tight_layout()
    plt.show()
    
    print("\nKvantitativ analys:")
    for i, z in enumerate(zeros_approx, 1):
        dg_val = np.abs(dg(z))
        status = "Ja" if dg_val < 1 else "Nej"
        print(f"  Nollställe {i} (x≈{z:.3f}): |g'(x)| = {dg_val:.3f} → {status}")


# UPPGIFT 1c: FIXPUNKTSMETODEN
def fixpunktsmetoden(g, x0, tol, max_iter, verbose=True):
    """
    Implementerar fixpunktsiteration enligt bokens metod.
    Algoritm: x_{n+1} = g(x_n)
    """
    x = x0
    history = [x]
    DeltaX = tol + 1.0
    n = 0
    
    if verbose:
        print(f"\n{'Iteration':<12} {'x_n':<22} {'|x_n+1 - x_n|':<18}")
        print("-" * 52)
    
    while DeltaX > tol:
        n += 1
        xold = x
        x = g(xold)
        DeltaX = np.abs(x - xold)
        history.append(x)
        
        if verbose:
            print(f"{n:<12} {x:<22.15f} {DeltaX:<18.2e}")
        
        if n > max_iter:
            raise RuntimeError("Fixpunktsiteration konvergerade inte")
    
    if verbose:
        print(f"\n  Nollställe: x = {x:.15f}")
        print(f"  Verifiering: f(x) = {f(x):.2e}")
    
    return x, n, history


# UPPGIFT 1d: NEWTONS METOD
def newtons_metod(f, df, x0, tol, max_iter, verbose=True):
    """
    Implementerar Newtons metod enligt bokens metod.
    Algoritm: x_{n+1} = x_n - f(x_n)/f'(x_n)
    """
    x = x0
    history = [x]
    DeltaX = tol + 1.0
    n = 0
    
    if verbose:
        print(f"\n{'Iteration':<12} {'x_n':<22} {'|x_n+1 - x_n|':<18}")
        print("-" * 52)
    
    while DeltaX > tol:
        n += 1
        dfx = df(x)
        
        if np.abs(dfx) < 1e-15:
            raise RuntimeError("Derivatan är nästan noll")
        
        xold = x
        x = xold - f(xold) / dfx
        DeltaX = np.abs(x - xold)
        history.append(x)
        
        if verbose:
            print(f"{n:<12} {x:<22.15f} {DeltaX:<18.2e}")
        
        if n > max_iter:
            raise RuntimeError("Newtons metod konvergerade inte")
    
    if verbose:
        print(f"\n  Nollställe: x = {x:.15f}")
        print(f"  Verifiering: f(x) = {f(x):.2e}")
    
    return x, n, history


# UPPGIFT 1e: JÄMFÖRELSE AV KONVERGENSHASTIGHET
def compare_convergence(x0_compare):
    """
    Jämför konvergenshastigheten mellan fixpunkt och Newton.
    """
    print(f"\nStartvärde för båda metoderna: x0 = {x0_compare}")
    
    # Fixpunktsmetoden
    x_fp, n_fp, hist_fp = fixpunktsmetoden(g, x0_compare, tol, max_iter, verbose=False)
    err_fp = [np.abs(hist_fp[i+1] - hist_fp[i]) for i in range(len(hist_fp)-1)]
    
    # Newtons metod
    x_n, n_n, hist_n = newtons_metod(f, df, x0_compare, tol, max_iter, verbose=False)
    err_n = [np.abs(hist_n[i+1] - hist_n[i]) for i in range(len(hist_n)-1)]
    
    print(f"\nFixpunktsmetoden: {n_fp} iterationer, x = {x_fp:.10f}")
    print(f"Newtons metod: {n_n} iterationer, x = {x_n:.10f}")
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(range(len(err_fp)), err_fp, 'o-', color='red', 
                 linewidth=2, markersize=6, label='Fixpunktsmetoden')
    plt.semilogy(range(len(err_n)), err_n, 's-', color='blue', 
                 linewidth=2, markersize=6, label='Newtons metod')
    plt.xlabel('Iteration n', fontsize=12)
    plt.ylabel(r'$|x_{n+1} - x_n|$', fontsize=12)
    plt.title(f'Konvergensjämförelse (x0 = {x0_compare})', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"\nKvot: {n_fp / n_n:.1f}x fler iterationer för fixpunkt")


# HUVUDPROGRAM
def main():
    console_clear()
    
    print("UPPGIFT 1: NUMERISK BERÄKNING AV NOLLSTÄLLEN\n")
    
    # UPPGIFT 1a
    print("1a) Identifiering av nollställen")
    zeros_approx = plot_function()
    
    # UPPGIFT 1b
    print("\n1b) Konvergensanalys")
    analyze_convergence(zeros_approx)
    
    # UPPGIFT 1c
    print("\n1c) Fixpunktsmetoden")
    x0_fp = 0.85
    print(f"Startvärde: x0 = {x0_fp}")
    try:
        root_fp, iter_fp, hist_fp = fixpunktsmetoden(g, x0_fp, tol, max_iter, verbose=True)
    except RuntimeError as e:
        print(f"Fel: {e}")
    
    # UPPGIFT 1d
    print("\n1d) Newtons metod")
    x0_newton = 0.25
    print(f"Startvärde: x0 = {x0_newton}")
    try:
        root_newton, iter_newton, hist_newton = newtons_metod(f, df, x0_newton, tol, max_iter, verbose=True)
    except RuntimeError as e:
        print(f"Fel: {e}")
    
    # UPPGIFT 1e
    print("\n1e) Konvergensjämförelse")
    x0_compare = 0.85
    compare_convergence(x0_compare)


if __name__ == "__main__":
    main()
