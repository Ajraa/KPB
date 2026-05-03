"""
Ověření výpočtů pro 3. zápočtový úkol KPB
"""
import math


def uloha1():
    print("=" * 50)
    print("ÚLOHA 1: (3^547) mod 29")
    print("=" * 50)
    p = 29
    a = 3
    exp = 547
    phi = p - 1  # fi(29) = 28

    q, r = divmod(exp, phi)
    print(f"φ(29) = {phi}")
    print(f"gcd(3, 29) = {math.gcd(a, p)}")
    print(f"547 = {phi} × {q} + {r}  →  3^547 ≡ 3^{r} (mod 29)")
    print()
    print("Opakované umocňování pro 3^15 mod 29:")
    print(f"  3^1  = {pow(3, 1, 29)}")
    print(f"  3^2  = {pow(3, 2, 29)}")
    print(f"  3^4  = {pow(3, 4, 29)}")
    print(f"  3^8  = {pow(3, 8, 29)}")
    step1 = (pow(3, 8, 29) * pow(3, 4, 29)) % 29
    step2 = (step1 * pow(3, 2, 29)) % 29
    step3 = (step2 * pow(3, 1, 29)) % 29
    print(f"  7 × 23 = 161 ≡ {step1} (mod 29)")
    print(f"  {step1} × 9 = {step1*9} ≡ {step2} (mod 29)")
    print(f"  {step2} × 3 = {step2*3} ≡ {step3} (mod 29)")
    print()
    result = pow(a, exp, p)
    print(f"VÝSLEDEK: (3^547) mod 29 = {result}")


def uloha2():
    print()
    print("=" * 50)
    print("ÚLOHA 2: Prvek, který NENÍ generátorem v Z₈₂₇")
    print("=" * 50)
    p = 827
    phi = p - 1  # 826

    n = phi
    factors = []
    tmp = n
    d = 2
    while d * d <= tmp:
        while tmp % d == 0:
            factors.append(d)
            tmp //= d
        d += 1
    if tmp > 1:
        factors.append(tmp)
    prime_factors = sorted(set(factors))

    print(f"φ(827) = {phi} = 2 × 7 × 59")
    print(f"Prvočíselní dělitelé: {prime_factors}")
    print()
    g = 826
    print(f"Volba: g = {g} ≡ -1 (mod 827)")
    print(f"  ord({g}) = 2, protože:")
    print(f"  {g}^1 mod 827 = {pow(g, 1, p)}")
    print(f"  {g}^2 mod 827 = {pow(g, 2, p)}")
    print()
    print("Lucasův test (g je generátor ↔ g^(φ/q) ≢ 1 pro všechna prvočísla q | φ):")
    for q in prime_factors:
        val = pow(g, phi // q, p)
        fail = "✗ NESPLNĚNO → g NENÍ generátor" if val == 1 else "✓"
        print(f"  g^({phi}/{q}) = g^{phi//q} mod 827 = {val}  {fail}")
    print()
    print(f"VÝSLEDEK: g = 826 NENÍ generátorem pro p = 827")


def uloha3():
    print()
    print("=" * 50)
    print("ÚLOHA 3: GCD a LCM čísel 330 a 65")
    print("=" * 50)
    a, b = 330, 65
    gcd = math.gcd(a, b)
    lcm = a * b // gcd

    print(f"330 = 2 × 3 × 5 × 11")
    print(f"65  = 5 × 13")
    print(f"GCD(330, 65) = {gcd}")
    print(f"Společní dělitelé = dělitelé GCD: {[d for d in range(1, gcd+1) if gcd % d == 0]}")
    print(f"D = nejmenší společný dělitel > 1 = {gcd}")
    print(f"LCM(330, 65) = {a} × {b} / {gcd} = {lcm}")
    print()
    options = [("a", 2, 5), ("b", 5, 4290), ("c", 3, 5), ("d", 3, 4290), ("e", 5, 330)]
    for letter, d_val, l_val in options:
        mark = "✓ SPRÁVNĚ" if d_val == gcd and l_val == lcm else "✗"
        print(f"  ({letter}) D={d_val}, L={l_val}  {mark}")
    print()
    print(f"VÝSLEDEK: Správná odpověď je (b): D = 5, L = 4290")


def uloha4():
    print()
    print("=" * 50)
    print("ÚLOHA 4: Multiplikativní inverze 29 mod 68 (EEA)")
    print("=" * 50)
    a, b = 68, 29
    print("Rozšířený Euklidův algoritmus:")

    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    step = 1
    while r1 != 0:
        q = r0 // r1
        print(f"  Krok {step}: {r0} = {q} × {r1} + {r0 % r1}")
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        step += 1

    print(f"\nGCD(68, 29) = {r0}")
    print()
    print("Zpětná substituce:")
    print("  1 = 10 - 1 × 9")
    print("  1 = 10 - 1 × (29 - 2 × 10)  =  3 × 10 - 1 × 29")
    print("  1 = 3 × (68 - 2 × 29) - 1 × 29  =  3 × 68 - 7 × 29")
    print(f"\n  1 = 68 × {x0} + 29 × {y0}")
    print(f"  Ověření: 68 × {x0} + 29 × {y0} = {68*x0 + 29*y0}")
    inv = y0 % a
    print(f"\n  y = {y0}  ≡  {inv} (mod 68)")
    print(f"  Ověření: 29 × {inv} mod 68 = {(29 * inv) % 68}")
    print()
    print(f"VÝSLEDEK: Multiplikativní inverze 29 mod 68 = {inv}  (y = {y0})")


if __name__ == "__main__":
    uloha1()
    uloha2()
    uloha3()
    uloha4()
