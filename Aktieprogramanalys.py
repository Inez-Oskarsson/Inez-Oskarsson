"""
AKTIEANALYSPROGRAM
Allt i en fil 
"""

class Aktie:
    """Klass som representerar en aktie"""
    def __init__(self, namn, soliditet, p_e_tal, p_s_tal):
        """
        Initierar en Aktie-instans
        
        Args:
            namn (str): Aktiens namn
            soliditet (float): Soliditet i procent
            p_e_tal (float eller str): P/E-tal (eller "negativt" för negativa tal)
            p_s_tal (float): P/S-tal
        """
        self.namn = namn
        self.soliditet = soliditet
        self.p_e_tal = p_e_tal
        self.p_s_tal = p_s_tal
        self.historiska_kurser = []
    
    def berakna_avkastning(self):
        """
        Beräknar avkastning i procent baserat på historiska kurser
        
        Returns:
            float: Avkastning i procent (positiv eller negativ)
        """
        if len(self.historiska_kurser) < 2:
            return 0.0
        forsta = self.historiska_kurser[0]
        sista = self.historiska_kurser[-1]
        avkastning = (sista / forsta) - 1
        return round(avkastning * 100, 2)
    
    def hamta_lagsta_kurs(self):
        """
        Returnerar lägsta kursen från historiska kurser
        
        Returns:
            float: Lägsta kursvärdet, eller 0.0 om ingen kursdata finns
        """
        if not self.historiska_kurser:
            return 0.0
        return min(self.historiska_kurser)
    
    def hamta_hogsta_kurs(self):
        """
        Returnerar högsta kursen från historiska kurser
        
        Returns:
            float: Högsta kursvärdet, eller 0.0 om ingen kursdata finns
        """
        if not self.historiska_kurser:
            return 0.0
        return max(self.historiska_kurser)
    
    def berakna_betavarde(self, marknads_avkastning):
        """
        Beräknar risk (betavärde) jämfört med marknaden
        
        Args:
            marknads_avkastning (float): Marknadens totala avkastning (som decimaltal, t.ex. 0.05 för 5%)
            
        Returns:
            float: Betavärde som indikerar risknivå
        """
        if marknads_avkastning == 0:
            return 0.0
        egen = self.berakna_avkastning() / 100
        return round(egen / marknads_avkastning, 2)


def las_fundamenta(filnamn):
    """
    Läser aktiefundamenta från textfil
    
    Args:
        filnamn (str): Sökväg till filen med fundamenta
        
    Returns:
        dict: Dictionary med aktienamn som nyckel och Aktie-objekt som värde
    """
    aktier = {}
    try:
        with open(filnamn, 'r') as f:
            rader = [rad.strip() for rad in f]
    except FileNotFoundError:
        print(f"Fel: {filnamn} hittades inte")
        return aktier
    
    i = 0
    while i < len(rader):
        if i + 3 >= len(rader):
            break
        namn = rader[i]
        try:
            soliditet = float(rader[i+1])
            p_e_tal = rader[i+2]
            if p_e_tal != "negativt":
                p_e_tal = float(p_e_tal)
            p_s_tal = float(rader[i+3])
            aktier[namn] = Aktie(namn, soliditet, p_e_tal, p_s_tal)
        except ValueError:
            print(f"Varning: Felaktig data för {namn}, hoppar över")
        i += 4
    return aktier


def las_kurser(filnamn, aktier):
    """
    Läser historiska kurser och länkar till respektive aktie
    
    Args:
        filnamn (str): Sökväg till filen med kursdata
        aktier (dict): Dictionary med Aktie-objekt
    """
    try:
        with open(filnamn, 'r') as f:
            nuvarande = None
            for rad in f:
                rad = rad.strip()
                if not rad:
                    continue
                if rad in aktier:
                    nuvarande = aktier[rad]
                elif nuvarande and " " in rad:
                    try:
                        # Ta bort datum och hämta kursvärdet
                        kurs = float(rad.split()[-1])
                        nuvarande.historiska_kurser.append(kurs)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Fel: {filnamn} hittades inte")


def las_omx(filnamn):
    """
    Läser OMX-index historiska värden
    
    Args:
        filnamn (str): Sökväg till filen med OMX-data
        
    Returns:
        list: Lista med OMX-värden som float
    """
    omx = []
    try:
        with open(filnamn, 'r') as f:
            for rad in f:
                rad = rad.strip()
                if rad and " " in rad:
                    try:
                        varde = float(rad.split()[-1])
                        omx.append(varde)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Fel: {filnamn} hittades inte")
    return omx


def visa_meny():
    """
    Visar huvudmenyn och hanterar användarens val
    
    Returns:
        int: Vald meny-alternativ (1-4)
    """
    print("\n" + "_" * 40)
    print("MENY")
    print("_" * 40)
    print("1. Fundamental analys (Vid långsiktigt aktieinnehav)")
    print("2. Teknisk analys (Vid kort aktieinnehav)")
    print("3. Rangordning av aktier med avseende på dess betavärde")
    print("4. Avsluta")
    print("_" * 40)
    
    while True:
        try:
            val = int(input("Vilket alternativ vill du välja? "))
            if 1 <= val <= 4:
                return val
            else:
                print("Fel! Välj mellan 1 och 4")
        except ValueError:
            print("Fel! Ange en siffra mellan 1 och 4")


def valj_aktie(aktier, analys_typ):
    """
    Låter användaren välja en aktie från listan
    
    Args:
        aktier (dict): Dictionary med tillgängliga aktier
        analys_typ (str): Typ av analys ("fundamental" eller "teknisk")
        
    Returns:
        Aktie: Vald Aktie-instans, eller None om avbrutet
    """
    namn_lista = list(aktier.keys())
    
    print(f"\nEn {analys_typ} analys kan utföras för följande aktier:")
    for i, namn in enumerate(namn_lista, 1):
        print(f"{i}. {namn}")
    
    while True:
        try:
            val = int(input(f"Vilken aktie vill du göra {analys_typ} analys på? "))
            if 1 <= val <= len(namn_lista):
                return aktier[namn_lista[val-1]]
            else:
                print(f"Felaktigt val! Välj mellan 1 och {len(namn_lista)}")
        except ValueError:
            print("Fel! Ange en siffra")
        except KeyboardInterrupt:
            return None


def gor_langsiktig_analys(aktier):
    """
    Gör fundamental analys av en aktie baserat på fundamenta
    
    Args:
        aktier (dict): Dictionary med tillgängliga aktier
    """
    if not aktier:
        print("Inga aktier!")
        return
    
    aktie = valj_aktie(aktier, "fundamental")
    if not aktie:
        return
    
    print("\n" + "_" * 40)
    print(f"Fundamental analys för {aktie.namn}")
    print("_" * 40)
    
    # Använd kommatecken för procentenligt svenskt format
    soliditet_str = str(aktie.soliditet).replace('.', ',')
    print(f"företagets soliditet är {soliditet_str} %")
    print(f"företagets p/e-tal är {aktie.p_e_tal}")
    
    # Formatera P/S-tal med kommatecken
    p_s_str = str(aktie.p_s_tal).replace('.', ',')
    print(f"företagets p/s-tal är {p_s_str}")
    
    print("\nBedömning:")
    if aktie.soliditet > 50:
        print("Mycket stark soliditet (>50%) - Företaget har goda marginaler")
    elif aktie.soliditet > 30:
        print("Godkänd soliditet (30-50%) - Företaget har stabil ekonomi")
    else:
        print("Låg soliditet (<30%) - Företaget har smala marginaler")
    
    if aktie.p_e_tal == "negativt":
        print("Företaget går med förlust - inget P/E-tal kan beräknas")
    elif isinstance(aktie.p_e_tal, (int, float)):
        if aktie.p_e_tal < 15:
            print("Bra P/E-tal (<15) - Aktien kan vara undervärderad")
        elif aktie.p_e_tal < 25:
            print("Normalt P/E-tal (15-25) - Aktien är rimligt värderad")
        else:
            print("Högt P/E-tal (>25) - Aktien kan vara övervärderad")


def gor_kortsiktig_analys(aktier, marknad):
    """
    Gör teknisk analys av en aktie baserat på kursutveckling
    
    Args:
        aktier (dict): Dictionary med tillgängliga aktier
        marknad (float): Marknadens totala avkastning som decimaltal
    """
    if not aktier:
        print("Inga aktier!")
        return
    
    aktie = valj_aktie(aktier, "teknisk")
    if not aktie:
        return
    
    if len(aktie.historiska_kurser) < 2:
        print(f"Inte tillräckligt med kursdata för {aktie.namn}")
        return
    
    print("\n" + "_" * 40)
    print(f"Teknisk analys för {aktie.namn}")
    print("_" * 40)
    
    avkastning = aktie.berakna_avkastning()
    beta = aktie.berakna_betavarde(marknad)
    lagsta = aktie.hamta_lagsta_kurs()
    hogsta = aktie.hamta_hogsta_kurs()
    
    # Formatera med kommatecken enligt svenskt format
    avkastning_str = str(avkastning).replace('.', ',')
    beta_str = str(beta).replace('.', ',')
    lagsta_str = str(lagsta).replace('.', ',')
    hogsta_str = str(hogsta).replace('.', ',')
    
    print(f"kursutveckling(30 senaste dagarna) {avkastning_str} %")
    print(f"betavärde {beta_str}")
    print(f"lägsta kurs(30 senaste dagarna) {lagsta_str}")
    print(f"högsta kurs(30 senaste dagarna) {hogsta_str}")
    
    print("\nBedömning:")
    if avkastning > 10:
        print("Stark avkastning (>10%) - Mycket positiv utveckling")
    elif avkastning > 0:
        print("Positiv avkastning (0-10%) - God utveckling")
    else:
        print("Negativ avkastning - Nedåtgående trend")
    
    if beta > 1.5:
        print("Hög risk (beta > 1,5) - Volatil aktie, stora svängningar")
    elif beta > 0.8:
        print("Normal risk (beta 0,8-1,5) - Normal volatilitet")
    else:
        print("Låg risk (beta < 0,8) - Stabil aktie, små svängningar")


def rangordna_efter_risk(aktier, marknad):
    """
    Rangordnar aktier efter risk (betavärde)
    
    Args:
        aktier (dict): Dictionary med tillgängliga aktier
        marknad (float): Marknadens totala avkastning som decimaltal
    """
    if not aktier:
        print("Inga aktier!")
        return
    
    lista = []
    for namn, aktie in aktier.items():
        if len(aktie.historiska_kurser) >= 2:
            risk = aktie.berakna_betavarde(marknad)
            lista.append((namn, risk))
    
    if not lista:
        print("Ingen tillräcklig kursdata för att beräkna betavärden!")
        return
    
    # Sortera efter risk (högst först)
    lista.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "_" * 50)
    print("Rangordning av aktier med avseende på dess betavärde")
    print("_" * 50)
    
    for i, (namn, risk) in enumerate(lista, 1):
        risk_str = str(risk).replace('.', ',')
        print(f"{i}. {namn} {risk_str}")


def main():
    """Huvudfunktion som kör aktieanalysprogrammet"""
    print("Startar aktieanalysprogram...")
    
    # 1. Definiera filnamn som vanliga variabler med små bokstäver
    fundamenta_fil = "fundamenta.txt"
    kurser_fil = "kurser.txt"
    omx_fil = "omx.txt"
    
    # 2. Läs data från filer
    aktier = las_fundamenta(fundamenta_fil)
    if not aktier:
        print(f"Inga aktier hittades i {fundamenta_fil}! Avslutar.")
        return
    
    las_kurser(kurser_fil, aktier)
    omx = las_omx(omx_fil)
    
    # 3. Beräkna marknadsavkastning
    if len(omx) >= 2:
        marknad = (omx[-1] / omx[0]) - 1
        marknad_procent = round(marknad * 100, 2)
        marknad_str = str(marknad_procent).replace('.', ',')
        print(f"\nMarknadsavkastning (OMX): {marknad_str}%")
    else:
        print("\nVarning: Otillräcklig OMX-data, använder standardvärde 5%")
        marknad = 0.05
    
    print(f"{len(aktier)} aktier laddade")
    
    # 4. Huvudloop
    while True:
        val = visa_meny()
        
        if val == 1:
            gor_langsiktig_analys(aktier)
        elif val == 2:
            gor_kortsiktig_analys(aktier, marknad)
        elif val == 3:
            rangordna_efter_risk(aktier, marknad)
        elif val == 4:
            print("\nTack för att du använde programmet!")
            break


if __name__ == "__main__":
    main()
