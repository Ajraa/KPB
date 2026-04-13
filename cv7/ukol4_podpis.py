"""
Cvičení 7 – Úloha 4: Digitální podpis RSA

Demonstrace:
  a) Generování klíčového páru RSA, podpis zprávy M1, ověření podpisu
  b) Pokus o ověření PŮVODNÍHO podpisu se ZMĚNĚNOU zprávou M2 → selže
  c) Nový pár klíčů, podpis M1 NOVÝM soukromým klíčem,
     pokus o ověření PŮVODNÍM veřejným klíčem → selže

Instalace závislostí:
  pip install cryptography

Princip RSA podpisu:
  1. Spočítej hash zprávy (SHA-256).
  2. Zašifruj hash SOUKROMÝM klíčem → to je podpis.
  3. Ověření: dešifruj podpis VEŘEJNÝM klíčem → porovnej s hash(zprávy).
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

ODDELOVAC = "=" * 65


# Pomocné funkce
def generuj_rsa_klic(bits: int = 2048):
    """
    Vygeneruje RSA klíčový pár.

    bits = délka modulu (doporučeno ≥ 2048, pro produkci 3072/4096).
    Soukromý klíč obsahuje p, q, d (tajné).
    Veřejný klíč obsahuje n, e (veřejné, e = 65537 standardně).
    """
    soukromy = rsa.generate_private_key(
        public_exponent=65537,   # standardní Fermatovo číslo F4
        key_size=bits,
    )
    verejny = soukromy.public_key()
    return soukromy, verejny


def podepis(soukromy_klic, zprava: bytes) -> bytes:
    """
    Podepíše zprávu:
      1. SHA-256 hash zprávy se spočítá interně.
      2. Hash se ŠIFRUJE soukromým klíčem (RSA-PSS schéma).

    PSS (Probabilistic Signature Scheme) je doporučené padding schéma
    (bezpečnější než starší PKCS#1 v1.5 padding).
    """
    podpis_bytes = soukromy_klic.sign(
        zprava,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return podpis_bytes


def over_podpis(verejny_klic, zprava: bytes, podpis_bytes: bytes) -> bool:
    """
    Ověří podpis:
      1. Dešifruje podpis VEŘEJNÝM klíčem → hash_z_podpisu.
      2. Spočítá SHA-256 zprávy → hash_zpravy.
      3. Porovná: hash_z_podpisu == hash_zpravy.

    Vrátí True pokud podpis platí, False pokud ne.
    """
    try:
        verejny_klic.verify(
            podpis_bytes,
            zprava,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def tiskni_klic_info(verejny_klic, label: str):
    """Vytiskne veřejný exponent a délku klíče."""
    pub = verejny_klic.public_numbers()
    bits = verejny_klic.key_size
    print(f"  {label}")
    print(f"    Délka klíče: {bits} bitů")
    print(f"    Veřejný exponent e: {pub.e}")
    # Zobrazíme prvních a posledních 16 hexadecimálních číslic modulu n
    n_hex = hex(pub.n)[2:]
    print(f"    Modul n (hex, zkráceno): {n_hex[:16]}…{n_hex[-16:]}")


def tiskni_vysledek(label: str, platny: bool):
    znacka = "✓  PLATNÝ" if platny else "✗  NEPLATNÝ"
    print(f"  {label:<55}  {znacka}")


# Úloha 4a – Generování klíčů, podpis M1, ověření
def ukol_4a(M1: bytes):
    print()
    print(ODDELOVAC)
    print("  4a: Generování klíčů RSA, podpis M1, ověření")
    print(ODDELOVAC)

    sk1, pk1 = generuj_rsa_klic(bits=2048)
    tiskni_klic_info(pk1, "Klíčový pár #1 (RSA-2048):")

    print()
    print(f"  Zpráva M1: {M1.decode()!r}")

    podpis_m1 = podepis(sk1, M1)
    print(f"  Podpis (prvních 32 bajtů hex): {podpis_m1[:32].hex()}…")

    print()
    print("  Ověření podpisu:")
    vysledek = over_podpis(pk1, M1, podpis_m1)
    tiskni_vysledek("Veřejný klíč #1 + zpráva M1 + podpis klíčem #1", vysledek)

    return sk1, pk1, podpis_m1


# Úloha 4b – Ověření původního podpisu se změněnou zprávou M2
def ukol_4b(pk1, M1: bytes, M2: bytes, podpis_m1: bytes):
    print()
    print(ODDELOVAC)
    print("  4b: Ověření původního podpisu se ZMĚNĚNOU zprávou M2")
    print(ODDELOVAC)

    print(f"  Původní zpráva M1: {M1.decode()!r}")
    print(f"  Změněná zpráva M2: {M2.decode()!r}")
    print()
    print("  Pokus o ověření (původní podpis + změněná zpráva M2):")

    vysledek = over_podpis(pk1, M2, podpis_m1)
    tiskni_vysledek("Veřejný klíč #1 + zpráva M2 + podpis klíčem #1", vysledek)


# Úloha 4c – Nový pár klíčů, podpis jiným klíčem, ověření původním PK
def ukol_4c(pk1, M1: bytes):
    print()
    print(ODDELOVAC)
    print("  4c: Nový klíčový pár, podpis M1 jiným klíčem, ověření původním PK")
    print(ODDELOVAC)

    sk2, pk2 = generuj_rsa_klic(bits=2048)
    tiskni_klic_info(pk2, "Klíčový pár #2 (nově vygenerovaný RSA-2048):")

    podpis_m1_sk2 = podepis(sk2, M1)
    print()
    print(f"  Zpráva M1: {M1.decode()!r}")
    print(f"  Podpis vytvořen klíčem SK2 (prvních 32 bajtů hex): {podpis_m1_sk2[:32].hex()}…")

    print()
    print("  Ověření podpisu:")

    # Správné ověření: PK2 + podpis SK2 → platný
    vysledek_spravny = over_podpis(pk2, M1, podpis_m1_sk2)
    tiskni_vysledek("Veřejný klíč #2 + zpráva M1 + podpis klíčem #2", vysledek_spravny)

    # Nesprávné ověření: PK1 + podpis SK2 → neplatný
    vysledek_chybny = over_podpis(pk1, M1, podpis_m1_sk2)
    tiskni_vysledek("Veřejný klíč #1 + zpráva M1 + podpis klíčem #2", vysledek_chybny)



# Hlavní výstup
def main():
    # Definice zpráv
    M1 = b"Toto je originalni zprava M1. KPB 2026."
    M2 = b"Toto je ZMENENA zprava M2.  KPB 2026."

    print(f"  M1: {M1.decode()!r}")
    print(f"  M2: {M2.decode()!r}")
    print()
    print("  Generuji klíče (RSA-2048)…")

    # Úlohy
    sk1, pk1, podpis_m1 = ukol_4a(M1)
    ukol_4b(pk1, M1, M2, podpis_m1)
    ukol_4c(pk1, M1)

if __name__ == "__main__":
    main()
