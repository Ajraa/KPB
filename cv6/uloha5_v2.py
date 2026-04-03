"""
Uloha 5 - Desifrovani sloupcove transpozice (columnar transposition)
Cesky text, anglicka abeceda bez mezer.
Optimalizovana verze - zkousi nejprve male pocty sloupcu.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import math
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

# Ceske bigramy a trigramy s vahou
CZECH_COMMON = {
    # bigramy
    'NI': 3, 'NE': 3, 'NA': 3, 'NO': 2, 'NU': 1,
    'JE': 3, 'JA': 2, 'JI': 2,
    'PO': 3, 'PR': 3, 'PA': 2, 'PE': 2,
    'ST': 3, 'SE': 2, 'SI': 2, 'SK': 2, 'SL': 2, 'SV': 1, 'SN': 1,
    'RA': 2, 'RE': 2, 'RO': 2, 'RI': 2,
    'TA': 2, 'TE': 2, 'TI': 2, 'TO': 2, 'TN': 2, 'TR': 2,
    'OV': 2, 'OD': 2, 'OS': 2, 'OU': 2, 'ON': 2,
    'EN': 2, 'EM': 2, 'EK': 2, 'ED': 2, 'EJ': 2, 'EL': 2,
    'AN': 2, 'AL': 2, 'AT': 2, 'AK': 2, 'AD': 2,
    'IN': 2, 'IC': 2, 'IS': 2, 'IT': 2,
    'DO': 2, 'DE': 2, 'DN': 2, 'DI': 2,
    'KO': 2, 'KA': 2, 'KE': 2, 'KU': 1,
    'VA': 2, 'VE': 2, 'VI': 2, 'VY': 2, 'VO': 2,
    'CE': 2, 'CI': 2, 'CK': 2, 'CH': 2,
    'LA': 2, 'LE': 2, 'LI': 2, 'LO': 1, 'LN': 1,
    'MA': 2, 'ME': 2, 'MI': 2,
    'ZA': 2, 'ZE': 2, 'ZN': 1,
    'HO': 2, 'HL': 1,
    'BY': 2,
    'OT': 2,
    # trigramy
    'PRO': 4, 'PRE': 3, 'PRI': 3,
    'STA': 3, 'STI': 3, 'STE': 3, 'STR': 3,
    'NIC': 3, 'JED': 3, 'JEN': 3,
    'POD': 3, 'POS': 2, 'POV': 2,
    'OVA': 3, 'ENI': 3, 'ANI': 3,
    'OST': 3, 'IST': 3,
    'KTE': 3, 'NEJ': 3,
    'VAN': 2, 'VAT': 2,
    'SKE': 2, 'SKA': 2, 'SKY': 2,
    'CKE': 2, 'CKA': 2,
    'ALE': 2, 'ZNA': 2,
    'MEN': 2, 'ROZ': 2,
}

# Penalizace
BAD = {'QU': -3, 'WH': -2, 'WW': -5, 'XX': -5, 'QQ': -5, 'QY': -3, 'YQ': -3}


def score_text(text):
    s = 0.0
    t = text.upper()
    for i in range(len(t) - 2):
        tri = t[i:i+3]
        if tri in CZECH_COMMON:
            s += CZECH_COMMON[tri]
    for i in range(len(t) - 1):
        bi = t[i:i+2]
        if bi in CZECH_COMMON:
            s += CZECH_COMMON[bi]
        if bi in BAD:
            s += BAD[bi]
    return s


def decrypt_columnar(ct, ncols, perm):
    """
    Desifrovani sloupcove transpozice.

    Sifrovani: text se zapise po radcich do matice, sloupce se preskupi
    podle perm (perm[i] = kam jde sloupec i), pak se cte po sloupcich.

    Desifrovani: obraceny proces.
    """
    n = len(ct)
    nrows = math.ceil(n / ncols)
    extra = n % ncols  # pocet sloupcu s nrows radky (pokud extra > 0)
    if extra == 0:
        extra = ncols

    # Inverzni permutace: inv_perm[j] = i znamena, ze na pozici j v sifrovem textu
    # je puvodni sloupec i
    inv_perm = [0] * ncols
    for i in range(ncols):
        inv_perm[perm[i]] = i

    # Delky sloupcu v sifrovem textu
    col_lens = []
    for j in range(ncols):
        orig_col = inv_perm[j]
        if n % ncols == 0:
            col_lens.append(nrows)
        elif orig_col < extra:
            col_lens.append(nrows)
        else:
            col_lens.append(nrows - 1)

    # Rozdeleni na sloupce
    cols = []
    idx = 0
    for j in range(ncols):
        cols.append(ct[idx:idx+col_lens[j]])
        idx += col_lens[j]

    if idx != n:
        return None

    # Preskladani zpet
    orig_cols = [None] * ncols
    for j in range(ncols):
        orig_cols[inv_perm[j]] = cols[j]

    # Cteni po radcich
    result = []
    for r in range(nrows):
        for c in range(ncols):
            if r < len(orig_cols[c]):
                result.append(orig_cols[c][r])

    return ''.join(result)


def main():
    ct = CIPHERTEXT
    n = len(ct)
    print(f"Delka sifr. textu: {n}")
    print(f"Delitele 3-15: {[i for i in range(3, 16) if n % i == 0]}")
    print()

    all_results = []

    # Zkousicme male pocty sloupcu (3-8), pro ktere muzeme otestovat vsechny permutace
    for ncols in range(3, 10):
        total = math.factorial(ncols)
        print(f"Testuju {ncols} sloupcu ({total} permutaci)...", flush=True)

        best_score = -999
        best_perm = None
        best_pt = None
        count = 0

        for perm in permutations(range(ncols)):
            pt = decrypt_columnar(ct, ncols, list(perm))
            if pt is None:
                continue
            s = score_text(pt)
            if s > best_score:
                best_score = s
                best_perm = list(perm)
                best_pt = pt
            count += 1

        print(f"  Nejlepsi: skore={best_score:.1f}, perm={best_perm}")
        print(f"  Text: {best_pt[:120]}...")
        all_results.append((best_score, best_perm, best_pt, ncols))
        print()

    # Seradit a vypsat nejlepsi vysledky
    all_results.sort(key=lambda x: -x[0])

    print("=" * 80)
    print("NEJLEPSI VYSLEDKY:")
    print("=" * 80)

    for i, (score, perm, pt, ncols) in enumerate(all_results[:5]):
        inv_perm = [0] * ncols
        for j in range(ncols):
            inv_perm[perm[j]] = j

        print(f"\n#{i+1}: Skore={score:.1f}, Sloupce={ncols}")
        print(f"  Sifrovaci permutace (klic): {perm}")
        print(f"  Desifrovaci permutace:      {inv_perm}")
        # Klic jako 1-based
        perm_1based = [p+1 for p in perm]
        inv_1based = [p+1 for p in inv_perm]
        print(f"  Sifrovaci klic (1-based):   {perm_1based}")
        print(f"  Desifrovaci klic (1-based):  {inv_1based}")
        print(f"  Otevreny text (prvnich 300 znaku):")
        print(f"  {pt[:300]}")
        if i == 0:
            print(f"\n  CELY TEXT:")
            print(f"  {pt}")


if __name__ == "__main__":
    main()
