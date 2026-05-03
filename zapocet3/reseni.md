# 3. zápočtový úkol z KPB

---

## Úloha 1 — (3^547) mod 29

**Postup: Eulerova věta**

Protože 29 je prvočíslo, platí:
$$\varphi(29) = 28$$

Protože $\gcd(3, 29) = 1$, lze použít Eulerovu větu:
$$3^{28} \equiv 1 \pmod{29}$$

Rozdělíme exponent: $547 = 28 \cdot 19 + 15$

$$3^{547} = 3^{28 \cdot 19 + 15} = (3^{28})^{19} \cdot 3^{15} \equiv 1^{19} \cdot 3^{15} \equiv 3^{15} \pmod{29}$$

Výpočet $3^{15} \pmod{29}$ metodou opakovaného umocňování:

| mocnina | výpočet            | výsledek mod 29 |
|---------|--------------------|-----------------|
| $3^1$   | 3                  | 3               |
| $3^2$   | $3^2 = 9$          | 9               |
| $3^4$   | $9^2 = 81$         | $81 - 2 \cdot 29 = 23$ |
| $3^8$   | $23^2 = 529$       | $529 - 18 \cdot 29 = 7$ |

$3^{15} = 3^8 \cdot 3^4 \cdot 3^2 \cdot 3^1$

$$7 \cdot 23 = 161 \equiv 161 - 5 \cdot 29 = 16 \pmod{29}$$
$$16 \cdot 9 = 144 \equiv 144 - 4 \cdot 29 = 28 \pmod{29}$$
$$28 \cdot 3 = 84 \equiv 84 - 2 \cdot 29 = 26 \pmod{29}$$

### Výsledek: **(3^547) mod 29 = 26**

---

## Úloha 2 — Prvek, který není generátorem v Z₈₂₇

Pro prvočíslo $p = 827$ platí $\varphi(827) = 826$.

Faktorizace: $826 = 2 \cdot 7 \cdot 59$

Prvek $g$ je generátor grupy $\mathbb{Z}_{827}^*$, pokud $\text{ord}(g) = 826$. Podle Lucasova testu generátornosti to nastane právě tehdy, když:
1. $g^{826} \equiv 1 \pmod{827}$
2. Pro každé prvočíslo $q \mid 826$: $g^{826/q} \not\equiv 1 \pmod{827}$

Prvočíselní dělitelé čísla 826 jsou: $2, 7, 59$.

**Volba:** $g = 826 \equiv -1 \pmod{827}$

Ověření:
- $g^{826/2} = g^{413} = (-1)^{413} = -1 \equiv 826 \not\equiv 1 \pmod{827}$ ✓ (podmínka splněna)
- $g^{826/7} = g^{118} = (-1)^{118} = 1 \equiv 1 \pmod{827}$ ✗ (podmínka **nesplněna**)

Protože $g^{826/7} = 1$, prvek $g = 826$ **neprojde Lucasovým testem** — není generátorem.

Přímý důkaz: $\text{ord}(826) = 2$, protože $826^1 \equiv -1 \not\equiv 1$ a $826^2 \equiv 1 \pmod{827}$. Řád 2 je vlastním dělitelem čísla 826, tedy $g = 826$ **není generátorem**.

### Výsledek: **g = 826 není generátorem pro p = 827**

---

## Úloha 3 — NSN čísel 330 a 65, nejmenší společný dělitel D > 1

**Rozklad na prvočinitele:**

$$330 = 2 \cdot 3 \cdot 5 \cdot 11$$
$$65 = 5 \cdot 13$$

**NSD (GCD):**
$$\gcd(330, 65) = 5$$

Společní dělitelé čísel 330 a 65 jsou právě dělitelé jejich GCD:
$$\text{dělitelé}(5) = \{1, 5\}$$

Nejmenší společný dělitel $D > 1$: $D = 5$

**NSN (LCM):**
$$\text{NSN}(330, 65) = \frac{330 \cdot 65}{\gcd(330, 65)} = \frac{21450}{5} = 4290$$

Ověření správné možnosti:
- (a) D = 2, L = 5 ✗
- **(b) D = 5, L = 4290 ✓**
- (c) D = 3, L = 5 ✗
- (d) D = 3, L = 4290 ✗
- (e) D = 5, L = 330 ✗

### Výsledek: **Správná odpověď je (b): D = 5, L = 4290**

---

## Úloha 4 — Multiplikativní inverze 29 modulo 68 (EEA)

Hledáme $y \in \mathbb{Z}_{68}$ takové, že $29 \cdot y \equiv 1 \pmod{68}$, tzn. řešíme:
$$\gcd(68, 29) = 68 \cdot x + 29 \cdot y$$

**Rozšířený Euklidův algoritmus:**

| krok | rovnice                          |
|------|----------------------------------|
| 1    | $68 = 2 \cdot 29 + 10$           |
| 2    | $29 = 2 \cdot 10 + 9$            |
| 3    | $10 = 1 \cdot 9 + 1$             |
| 4    | $9 = 9 \cdot 1 + 0$              |

$\gcd(68, 29) = 1$ ✓ (inverze existuje)

**Zpětná substituce:**

$$1 = 10 - 1 \cdot 9$$
$$1 = 10 - 1 \cdot (29 - 2 \cdot 10) = 3 \cdot 10 - 1 \cdot 29$$
$$1 = 3 \cdot (68 - 2 \cdot 29) - 1 \cdot 29 = 3 \cdot 68 - 6 \cdot 29 - 1 \cdot 29$$
$$\boxed{1 = 3 \cdot 68 + (-7) \cdot 29}$$

Výsledek: $x = 3$, $y = -7$

Převod do $\mathbb{Z}_{68}$: $y = -7 \equiv 61 \pmod{68}$

Ověření: $29 \cdot 61 = 1769 = 26 \cdot 68 + 1 \equiv 1 \pmod{68}$ ✓

### Výsledek: **Multiplikativní inverze 29 mod 68 = 61 (y = -7)**
