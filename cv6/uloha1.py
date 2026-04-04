CIPHERTEXT = (
    "APSECETEADEJSFDDELFJTFEQEJTPFAQEJLDYUSEDEZFIEJVAPEKUQQFTUPESYAQMFTSQSKFJNAJTFSNPFASIFSFTSEKJEJTEIFJSPFQMKJQFAJIKVFPADDTYRFPQFTUPESYNFPFAPFQKHFBFYWAYQAEEQUQFIEJQFTUPESYAIVAJTFISNPFASIFSFTSEKJAJKHADYIFSFTSEKJAEEIFJSECEFQUJUQUADMASSFPJQEJIETASEJLMKSFJSEADSNPFASQRFNAVEKPADAJADYSETQHKJESKPQUQFPAJIJFSWKPBRFNAVEKPCKPQUQMETEKUQATSEVESEFQQELJASUPFDFQQIFSFTSEKJPFTKLJEZFQJFWAJIUJBJKWJSNPFASQRAQFIKJHADETEKUQRFNAVEKPJFSWKPBMPKSFTSEKJEJSPUQEKJIFSFTSEKJAJIMPFVFJSEKJAEOUETBDYIFSFTSQAJIPFQMKJIQSKJFSWKPBEJSPUQEKJQCEPFWADDKMSEHEZASEKJAJADYZFQJFSWKPBSPACCETSKKMSEHEZFCEPFWADDPUDFQAJIEIFJSECYVUDJFPAREDESEFQFJIMKEJSQFTUPESYFJNAJTFHFJSFJIMKEJSMPKSFTSEKJAEIPEVFJAJSEVEPUQAJIAJSEHADWAPFIFSFTSAJIMPFVFJSHADWAPFEJCFTSEKJQZFPKIAYSNPFASIFSFTSEKJEIFJSECEFQUJBJKWJSNPFASQRYHKJESKPEJLFJIMKEJSRFNAVEKPUQFPAUSNFJSETASEKJAJIATTFQQQQFTUPESYREKHFSPETAUSNFJSETASEKJAEFJARDFQQFTUPFATTFQQUQEJLREKHFSPETQRFNAVEKPRAQFIAUSNFJSETASEKJAJADYZFQUQFPRFNAVEKPMASSFPJQCKPUJAUSNKPEZFIATTFQQIFSFTSEKJQFTUPESYKMFPASEKJQKMSEHEZASEKJQEFHFJNAJTFHFJSAEAUSKHASFQQEFHMDASCKPHQSNPFASAJADYQEQADFPSMPEKPESEZASEKJAJIEJTEIFJSPFQMKJQFTNASRKSQAJIVEPSUADAQQEQSAJSQAEAEIQQFTUPESYAJADYQSQEJPFADSEHFEJTEIFJSEIFJSECETASEKJAJIHESELASEKJMNEQNEJLAJICPAUIMPFVFJSEKJFHAEDQFTUPESYAEAJADYZFQFHAEDTKJSFJSAJIQFJIFPRFNAVEKPSKIFSFTSMNEQNEJLAJIHADETEKUQFHAEDQSPAJQATSEKJHKJESKPEJLCDALQQUQMETEKUQCEJAJTEADSPAJQATSEKJQAJICPAUIEJIETASKPQVUDJFPAREDESYHAJALFHFJSAUSKHASFIQTAJJEJLAEAUSKHASFQVUDJFPAREDESYQTAJJEJLAJIAQQFQQHFJSPEQBAQQFQQHFJSAEFVADUASFQVUDJFPAREDESYQFVFPESYAJIEHMATSCKPMPEKPESEZFIPFHFIEASEKJQFTUPESYAUSKHASEKJAJIKPTNFQSPASEKJEJTEIFJSPFQMKJQFAUSKHASEKJAEIPEVFJWKPBCDKWQAUSKHASFPFQMKJQFQSKTKHHKJQFTUPESYEJTEIFJSQKPTNFQSPASEKJAETKKPIEJASFQQFTUPESYMPKTFQQFQCKPTKHMDFXSNPFASPFQMKJQFQMPFIETSEVFAJADYQEQCKPSNPFASQSNPFASEJSFDDELFJTFAEAJADYZFQSNPFASEJSFDDELFJTFCFFIQSKMPFIETSFHFPLEJLSNPFASQAJIVUDJFPAREDESEFQMNYQETADQFTUPESYFJNAJTFHFJSQUPVFEDDAJTFAEMKWFPFIVEIFKAJADYSETQEIFJSECEFQQUQMETEKUQATSEVESEFQCKPEHMPKVFIMNYQETADQFTUPESYTKHMDEAJTFAJIPFMKPSEJLAUSKHASEKJAUIESAJITKHMDEAJTFAEAQQEQSQEJAUSKHASEJLTKHMDEAJTFTNFTBQAJILFJFPASEJLPFMKPSQSKHFFSPFLUDASEKJQQFTUPFQKCSWAPFIFVFDKMHFJSQUMMKPSQSASETAJIIYJAHETTKIFAJADYQEQAEAJADYZFQTKIFCKPQFTUPESYVUDJFPAREDESEFQIUPEJLIFVFDKMHFJSTKJSEJUKUQHKJESKPEJLUMIASFQAJISPAEJEJLAPFFQQFJSEADSKQSAYANFAIKCFVKDVEJLSNPFASQ"
)

# Anglické frekvence písmen (od nejčastějšího)
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def frequency_analysis(text):
    """Spočítá frekvenci každého písmene v textu."""
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    total = len(text)
    # Seřazení podle frekvence sestupně
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    print("=== Frekvenční analýza šifrového textu ===")
    for ch, count in sorted_freq:
        print(f"  {ch}: {count:4d} ({100*count/total:.2f}%)")
    return sorted_freq


def get_bigrams(text):
    """Spočítá bigramy."""
    bigrams = {}
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        bigrams[bg] = bigrams.get(bg, 0) + 1
    return sorted(bigrams.items(), key=lambda x: -x[1])


def get_trigrams(text):
    """Spočítá trigramy."""
    trigrams = {}
    for i in range(len(text) - 2):
        tg = text[i:i+3]
        trigrams[tg] = trigrams.get(tg, 0) + 1
    return sorted(trigrams.items(), key=lambda x: -x[1])


def decrypt(ciphertext, mapping):
    """Dešifruje text pomocí mapování."""
    result = []
    for ch in ciphertext:
        result.append(mapping.get(ch, '?'))
    return ''.join(result)


def print_mapping(mapping):
    """Vypíše mapování šifrové abecedy na otevřenou."""
    print("\n=== Klíč (šifrová -> otevřená) ===")
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        plain = mapping.get(c, '?')
        print(f"  {c} -> {plain}")


def main():
    ct = CIPHERTEXT

    # 1. Frekvenční analýza
    sorted_freq = frequency_analysis(ct)
    cipher_freq_order = ''.join([ch for ch, _ in sorted_freq])

    print(f"\nŠifrová abeceda podle frekvence: {cipher_freq_order}")
    print(f"Anglická abeceda podle frekvence: {ENGLISH_FREQ_ORDER}")

    # 2. Bigramy a trigramy
    bigrams = get_bigrams(ct)
    trigrams = get_trigrams(ct)

    print("\n=== Top 20 bigramů ===")
    for bg, count in bigrams[:20]:
        print(f"  {bg}: {count}")

    print("\n=== Top 20 trigramů ===")
    for tg, count in trigrams[:20]:
        print(f"  {tg}: {count}")

    # Ruční mapování
    # Na základě frekvenční analýzy a kontextu (IT security text bez mezer):
    #
    # Nejčastější písmeno v šifře: F -> E (nejčastější v angličtině)
    # EJ -> často se opakuje, mohlo by být EN nebo IN
    # Trigram FJS -> ENT (velmi časté)
    # Pokud F=E, J=N, S=T -> pak EJS = ENT ✓
    # SKJ -> TON? nebo jiné
    # Trigram EKJ -> ION (velmi časté v IT textech)
    # Pokud E=I, K=O, J=N -> I je velmi časté písmeno
    # F=E, E=I, K=O, J=N, S=T
    #
    # Bigram FQ -> ES (časté), takže Q=S
    # Bigram EJ -> IN ✓
    # Trigram SEK -> TIO ✓
    # Bigram EQ -> IS ✓
    #
    # AJI -> AND, takže A=A, I=D
    # SNPFAS -> THREAT, S=T, N=H, P=R, F=E, A=A, S=T ✓
    # IFSFTSEKJ -> DETECTION, I=D, F=E, S=T, K=O, J=N ✓
    # QFTUPESY -> SECURITY, Q=S, F=E, T=C, U=U, P=R, E=I, S=T, Y=Y ✓
    #
    # Ověření: EJSFDDELFJTF -> INTELLIGENCE
    # E=I, J=N, S=T, F=E, D=L, L=G, F=E, J=N, T=C, F=E
    # INTELLIGENCE ✓
    #
    # RFIAVEKP -> BEHAVIOR -> R=B, F=E, I=D(?), ne...
    # RFNAVEKP -> BEHAVIOR -> R=B, F=E, N=H, A=A, V=V, E=I, K=O, P=R ✓
    #
    # HADETEKUQ -> MALICIOUS -> H=M, A=A, D=L, E=I, T=C, E=I, K=O, U=U, Q=S ✓
    #
    # VUDJFPAREDESEFQ -> VULNERABILITIES
    # V=V, U=U, D=L, J=N, F=E, P=R, A=A, R=B, E=I, D=L, E=I, S=T, E=I, F=E, Q=S ✓
    #
    # MPFVFJSEKJ -> PREVENTION -> H? ne...
    # M=P, P=R, F=E, V=V, F=E, J=N, S=T, E=I, K=O, J=N ✓
    #
    # MASSFPJQ -> PATTERNS -> M=P, A=A, S=T, S=T, F=E, P=R, J=N, Q=S ✓
    #
    # PFTKLJEAFQ -> RECOGNIZES -> P=R, F=E, T=C, K=O, L=G, J=N, E=I, Z?=Z, F=E, Q=S
    # Hmm, PFTKLJEZFQ -> RECOGNIZES -> Z=Z ✓
    #
    # CEPFWADD -> FIREWALL -> C=F, E=I, P=R, F=E, W=W, A=A, D=L, D=L ✓
    #
    # FJIMKEJS -> ENDPOINT -> F=E, J=N, I=D, M=P, K=O, E=I, J=N, S=T ✓
    #
    # AUSKHASEKJ -> AUTOMATION -> A=A, U=U, S=T, K=O, H=M, A=A, S=T, E=I, K=O, J=N ✓
    #
    # TKHMDEAJTF -> COMPLIANCE -> T=C, K=O, H=M, M=P, D=L, E=I, A=A, J=N, T=C, F=E ✓
    #
    # KPTNFQSPASEKJ -> ORCHESTRATION ✓
    # K=O, P=R, T=C, N=H, F=E, Q=S, S=T, P=R, A=A, S=T, E=I, K=O, J=N
    #
    # Zbývá: B, G, X, O, W
    # UJBJKWJ -> UNKNOWN -> U=U, J=N, B=K, J=N, K=O, W=W, J=N ✓
    # B=K ✓
    #
    # BFYWAYQ -> KEYWAYS -> B=K, F=E, Y=Y, W=W, A=A, Y=Y, Q=S ✓
    #
    # AEOQUETBDY -> I + QUICKLY -> hmm
    # OUETBDY -> QUICKLY -> O=Q, U=U, E=I, T=C, B=K, D=L, Y=Y ✓
    # O=Q ✓
    #
    # TKHMDFX -> COMPLEX -> T=C, K=O, H=M, M=P, D=L, F=E, X=X ✓
    # X=X ✓
    #
    # MNEQNEJL -> PHISHING -> M=P, N=H, E=I, Q=S, N=H, E=I, J=N, L=G ✓
    #
    # CPAUIUJFJS -> ??? C=F, P=R, A=A, U=U, I=D -> FRAUD
    # CPAUIMPFVFJSEKJ -> FRAUDPREVENTION ✓
    #
    # QKCSWAPF -> SOFTWARE -> Q=S, K=O, C=F, S=T, W=W, A=A, P=R, F=E ✓
    #
    # IYJAHET -> DYNAMIC -> I=D, Y=Y, J=N, A=A, H=M, E=I, T=C ✓
    #
    # Zbývá: G (šifrový) -> ?
    # QELJASUPF -> SIGNATURE -> Q=S, E=I, L=G, J=N, A=A, S=T, U=U, P=R, F=E ✓
    # Ale QELJASUPFDFQQ -> SIGNATURELESS ✓
    #
    # G nezaúčtován - podívejme se kde se vyskytuje
    # PFLUDASEKJQ -> REG... -> REGULATIONS -> P=R, F=E, L=G, U=U, D=L, A=A, S=T, E=I, K=O, J=N, Q=S ✓
    # Takže G se v šifře nevyskytuje? Podívejme se...

    mapping = {
        'A': 'A',
        'B': 'K',
        'C': 'F',
        'D': 'L',
        'E': 'I',
        'F': 'E',
        'G': 'J',  # G se v šifrovém textu nevyskytuje, J chybí v otevřené abecedě
        'H': 'M',
        'I': 'D',
        'J': 'N',
        'K': 'O',
        'L': 'G',
        'M': 'P',
        'N': 'H',
        'O': 'Q',
        'P': 'R',
        'Q': 'S',
        'R': 'B',
        'S': 'T',
        'T': 'C',
        'U': 'U',
        'V': 'V',
        'W': 'W',
        'X': 'X',
        'Y': 'Y',
        'Z': 'Z',
    }

    plaintext = decrypt(ct, mapping)

    print_mapping(mapping)

    print("\n=== Dešifrovaný text ===")
    print(plaintext)

    # Ověření - inverzní klíč (otevřená -> šifrová)
    print("\n=== Klíč: otevřená abeceda -> šifrová abeceda ===")
    inverse = {}
    for cipher_ch, plain_ch in mapping.items():
        inverse[plain_ch] = cipher_ch
    for p in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        c = inverse.get(p, '?')
        print(f"  {p} -> {c}")

    # Dešifrovaný text s mezerami pro čitelnost (ruční segmentace klíčových slov)
    print("\n=== Dešifrovaný text (s ručně vloženými mezerami pro kontrolu) ===")
    # Prvních pár slov pro kontrolu
    words_check = [
        "ARTIFICIALINTELLIGENCEISINCREASINGLY",
        "UTILIZEDINVARIOUSSECURITYASPECTS",
        "TOENHANCETHREATDETECTION",
        "INCIDENTRESPONSEANDOVERALLCYBERSECURITY",
    ]
    for w in words_check:
        print(f"  {w}")


if __name__ == "__main__":
    main()
