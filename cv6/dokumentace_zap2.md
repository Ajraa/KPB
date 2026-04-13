# Dokumentace - 2. zápočtový úkol KPB

## Úloha 1: Monoalfabetická substituce (dlouhý text)

### Postup řešení

1. **Frekvenční analýza** - Spočítány frekvence všech 26 písmen v šifrovém textu (1755 znaků).

2. **Identifikace nejčastějších písmen:**
   - F (12.14%) -> E (nejčastější v angličtině ~13%)
   - S (8.89%) -> T
   - E (8.49%) -> I
   - J (6.55%) -> N
   - K (5.81%) -> O

3. **Analýza bigramů a trigramů:**
   - FJS (časté) -> ENT
   - SEK -> TIO
   - EKJ -> ION
   - FQ -> ES, tedy Q = S

4. **Kontextová analýza** - Text pochází z oblasti kybernetické bezpečnosti:
   - SNPFAS -> THREAT
   - IFSFTSEKJ -> DETECTION
   - QFTUPESY -> SECURITY
   - EJSFDDELFJTF -> INTELLIGENCE
   - VUDJFPAREDESEFQ -> VULNERABILITIES

5. **Iterativní upřesnění** - Mapování se postupně zpřesňovalo na základě rozpoznaných slov.

### Klíč (šifrová abeceda)

| Otevřená | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|----------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Šifrová  | A | R | T | I | F | C | L | N | E | G | B | D | H | J | K | M | O | P | Q | S | U | V | W | X | Y | Z |

### Otevřený text (začátek)

ARTIFICIALINTELLIGENCEISINCREASINGLY UTILIZEDINVARIOUS SECURITYASPECTS TOENHANCETHREATDETECTION INCIDENTRESPONSEAND OVERALLCYBERSECURITY...

(Text pojednává o využití AI v kybernetické bezpečnosti - detekce hrozeb, ochrana endpointů, autentizace, SIEM, phishing, správa zranitelností atd.)

---

## Úloha 2: Monoalfabetická substituce (krátký text) - ATBASH

### Postup řešení

1. **Frekvenční analýza** - Text má 765 znaků. Nejčastější: G (9.54%), R (8.63%), H (7.71%).

2. **Klíčové pozorování:**
   - Trigram GSR (14x) -> THE (nejčastější anglický trigram)
   - GSZG -> THAT
   - ZMW -> AND
   - BLF -> YOU

3. **Identifikace šifry ATBASH:**
   - Všechna mapování odpovídají vzoru A<->Z, B<->Y, C<->X, ..., M<->N
   - Šifra ATBASH je speciální monoalfabetická substituce s fixním klíčem

### Klíč (ATBASH)

ZYXWVUTSRQPONMLKJIHGFEDCBA

(Každé písmeno se nahradí "zrcadlovým" písmem: A<->Z, B<->Y, ..., M<->N)

### Neobvyklost otevřeného textu

**Text je LIPOGRAM - záměrně neobsahuje písmeno E!**

Písmeno E je nejčastější písmeno anglické abecedy (~13%), ale v dešifrovaném textu se nevyskytuje ani jednou. Text sám o sobě vyzývá čtenáře, aby zjistil, co je na něm neobvyklého.

**Důsledky:**
- Frekvenční analýza nefunguje standardně, protože distribuce písmen je posunutá
- Absence E způsobuje, že v šifrovém textu chybí písmeno V (protože ATBASH mapuje E<->V)
- Automatické přiřazení frekvenčních tabulek může vést k chybným závěrům

### Otevřený text (začátek)

THIS IS AN UNUSUAL PARAGRAPH I AM CURIOUS AS TO JUST HOW QUICKLY YOU CAN FIND OUT WHAT IS SO UNUSUAL ABOUT IT...

---

## Úloha 3: Vigenèrova šifra

### Postup řešení

#### 1. Kasiski test
Nalezeny opakující se sekvence v šifrovém textu a jejich vzdálenosti:
- ESLXVV (6x): vzdálenosti 354, 180, 180, 174, ...
- LIMSLBEEW (3x): vzdálenosti 972, 174
- XEJXEJBW (2x): vzdálenost 888

Faktor 6 se vyskytuje nejčastěji -> naznačuje délku klíče 6.

#### 2. Index koincidence (IC)

| Délka klíče | Průměrné IC | Odchylka od 0.0667 |
|-------------|-------------|---------------------|
| 1           | 0.0459      | 0.0208             |
| 2           | 0.0493      | 0.0174             |
| 3           | 0.0566      | 0.0101             |
| 4           | 0.0492      | 0.0175             |
| 5           | 0.0456      | 0.0211             |
| **6**       | **0.0673**  | **0.0006**         |
| 7           | 0.0456      | 0.0211             |
| 8           | 0.0489      | 0.0178             |

**Nejlepší IC pro délku klíče 6** (0.0673 ≈ 0.0667 anglický text).

#### 3. Chi-squared test pro každou pozici klíče

| Pozice | Nejlepší posun | Písmeno | Chi-squared |
|--------|---------------|---------|-------------|
| 0      | 4             | E       | 56.55       |
| 1      | 0             | A       | 32.34       |
| 2      | 18            | S       | 30.90       |
| 3      | 19            | T       | 16.02       |
| 4      | 4             | E       | 39.91       |
| 5      | 17            | R       | 42.51       |

### Klíč: **EASTER**

### Otevřený text (začátek)

EASTER IS A CHRISTIAN FESTIVAL WHICH MARKS THE RESURRECTION OF JESUS CHRIST FOR MANY CHRISTIANS EASTER IS A CELEBRATION OF THE TRIUMPH OF LIFE OVER DEATH...

---

## Úloha 4: Vernam/OTP s opakovaným klíčem

### Postup řešení

**Šifrové texty:**
- C1 = 22 02 0f 1c 0b 1a 1e 0f 1d 08 18 16
- C2 = 2c 11 1c 06 14 1b 07 00 00 12 1a 00

#### 1. XOR šifrových textů

C1 XOR C2 = 0e 13 13 1a 1f 01 19 0f 1d 1a 02 16

Pokud byly oba texty šifrovány stejným klíčem K:
- C1 XOR C2 = (M1 XOR K) XOR (M2 XOR K) = M1 XOR M2

#### 2. Slovníkový útok

Stažen slovník anglických slov, filtrována slova délky 12 znaků (29 124 slov).
Pro každé kandidátní slovo W spočítáno W XOR (C1 XOR C2) a ověřeno, zda výsledek je také platné slovo.

#### 3. Výsledek

| | Hodnota | Hex |
|---|---------|-----|
| M1 | accumulative | 61 63 63 75 6d 75 6c 61 74 69 76 65 |
| M2 | opportunists | 6f 70 70 6f 72 74 75 6e 69 73 74 73 |
| K  | Californians | 43 61 6c 69 66 6f 72 6e 69 61 6e 73 |

**Ověření:**
- M1 XOR K = C1 ✓
- M2 XOR K = C2 ✓

**Klíče jsou STEJNÉ** - oba texty byly šifrovány klíčem "Californians".

---

## Úloha 5: Sloupcová transpozice (český text)

### Postup řešení

1. **Délka textu:** 540 znaků
2. **Dělitelé 3-15:** 3, 4, 5, 6, 9, 10, 12, 15

3. **Brute-force** všech permutací pro počty sloupců 3-9, hodnocení pomocí českých bigramů a trigramů.

4. **Výsledek:** Nejlepší skóre pro **5 sloupců** (skóre 715, výrazně lepší než ostatní).

### Klíče

- **Šifrovací permutace (klíč):** [3, 1, 4, 5, 2] (1-based)
- **Dešifrovací permutace:** [2, 5, 1, 3, 4] (1-based)
- (0-based: šifrovací [2, 0, 3, 4, 1], dešifrovací [1, 4, 0, 2, 3])

### Otevřený text

LIDE VE VLACICH CD STAHUJI MOC DAT OPERATOR JE NEZLEVNI NA OPAK JE OMEZI ZAKAZNICI CESKYCH DRAH SE NA SOCIALNICH SITICH PODIVUJI NAD ZVAZOVANYM OMEZENIM DAT STAHOVANYCHPRES WIFI VE VLACICH POPISUJI ZKUSENOSTI S POMALYM A NESTABILNIM PRIPOJENIM PARADOXNE TAK BYLA POPRENA ORIGINALNI EKONOMICKA TEORIE MINISTRYNE MARTYNOVAKOVE KDY VICE STAZENYCH DAT ZNAMENA JEJICH ZLEVNENI CO TAM KDO STAHUJE VZDY TSI GNAL FURT PADA A JE TO POMALE TO MAM RYCHLEJSI MOBILNI POPSAL JEDEN Z DISKUTUJICICH NA FACEBOOKU UME ALE SPON TAKRKA VZDY NEFUNKCNI ZNI DALSI KOMENTAR NA ADRESU WIFI CDO MEZI TDAT AVIC UZ TO SNAD ANI NEJDE NEPTA SE RECNICKY DALSI CESTUJICI QQ

---

## Použité nástroje

- Python 3.13 s knihovnou `cryptography` (pro cvičení 6)
- Vlastní implementace frekvenční analýzy, Kasiski testu, IC, chi-squared testu
- Slovník anglických slov z https://github.com/dwyl/english-words (pro úlohu 4)
