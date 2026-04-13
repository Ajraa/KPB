"""
Cvičení 7 – Úloha 3: SHA-256 hashe a počet rozdílných bitů

Vygeneruje SHA-256 hashe pro: heslo123, heslo124, Heslo123
Porovná každý pár hashů a spočítá počet bitů, které se liší
na stejných pozicích (Hammingova vzdálenost na bitech).

Tato vlastnost se nazývá AVALANCHE EFFECT (lavinový efekt):
  → Malá změna na vstupu → velká změna na výstupu.
  → Ideálně by se mělo lišit ~50 % bitů (= 128 bitů z 256).
"""

import hashlib
import sys

# Nastavení UTF-8 výstupu (nutné na Windows s cp1250)
sys.stdout.reconfigure(encoding="utf-8")

ODDELOVAC = "=" * 65
HESLA = ["heslo123", "heslo124", "Heslo123"]


# Výpočet SHA-256 hashe
def sha256_hash(text: str) -> bytes:
    """Vrátí SHA-256 hash jako bajty (32 bajtů = 256 bitů)."""
    return hashlib.sha256(text.encode("utf-8")).digest()


def bajty_na_bity(bajty: bytes) -> str:
    """Převede bajty na binární řetězec '010110…' (256 znaků pro SHA-256)."""
    return "".join(f"{b:08b}" for b in bajty)


# Hammingova vzdálenost (počet rozdílných bitů na stejných pozicích)
def hammingova_vzdalenost(bity_a: str, bity_b: str) -> int:
    """
    Počet pozic, kde se dva binární řetězce liší.
    Implementace: XOR na celých číslech → popcnt (bin().count('1')).

    bin_a XOR bin_b → 1 tam, kde jsou bity různé → count('1') = vzdálenost.
    """
    a = int(bity_a, 2)
    b = int(bity_b, 2)
    xor = a ^ b                      # bit je 1 tam, kde se liší
    vzdalenost = bin(xor).count("1") # počet jedniček = počet rozdílů
    return vzdalenost

# Vizualizace: ukázka prvních N bitů s vyznačením rozdílů
def vizualizuj_bity(bity_a: str, bity_b: str, pocet_bitu: int = 64) -> str:
    """
    Vrátí řetězec označující rozdílné bity symbolem '▲'.
    Zobrazí prvních pocet_bitu bitů každého hashe.
    """
    a_cast = bity_a[:pocet_bitu]
    b_cast = bity_b[:pocet_bitu]
    rozdily = "".join("▲" if x != y else " " for x, y in zip(a_cast, b_cast))
    return a_cast, b_cast, rozdily


# Hlavní výstup
def main():
    #Výpočet hashů
    vysledky: dict[str, dict] = {}
    for heslo in HESLA:
        h_bytes = sha256_hash(heslo)
        h_hex   = h_bytes.hex()
        h_bity  = bajty_na_bity(h_bytes)
        vysledky[heslo] = {"hex": h_hex, "bity": h_bity}

    #Výpis hashů
    print()
    print("SHA-256 hashe:")
    print("" + "-" * 62)
    for heslo, data in vysledky.items():
        print(f"{heslo:<12}  {data['hex']}")

    #Porovnání párů
    pary = [
        ("heslo123", "heslo124"),    # 1 číslice změněna (3 → 4)
        ("heslo123", "Heslo123"),    # 1 znak změněn (h → H, malé vs. velké)
        ("heslo124", "Heslo123"),    # kombinace obou změn
    ]

    print()
    print(ODDELOVAC)
    print("Porovnání párů – Hammingova vzdálenost:")
    print(ODDELOVAC)
    print(f"{'Pár':<28}  {'Rozdíl [bitů]':>13}  {'Rozdíl [%]':>11}  {'Hodnocení':>12}")
    print("-" * 70)

    for a, b in pary:
        bity_a = vysledky[a]["bity"]
        bity_b = vysledky[b]["bity"]
        vzd = hammingova_vzdalenost(bity_a, bity_b)
        procenta = (vzd / 256) * 100
        hodnoceni = "ideální" if 100 <= vzd <= 156 else ("nízký" if vzd < 80 else "vysoký")
        par_str = f"{a}  ↔  {b}"
        print(f"  {par_str:<28}  {vzd:>13}  {procenta:>10.1f}%  {hodnoceni:>12}")

    #Vizualizace prvních 64 bitů
    print()
    print(ODDELOVAC)
    print("Vizualizace prvních 64 bitů (▲ = rozdílný bit):")
    print(ODDELOVAC)

    for a, b in pary:
        bity_a = vysledky[a]["bity"]
        bity_b = vysledky[b]["bity"]
        cast_a, cast_b, rozdily = vizualizuj_bity(bity_a, bity_b, 64)
        pocet_rozdilu_64 = rozdily.count("▲")
        print(f"\nPár: {a}  ↔  {b}  ({pocet_rozdilu_64}/64 bitů)")
        print(f"{a:<12}: {cast_a}")
        print(f"{b:<12}: {cast_b}")
        print(f"{'rozdíly':<12}: {rozdily}")


if __name__ == "__main__":
    main()
