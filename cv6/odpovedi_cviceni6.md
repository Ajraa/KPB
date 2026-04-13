# Cvičení 6 - Odpovědi

## 1.1 Je nějaký vzor z otevřeného textu zachován v textu šifrovém? Má zvětšená velikost bloku AES vliv?

**Ano, v režimu ECB je vzor zachován.** Identické bloky otevřeného textu produkují identické bloky šifrového textu. Režim ECB šifruje každý blok nezávisle stejným klíčem — pokud se dva bloky OT shodují, shodují se i odpovídající bloky ŠT.

**Zvětšená velikost klíče AES (128 vs 256 bit) NEMÁ vliv na vzory.** AES vždy pracuje s 16-bajtovými (128-bitovými) bloky bez ohledu na délku klíče. Velikost klíče zvyšuje bezpečnost proti brute-force útokům, ale neřeší problém deterministického šifrování identických bloků v ECB režimu.

## 1.2 AES a DES v režimu CBC - zachovávají vzory?

**Ne, v režimu CBC vzory NEJSOU zachovány.** Identické bloky OT produkují různé bloky ŠT, a to jak u AES, tak u DES.

**Důvod:** V CBC režimu se každý blok OT nejprve XORuje s předchozím blokem ŠT (nebo IV u prvního bloku) a teprve poté se šifruje. Toto řetězení (chaining) zajistí, že i identické bloky OT produkují různé bloky ŠT. Princip CBC je stejný bez ohledu na použitý blokový šifrovací algoritmus.

## 2(a) Byl zachován vzor v režimu CTR?

**Ne, v režimu CTR vzory NEJSOU zachovány.** Identické bloky OT produkují různé bloky ŠT.

**Důvod:** CTR režim šifruje inkrementující se čítač (counter) blokovým šifrovacím algoritmem a výsledek XORuje s OT. Protože čítač je pro každý blok jiný, keystream je pro každý blok unikátní, a tedy i stejné bloky OT produkují různé bloky ŠT.

## 2(b) Kolik informace bylo po dešifrování změněného ŠT porušeno?

**Porušen 1 bajt (= část 1 bloku).**

Změna 1 bajtu šifrového textu v režimu CTR způsobí porušení pouze 1 bajtu otevřeného textu na stejné pozici. CTR se chová jako proudová šifra — každý bajt ŠT přímo odpovídá jednomu bajtu OT přes XOR s keystreamem. Chyby se nešíří.

**Poznámka:** Toto je zároveň bezpečnostní riziko — útočník může cíleně měnit konkrétní bajty OT (bit-flipping attack) bez ovlivnění ostatních bajtů.

## 2(c) Efekt zrušeného (smazaného) bajtu

**Smazání bajtu ze ŠT způsobí katastrofální desynchronizaci.**

- **Bajty PŘED pozicí smazání:** Korektní (neovlivněny)
- **Bajty OD pozice smazání do konce:** VŠECHNY porušeny

**Důvod:** Keystream je generován sekvenčně (counter se inkrementuje po blocích), ale po smazání bajtu je ŠT posunutý o 1 bajt vůči keystreaemu. Každý bajt ŠT od pozice smazání je XORován se špatným bajtem keystreaemu.

**Dešifrování proběhne** (operace se provede bez chyby), ale výsledný OT je od místa smazání nesmyslný. Navíc je výsledek kratší o 1 bajt.
