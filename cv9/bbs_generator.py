import sys
import secrets
import os
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")


# Primality test (Miller-Rabin)

def is_prime(n: int, rounds: int = 25) -> bool:
    """Miller-Rabinův test prvočíselnosti."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    # Zapsat n-1 jako 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_blum_prime(bits: int) -> int:
    """Generuje prvočíslo délky `bits` bitů splňující p ≡ 3 (mod 4)."""
    while True:
        # Náhodné číslo přesně `bits` bitů, liché
        p = secrets.randbits(bits)
        p |= (1 << (bits - 1))  # zajistí přesnou délku
        p |= 1                   # zajistí lichost

        # Upravit na p ≡ 3 (mod 4)
        remainder = p % 4
        if remainder == 1:
            p += 2          # 1 → 3
        elif remainder == 0:
            p += 3
        elif remainder == 2:
            p += 1

        if p.bit_length() != bits:
            continue        # přetečení bitu — zkusit znovu
        if is_prime(p):
            assert p % 4 == 3
            return p


# BBS generátor

def blum_blum_shub(n: int, x0: int, num_bits: int) -> list[int]:
    """Generuje `num_bits` bitů pomocí BBS generátoru."""
    bits = []
    x = x0
    for _ in range(num_bits):
        x = pow(x, 2, n)
        bits.append(x & 1)
    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    assert len(bits) % 8 == 0
    result = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)


# Statistické testy

def test_uniform(bits: list[int]) -> dict:
    """Test uniformního rozdělení — poměr jedniček a nul."""
    ones = sum(bits)
    zeros = len(bits) - ones
    ratio = ones / len(bits)
    return {
        "ones":        ones,
        "zeros":       zeros,
        "ratio_ones":  ratio,
        "balanced":    abs(ratio - 0.5) < 0.05,
    }


def test_repeatability(n: int, x0: int, num_bits: int) -> bool:
    """Ověří, zda BBS vrátí stejný výstup pro stejné vstupy."""
    a = blum_blum_shub(n, x0, num_bits)
    b = blum_blum_shub(n, x0, num_bits)
    return a == b


def test_runs(bits: list[int]) -> dict:
    """Test délky běhů jedniček a nul (runs & gaps)."""
    runs = []
    cur_val = bits[0]
    cur_len = 1
    for b in bits[1:]:
        if b == cur_val:
            cur_len += 1
        else:
            runs.append((cur_val, cur_len))
            cur_val = b
            cur_len = 1
    runs.append((cur_val, cur_len))

    ones_runs  = [l for v, l in runs if v == 1]
    zeros_runs = [l for v, l in runs if v == 0]

    return {
        "total_runs":        len(runs),
        "ones_runs_count":   len(ones_runs),
        "zeros_runs_count":  len(zeros_runs),
        "avg_run_length":    len(bits) / len(runs),
        "ones_run_dist":     Counter(ones_runs),
        "zeros_run_dist":    Counter(zeros_runs),
        "longest_run":       max(l for _, l in runs),
    }


# Generování bezpečného bitového řetězce pomocí secrets

def generate_secure_bits(num_bits: int) -> list[int]:
    """Kryptograficky bezpečný bitový řetězec (os.urandom přes secrets)."""
    num_bytes = (num_bits + 7) // 8
    data = secrets.token_bytes(num_bytes)
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits[:num_bits]


# Výstupní report

def report_bits(name: str, bits: list[int],
                uniform: dict, runs: dict,
                repeatability: bool | None = None) -> str:
    lines = []
    lines.append(f"\n{'─' * 50}")
    lines.append(f"  {name}")
    lines.append(f"{'─' * 50}")
    lines.append(f"Délka sekvence : {len(bits)} bitů")

    lines.append(f"\n[a] Test uniformního rozdělení")
    lines.append(f"    Jedničky : {uniform['ones']} ({uniform['ratio_ones'] * 100:.2f} %)")
    lines.append(f"    Nuly     : {uniform['zeros']} ({(1 - uniform['ratio_ones']) * 100:.2f} %)")
    lines.append(f"    Vyváženo : {'ANO [OK]' if uniform['balanced'] else 'NE [!!]'}")

    if repeatability is not None:
        lines.append(f"\n[b] Test opakovatelnosti")
        lines.append(f"    Deterministický výstup : {'ANO [OK]' if repeatability else 'NE [!!]'}")

    lines.append(f"\n[c] Běžné sekvence — runs & gaps")
    lines.append(f"    Celkem běhů        : {runs['total_runs']}")
    lines.append(f"    Průměrná délka     : {runs['avg_run_length']:.2f}")
    lines.append(f"    Nejdelší běh       : {runs['longest_run']}")
    lines.append(f"    Běhů jedniček      : {runs['ones_runs_count']}")
    lines.append(f"    Běhů nul           : {runs['zeros_runs_count']}")

    lines.append(f"\n    Rozdělení délek běhů jedniček:")
    for length in sorted(runs["ones_run_dist"])[:8]:
        lines.append(f"      délka {length:2d}: {runs['ones_run_dist'][length]:3d}×")

    lines.append(f"\n    Rozdělení délek běhů nul:")
    for length in sorted(runs["zeros_run_dist"])[:8]:
        lines.append(f"      délka {length:2d}: {runs['zeros_run_dist'][length]:3d}×")

    text = "\n".join(lines)
    print(text)
    return text


def comparison_report(bbs_u: dict, sec_u: dict,
                      bbs_r: dict, sec_r: dict) -> str:
    lines = []
    lines.append(f"  POROVNÁNÍ: BBS vs. secrets")
    lines.append(f"{'Vlastnost':<40} {'BBS':>10} {'secrets':>10}")
    lines.append(f"{'─' * 64}")
    lines.append(f"{'Poměr jedniček (%)':<40} {bbs_u['ratio_ones']*100:>9.2f}% {sec_u['ratio_ones']*100:>9.2f}%")
    lines.append(f"{'Celkem běhů':<40} {bbs_r['total_runs']:>10} {sec_r['total_runs']:>10}")
    lines.append(f"{'Průměrná délka běhu':<40} {bbs_r['avg_run_length']:>10.2f} {sec_r['avg_run_length']:>10.2f}")
    lines.append(f"{'Nejdelší běh':<40} {bbs_r['longest_run']:>10} {sec_r['longest_run']:>10}")
    lines.append(f"{'─' * 64}")
    
    text = "\n".join(lines)
    print(text)
    return text


# Hlavní program

if __name__ == "__main__":
    NUM_BITS = 1024
    PRIME_BITS = 512

    print(f"Generuji dvě {PRIME_BITS}-bitová Blumova prvočísla (p ≡ q ≡ 3 mod 4)...")

    p = generate_blum_prime(PRIME_BITS)
    q = generate_blum_prime(PRIME_BITS)
    while q == p:
        q = generate_blum_prime(PRIME_BITS)

    n = p * q
    print(f"p ≡ {p % 4} (mod 4)  [{'OK' if p % 4 == 3 else 'CHYBA'}]")
    print(f"q ≡ {q % 4} (mod 4)  [{'OK' if q % 4 == 3 else 'CHYBA'}]")
    print(f"n = p·q má {n.bit_length()} bitů")

    # Seed musí být nesoudělný s n (prakticky libovolné číslo ≠ násobek p nebo q)
    x0 = secrets.randbelow(n - 2) + 2
    while x0 % p == 0 or x0 % q == 0:
        x0 = secrets.randbelow(n - 2) + 2

    print(f"Generování {NUM_BITS} bitů pomocí BBS")
    bbs_bits = blum_blum_shub(n, x0, NUM_BITS)

    # [b] Opakovatelnost
    repeatable = test_repeatability(n, x0, NUM_BITS)

    # Statistické testy — BBS
    bbs_uniform = test_uniform(bbs_bits)
    bbs_runs    = test_runs(bbs_bits)

    # [d] Generování pomocí secrets
    print("Generování bezpečného bitového řetězce (secrets)")
    sec_bits    = generate_secure_bits(NUM_BITS)
    sec_uniform = test_uniform(sec_bits)
    sec_runs    = test_runs(sec_bits)

    # [e] Report
    print("Statistické testy a report")
    report_bits("Blum Blum Shub", bbs_bits, bbs_uniform, bbs_runs, repeatability=repeatable)
    report_bits("secrets (CSPRNG)", sec_bits, sec_uniform, sec_runs)
    comparison_report(bbs_uniform, sec_uniform, bbs_runs, sec_runs)
