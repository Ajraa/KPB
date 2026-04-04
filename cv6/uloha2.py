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

freq = Counter(ciphertext)
total = len(ciphertext)

print(f"Delka textu: {total} znaku\n")
for char, count in freq.most_common():
    bar = "#" * int(50 * count / total)
    print(f"  {char}: {count:4d} ({100*count/total:5.2f}%) {bar}")

# Anglicke frekvence (sestupne)
english_freq_order = "ETAOINSRHLDCUMWFGYPBVKJXQZ"
cipher_freq_order = "".join([c for c, _ in freq.most_common()])

print(f"\nSifrova abeceda (dle frekvence):  {cipher_freq_order}")
print(f"Anglicka abeceda (dle frekvence): {english_freq_order}")

def decrypt(ct, mapping):
    return "".join(mapping.get(c, "?") for c in ct)

# Atbash: kazde pismeno na pozici i se nahradi pismenem na pozici (25-i)
mapping = {}
for i in range(26):
    c = chr(ord('A') + i)
    p = chr(ord('Z') - i)
    mapping[c] = p

# Overeni Atbash
is_atbash = True
for c in mapping:
    expected = chr(ord('Z') - (ord(c) - ord('A')))
    if mapping[c] != expected:
        is_atbash = False
        break
print(f"  Overeni Atbash: {'ANO - vsechna mapovani odpovidaji' if is_atbash else 'NE'}")

plaintext = decrypt(ciphertext, mapping)

print("\n" + "=" * 60)
print("DESIFROVANY TEXT (bez mezer)")
print("=" * 60)
print(plaintext)

plain_freq = Counter(plaintext)
missing = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in plain_freq]
print(f"Chybejici pismena v otevrenom textu: {', '.join(missing)}")
