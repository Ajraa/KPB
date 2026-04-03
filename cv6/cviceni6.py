"""
Cviceni 6 - AES/DES v rezimech ECB, CBC, CTR
Odpovedi na otazky formulare
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os

# === SPOLEČNÉ NASTAVENÍ ===
# Klíče
aes_key_128 = b'\x01' * 16   # AES-128
aes_key_256 = b'\x02' * 32   # AES-256
des_key = b'\x03' * 8        # DES (8 bajtů)
iv_16 = b'\x00' * 16         # IV pro AES (16 bajtů)
iv_8 = b'\x00' * 8           # IV pro DES (8 bajtů)
nonce_16 = b'\x00' * 16      # Nonce pro AES-CTR

# Otevřený text se vzorem — opakující se bloky
# 16 bajtů opakovaných 4× = 64 bajtů, vzor je jasně viditelný
pattern_block = b'ABCDEFGHIJKLMNOP'  # 16 bajtů = 1 AES blok
plaintext = pattern_block * 4  # 4 identické bloky

print("=" * 70)
print("CVIČENÍ 6 - AES/DES režimy ECB, CBC, CTR")
print("=" * 70)
print(f"\nOtevřený text (hex): {plaintext.hex()}")
print(f"Otevřený text (ASCII): {plaintext.decode()}")
print(f"Délka: {len(plaintext)} bajtů = {len(plaintext)//16} bloků po 16 bajtech")
print(f"Poznámka: Všechny 4 bloky jsou identické → vzor v otevřeném textu")

# === 1.1 AES v režimu ECB - zachování vzorů ===
print("\n" + "=" * 70)
print("1.1 AES-ECB - zachování vzorů")
print("=" * 70)

# AES-128 ECB
cipher = Cipher(algorithms.AES(aes_key_128), modes.ECB())
enc = cipher.encryptor()
ct_aes128_ecb = enc.update(plaintext) + enc.finalize()

print(f"\nAES-128 ECB šifrový text (hex):")
for i in range(0, len(ct_aes128_ecb), 16):
    block = ct_aes128_ecb[i:i+16]
    print(f"  Blok {i//16 + 1}: {block.hex()}")

# AES-256 ECB
cipher = Cipher(algorithms.AES(aes_key_256), modes.ECB())
enc = cipher.encryptor()
ct_aes256_ecb = enc.update(plaintext) + enc.finalize()

print(f"\nAES-256 ECB šifrový text (hex):")
for i in range(0, len(ct_aes256_ecb), 16):
    block = ct_aes256_ecb[i:i+16]
    print(f"  Blok {i//16 + 1}: {block.hex()}")

# Kontrola vzorů
blocks_128 = [ct_aes128_ecb[i:i+16] for i in range(0, len(ct_aes128_ecb), 16)]
blocks_256 = [ct_aes256_ecb[i:i+16] for i in range(0, len(ct_aes256_ecb), 16)]

print(f"\nAES-128 ECB: Všechny bloky stejné? {len(set(blocks_128)) == 1}")
print(f"AES-256 ECB: Všechny bloky stejné? {len(set(blocks_256)) == 1}")

print("""
ODPOVĚĎ 1.1:
Ano, vzor z otevřeného textu JE zachován v šifrovém textu v režimu ECB.
Identické bloky otevřeného textu produkují identické bloky šifrového textu.

Zvětšená velikost bloku AES (128 vs 256 bitový klíč) NEMÁ vliv na vzory
v šifrovém textu. AES vždy pracuje s 16-bajtovými bloky bez ohledu na
délku klíče. Režim ECB šifruje každý blok nezávisle stejným klíčem,
takže identické bloky OT vždy produkují identické bloky ŠT.

Poznámka: Větší klíč (AES-256) zvyšuje bezpečnost proti brute-force
útokům, ale neřeší problém zachování vzorů v ECB režimu.
""")

# === 1.2 AES a DES v režimu CBC ===
print("=" * 70)
print("1.2 AES-CBC a DES-CBC - zachování vzorů")
print("=" * 70)

# AES-128 CBC
cipher = Cipher(algorithms.AES(aes_key_128), modes.CBC(iv_16))
enc = cipher.encryptor()
ct_aes_cbc = enc.update(plaintext) + enc.finalize()

print(f"\nAES-128 CBC šifrový text (hex):")
for i in range(0, len(ct_aes_cbc), 16):
    block = ct_aes_cbc[i:i+16]
    print(f"  Blok {i//16 + 1}: {block.hex()}")

blocks_cbc = [ct_aes_cbc[i:i+16] for i in range(0, len(ct_aes_cbc), 16)]
print(f"\nAES-128 CBC: Všechny bloky stejné? {len(set(blocks_cbc)) == 1}")
print(f"AES-128 CBC: Počet unikátních bloků: {len(set(blocks_cbc))}/{len(blocks_cbc)}")

# DES CBC - DES má 8-bajtové bloky, potřebujeme plaintext dělitelný 8
des_pattern = b'ABCDEFGH'  # 8 bajtů = 1 DES blok
des_plaintext = des_pattern * 4

cipher = Cipher(algorithms.TripleDES(des_key + des_key + des_key), modes.CBC(iv_8))
enc = cipher.encryptor()
ct_des_cbc = enc.update(des_plaintext) + enc.finalize()

print(f"\nDES CBC šifrový text (hex):")
for i in range(0, len(ct_des_cbc), 8):
    block = ct_des_cbc[i:i+8]
    print(f"  Blok {i//8 + 1}: {block.hex()}")

des_blocks_cbc = [ct_des_cbc[i:i+8] for i in range(0, len(ct_des_cbc), 8)]
print(f"\nDES CBC: Všechny bloky stejné? {len(set(des_blocks_cbc)) == 1}")
print(f"DES CBC: Počet unikátních bloků: {len(set(des_blocks_cbc))}/{len(des_blocks_cbc)}")

print("""
ODPOVĚĎ 1.2:
Ne, v režimu CBC vzory NEJSOU zachovány. Identické bloky otevřeného textu
produkují RŮZNÉ bloky šifrového textu.

Důvod: V CBC režimu se každý blok otevřeného textu nejprve XORuje
s předchozím blokem šifrového textu (nebo IV u prvního bloku) a teprve
poté se šifruje. Tím se vytváří řetězení (chaining), které zajistí,
že i identické bloky OT produkují různé bloky ŠT.

Toto platí jak pro AES, tak pro DES — princip CBC je stejný bez ohledu
na použitý blokový šifrovací algoritmus.
""")

# === 2(a) AES v režimu CTR ===
print("=" * 70)
print("2(a) AES-CTR - zachování vzorů")
print("=" * 70)

cipher = Cipher(algorithms.AES(aes_key_128), modes.CTR(nonce_16))
enc = cipher.encryptor()
ct_aes_ctr = enc.update(plaintext) + enc.finalize()

print(f"\nAES-128 CTR šifrový text (hex):")
for i in range(0, len(ct_aes_ctr), 16):
    block = ct_aes_ctr[i:i+16]
    print(f"  Blok {i//16 + 1}: {block.hex()}")

blocks_ctr = [ct_aes_ctr[i:i+16] for i in range(0, len(ct_aes_ctr), 16)]
print(f"\nAES-128 CTR: Všechny bloky stejné? {len(set(blocks_ctr)) == 1}")
print(f"AES-128 CTR: Počet unikátních bloků: {len(set(blocks_ctr))}/{len(blocks_ctr)}")

print("""
ODPOVĚĎ 2(a):
Ne, v režimu CTR vzory NEJSOU zachovány. Identické bloky otevřeného textu
produkují RŮZNÉ bloky šifrového textu.

Důvod: CTR režim šifruje inkrementující se čítač (counter) a výsledek
XORuje s otevřeným textem. Protože čítač je pro každý blok jiný,
keystream je pro každý blok jiný, a tedy i stejné bloky OT produkují
různé bloky ŠT.
""")

# === 2(b) CTR - modifikace bajtu v šifrovém textu ===
print("=" * 70)
print("2(b) CTR - efekt modifikace bajtu šifrového textu")
print("=" * 70)

# Zašifrujeme delší text
long_plaintext = b'A' * 16 + b'B' * 16 + b'C' * 16 + b'D' * 16  # 64 bajtů = 4 bloky

cipher = Cipher(algorithms.AES(aes_key_128), modes.CTR(nonce_16))
enc = cipher.encryptor()
ct_original = enc.update(long_plaintext) + enc.finalize()

# Změníme 1 bajt v 2. bloku šifrového textu
ct_modified = bytearray(ct_original)
ct_modified[20] ^= 0xFF  # Změna bajtu na pozici 20 (v 2. bloku)
ct_modified = bytes(ct_modified)

# Dešifrujeme modifikovaný šifrový text
cipher = Cipher(algorithms.AES(aes_key_128), modes.CTR(nonce_16))
dec = cipher.decryptor()
pt_from_modified = dec.update(ct_modified) + dec.finalize()

print(f"Originální OT:          {long_plaintext.hex()}")
print(f"Dešifrovaný modifik. ŠT: {pt_from_modified.hex()}")
print(f"\nZměněné bajty:")
diff_count = 0
diff_blocks = set()
for i in range(len(long_plaintext)):
    if long_plaintext[i] != pt_from_modified[i]:
        diff_count += 1
        diff_blocks.add(i // 16)
        print(f"  Pozice {i} (blok {i//16 + 1}): 0x{long_plaintext[i]:02x} -> 0x{pt_from_modified[i]:02x}")

print(f"\nPočet porušených bajtů: {diff_count}")
print(f"Počet porušených bloků: {len(diff_blocks)}")

print("""
ODPOVĚĎ 2(b):
V režimu CTR způsobí změna 1 bajtu šifrového textu porušení pouze 1 bajtu
otevřeného textu (na stejné pozici). Porušen je tedy 1 bajt = část 1 bloku.

Důvod: CTR je proudová šifra — každý bajt šifrového textu odpovídá přímo
jednomu bajtu otevřeného textu přes XOR s keystreamem. Změna jednoho bajtu
ŠT ovlivní pouze odpovídající bajt OT. Toto je zásadní vlastnost CTR režimu
— chyby se nešíří (na rozdíl od CBC).

Poznámka: Toto je zároveň bezpečnostní riziko — útočník může cíleně měnit
konkrétní bajty otevřeného textu (bit-flipping attack).
""")

# === 2(c) CTR - zrušení (smazání) bajtu v šifrovém textu ===
print("=" * 70)
print("2(c) CTR - efekt zrušení (smazání) bajtu šifrového textu")
print("=" * 70)

# Smažeme 1 bajt z šifrového textu (pozice 20)
ct_deleted = ct_original[:20] + ct_original[21:]

print(f"Délka originálního ŠT: {len(ct_original)} bajtů")
print(f"Délka ŠT po smazání:   {len(ct_deleted)} bajtů")

# Dešifrování zkráceného šifrového textu
cipher = Cipher(algorithms.AES(aes_key_128), modes.CTR(nonce_16))
dec = cipher.decryptor()
pt_from_deleted = dec.update(ct_deleted) + dec.finalize()

print(f"\nOriginální OT:       {long_plaintext.hex()}")
print(f"Dešifrovaný po smaz: {pt_from_deleted.hex()}")

# Porovnání
diff_count = 0
min_len = min(len(long_plaintext), len(pt_from_deleted))
for i in range(min_len):
    if long_plaintext[i] != pt_from_deleted[i]:
        diff_count += 1

print(f"\nPočet porušených bajtů (ze společné délky {min_len}): {diff_count}")
print(f"Bajty, které se neshodují od pozice smazání:")
for i in range(19, min(min_len, 48)):
    match = "OK" if long_plaintext[i] == pt_from_deleted[i] else "PORUŠEN"
    print(f"  Pozice {i}: OT=0x{long_plaintext[i]:02x} vs dešifr=0x{pt_from_deleted[i]:02x} [{match}]")

print("""
ODPOVĚĎ 2(c):
Smazání bajtu ze šifrového textu způsobí katastrofální desynchronizaci.

Od pozice smazaného bajtu jsou VŠECHNY následující bajty porušeny, protože
keystream je generován sekvenčně (counter se inkrementuje po blocích),
ale šifrový text je nyní posunutý o 1 bajt. Každý bajt ŠT od pozice smazání
je XORován se špatným bajtem keystreaemu.

Bajty PŘED pozicí smazání zůstávají korektní (nejsou ovlivněny).
Šifrový text se podaří dešifrovat (operace proběhne), ale výsledek je
od místa smazání nesmyslný.

Porušeno: všechny bajty od pozice smazání do konce = {0} bajtů.
Neporušeno: bajty před pozicí smazání = prvních 20 bajtů.
""".format(len(long_plaintext) - 20))

print("=" * 70)
print("SHRNUTÍ")
print("=" * 70)
print("""
ECB: Zachovává vzory (identické bloky → identické šifrové bloky)
CBC: Nezachovává vzory (řetězení bloků)
CTR: Nezachovává vzory (unikátní čítač pro každý blok)

CTR modifikace bajtu: Porušen pouze 1 bajt OT (bit-flipping)
CTR smazání bajtu: Porušeny všechny bajty od pozice smazání (desynchronizace)
""")
