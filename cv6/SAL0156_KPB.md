# Druhý bodovaný zápočtový úkol — KPB
**Student:** SAL0156  

---

## Úloha 1 — Obecná monoalfabetická substituce

### Šifrový text
```
APSECETEADEJSFDDELFJTFEQEJTPFAQEJLDYUSEDEZFIEJVAPEKUQQFTUPESYAQMFTSQS...
```

### Postup řešení

**Nástroje:** vlastní implementace (`uloha1.py`), ověření online nástrojem [quipqiup.com](https://quipqiup.com/), který po vložení šifrového textu vrátil shodný výsledek.

#### Krok 1 — Frekvenční analýza

Délka šifrového textu: **2270 znaků**. Frekvence písmen šifrového textu vs. standardní anglická abeceda:

| Šifrové | Počet | %     | → | Anglické (standard) | % |
|---------|-------|-------|---|---------------------|---|
| **F**   | 253   | 11,15 | → | **E**               | 12,70 |
| **E**   | 249   | 10,97 | → | **T**               |  9,06 |
| **S**   | 219   |  9,65 | → | **A**               |  8,17 |
| **A**   | 215   |  9,48 | → | **O**               |  7,51 |
| **J**   | 211   |  9,30 | → | **I**               |  6,97 |
| **Q**   | 170   |  7,49 | → | **N**               |  6,75 |
| **K**   | 141   |  6,21 | → | **S**               |  6,33 |
| **P**   | 139   |  6,13 | → | **H**               |  6,09 |
| **T**   | 104   |  4,58 | → | **R**               |  5,99 |
| **I**   |  84   |  3,70 | → | **D**               |  4,25 |

Přímé mapování frekvencí F→E, E→T, ... by dávalo nesprávný výsledek (text je tematický — IT bezpečnost — s charakteristickým slovníkem). Proto bylo nutné pokračovat analýzou n-gramů.

#### Krok 2 — Analýza trigramů a bigramů

Top 10 trigramů šifrového textu a jejich identifikace:

| Trigram | Výskytů | Identifikace | Nová přiřazení |
|---------|---------|--------------|----------------|
| **EKJ** | 32 | → **ION** | E=I, K=O, J=N |
| **SEK** | 30 | → **TIO** | S=T ✓, E=I ✓, K=O ✓ |
| **FJS** | 27 | → **ENT** | F=E, J=N ✓, S=T ✓ |
| **AJI** | 25 | → **AND** | A=A, J=N ✓, I=D |
| **ESY** | 18 | → **ITY** | E=I ✓, S=T ✓, Y=Y |
| **QFT** | 17 | → **SEC** | Q=S, F=E ✓, T=C |
| **FTU** | 16 | → **ECU** | F=E ✓, T=C ✓, U=U |
| **TUP** | 16 | → **CUR** | T=C ✓, U=U ✓, P=R |
| **UPE** | 15 | → **URI** | U=U ✓, P=R ✓, E=I ✓ |

Po prvních 9 trigramech bylo přiřazeno 9 písmen: **A=A, E=I, F=E, I=D, J=N, K=O, P=R, Q=S, S=T, T=C, U=U, Y=Y**.

Top 5 bigramů jako doplnění:

| Bigram | Výskytů | Identifikace |
|--------|---------|--------------|
| SE     | 70      | → TI (S=T ✓, E=I ✓) |
| AJ     | 55      | → AN (A=A ✓, J=N ✓) |
| EK     | 49      | → IO (E=I ✓, K=O ✓) |
| KJ     | 47      | → ON (K=O ✓, J=N ✓) |
| FQ     | 42      | → ES (F=E ✓, Q=S ✓) |

#### Krok 3 — Ověření na klíčových slovech

Se získanými přiřazeními byla ověřena a doplněna zbývající písmena rozluštěním konkrétních slov:

| Šifrové slovo | Přeložení dosud zn. písm. | Identifikace | Nová přiřazení |
|---------------|--------------------------|--------------|----------------|
| `QFTUPESY`    | `S_C_R_TY` → **SECURITY** | jistá shoda | P=R ✓, U=U ✓ |
| `EJSFDDELFJTF` | `INT_LL_G_NC_` → **INTELLIGENCE** | jistá shoda | D=L, L=G |
| `SNPFAS`      | `T_?EAT` → **THREAT**      | jistá shoda | N=H |
| `RFNAVEKP`    | `?EHAV_OR` → **BEHAVIOR**  | jistá shoda | R=B, V=V |
| `CEPFWADD`    | `?_RE_ALL` → **FIREWALL**  | jistá shoda | C=F, W=W |
| `HADETEKUQ`   | `?AL_CIOUS` → **MALICIOUS**| jistá shoda | H=M |
| `UJBJKWJ`     | `U_?NO_N` → **UNKNOWN**    | jistá shoda | B=K |
| `OUETBDY`     | `?UICKLY` → **QUICKLY**    | jistá shoda | O=Q |
| `MPFVFJSEKJ`  | `?R_V_NTION` → **PREVENTION** | jistá shoda | M=P |

Písmena G, X, Z se v šifrovém textu vyskytují pouze 1×, 1× a 14× → přiřazena jako G=J, X=X, Z=Z na základě zbytku abecedy.

### Klíč (šifrová abeceda)

Šifrová abeceda seřazená dle otevřené (A–Z):

```
Otevřená:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Šifrová:   A R T I F C L N E G B D H J K M O P Q S U V W X Y Z
```

Mapování šifrová → otevřená:

| Šifrová | Otevřená | Šifrová | Otevřená | Šifrová | Otevřená |
|---------|----------|---------|----------|---------|----------|
| A       | A        | J       | N        | S       | T        |
| B       | K        | K       | O        | T       | C        |
| C       | F        | L       | G        | U       | U        |
| D       | L        | M       | P        | V       | V        |
| E       | I        | N       | H        | W       | W        |
| F       | E        | O       | Q        | X       | X        |
| G       | J        | P       | R        | Y       | Y        |
| H       | M        | Q       | S        | Z       | Z        |
| I       | D        | R       | B        |         |          |

### Výsledek — otevřený text

```
ARTIFICIALINTELLIGENCEISINCREASINGLYUTILIZEDINVARIOUSSECURITYASPECTSTOENHANCE
THREATDETECTIONINCIDENTRESPONSEANDOVERALLCYBERSECURITY
HEREARESOMEKEYWAYSAIISUSEDINSECURITYADVANCEDTHREATDETECTIONANOMALYDETECTIONAI
IDENTIFIESUNUSUALPATTERNSINDICATINGPOTENTIALTHREATSBEHAVIORALANALYTICSMONITORS
USERANDNETWORKBEHAVIORFORSUSPICIOUSACTIVITIESSIGNATURELESSDETECTIONRECOGNIZES
NEWANDUNKNOWNTHREATSBASEDONMALICIOUSBEHAVIORNETWORKPROTECTIONINTRUSIONDETECTION
ANDPREVENTIONAIQUICKLYDETECTSANDRESPONDSTONETWORKINTRUSIONSFIREWALLOPTIMIZATION
ANALYZESNETWORKTRAFFICTOOPTIMIZEFIREWALLRULESANDIDENTIFYVULNERABILITIES...
```

---

## Úloha 2 — Monoalfabetická substituce (Atbash)

### Šifrový text
```
GSRHRHZMFMFHFZOKZIZTIZKSRZNXFIRLFHZHGLQFHGSLDJFRXPOBBLFXZMURMWLFGDSZG...
```

### Postup řešení

**Nástroj:** vlastní implementace (`uloha2.py`)

#### 1. Frekvenční analýza
Délka textu: 906 znaků. Nejčastější písmena šifry:

| Písmeno | Počet | % |
|---------|-------|----|
| G       | 109   | 12.03% |
| R       | 99    | 10.93% |
| L       | 99    | 10.93% |
| Z       | 84    |  9.27% |

Písmeno **V se v šifrovém textu téměř nevyskytuje** (bylo by očekáváno ~1 % pro náhodný text, resp. ~13 % pro E v angličtině). To je první indicie.

#### 2. Identifikace trigramů a vzorů

- `GSR` (14×) → identifikováno jako `THE` (nejčastější anglický trigram)
  → G=T, S=H, R=I *(ale brzy zjištěno: GSR → THIS, tedy R=I, H=S)*
- `GSRH` → `THIS` → potvrzuje G=T, S=H, R=I, H=S
- `GSZG` → `THAT` → Z=A
- `ZMW` (6×) → `AND` → Z=A, M=N, W=D
- `DRGS` → `WITH` → D=W
- `BLF` → `YOU` → B=Y, F=U, L=O
- `KZIZTIZKS` → `PARAGRAPH` → K=P, I=R, T=G
- `FMFHFZO` → `UNUSUAL` → F=U, H=S ✓

Po sestavení celého mapování bylo zjištěno, že **každé písmeno je nahrazeno svým „zrcadlovým" protějškem v abecedě** (A↔Z, B↔Y, C↔X, ..., M↔N).

#### 3. Identifikace šifry — Atbash

Mapování odpovídá **Atbash šifře**:
- Každé písmeno na pozici `i` (0–25) je nahrazeno písmenem na pozici `25 - i`
- A↔Z, B↔Y, C↔X, D↔W, E↔V, F↔U, G↔T, H↔S, I↔R, J↔Q, K↔P, L↔O, M↔N

### Klíč (šifrová abeceda)

```
Otevřená: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Šifrová:  Z Y X W V U T S R Q P O N M L K J I H G F E D C B A
```

Ověření: `is_atbash` = **ANO — všechna mapování odpovídají**.

### Výsledek — otevřený text

```
THISISANUNUSUALPARAGRAPHIAMCURIOUSASTOJUSTHOWQUICKLYYOUCANFINDOUTWHATISSOUNUSUAL
ABOUTITITLOOKSSOORDINARYANDPLAINTHATYOUWOULDTHINKNOTHINGWASWRONGWITHITINFACTNOTHING
ISWRONGWITHITISHIGHLYUNUSUALTHOUGHSTUDYITANDTHINKABOUTITBUTYOUSTILLMAYNOTFINDANYTHING
ODDIFYOUWORKATITABITYOUMIGHTFINDOUTTRYTODOSOWITHOUTANYCOACHINGALTHOUGHITISHIGHLYCOMMON
INPARAGRAPHSATRIALATACCOMPLISHINGSUCHANACCOUNTOFWRITINGISNOTTHATDIFFICULTYOUWOULDWANTTO
KNOWTHATTHISTASKMIGHTOCCUPYMOSTOFYOURBRAINFORHOURSANDASYOUWOTHROUGHTHISACCOUNTITSCOMPO
SITIONWILLLOOKATYPICALINAWAYTHISISSOFORIAMSTRUGGLINGTOATTAINWORDSTHATWOULDIMPARTWHATIWANT
TOSAYANDINDOINGSOIMALSOMISSINGOUTSOMANYWORDSTHATIMUSTDISMISSOWINGTOOURCONDITIONTHATBINDS
THISSOLUTIONNOTWILLINGTOGOONANDONWITHTHISSUPPOSINGLYSILLYANDABSURDPARAGRAPHILLOPTTOPUTAHALT
ATTHISPOINTHAVINGSHOWNPRACTICALLYTHATITISNOTIMPRACTICALTOATTAINAPARAGRAPHWITHOURSYMBOLOF
HIGHLIGHT
```

### Co je neobvyklé na otevřeném textu?

**Otevřený text je LIPOGRAM — záměrně neobsahuje písmeno 'E'.**

Chybějící písmena v otevřeném textu: **E, X, Z**

---

## Úloha 3 — Vigenèrova šifra

### Šifrový text
```
IAKMIIMSSVLIMSLBEEJEKMMMELOAMTLMSKOJXHWKIJYRJXGKMOFHJAISMLGYVIKMJFVMSG...
```

### Postup řešení

**Nástroj:** vlastní implementace (`uloha3.py`)

#### 1. Kasiski test

Hledány opakující se sekvence délky 3–5 a vzdálenosti jejich výskytů.

Nejvýznamnější opakující se sekvence:

| Sekvence | Pozice                  | Vzdálenosti                  |
|----------|-------------------------|------------------------------|
| ESLXV    | [283, 445, 553, 631, 744] | 162, 270, 348, 461, 108, 186, 299, 78 |
| LIMSL    | [10, 166, 1138, 1192]   | 156, 1128, 1182, 972, 1026, 54 |
| SLBEE    | [13, 169, 1141, 1195]   | 156, 1128, 1182, 972, 1026, 54 |

Počty dělitelnosti vzdáleností faktory 2–8:

| Faktor | Počet výskytů |
|--------|--------------|
| 2      | 539×         |
| 3      | 556×         |
| 6      | 517×         |
| 4      | 246×         |

Kasiski test nejsilněji ukazuje na faktor **3** (556×) nebo **6** (517×). GCD vzdáleností sekvencí délky ≥ 4 = 1 (nejednoznačné), ale faktorová analýza favorizuje **6**.

#### 2. Index koincidence (IC)

IC angličtiny ≈ 0,0667; IC náhodného textu ≈ 0,0385.

| Délka klíče | Průměrný IC | Odchylka od 0,0667 |
|-------------|-------------|---------------------|
| 1           | 0,045880    | 0,020820            |
| 2           | 0,049304    | 0,017396            |
| 3           | 0,056599    | 0,010101            |
| 4           | 0,049235    | 0,017465            |
| 5           | 0,045557    | 0,021143            |
| **6**       | **0,067334**| **0,000634**        |
| 7           | 0,045598    | 0,021102            |
| 8           | 0,048869    | 0,017831            |

**Délka klíče = 6** dává IC nejblíže hodnotě pro angličtinu (0,0673 ≈ 0,0667). ✓

#### 3. Chi-kvadrát test

Pro každou ze 6 pozic klíče byl extrahován podtext (každý 6. znak) a testovány všechny posuny 0–25. Nejlepší posun minimalizuje chi-kvadrát statistiku.

| Pozice | Nejlepší posun | Písmeno klíče | χ² hodnota |
|--------|---------------|---------------|------------|
| 0      | 4             | **E**         | 56,55      |
| 1      | 0             | **A**         | 32,34      |
| 2      | 18            | **S**         | 30,90      |
| 3      | 19            | **T**         | 16,02      |
| 4      | 4             | **E**         | 39,91      |
| 5      | 17            | **R**         | 42,51      |

### Klíč

```
EASTER
```

### Výsledek — otevřený text

```
EASTERISACHRISTIANFESTIVALWHICHMARKSTHERESURRECTIONOFJESUSCHRISTFORMANY
CHRISTIANSEASTERISACELEBRATIONOFTHETRIUMPHOFLIFEOVERDEATHANDAVERYIMPORTANT
TIMEOFTHEYEARMANYNONCHRISTIANSALSOHAVEAHOLIDAYATTHISTIMESOITISAPOPULARTIME
TOTRAVELORSPENDWITHFRIENDSANDFAMILYWESEELOTSOFSYMBOLSOFNEWLIFEATEASTERESPECIALLY
EGGSCHICKSFLOWERSANDRABBITSTHESESYMBOLSGOBACKTOANCIENTPAGANTRADITIONSWHICH
CELEBRATEDFERTILITYREBIRTHA NDNEWGROWTHAFTERTHELONGWINTERMONTHSTHEDATESOF
EASTERCHANGEFROMYEARTOYEARBUTIUSUALLYFALLSSOMETIMEBETWEENTHEENDOFMARCHANDTHE
ENDOFAPRILINWESTERNCHRISTIANITYEASTERSUNDAYISTHEFIRSTSUNDAYAFTERTHEFIRSTFULL
MOONOFSPRINGWHICHSTARTSONMARCHTHEEASTERNORTHODOXCHURCHESWHICHUSEADIFFERENT
CALENDARHAVEASLIGHTLYDIFFERENTWAYOFCALCULATINGEASTERANDUSUALLYCELEBRATEEASTER
ALITTLEEARLIERORLATERTHEWEEKBEFOREEASTERISCALLEDHOLYWEEKTHEFIRSTDAYOFHOLYWEE
KISPALMSUNDAYWHICHISTHESUNDAYBEFOREEASTERMANYCHRISTIANSCELEBRATETHISASTHEDAYTHAT
JESUSENTEREDJERUSALEMANDPEOPLETHREWDOWNBRANCHESFROMPA LMTREESONTHEROADTOWELCOME
HIMFOURDAYSLATERISMAUNDYTHURSDAYWHICHMARKSTHELASTSUPPERWHENJESUSATEBREADAND
DRANKWINEWITHHISTWELVEDISCIPLESTHEFOLLOWINGDAYISGOODFRIDAYWHICHISSIGNIFICANT
FORCHRISTIANSASTHEDAYTHATJESUSWASPUTTODEATHONTHECROSSMANYCHRISTIANSBELEVETHAT
JESUSWASKILLEDANDBURIEDINATOMBONTHEFRIDAYANDTHATGODRAISEDHIMFROMTHEDEADONTHE
SUNDAYSOEASTERSUNDAYISACELEBRATIONOFTHERESURRECTIONOFJESUS
```

---

## Úloha 4 — Vernamova šifra (One-time Pad) s opakovaným klíčem

### Zadání

Dva 12-znakové šifrové texty šifrované OTP:

```
C1 = 22 02 0f 1c 0b 1a 1e 0f 1d 08 18 16
C2 = 2c 11 1c 06 14 1b 07 00 00 12 1a 00
```

### Postup řešení

**Nástroj:** vlastní implementace (`uloha4.py`)

#### 1. Rozhodnutí — stejný nebo různý klíč?

Pokud by klíče byly různé (K1 ≠ K2), pak C1 ⊕ C2 = M1 ⊕ M2 ⊕ K1 ⊕ K2, což je kryptograficky nesystematické. Pokud jsou klíče **stejné** (K1 = K2 = K), pak:

```
C1 ⊕ C2 = M1 ⊕ K ⊕ M2 ⊕ K = M1 ⊕ M2
```

Klíče jsou **stejné** — to potvrdí slovníkový útok níže.

#### 2. Eliminace klíče

```
C1 ⊕ C2 = [0x0e, 0x13, 0x13, 0x1a, 0x1f, 0x01, 0x19, 0x0f, 0x1d, 0x1a, 0x02, 0x16]
         = M1 ⊕ M2
```

#### 3. Slovníkový útok (crib dragging)

Ze souboru `dic.txt` načteno **737 slov délky 12**. Pro každé kandidátské slovo M1 ze slovníku:
1. Vypočítáno M2 = M1 ⊕ (C1 ⊕ C2)
2. Ověřeno, zda M2 tvoří pouze alfabetické znaky (a–z, A–Z)
3. Ověřeno, zda M2 (lowercase) je ve slovníku

#### 4. Výsledek

Nalezena jedinečná trojice:

| | Slovo | Hex hodnoty |
|-|-------|-------------|
| **M1** | `accumulative` | `61 63 63 75 6d 75 6c 61 74 69 76 65` |
| **M2** | `opportunists` | `6f 70 70 6f 72 74 75 6e 69 73 74 73` |
| **K**  | `californians` | `43 61 6c 69 66 6f 72 6e 69 61 6e 73` |

### Ověření

```
M1 ⊕ K = C1  →  [0x22, 0x02, 0x0f, 0x1c, 0x0b, 0x1a, 0x1e, 0x0f, 0x1d, 0x08, 0x18, 0x16]  ✓
M2 ⊕ K = C2  →  [0x2c, 0x11, 0x1c, 0x06, 0x14, 0x1b, 0x07, 0x00, 0x00, 0x12, 0x1a, 0x00]  ✓
```

### Závěr

Oba šifrové texty byly zašifrovány **stejným klíčem K = `californians`**.

Opakované použití OTP klíče je nebezpečné, protože:
- C1 ⊕ C2 = M1 ⊕ M2 — útočník bez znalosti klíče získá XOR obou plaintextů
- Slovníkovým útokem pak může rekonstruovat oba plaintexty

---

## Úloha 5 — Sloupcová transpozice (Columnar Transposition)

### Šifrový text
```
IVCTIARJLNKEKCKRNICIDIVAMISVHWEIPIEIANBMOMDTLRRAKIEMTMNOYSNAMEZETOUDGUDTAMCSIOJZUCAB...
```

### Postup řešení

**Nástroj:** vlastní implementace (`uloha5.py`) s ohodnocením českých bigramů

#### 1. Nalezení počtu sloupců

Délka 540 je dělitelná: 3, 4, 5, 6, 9, 10, 12, 15.

Pro každý počet sloupců (3–9) bylo brute-force otestováno všech n! permutací. Každý výsledný text byl ohodnocen skóre na základě **českých bigramů** (bigramy jako NI, JE, PO, ST, RA, TA, OV, KO, VA, ... mají kladné váhy; vzácné bigramy QU, WH, XX mají záporné váhy).

| Počet sloupců | Nejlepší skóre | Permutace         | Začátek textu |
|---------------|---------------|-------------------|---------------|
| 3             | 401,0         | [0, 2, 1]         | ILTVERCIETPOI... |
| 4             | 413,0         | [2, 3, 0, 1]      | YIIYKFVEDOCIEM... |
| **5**         | **719,5**     | **[2, 0, 3, 4, 1]** | **LIDEVEVLACICH...** |
| 6             | 431,0         | [4, 0, 5, 3, 2, 1] | LISYTNEVHKRSIC... |
| 9             | 463,5         | [4, 7, 2, 6, ...]  | OENLUTINMNAEL... |

Počet sloupců **5** jednoznačně vítězí (skóre 719,5 vs. maximum ostatních 463,5).

#### 2. Šifrovací a dešifrovací permutace

- **Šifrovací permutace (klíč):** `[2, 0, 3, 4, 1]`
  - Sloupec 0 originálního textu → pozice 2 v šifře
  - Sloupec 1 → pozice 0
  - Sloupec 2 → pozice 3
  - Sloupec 3 → pozice 4
  - Sloupec 4 → pozice 1

- **Dešifrovací permutace (inverzní):** `[1, 4, 0, 2, 3]`

### Výsledek — otevřený text

```
LIDEVEVLACICHCDSTAHUJIMOCDATOPERATORJENEZLEVNINAOPAKJEOMEZIZAKAZNICICESKYCH
DRAHSENASOCIALNICHSITICHPODIVUJINADZVAZOVANYMOMEZENIMDATSTAHOVANYCHPRESWIFI
VEVLACICHPOPISUJIZKUSENOSTISPOMALYMANESTABILNIMPRIPOJENIMPARADOXNETAKBYLAPOPRENA
ORIGINALNIEKONOMICKATEORIEMINISTRYNEMARTYNOVAKOVEKDYVICESTAZENYCHDATZNAMENAJEJICH
ZLEVNENICOTAMKDOSTAHUJEVZDYTSIGNALFURTPADAAJETOPOMALETOMAMRYCHLEJSIMOBILNIPOPSAL
JEDENZDISKUTUJICICHNAFACEBOOKUUMEALESPONTAKRKAVZDYNEFUNKCNIZNIDALSIKOMENTARNAADRESU
WIFICDOMEZITDATAVICUZTOSNADANINEJDENEPTASERECNICKYDALSICESTUJICIQQ
```