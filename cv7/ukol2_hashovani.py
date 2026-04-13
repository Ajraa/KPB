"""
Cvičení 7 – Úloha 2: Měření rychlosti hashovacích funkcí

Porovnání: SHA-256 (hashlib), bcrypt, Argon2 (argon2-cffi)

Spustíme každou funkci po dobu MERENI_SEKUND sekund a změříme:
  • celkový počet hashů
  • čas na jeden hash (průměr)
  • počet hashů za sekundu

Instalace závislostí:
  pip install bcrypt argon2-cffi
"""

import hashlib
import sys
import time
from argon2 import PasswordHasher
import bcrypt as _bcrypt



sys.stdout.reconfigure(encoding="utf-8")

ODDELOVAC = "=" * 65
HESLO_BYTES = b"TestHeslo123"   # stejné heslo pro všechny funkce
MERENI_SEKUND = 3               # délka měřicího okna


# SHA-256  (hashlib – standardní knihovna)
def benchmark_sha256() -> tuple[int, float]:
    """
    Vrátí (počet_hashů, čas_na_jeden_hash_v_µs).
    """
    pocet = 0
    zacatek = time.perf_counter()
    while time.perf_counter() - zacatek < MERENI_SEKUND:
        hashlib.sha256(HESLO_BYTES).hexdigest()
        pocet += 1
    celkovy_cas = time.perf_counter() - zacatek
    cas_na_hash_us = (celkovy_cas / pocet) * 1_000_000
    return pocet, cas_na_hash_us


# bcrypt  (knihovna: bcrypt)
def benchmark_bcrypt(cost_factor: int = 12) -> tuple[int, float]:
    """
    bcrypt automaticky přidává SALT (zabránění rainbow table útokům).

    Vrátí (počet_hashů, čas_na_jeden_hash_v_ms).
    """

    # Předem vygenerujeme salt (bcrypt.gensalt je deterministické per-call)
    salt = _bcrypt.gensalt(rounds=cost_factor)

    pocet = 0
    zacatek = time.perf_counter()
    while time.perf_counter() - zacatek < MERENI_SEKUND:
        _bcrypt.hashpw(HESLO_BYTES, salt)
        pocet += 1
    celkovy_cas = time.perf_counter() - zacatek
    cas_na_hash_ms = (celkovy_cas / pocet) * 1_000
    return pocet, cas_na_hash_ms


# Argon2  (argon2-cffi)
def benchmark_argon2() -> tuple[int, float]:
    """
    Parametry (PasswordHasher výchozí hodnoty):
      time_cost  = počet iterací (rounds)
      memory_cost = paměť v KiB (výchozí 65 536 = 64 MB)
      parallelism = počet paralelních vláken
    Vrátí (počet_hashů, čas_na_jeden_hash_v_ms).
    """

    ph = PasswordHasher()   # výchozí parametry: time=3, memory=65536 KiB, parallel=4
    heslo_str = HESLO_BYTES.decode()

    pocet = 0
    zacatek = time.perf_counter()
    while time.perf_counter() - zacatek < MERENI_SEKUND:
        ph.hash(heslo_str)
        pocet += 1
    celkovy_cas = time.perf_counter() - zacatek
    cas_na_hash_ms = (celkovy_cas / pocet) * 1_000
    return pocet, cas_na_hash_ms

def vytiskni_vysledek(nazev: str, pocet: int, cas: float, jednotka: str):
    """Formátovaný výpis výsledků benchmarku."""
    if pocet == 0:
        print(f"  {nazev:<12}  (přeskočeno – chybí knihovna)")
        return
    hs = pocet / MERENI_SEKUND
    print(f"  {nazev:<12}  {pocet:>7} hashů / {MERENI_SEKUND}s"
          f"  |  {hs:>12.1f} h/s"
          f"  |  {cas:>10.3f} {jednotka}/hash")


def main():
    print(f"  Heslo: '{HESLO_BYTES.decode()}'")
    print(f"  Měření po {MERENI_SEKUND} sekundách na funkci")

    #SHA-256
    print("  SHA-256…")
    sha_pocet, sha_cas_us = benchmark_sha256()

    #bcrypt
    print("  bcrypt (cost factor 12)…")
    bcrypt_pocet, bcrypt_cas_ms = benchmark_bcrypt(cost_factor=12)

    #Argon2
    print("  Argon2…")
    argon2_pocet, argon2_cas_ms = benchmark_argon2()

    #Výsledky
    print()
    print(ODDELOVAC)
    print(f"  {'Funkce':<12}  {'Hashů / 3s':>16}  {'Hashů/s':>14}  {'Čas/hash':>14}")
    print("  " + "-" * 60)
    vytiskni_vysledek("SHA-256",    sha_pocet,    sha_cas_us,    "µs")
    vytiskni_vysledek("bcrypt-12",  bcrypt_pocet, bcrypt_cas_ms, "ms")
    vytiskni_vysledek("Argon2id",   argon2_pocet, argon2_cas_ms, "ms")


if __name__ == "__main__":
    main()