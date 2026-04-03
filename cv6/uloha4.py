"""
Vernamova šifra (OTP) s opakovaným klíčem - kryptanalýza.
Dva šifrové texty C1, C2 byly zašifrovány stejným klíčem K.
Hledáme otevřené texty M1, M2 a klíč K.
"""

import urllib.request
import string

# Šifrové texty
C1 = [0x22, 0x02, 0x0f, 0x1c, 0x0b, 0x1a, 0x1e, 0x0f, 0x1d, 0x08, 0x18, 0x16]
C2 = [0x2c, 0x11, 0x1c, 0x06, 0x14, 0x1b, 0x07, 0x00, 0x00, 0x12, 0x1a, 0x00]

# Krok 1: Spočítáme C1 XOR C2 (eliminace klíče)
C1_xor_C2 = [a ^ b for a, b in zip(C1, C2)]
print("C1 XOR C2 =", [hex(x) for x in C1_xor_C2])

# Krok 2: Načtení slovníku 12-písmenných slov
def load_words():
    """Načte 12-písmenná anglická slova z různých zdrojů."""
    words = set()

    # Zkusíme stáhnout slovník z webu
    urls = [
        "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
        "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt",
    ]

    for url in urls:
        try:
            print(f"Stahuji slovník z {url}...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=15)
            text = response.read().decode("utf-8", errors="ignore")
            for line in text.splitlines():
                w = line.strip().lower()
                if len(w) == 12 and w.isalpha():
                    words.add(w)
            print(f"  Načteno {len(words)} slov délky 12.")
            if len(words) > 100:
                break
        except Exception as e:
            print(f"  Chyba: {e}")

    # Záložní varianta - zkusíme NLTK
    if len(words) < 100:
        try:
            import nltk
            nltk.download("words", quiet=True)
            from nltk.corpus import words as nltk_words
            for w in nltk_words.words():
                wl = w.lower()
                if len(wl) == 12 and wl.isalpha():
                    words.add(wl)
            print(f"  NLTK: celkem {len(words)} slov délky 12.")
        except Exception as e:
            print(f"  NLTK nedostupné: {e}")

    return words


def xor_bytes(data, key_bytes):
    """XOR dvou seznamů bajtů."""
    return [a ^ b for a, b in zip(data, key_bytes)]


def word_to_bytes(word):
    """Převede slovo na seznam ASCII hodnot."""
    return [ord(c) for c in word]


def bytes_to_word(b):
    """Převede seznam ASCII hodnot na řetězec, pokud jsou všechny platné ASCII znaky."""
    try:
        return "".join(chr(x) for x in b)
    except (ValueError, OverflowError):
        return None


def is_alpha_word(b):
    """Zkontroluje, zda všechny bajty odpovídají písmenům (a-z, A-Z)."""
    return all(
        (0x41 <= x <= 0x5A) or (0x61 <= x <= 0x7A) for x in b
    )


def main():
    words = load_words()
    if not words:
        print("CHYBA: Nepodařilo se načíst žádná slova.")
        return

    # Přidáme i varianty s velkým prvním písmenem
    all_variants = set()
    for w in words:
        all_variants.add(w.lower())
        all_variants.add(w.capitalize())
        all_variants.add(w.upper())

    # Slovník pro rychlé vyhledávání (lowercase)
    words_lower = {w.lower() for w in words}

    print(f"\nHledám páry M1, M2 (slovník: {len(words)} slov, varianty: {len(all_variants)})...\n")

    found = []

    for w1 in all_variants:
        m1_bytes = word_to_bytes(w1)
        # M2 = M1 XOR (C1 XOR C2)
        m2_bytes = xor_bytes(m1_bytes, C1_xor_C2)

        # Zkontrolujeme, zda M2 jsou platná písmena
        if not is_alpha_word(m2_bytes):
            continue

        m2 = bytes_to_word(m2_bytes)
        if m2 is None:
            continue

        # Zkontrolujeme, zda M2 (lowercase) je ve slovníku
        if m2.lower() in words_lower:
            # Spočítáme klíč
            key_bytes = xor_bytes(m1_bytes, C1)
            key_word = bytes_to_word(key_bytes)

            # Zkontrolujeme, zda klíč je taky platné slovo
            if is_alpha_word(key_bytes) and key_word and key_word.lower() in words_lower:
                found.append((w1, m2, key_word))
                print(f"NALEZENO!")
                print(f"  M1  = {w1}")
                print(f"  M2  = {m2}")
                print(f"  K   = {key_word}")
                print(f"  M1 (hex) = {[hex(x) for x in m1_bytes]}")
                print(f"  M2 (hex) = {[hex(x) for x in m2_bytes]}")
                print(f"  K  (hex) = {[hex(x) for x in key_bytes]}")
                print()

    if not found:
        print("Nenalezen žádný platný pár M1, M2 s platným klíčem K.")
        print("Zkouším bez podmínky na klíč (klíč nemusí být slovo ze slovníku)...")
        print()

        for w1 in all_variants:
            m1_bytes = word_to_bytes(w1)
            m2_bytes = xor_bytes(m1_bytes, C1_xor_C2)
            if not is_alpha_word(m2_bytes):
                continue
            m2 = bytes_to_word(m2_bytes)
            if m2 is None:
                continue
            if m2.lower() in words_lower:
                key_bytes = xor_bytes(m1_bytes, C1)
                key_word = bytes_to_word(key_bytes)
                key_is_alpha = is_alpha_word(key_bytes)
                found.append((w1, m2, key_word))
                print(f"  M1 = {w1}, M2 = {m2}, K = {key_word} (písmena: {key_is_alpha})")

    if not found:
        print("\nŽádný pár nenalezen ani bez podmínky na klíč.")
        print("Klíče jsou pravděpodobně různé, nebo slova nejsou ve slovníku.")

    # Ověření
    if found:
        print("\n=== OVĚŘENÍ prvního nalezeného řešení ===")
        m1, m2, key = found[0]
        m1b = word_to_bytes(m1)
        m2b = word_to_bytes(m2)
        kb = word_to_bytes(key)
        c1_check = xor_bytes(m1b, kb)
        c2_check = xor_bytes(m2b, kb)
        print(f"M1 XOR K = {[hex(x) for x in c1_check]}")
        print(f"C1       = {[hex(x) for x in C1]}")
        print(f"Shoda C1: {c1_check == C1}")
        print(f"M2 XOR K = {[hex(x) for x in c2_check]}")
        print(f"C2       = {[hex(x) for x in C2]}")
        print(f"Shoda C2: {c2_check == C2}")


if __name__ == "__main__":
    main()
