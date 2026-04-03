#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uloha 2 - Desifrovani monoalfabeticke substituce
Frekvencni analyza a iterativni upresneni mapovani.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collections import Counter

ciphertext = (
    "GSRHRHZMFMFHFZOKZIZTIZKSRZNXFIRLFHZHGLQFHGSLDJFRXPOBBLFXZMURMWLFGDSZG"
    "RHHLFMFHFZOZYLFGRGRGOLLPHHLLIWRMZIBZMWKOZRMGSZGBLFDLFOWGSRMPMLGSRMTDZHH"
    "FILMTDRGSRGRMUZXGMLGSRMTRHDILMTDRGSRGRHSRTSOBFMFHFZOGSLFTSHGFWBRGZMWGSR"
    "MPZYLFGRGYFGBLFHGROONZBMLGURMWZMBGSRMTLWWRUBLFDLIPZGRGZYRGBLFNRTSGURMWL"
    "FGGIBGLWLHLDRGSLFGZMBXLZXSRMTZOGSLFTSRGRHSRTSOBXLNNLMRMNLHGKZIZTIZKSHZ"
    "GIRZOZGZXXLNKORHSRMTHFXSZMZXXLFMGLUDIRGRMTRHMLGGSZGWRUURXFOGBLFDLFOWDZM"
    "GGLPMLDGSZGGSRHGZHPNRTSGLXXFKBNLHGLUBLFIYIZRMULISLFIHRUMLGULIZHSLIGWFIZ"
    "GRLMZMWZHBLFDLGSILFTSGSRHZXXLFMGRGHXLNKLHRGRLMDROOOLLPZGBKRXZORMZDZBLIG"
    "DLGSRHRHHLULIRZNHGIFTTORMTGLZGGZRMDLIWHGSZGDLFOWRNKZIGDSZGRDZMGGLHZBZMW"
    "RMWLRMTHLRNZOHLNRHHRMTLFGHLNLNZMBDLIWHGSZGRNFHGWRHNRHHLDRMTGLLFIXLMWRG"
    "RLMGSZGYRMWHGSRHHLOFGRLMMLGDROORMTGLTLLMZMWLMDRGSGSRHHFKKLHRMTOBHROOBZM"
    "WZYHFIWKZIZTIZKSROOLKGGLKFGZSZOGZGGSRHKLRMGSZERMTHSLDMKIZXGRXZOOBGSZGRG"
    "RHMLGRNKIZXGRXZOGLZGGZRMZKZIZTIZKSDRGSLFIHBNYLOLUSRTSORTSG"
)

# ============================================================
# 1. Frekvencni analyza
# ============================================================
freq = Counter(ciphertext)
total = len(ciphertext)

print("=" * 60)
print("1. FREKVENCNI ANALYZA SIFROVEHO TEXTU")
print("=" * 60)
print(f"Delka textu: {total} znaku\n")
for char, count in freq.most_common():
    bar = "#" * int(50 * count / total)
    print(f"  {char}: {count:4d} ({100*count/total:5.2f}%) {bar}")

# Anglicke frekvence (sestupne)
english_freq_order = "ETAOINSRHLDCUMWFGYPBVKJXQZ"
cipher_freq_order = "".join([c for c, _ in freq.most_common()])

print(f"\nSifrova abeceda (dle frekvence):  {cipher_freq_order}")
print(f"Anglicka abeceda (dle frekvence): {english_freq_order}")

# ============================================================
# 2. Pocatecni mapovani na zaklade frekvenci
# ============================================================
initial_mapping = {}
for i, c in enumerate(cipher_freq_order):
    if i < len(english_freq_order):
        initial_mapping[c] = english_freq_order[i]

def decrypt(ct, mapping):
    return "".join(mapping.get(c, "?") for c in ct)

print("\n" + "=" * 60)
print("2. POCATECNI DESIFROVANI (ciste frekvencni)")
print("=" * 60)
initial_plain = decrypt(ciphertext, initial_mapping)
# Zobrazime prvnich 200 znaku
print(initial_plain[:200] + "...")
print("\n(Text neni citelny -> je treba rucne upravit mapovani)")

# ============================================================
# 3. Analyza bigramu a trigramu
# ============================================================
bigrams = Counter(ciphertext[i:i+2] for i in range(len(ciphertext)-1))
trigrams = Counter(ciphertext[i:i+3] for i in range(len(ciphertext)-2))

print("\n" + "=" * 60)
print("3. NEJCASTEJSI BIGRAMY A TRIGRAMY")
print("=" * 60)
print("Bigramy:", ", ".join(f"{bg}:{c}" for bg, c in bigrams.most_common(10)))
print("Trigramy:", ", ".join(f"{tg}:{c}" for tg, c in trigrams.most_common(10)))

# ============================================================
# 4. Iterativni upresneni mapovani
# ============================================================
print("\n" + "=" * 60)
print("4. ITERATIVNI UPRESNENI MAPOVANI")
print("=" * 60)

print("""
Analyza vzoru:
  GSR (14x) -> THE (nejcastejsi trigram v anglictine)
    => G=T, S=H, R=I (ale text je lipogram bez E, takze GSR->THI)
  GSRH -> THIS: potvrzuje G->T, S->H, R->I, H->S
  GSZG -> THAT: potvrzuje Z->A
  ZMW (6x) -> AND: Z->A, M->N, W->D
  DRGS -> WITH: D->W
  BLF -> YOU: B->Y, F->U
  DLFOW -> WOULD: O->L
  KZIZTIZKS -> PARAGRAPH: K->P, I->R, T->G
  FMFHFZO -> UNUSUAL: potvrzuje F->U, H->S
  XFIRLFH -> CURIOUS: X->C
  RNKZIG -> IMPART: N->M
  YIZRM -> BRAIN: Y->B
  SZERMTHSLDM -> HAVINGSHOWN: E->V
  JFRXPOB -> QUICKLY: J->Q
  SRTSORTSG -> HIGHLIGHT: potvrzuje vsechna mapovani

  Vysledne mapovani odpovida ATBASH sifre (A<->Z, B<->Y, ..., M<->N)
""")

# ============================================================
# 5. Finalni mapovani - ATBASH sifra
# ============================================================
# Atbash: kazde pismeno na pozici i se nahradi pismenem na pozici (25-i)
mapping = {}
for i in range(26):
    c = chr(ord('A') + i)
    p = chr(ord('Z') - i)
    mapping[c] = p

print("=" * 60)
print("5. FINALNI MAPOVANI (ATBASH)")
print("=" * 60)
for c in sorted(mapping.keys()):
    print(f"  {c} -> {mapping[c]}", end="")
    if (ord(c) - ord('A') + 1) % 6 == 0:
        print()
print()

# Overeni Atbash
is_atbash = True
for c in mapping:
    expected = chr(ord('Z') - (ord(c) - ord('A')))
    if mapping[c] != expected:
        is_atbash = False
        break
print(f"  Overeni Atbash: {'ANO - vsechna mapovani odpovidaji' if is_atbash else 'NE'}")

# ============================================================
# 6. Desifrovany text
# ============================================================
plaintext = decrypt(ciphertext, mapping)

print("\n" + "=" * 60)
print("6. DESIFROVANY TEXT (bez mezer)")
print("=" * 60)
print(plaintext)

# Pridame mezery rucne pro citelnost
readable = (
    "THIS IS AN UNUSUAL PARAGRAPH I AM CURIOUS AS TO JUST HOW QUICKLY YOU CAN "
    "FIND OUT WHAT IS SO UNUSUAL ABOUT IT IT LOOKS SO ORDINARY AND PLAIN THAT "
    "YOU WOULD THINK NOTHING WAS SURONG WITH IT IN FACT NOTHING IS WRONG WITH "
    "IT IS HIGHLY UNUSUAL THOUGH STUDY IT AND THINK ABOUT IT BUT YOU STILL MAY "
    "NOT FIND ANY THING ODD IF YOU WORK AT IT A BIT YOU MIGHT FIND OUT TRY TO "
    "DO SO WITHOUT ANY COACHING ALTHOUGH IT IS HIGHLY COMMON IN MOST PARAGRAPHS "
    "A TRIAL AT ACCOMPLISHING SUCH AN ACCOUNT OF WRITING IS NOT THAT DIFFICULT "
    "YOU WOULD WANT TO KNOW THAT THIS TASK MIGHT OCCUPY MOST OF YOUR BRAIN FOR "
    "HOURS IF NOT FOR A SHORT DURATION AND AS YOU WO THROUGH THIS ACCOUNT ITS "
    "COMPOSITION WILL LOOK ATYPICAL IN A WAY OR TWO THIS IS SO FOR I AM "
    "STRUGGLING TO ATTAIN WORDS THAT WOULD IMPART WHAT I WANT TO SAY AND IN "
    "DOING SO I M ALSO MISSING OUT SO MANY WORDS THAT I MUST DISMISS OWING TO "
    "OUR CONDITION THAT BINDS THIS SOLUTION NOT WILLING TO GO ON AND ON WITH "
    "THIS SUPPOSINGLY SILLY AND ABSURD PARAGRAPH ILL OPT TO PUT A HALT AT THIS "
    "POINT HAVING SHOWN PRACTICALLY THAT IT IS NOT IMPRACTICAL TO ATTAIN A "
    "PARAGRAPH WITH OUR SYMBOL OF HIGHLIGHT"
)

print("\n" + "=" * 60)
print("7. CITELNY TEXT (s mezerami)")
print("=" * 60)
print(readable)

# ============================================================
# 8. Analyza neobvyklosti
# ============================================================
print("\n" + "=" * 60)
print("8. ANALYZA NEOBVYKLOSTI OTEVRENEHO TEXTU")
print("=" * 60)

plain_freq = Counter(plaintext)
missing = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in plain_freq]
print(f"Chybejici pismena v otevrenom textu: {', '.join(missing)}")
print()

# Pismeno E
print("KLICOVE ZJISTENI:")
print("-" * 40)
print(f"  Pismeno 'E' se v textu NEVYSKYTUJE (0 vyskytu)!")
print(f"  Pismeno 'E' je pritom NEJCASTEJSI pismeno v anglictine (~13%).")
print(f"  Text je LIPOGRAM - text zamerne vynechavajici pismeno 'E'.")
print()
print(f"  (Pismena X a Z take chybi, ale to je u kratkych textu bezne,")
print(f"   protoze jsou to nejmin castejsi pismena anglicke abecedy.)")

print()
print("TEXT SAM O SOBE POPISUJE TUTO VLASTNOST:")
print("-" * 40)
print("  'This is an unusual paragraph...'")
print("  'I am curious as to just how quickly you can find out")
print("   what is so unusual about it...'")
print("  'our symbol of highlight' = pismeno E (nejcastejsi, 'highlight')")
print("  Text vyziva ctenare, aby zjistil, co je neobvykleho.")

# ============================================================
# 9. Shrnutí
# ============================================================
print("\n" + "=" * 60)
print("9. SHRNUTI")
print("=" * 60)
print()
print("SIFRA: Atbash (monoalfabeticka substituce)")
print("  Kazde pismeno se nahradi 'zrcadlovym' pismenem v abecede:")
print("  A<->Z, B<->Y, C<->X, ..., M<->N")
print("  Klic je tedy fixni: ZYXWVUTSRQPONMLKJIHGFEDCBA")
print()
print("NEOBVYKLOST: Otevreny text je LIPOGRAM BEZ PISMENE E.")
print("  - E je nejcastejsi pismeno anglictiny")
print("  - Jeho absence zpusobuje, ze frekvencni analyza nefunguje")
print("    spravne pri automatickem prirazeni (E v sifrovem textu")
print("    neni nejcastejsi -> nelze jednoduse prirazovat dle frekvenci)")
print("  - Diky absenci E je distribuce frekvenci posunuta a muze")
print("    vest k chybnym zaverum pri ciste frekvencni analyze")
print("  - Sifra Atbash mapuje E<->V, a protoze E v plaintextu")
print("    chybi, pismeno V se v sifrovem textu (skoro) nevyskytuje")
