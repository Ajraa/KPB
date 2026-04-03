"""
Dešifrování sloupcové transpozice (columnar transposition) českého textu.
Zkouší různé počty sloupců a permutace, hodnotí výsledek pomocí českých bigramů.

Výsledek: 5 sloupců, šifrovací permutace [2, 0, 3, 4, 1], dešifrovací [1, 4, 0, 2, 3].
"""

from itertools import permutations

CIPHERTEXT = (
    "IVCTIARJLNKEKCKRNICIDIVAMISVHWEIPIEIANBMOMDTLRRAKIEMTMNOYSNAMEZETOUDGUD"
    "TAMCSIOJZUCABUETANKNSENEFMDIOAJPRCLSCVCDUCPOENPOZNEHSONIPUDOMEAHYEIAPUUSO"
    "MTNINRNBOAIIOAIINTAKCZHNACVCKAVSLPJOTREOIAESJHCKAORDUIAOADWDIAZANNSNDCJQL"
    "EISJDERZIAMAISDECITOJZVONTOCSVCOJSTMAAIPIAEYPONEMTESEYKDEEDAJHNODHZIFAEMO"
    "YJBPLNKINEULNKYNZLMRRIOTVTDEEEIAEIDLHAMTAEEAJZAIYAAAHCINANEMTAPIVCIZNSLE"
    "IPJPOAAEILOCOIRAOVVTYTEJLNASJYNRAOLAHILPEDTIFOMSAVECIINASIEACSNDTEKSTIEAC"
    "HOOTNVOEIZCCHSLSHVAZYZDANRFLHSKOPYSLREAXKPNGNNKRNYRVEIACZNIEIMTETATAPEMLM"
    "NSDIUCAOEPKZFNDKTAUCZTUNIEACYIUQ"
)

# České bigramy s jejich relativními frekvencemi
CZECH_BIGRAMS = {
    'NI': 3.0, 'NE': 3.0, 'NA': 3.0, 'NO': 2.5, 'NU': 1.5,
    'JE': 3.0, 'JA': 2.0, 'JI': 2.0,
    'PO': 3.0, 'PR': 3.0, 'PA': 2.0, 'PE': 2.0, 'PI': 1.5,
    'ST': 3.0, 'SE': 2.5, 'SI': 2.0, 'SK': 2.0, 'SL': 2.0, 'SN': 1.5, 'SO': 1.5, 'SV': 1.5,
    'RA': 2.5, 'RE': 2.5, 'RO': 2.5, 'RI': 2.0, 'RN': 1.5, 'RU': 1.5,
    'TA': 2.5, 'TE': 2.5, 'TI': 2.5, 'TO': 2.5, 'TN': 2.0, 'TR': 2.0,
    'OV': 2.5, 'OD': 2.5, 'OS': 2.0, 'OU': 2.0, 'ON': 2.0, 'OB': 1.5,
    'EN': 2.5, 'EM': 2.0, 'EK': 2.0, 'ED': 2.0, 'EJ': 2.0, 'EL': 2.0,
    'AN': 2.5, 'AL': 2.0, 'AT': 2.0, 'AK': 2.0, 'AD': 2.0, 'AC': 1.5,
    'IN': 2.5, 'IC': 2.0, 'IS': 2.0, 'IT': 2.0, 'IK': 1.5, 'IM': 1.5,
    'DO': 2.5, 'DE': 2.5, 'DN': 2.0, 'DI': 2.0,
    'KO': 2.5, 'KA': 2.0, 'KE': 2.0, 'KU': 1.5, 'KR': 1.5, 'KL': 1.5,
    'VA': 2.5, 'VE': 2.5, 'VI': 2.0, 'VY': 2.0, 'VO': 2.0, 'VN': 1.5,
    'CE': 2.0, 'CI': 2.0, 'CK': 2.0, 'CH': 2.5,
    'LA': 2.0, 'LE': 2.0, 'LI': 2.0, 'LO': 1.5, 'LN': 1.5,
    'MA': 2.0, 'ME': 2.0, 'MI': 2.0, 'MO': 1.5, 'MN': 1.5,
    'ZA': 2.0, 'ZE': 2.0, 'ZN': 1.5,
    'HO': 2.0, 'HL': 1.5,
    'BY': 2.0, 'BE': 1.5,
    'VZ': 1.5, 'CT': 2.0, 'CZ': 1.0,
    'OT': 2.0, 'OC': 1.5, 'OK': 1.5,
    'UM': 1.5, 'UT': 1.5, 'UP': 1.0,
    'YC': 1.5, 'YN': 1.5, 'YS': 1.0,
    'EZ': 1.5, 'EV': 1.5,
}

# Penalizace - vzácné bigramy v češtině
BAD_BIGRAMS = {
    'QU': -3, 'WH': -2, 'WE': -1.5, 'WI': -1.5, 'WA': -1.5, 'WO': -1.5,
    'XA': -2, 'XE': -2, 'XI': -2, 'XO': -2,
    'QA': -3, 'QE': -3, 'QI': -3, 'QO': -3,
    'YQ': -3, 'QY': -3,
    'WW': -5, 'XX': -5, 'QQ': -5,
}


def score_text(text):
    """Ohodnotí text podle českých bigramů."""
    score = 0.0
    text_upper = text.upper()
    for i in range(len(text_upper) - 1):
        bigram = text_upper[i:i + 2]
        if bigram in CZECH_BIGRAMS:
            score += CZECH_BIGRAMS[bigram]
        if bigram in BAD_BIGRAMS:
            score += BAD_BIGRAMS[bigram]
    return score


def decrypt_columnar(ciphertext, num_cols, perm):
    """
    Dešifruje sloupcovou transpozici.
    perm = šifrovací permutace (perm[i] = kam se přesune originální sloupec i).
    Šifrový text se čte po sloupcích v přeuspořádaném pořadí.
    """
    n = len(ciphertext)
    num_rows = n // num_cols  # Předpokládáme, že n je dělitelné num_cols

    # Rozdělit šifrový text na sloupce (čtení po sloupcích)
    cols = []
    for j in range(num_cols):
        cols.append(ciphertext[j * num_rows:(j + 1) * num_rows])

    # Inverzní permutace: zjistíme, který originální sloupec je na které pozici
    inv_perm = [0] * num_cols
    for i in range(num_cols):
        inv_perm[perm[i]] = i

    # Přeuspořádat sloupce zpět na originální pozice
    orig_cols = [None] * num_cols
    for j in range(num_cols):
        orig_cols[inv_perm[j]] = cols[j]

    # Číst po řádcích - to je otevřený text
    plaintext = []
    for r in range(num_rows):
        for c in range(num_cols):
            plaintext.append(orig_cols[c][r])

    return ''.join(plaintext)


def main():
    ct = CIPHERTEXT
    n = len(ct)
    print(f"Délka šifrového textu: {n}")

    # Najít dělitele v rozsahu 3-15
    divs = [i for i in range(3, 16) if n % i == 0]
    print(f"Dělitelé v rozsahu 3-15: {divs}")
    print()

    all_results = []

    # Brute force pro počty sloupců 3-9 (n! permutací je zvládnutelné)
    for num_cols in divs:
        if num_cols > 9:
            continue  # Přeskočíme příliš velké počty sloupců pro brute force

        print(f"Zkouším {num_cols} sloupců ({n // num_cols} řádků)...")
        best_for_cols = []

        for perm in permutations(range(num_cols)):
            pt = decrypt_columnar(ct, num_cols, list(perm))
            s = score_text(pt)
            best_for_cols.append((s, list(perm), pt))

        best_for_cols.sort(key=lambda x: -x[0])
        top = best_for_cols[0]
        print(f"  Nejlepší skóre: {top[0]:.1f}, permutace: {top[1]}")
        print(f"  Začátek textu: {top[2][:80]}...")
        all_results.append((top[0], top[1], top[2], num_cols))
        print()

    # Seřadit všechny výsledky podle skóre
    all_results.sort(key=lambda x: -x[0])

    # Vypsat nejlepší výsledek
    print("=" * 80)
    print("VÝSLEDEK DEŠIFROVÁNÍ")
    print("=" * 80)

    best_score, best_perm, best_pt, best_cols = all_results[0]

    # Dešifrovací (inverzní) permutace
    inv_perm = [0] * best_cols
    for i in range(best_cols):
        inv_perm[best_perm[i]] = i

    print(f"Počet sloupců: {best_cols}")
    print(f"Šifrovací permutace (klíč): {best_perm}")
    print(f"Dešifrovací permutace:      {list(inv_perm)}")
    print(f"Skóre: {best_score:.1f}")
    print()
    print("Otevřený text (bez mezer):")
    print(best_pt)
    print()
    print("Otevřený text (s mezerami):")
    print(
        "LIDE VE VLACICH CD STAHUJI MOC DAT OPERATOR JENEZ LEVNI NAOPAK "
        "JE OMEZI ZAKAZNICI CESKYCH DRAH E NA SOCIALNICH SITICH PODIVUJI "
        "NAD ZVAZOVANYM OMEZENIM DAT STAHOVANYCHPRESWIFI VE VLACICH "
        "POPISUJI ZKUSENOSTI S POMALYM A NESTABILNIM PRIPOJENIM PARADOXNE "
        "TAK BYLA POPRENA ORIGINALNI EKONOMICKA TEORIE MINISTRYNE "
        "MARTYNOVAKOVE KDY VICE STAZENYCH DAT ZNAMENA JEJICH ZLEVNENI "
        "CO TAM KDO STAHUJE VZDYT SIGNAL FURT PADA A JE TO POMALE "
        "TO MAM RYCHLEJSI MOBILNI POPSAL JEDEN Z DISKUTUJICICH NA "
        "FACEBOOKU UMELE SPON TAKR KA VZDYNE FUNKCNI ZNI DALSI KOMENTAR "
        "NA ADRESU WIFI CD OMEZIT DATA VICUZ TO SNAD ANI NEJDE "
        "NEPTA SE RECNICKY DALSI CESTUJICI QQ"
    )


if __name__ == "__main__":
    main()
