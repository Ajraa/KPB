"""
Cvičení 7 – Úloha 1: Analýza hesel, slovníkový útok, brute-force, entropie

Testovaná hesla: abc3, Heslo123, x7Kp9Lm2, strom-pes-auto
"""

import hashlib
import itertools
import math
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

HESLA = ["abc3", "Heslo123", "x7Kp9Lm2", "strom-pes-auto"]
ODDELOVAC = "=" * 65


def cast_1a():
    print(ODDELOVAC)
    print("ČÁST 1a: Heslo123!  vs  strom-pes-auto-lampa")
    print(ODDELOVAC)

    h1 = "Heslo123!"
    h2 = "strom-pes-auto-lampa"

    N1 = 94
    L1 = len(h1)
    H1_char = L1 * math.log2(N1)

    N2_char = 63
    L2 = len(h2)
    H2_char = L2 * math.log2(N2_char)

    # Diceware slovník má W = 7 776 slov (5 hodů kostkou = 6^5)
    W_diceware = 7_776
    k = 4          # strom-pes-auto-lampa = 4 slova
    H2_dict = k * math.log2(W_diceware)

    print(f"\n{'Heslo':<25} {'Délka':>5}  {'H (char) [bit]':>14}  {'H (slova) [bit]':>15}")
    print("-" * 65)
    print(f"{h1:<25} {L1:>5}  {H1_char:>14.1f}  {'–':>15}")
    print(f"{h2:<25} {L2:>5}  {H2_char:>14.1f}  {H2_dict:>15.1f}")

    print("\nVýsledek:")
    print(f"Heslo123!           znaková entropie ≈ {H1_char:.1f} bit")
    print(f"strom-pes-auto-lampa  znaková entropie ≈ {H2_char:.1f} bit")
    print(f"strom-pes-auto-lampa  slovníková entropie ≈ {H2_dict:.1f} bit")


# ══════════════════════════════════════════════════════════════
# ČÁST 1b-i – Slovníkový útok
# ══════════════════════════════════════════════════════════════

def nacti_slovnik() -> list[str]:
    """Načte slova ze souboru slovnik.txt (řádky začínající '#' přeskočí)."""
    cesta = os.path.join(os.path.dirname(__file__), "slovnik.txt")
    with open(cesta, encoding="utf-8") as f:
        return [
            radek.strip()
            for radek in f
            if radek.strip() and not radek.startswith("#")
        ]


def spocitej_hash(text: str) -> bytes:
    """SHA-256 hash textu jako bajty (32 B)."""
    return hashlib.sha256(text.encode("utf-8")).digest()


def slovnikovy_utok(hesla: list[str], slovnik: list[str]):
    """
    Slovníkový útok pomocí hashů — takto funguje v praxi:

    Scénář: útočník ukradl databázi s SHA-256 hashe hesel (ne plaintext).
    Pro každé slovo ze slovníku spočítá jeho hash a porovná ho s ukradeným
    hashem cílového hesla. Pokud se hashe shodují → heslo nalezeno.

    Krok 1: Předem spočítáme hashe všech cílových hesel (= "ukradená DB").
    Krok 2: Pro každé slovo ze slovníku: hash(slovo) == uložený_hash?
    """
    print(ODDELOVAC)
    print("ČÁST 1b-i: Slovníkový útok (porovnání hashů)")
    print(f"Slovník: {len(slovnik)} slov")
    print(ODDELOVAC)

    # Krok 1 — "ukradená databáze": heslo → jeho SHA-256 hash
    ulozene_hashe: dict[str, bytes] = {
        heslo: spocitej_hash(heslo)
        for heslo in hesla
    }

    print("Hashe cílových hesel (= co má útočník z databáze):")
    for heslo, h in ulozene_hashe.items():
        print(f"    {heslo:<20}  {h.hex()}")
    print()

    # Krok 2 — útok: pro každé heslo zkusíme prohledat slovník
    for cil, cil_hash in ulozene_hashe.items():
        pocet_pokusu = 0
        nalezeno = False

        zacatek = time.perf_counter()
        for slovo in slovnik:
            kandidat_hash = spocitej_hash(slovo)   # hash kandidáta
            pocet_pokusu += 1
            if kandidat_hash == cil_hash:           # porovnání hashů
                nalezeno = True
                break
        konec = time.perf_counter()

        cas_ms = (konec - zacatek) * 1_000
        if nalezeno:
            kandidat_hash_hex = spocitej_hash(slovo).hex()
            print(f"[{cil}]  NALEZENO po {pocet_pokusu} pokusech  ({cas_ms:.3f} ms)")
            print(f"kandidát:      '{slovo}'")
            print(f"hash(kandidát): {kandidat_hash_hex}")
            print(f"hash(hesla):    {cil_hash.hex()}")
            shoda = "STEJNÝ" if kandidat_hash_hex == cil_hash.hex() else "RŮZNÝ"
            print(f"Hashe jsou: {shoda}")
        else:
            print(f"[{cil:<18}]  NENALEZENO (vyzkoušeno {pocet_pokusu} slov)  ({cas_ms:.3f} ms)")
        print()


# ══════════════════════════════════════════════════════════════
# ČÁST 1b-ii – Brute-force útok
# ══════════════════════════════════════════════════════════════

def brute_force_utok(hesla: list[str]):
    """
    Brute-force útok (znaky abc123, délka 1–4) — dle zadání z PDF.

    Postup:
      1. Předem spočítáme SHA-256 hashe všech cílových hesel ("ukradená DB").
      2. Vygenerujeme VŠECHNY kombinace znaků {a,b,c,1,2,3} délky 1 až 4.
      3. Každou kombinaci zahashujeme (SHA-256) a porovnáme se VŠEMI
         uloženými hashi najednou — jeden průchod, všechna hesla.
      4. Zaznamenáme číslo pokusu a čas při každém nalezení.

    Celkový počet kombinací: 6^1 + 6^2 + 6^3 + 6^4 = 1 554
    """
    ZNAKY = "abc123"
    DELKY = range(1, 5)   # 1 až 4 (včetně)

    celkem_kombinaci = sum(len(ZNAKY) ** d for d in DELKY)

    print()
    print(ODDELOVAC)
    print("ČÁST 1b-ii: Brute-force útok (porovnání hashů)")
    print(f"Abeceda: '{ZNAKY}'  ({len(ZNAKY)} znaků),  délka 1–4")
    print(f"Celkem kombinací: {celkem_kombinaci}")
    print(ODDELOVAC)

    # Krok 1 — "ukradená databáze": heslo → SHA-256 hash
    ulozene_hashe: dict[str, bytes] = {
        heslo: spocitej_hash(heslo)
        for heslo in hesla
    }

    print("Hashe cílových hesel (= co má útočník z databáze):")
    for heslo, h in ulozene_hashe.items():
        print(f"{heslo:<20}  {h.hex()}")
    print()

    # Výsledky: heslo → (číslo_pokusu, čas_ms) nebo None
    vysledky: dict[str, tuple[int, float, str] | None] = {h: None for h in hesla}
    # Zbývající nenalezená hesla (hashmap hash→heslo pro O(1) lookup)
    hledam: dict[bytes, str] = {h: p for p, h in ulozene_hashe.items()}

    pocet_pokusu = 0
    zacatek = time.perf_counter()

    # Krok 2+3 — generujeme VŠECHNY kombinace, hashujeme, porovnáváme
    for delka in DELKY:
        for kombinace in itertools.product(ZNAKY, repeat=delka):
            kandidat = "".join(kombinace)
            kandidat_hash = spocitej_hash(kandidat)   # SHA-256 kandidáta
            pocet_pokusu += 1

            # Krok 3 — porovnání s uloženými hashi
            if kandidat_hash in hledam:
                cil = hledam.pop(kandidat_hash)        # odstraníme nalezené
                cas_ms = (time.perf_counter() - zacatek) * 1_000
                vysledky[cil] = (pocet_pokusu, cas_ms, kandidat)

    cas_celkem_ms = (time.perf_counter() - zacatek) * 1_000

    # Krok 4 — výpis výsledků
    print(f"Celkem pokusů: {pocet_pokusu}  |  Celkový čas: {cas_celkem_ms:.3f} ms")
    print()
    for heslo in hesla:
        vysledek = vysledky[heslo]
        if vysledek is not None:
            n, t, kandidat = vysledek
            kandidat_hash_hex = spocitej_hash(kandidat).hex()
            heslo_hash_hex    = ulozene_hashe[heslo].hex()
            shoda = "STEJNÝ" if kandidat_hash_hex == heslo_hash_hex else "RŮZNÝ"
            print(f"[{heslo}]  NALEZENO po {n} pokusech  ({t:.3f} ms)")
            print(f"kandidát:       '{kandidat}'")
            print(f"hash(kandidát):  {kandidat_hash_hex}")
            print(f"hash(hesla):     {heslo_hash_hex}")
            print(f"Hashe jsou: {shoda}")
        else:
            print(f"[{heslo:<18}]  NENALEZENO  (mimo prostor abecedy/délky)")
        print()

# ══════════════════════════════════════════════════════════════
# ČÁST 1c – Výpočet entropie
# ══════════════════════════════════════════════════════════════

def urcit_abecedu(heslo: str) -> tuple[int, str]:
    """
    Odhadne velikost abecedy N na základě použitých tříd znaků:
      - malá písmena a–z  →  +26
      - velká písmena A–Z →  +26
      - číslice 0–9       →  +10
      - speciální znaky   →  +32
    Vrátí (N, popis).
    """
    tridy = []
    N = 0
    if any(c.islower() for c in heslo):
        N += 26
        tridy.append("malá [26]")
    if any(c.isupper() for c in heslo):
        N += 26
        tridy.append("velká [26]")
    if any(c.isdigit() for c in heslo):
        N += 10
        tridy.append("číslice [10]")
    # Speciální znaky: vše mimo alfanumeriku
    if any(not c.isalnum() for c in heslo):
        N += 32
        tridy.append("spec. [32]")
    return N, " + ".join(tridy)


def entropie_znakovym_modelem(hesla: list[str]):
    """
    H = L · log₂(N)

    L = délka hesla
    N = velikost abecedy (odhadnuta z použitých tříd znaků)
    """
    print(ODDELOVAC)
    print("ČÁST 1c-i: Entropie – znakovým modelem  [H = L · log₂(N)]")
    print(ODDELOVAC)
    print(f"{'Heslo':<20} {'L':>4}  {'N':>4}  {'H [bit]':>8}  Třídy znaků")
    print("  " + "-" * 62)
    for heslo in hesla:
        L = len(heslo)
        N, popis = urcit_abecedu(heslo)
        H = L * math.log2(N)
        print(f"  {heslo:<20} {L:>4}  {N:>4}  {H:>8.2f}  {popis}")


def entropie_slovnikovym_modelem(hesla: list[str]):
    """
    H = k · log₂(W)

    k = počet slov, ze kterých je heslo složeno
    W = velikost slovníku (Diceware: 7 776 slov)

    Tento model se hodí pro přístupové fráze (passphrase).
    Pro hesla jako 'abc3' nebo 'x7Kp9Lm2' model nedává smysl (nejsou složena ze slov).
    """
    W_DICEWARE = 7_776   # 6^5 – Diceware seznam

    print()
    print(ODDELOVAC)
    print("ČÁST 1c-ii: Entropie – slovníkovým modelem  [H = k · log₂(W)]")
    print(f"Slovník Diceware: W = {W_DICEWARE} slov")
    print(ODDELOVAC)

    # Pouze hesla složená ze slov mají smysl v tomto modelu
    passfraze = {
        "strom-pes-auto":   3,    # 3 slova oddělená pomlčkou
        "Heslo123":         1,    # 1 slovo (heslo) + čísla – slabý případ
    }

    print(f"{'Heslo':<20} {'k':>4}  {'W':>6}  {'H [bit]':>9}  Poznámka")
    print("  " + "-" * 62)
    for heslo, k in passfraze.items():
        H = k * math.log2(W_DICEWARE)
        poznamka = "passphrase" if k > 1 else "jediné slovo (slabé)"
        print(f"  {heslo:<20} {k:>4}  {W_DICEWARE:>6}  {H:>9.2f}  {poznamka}")

def main():
    print(f"Testovaná hesla: {HESLA}\n")

    cast_1a()

    print()
    slovnik = nacti_slovnik()
    slovnikovy_utok(HESLA, slovnik)

    brute_force_utok(HESLA)

    print()
    entropie_znakovym_modelem(HESLA)
    entropie_slovnikovym_modelem(HESLA)

if __name__ == "__main__":
    main()
