
"""
Created on Mon Feb  2 19:06:10 2026
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
max_iter = 100         # Max antal iterationer

# Originalfunktionen f(x) vars nollställen vi söker
f = lambda x: (8/3)*(x/L) - 3*(x/L)**2 + (1/3)*(x/L)**3 - (2/3)*np.sin(np.pi*x/L)

# Derivatan av f(x), behövs för Newtons metod
df = lambda x: (8/3)*(1/L) - 6*(x/L)*(1/L) + (x/L)**2*(1/L) - (2/3)*(np.pi/L)*np.cos(np.pi*x/L)

# Fixpunktfunktionen g(x) där x = g(x) vid fixpunkter
# Härledd från f(x) = 0 genom att lösa ut x:
# (8/3)*(x/L) = 3*(x/L)^2 - (1/3)*(x/L)^3 + (2/3)*sin(πx/L)
# x = (3L/8) * [3*(x/L)^2 - (1/3)*(x/L)^3 + (2/3)*sin(πx/L)]
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
    
    # Hitta ungefärliga nollställen genom teckenbyte
    zeros_approx = []
    for i in range(len(y)-1):
        if y[i] * y[i+1] < 0:  # Teckenbyte indikerar nollställe
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

def analyze_convergence():
    """
    Analyserar var fixpunktsmetoden kan konvergera genom att plotta |g'(x)|.
    
    Teori: Fixpunktsmetoden x_{n+1} = g(x_n) konvergerar om |g'(x)| < 1
    i närheten av fixpunkten.
    """
    x = np.linspace(0, L, 1000)
    dg_vals = np.abs(dg(x))
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, dg_vals, 'purple', linewidth=2, label="|g'(x)|")
    plt.axhline(1, color='r', linestyle='--', linewidth=1.5, label="|g'(x)| = 1 (konvergensgräns)")
    plt.xlabel('x', fontsize=12)
    plt.ylabel("|g'(x)|", fontsize=12)
    plt.title('Konvergensanalys för fixpunktsmetoden', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, L)
    plt.ylim(0, 2)
    
    # Hitta regioner där |g'(x)| < 1
    convergent_mask = dg_vals < 1
    
    plt.fill_between(x, 0, 2, where=convergent_mask, alpha=0.2, 
                     color='green', label='Konvergensområde')
    
    plt.tight_layout()
    plt.show()
    
    # Analysera konvergensregioner
    # Teori: Fixpunktsmetoden konvergerar om |g'(x)| < 1    
    # Hitta x-värden där nollställen finns
    zeros = plot_function.__wrapped__ if hasattr(plot_function, '__wrapped__') else None
    


# UPPGIFT 1c: FIXPUNKTSMETODEN

def fixpunktsmetoden(g, x0, tol, max_iter, verbose=True):
    """
    Implementerar fixpunktsiteration enligt bokens metod.
    
    Algoritm: x_{n+1} = g(x_n)
    
    Parameter:
        g         : Funktionen g(x) 
        x0        : Startgissning
        tol       : Tolerans för konvergens
        max_iter  : Max antal iterationer
        verbose   : Om True, skriv ut varje iteration

    Output:
        x         : Fixpunktsiterationens approximation
        n         : Antal iterationer som användes
        history   : Lista med alla x-värden
    """
    
    # Initiera
    x = x0
    history = [x]
    DeltaX = tol + 1.0
    n = 0
    
    if verbose:
        print(f"\n{'Iteration':<12} {'x_n':<22} {'|x_n+1 - x_n|':<18}")
        print("-" * 52)
    
    # Iterationsloop (baserad på lärarens while-loop struktur)
    while DeltaX > tol:
        n += 1
        xold = x
        x = g(xold)
        DeltaX = np.abs(x - xold)
        history.append(x)
        
        if verbose:
            print(f"{n:<12} {x:<22.15f} {DeltaX:<18.2e}")
        
        if n > max_iter:
            raise RuntimeError(
                "Fixpunktsiteration konvergerade inte inom maximalt antal iterationer")
    
    if verbose:
        print(f"\n  Nollställe: x = {x:.15f}")
        print(f"  Verifiering: f(x) = {f(x):.2e}")
    
    return x, n, history


# UPPGIFT 1d: NEWTONS METOD

def newtons_metod(f, df, x0, tol, max_iter, verbose=True):
    """
    Implementerar Newtons metod enligt bokens metod.
    
    Algoritm: x_{n+1} = x_n - f(x_n)/f'(x_n)
    
    Parameter:
        f         : Funktionen f(x) vars nollställe vi söker
        df        : Derivatan f'(x)
        x0        : Startgissning
        tol       : Tolerans för konvergens
        max_iter  : Max antal iterationer
        verbose   : Om True, skriv ut varje iteration

    Output:
        x         : Newtons metods approximation
        n         : Antal iterationer som användes
        history   : Lista med alla x-värden
    """
    
    # Initiera
    x = x0
    history = [x]
    DeltaX = tol + 1.0
    n = 0
    
    if verbose:
        print(f"\n{'Iteration':<12} {'x_n':<22} {'|x_n+1 - x_n|':<18}")
        print("-" * 52)
    
    # Iterationsloop (baserad på lärarens while-loop struktur)
    while DeltaX > tol:
        n += 1
        
        # Kontrollera att derivatan inte är noll (robusthet)
        dfx = df(x)
        if np.abs(dfx) < 1e-15:
            raise RuntimeError(
                "Newtons metod: Derivatan är nästan noll, metoden kan inte fortsätta")
        
        # Newtons formel
        xold = x
        x = xold - f(xold) / dfx
        DeltaX = np.abs(x - xold)
        history.append(x)
        
        if verbose:
            print(f"{n:<12} {x:<22.15f} {DeltaX:<18.2e}")
        
        if n > max_iter:
            raise RuntimeError(
                "Newtons metod konvergerade inte inom maximalt antal iterationer")
    
    if verbose:
        print(f"\n  Nollställe: x = {x:.15f}")
        print(f"  Verifiering: f(x) = {f(x):.2e}")
    
    return x, n, history


# UPPGIFT 1e: JÄMFÖRELSE AV KONVERGENSHASTIGHET

def compare_convergence(x0_compare):
    """
    Jämför konvergenshastigheten mellan fixpunkt och Newton.
    Plottar |x_{n+1} - x_n| som funktion av n för båda metoderna.
    
    Förväntat resultat:
    - Fixpunkt: Linjär konvergens
    - Newton: Kvadratisk konvergens
    """
    # Konvergensjämförelse
    print(f"Startvärde för båda metoderna: x0 = {x0_compare}")
    
    # Kör fixpunktsmetoden
    # Fixpunktsmetoden
    x_fp, n_fp, hist_fp = fixpunktsmetoden(g, x0_compare, tol, max_iter, verbose=False)
    
    # Beräkna felen |x_{n+1} - x_n|
    err_fp = [np.abs(hist_fp[i+1] - hist_fp[i]) for i in range(len(hist_fp)-1)]
    
    print(f"Fixpunktsmetoden:Konvergerade efter {n_fp} iterationer till x = {x_fp:.10f}")
    
    # Kör Newtons metod
    # Newtons medtod
    x_n, n_n, hist_n = newtons_metod(f, df, x0_compare, tol, max_iter, verbose=False)
    
    # Beräkna felen |x_{n+1} - x_n|
    err_n = [np.abs(hist_n[i+1] - hist_n[i]) for i in range(len(hist_n)-1)]
    
    print(f"Newtons metod:Konvergerade efter {n_n} iterationer till x = {x_n:.10f}")
    
    # Plotta jämförelsen
    plt.figure(figsize=(10, 6))
    plt.semilogy(range(len(err_fp)), err_fp, 'o-', color='red', 
                 linewidth=2, markersize=6, label='Fixpunktsmetoden')
    plt.semilogy(range(len(err_n)), err_n, 's-', color='blue', 
                 linewidth=2, markersize=6, label='Newtons metod')
    plt.xlabel('Iteration n', fontsize=12)
    plt.ylabel(r'$|x_{n+1} - x_n|$ (log-skala)', fontsize=12)
    plt.title(f'Konvergensjämförelse (x0 = {x0_compare})', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Analys
    # Fixpunktsmetoden:
        # Antal iterationer: 93
        # Konvergenstyp: Linjär konvergens
        # I log-plotten: Felet minskar linjärt
    # Newtons metod:
        # Antal iterationer: 5
        # Konvergenstyp: Kvadritsk konvergens
        # I log-plotten: Felet minskar exponetiellt
    print(f"\nKvot mellan iterationer: {n_fp / n_n:.1f}x fler för fixpunkt")
    # Man ser att newtons metod konvergerar mycket snabbare


# HUVUDPROGRAM

def main():
    """
    Huvudprogram som kör alla deluppgifter.
    """
    console_clear()
    
    print(" UPPGIFT 1: NUMERISK BERÄKNING AV NOLLSTÄLLEN")
    print(" Metoder: Fixpunktsiteration och Newtons metod")
    
    # UPPGIFT 1a: Plotta funktionen
    print("UPPGIFT 1a: Identifiering av nollställen")
    
    zeros_approx = plot_function()
    
    # UPPGIFT 1b: Konvergensanalys
    print("\nUPPGIFT 1b: Konvergensanalys för fixpunktsmetoden")
    
    analyze_convergence()
    
    print("Fixpunktsmetoden x_{n+1} = g(x_n) konvergerar lokalt om |g'(x*)| < 1")
    print("där x* är fixpunkten (nollstället).")
    print("  * För det första nollstället (x ~ 0.25): |g'(x)| < 1 Ja")
    print("  * För det andra nollstället (x ~ 0.75): |g'(x)| > 1 Nej")
    
    # UPPGIFT 1c: Fixpunktsmetoden
    print("\nUPPGIFT 1c: Beräkning med fixpunktsmetoden")
    
    x0_fp = 0.2  # Startvärde där |g'(x)| < 1
    # Valt eftersom |g'(x)| < 1 i denna region
    print(f"Startvärde: x0 = {x0_fp}")
    
    try:
        root_fp, iter_fp, hist_fp = fixpunktsmetoden(g, x0_fp, tol, max_iter, verbose=True)
    except RuntimeError as e:
        print(f"\nFEL: {e}")
    
    # UPPGIFT 1d: Newtons metod
    print("\nUPPGIFT 1d: Beräkning med Newtons metod")
    
    x0_newton = 0.8  # Startvärde för det andra nollstället
    # Valt för det andra nollstället där fixpunktsmetoden EJ konvergerar
    print(f"Startvärde: x0 = {x0_newton}")
    
    try:
        root_newton, iter_newton, hist_newton = newtons_metod(f, df, x0_newton, tol, max_iter, verbose=True)
    except RuntimeError as e:
        print(f"\nFEL: {e}")
    
    # UPPGIFT 1e: Jämförelse
    print("\nUPPGIFT 1e: Jämförelse av konvergenshastighet")
   
    x0_compare = 0.2  # Startvärde där båda metoderna konvergerar
    # Väljer nollställe där båda metoderna konvergerar
    compare_convergence(x0_compare)
    


if __name__ == "__main__":
    main()
