"""
Vigenèrova šifra — kryptoanalýza pomocí Kasiski testu, indexu koincidence a chi-squared testu.
"""

import math
from collections import Counter
from itertools import combinations

# Šifrový text
CIPHERTEXT = (
    "IAKMIIMSSVLIMSLBEEJEKMMMELOAMTLMSKOJXHWKIJYRJXGKMOFHJAISMLGYVIKMJFVMSGCTLRALXZENKXEJXEJBWRGEDXFIETAHRFJTZXXIMUEILFJLAYIFZEJWIRXHSGHRZEJRMDTOJMEEXTAFIFJTZXCVERETRPROFVLIMSLBEEWADLSYEVWTLFPIVTCRXTZBWKMMWLSZXIKTTFTUDTVKMMWMSKVANXPFVSHXRUAILAJIMEFWWRRDXTQZPYOXWVILGMWFJSQFFFPSGYRVALAYIRXESLXVVEKIITMADECVKGKVLZGKKYPFAEJLEEHRSUFZXSLAIJISQFFFPSYHFRGKLHEEGIWGXGEGSGXIEDAMMFRSOAMTLCWEISVALXHWIRLBPZXYJXFZVTZTRUREOZVFATZTJKIRLAICSNYPMEXEJFSEXHKMLVHALXWFJESLXVVCZTRXIFJHQPIAJMSPIAJUYKMTMLYRPLQYECPSKHQVXIEXFVXWWXRKLEWGHFJMSKGYENVMLVINVHJRTRAEMEAEKMIIRCZKMJXISGMKCESLXVVSMGHRCIKMLVJIJLXJYNVTCRJTWKXYIFAKWKJUDEQFSNGYWGVIFZAYMCZLXRVTKHRDERUAXYIESLXVVNGKXYSDGQGYYRUAIJAHAVLLWESWMWJEJXRKGADXRUERZTZVESDBKYXLQWMWJEJXRKAAQHJTELUNPRXIFZIRWTWKEEHUKNECPYUXPVFRSMIVESLXVRPILMPVIAJEMVVOJEEKIRLAINIECUIWSRWXEJXEJBWTELDXHYSLQPIVOTZXJZVSLWEPSFZHPPAEWDMJTADFWLRDSRAYMCZBWKLEKNRUEYTXJFVEWTWKIRETRPGHJBWKMAFLGVPETKEKITZBWRWTZXHRCTZTXAISMLIEXEJXHAIRMLECIMSGHGIOHEIKLRWPHFANTKEEGHWLJISMHTPDXRWXWFRTZXVFEDLHAVPCGFIYMMXHYIHAQLPRXEJBWDEUFWCKLUJLHRCWZBGYQAJDWKLEDTWKWUHIIIAHWGNVWUKTXVFRWTHRRDVKEEOWAGINMTZAMJXWWEZVHIKVMGPEKMLVJODESNMNYWEPMSYHSUJRAWEPAHAVLZWSAZRZJIUTRKJOJVLIMSLBEEWAKMLVHAQMLRXJWLYJAAKIYKXOVXEKLOFMLVGRGLWDENQVLIMSLBEEWBWEMVZELAEKNEKNWNESCBPCIDSGHSYRAXHZRALHQSSNLAIWVIVTCRRDLAEKKOVKEZWEVAMDJRGFXYIDWTHFRTZXWLRDSRWFIAKMIIWUFWEPMSSVICIBJTXZSNGYXYIRWLYIVEUMMFROXCIJYS"
)

# Frekvenční distribuce anglického jazyka
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074,
}


def find_repeated_sequences(text, min_len=3, max_len=6):
    """Najde opakující se sekvence a jejich vzdálenosti."""
    sequences = {}
    for seq_len in range(min_len, max_len + 1):
        for i in range(len(text) - seq_len):
            seq = text[i:i + seq_len]
            if seq not in sequences:
                positions = []
                start = 0
                while True:
                    idx = text.find(seq, start)
                    if idx == -1:
                        break
                    positions.append(idx)
                    start = idx + 1
                if len(positions) >= 2:
                    sequences[seq] = positions
    return sequences


def kasiski_test(text):
    """Provede Kasiski test — najde opakující se sekvence, spočítá vzdálenosti a GCD."""
    print("=" * 70)
    print("1) KASISKI TEST")
    print("=" * 70)

    sequences = find_repeated_sequences(text, min_len=3, max_len=5)

    # Filtr — jen sekvence s >= 2 výskyty
    repeated = {k: v for k, v in sequences.items() if len(v) >= 2}

    # Seřadíme podle délky sekvence sestupně, pak podle počtu výskytů
    sorted_seqs = sorted(repeated.items(), key=lambda x: (-len(x[0]), -len(x[1])))

    all_distances = []

    print(f"\nNalezeno {len(sorted_seqs)} opakujících se sekvencí (délka 3-5).")
    print(f"\nNejvýznamnější sekvence (délka >= 4, nebo 3 s >= 3 výskyty):")
    print(f"{'Sekvence':<12} {'Pozice':<30} {'Vzdálenosti':<30}")
    print("-" * 70)

    count = 0
    for seq, positions in sorted_seqs:
        distances = [positions[j] - positions[i] for i, j in combinations(range(len(positions)), 2)]
        all_distances.extend(distances)

        if len(seq) >= 4 or (len(seq) == 3 and len(positions) >= 3):
            if count < 25:
                print(f"{seq:<12} {str(positions):<30} {str(distances):<30}")
                count += 1

    # Spočítáme GCD všech vzdáleností
    factor_counts = Counter()
    for d in all_distances:
        for f in range(2, 9):
            if d % f == 0:
                factor_counts[f] += 1

    print(f"\nFaktory vzdáleností (kolikrát je vzdálenost dělitelná faktorem):")
    for f in range(2, 9):
        bar = "#" * (factor_counts[f] // 10)
        print(f"  {f}: {factor_counts[f]:>5}x  {bar}")

    # Celkové GCD nejdelších sekvencí
    long_distances = []
    for seq, positions in sorted_seqs:
        if len(seq) >= 4:
            for i, j in combinations(range(len(positions)), 2):
                long_distances.append(positions[j] - positions[i])

    if long_distances:
        overall_gcd = long_distances[0]
        for d in long_distances[1:]:
            overall_gcd = math.gcd(overall_gcd, d)
        print(f"\nGCD vzdáleností sekvencí délky >= 4: {overall_gcd}")

    best_key_len = max(range(2, 9), key=lambda f: factor_counts[f])
    print(f"\nKasiski test naznačuje délku klíče: {best_key_len}")
    return factor_counts


def calc_ic(text):
    """Spočítá index koincidence pro daný text."""
    n = len(text)
    if n <= 1:
        return 0.0
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic


def ic_analysis(text):
    """Spočítá IC pro různé délky klíče a vybere nejpravděpodobnější."""
    print("\n" + "=" * 70)
    print("2) INDEX KOINCIDENCE (IC)")
    print("=" * 70)

    # IC angličtiny ~ 0.0667, náhodný text ~ 0.0385
    print(f"\nOčekávaný IC pro angličtinu: ~0.0667")
    print(f"Očekávaný IC pro náhodný text: ~0.0385")
    print(f"\n{'Délka klíče':<15} {'Průměrný IC':<15} {'Odchylka od 0.0667':<20}")
    print("-" * 50)

    best_key_len = 1
    best_ic = 0.0

    for key_len in range(1, 9):
        # Rozdělení textu do skupin
        groups = ['' for _ in range(key_len)]
        for i, c in enumerate(text):
            groups[i % key_len] += c

        # Průměrný IC přes všechny skupiny
        ics = [calc_ic(g) for g in groups]
        avg_ic = sum(ics) / len(ics)
        deviation = abs(avg_ic - 0.0667)

        print(f"{key_len:<15} {avg_ic:<15.6f} {deviation:<20.6f}")

        if avg_ic > best_ic:
            best_ic = avg_ic
            best_key_len = key_len

    print(f"\nNejlepší délka klíče podle IC: {best_key_len} (IC = {best_ic:.6f})")
    return best_key_len


def chi_squared_test(text, key_len):
    """Pro každou pozici klíče najde nejlepší posun pomocí chi-squared testu."""
    print("\n" + "=" * 70)
    print("3) CHI-SQUARED TEST")
    print("=" * 70)

    key = []
    expected_freq = [ENGLISH_FREQ[chr(i + ord('A'))] for i in range(26)]

    for pos in range(key_len):
        # Extrahuji znaky na pozici pos, pos+key_len, pos+2*key_len, ...
        group = [text[i] for i in range(pos, len(text), key_len)]
        n = len(group)
        freq = Counter(group)

        best_shift = 0
        best_chi2 = float('inf')
        all_chi2 = []

        for shift in range(26):
            chi2 = 0.0
            for i in range(26):
                # Dešifrujeme posun: (i - shift) mod 26 odpovídá písmenu i v otevřeném textu
                observed = freq.get(chr((i + shift) % 26 + ord('A')), 0)
                expected = expected_freq[i] * n
                if expected > 0:
                    chi2 += (observed - expected) ** 2 / expected
            all_chi2.append((shift, chi2))

            if chi2 < best_chi2:
                best_chi2 = chi2
                best_shift = shift

        key.append(best_shift)

        # Seřadíme a ukážeme top 3
        all_chi2.sort(key=lambda x: x[1])
        top3 = all_chi2[:3]
        top3_str = ", ".join(f"{chr(s + ord('A'))}({c:.1f})" for s, c in top3)
        print(f"  Pozice {pos}: nejlepší posun = {best_shift} "
              f"('{chr(best_shift + ord('A'))}'), chi2 = {best_chi2:.2f}  |  Top 3: {top3_str}")

    key_str = ''.join(chr(k + ord('A')) for k in key)
    print(f"\nNalezený klíč: {key_str}")
    return key_str


def decrypt_vigenere(ciphertext, key):
    """Dešifruje Vigenèrovu šifru."""
    plaintext = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        shift = ord(key[i % key_len]) - ord('A')
        p = (ord(c) - ord('A') - shift) % 26
        plaintext.append(chr(p + ord('A')))
    return ''.join(plaintext)


def main():
    text = CIPHERTEXT
    print(f"Délka šifrového textu: {len(text)} znaků\n")

    # 1) Kasiski test
    kasiski_factors = kasiski_test(text)

    # 2) Index koincidence
    best_key_len = ic_analysis(text)

    # 3) Chi-squared test
    key = chi_squared_test(text, best_key_len)

    # 4) Dešifrování
    plaintext = decrypt_vigenere(text, key)

    print("\n" + "=" * 70)
    print("4) VÝSLEDEK DEŠIFROVÁNÍ")
    print("=" * 70)
    print(f"\nKlíč: {key}")
    print(f"Délka klíče: {len(key)}")
    print(f"\nOtevřený text:")
    # Formátování po 80 znacích
    for i in range(0, len(plaintext), 80):
        print(f"  {plaintext[i:i+80]}")


if __name__ == "__main__":
    main()
