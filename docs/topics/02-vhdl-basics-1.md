## 2. Osnove VHDL jezika (prvi dio)

**Video:** [Osnove VHDL jezika (prvi dio)](https://www.youtube.com/watch?v=-5Q7YpQmU40) (48:25) · **Kod:** [`video-tutorials/part-1/video-tutorial-02`](../../video-tutorials/part-1/video-tutorial-02) · **Vezana uputstva:** [Instalacija alata](../tools-setup.md), [Simulacija i testiranje](../simulation-and-testing.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:38](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=38s) | Preuzimanje i instalacija alata *Quartus Prime Lite* |
| [02:34](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=154s) | Kreiranje projekta (*New Project Wizard*) i izbor FPGA čipa |
| [05:18](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=318s) | Primjer: detektor parnog broja jedinica (*even detector*) |
| [07:13](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=433s) | Novi VHDL fajl, šabloni (*Insert Template*), biblioteke i paketi |
| [10:51](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=651s) | Tipovi `std_logic` i `std_logic_vector` i devet vrijednosti |
| [14:08](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=848s) | Entitet: generici i portovi |
| [16:48](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1008s) | Arhitektura i signali |
| [19:48](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1188s) | Konkurentne naredbe: opis sumom proizvoda |
| [24:47](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1487s) | Druga arhitektura istog entiteta (XOR) |
| [27:20](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1640s) | *Top-level* entitet, faze kompilacije |
| [31:07](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1867s) | Izvještaj o kompilaciji i *RTL Viewer* |
| [32:47](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=1967s) | Koja arhitektura se sintetiše |
| [33:33](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=2013s) | Izbor arhitekture konfiguracijom |
| [36:13](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=2173s) | *Cross-probing*: od prikaza do koda i čipa |
| [37:34](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=2254s) | Strukturni opis: komponente i instance |
| [47:12](https://www.youtube.com/watch?v=-5Q7YpQmU40&t=2832s) | Zaključak |

### Ključni pojmovi

- **Entitet** (`entity`) - interfejs dizajna: naziv, generici i portovi.
- **Arhitektura** (`architecture`) - implementacija (funkcionalnost) entiteta; jedan entitet može imati više arhitektura.
- **Port** - priključak entiteta sa smjerom (`in`, `out`, `inout`) i tipom.
- **Generik** (`generic`) - konstanta kojom se entitet parametrizuje (npr. širina magistrale).
- **Signal** - interna veza unutar arhitekture; nema smjer, pa se može i čitati i dodjeljivati.
- **`std_logic` / `std_logic_vector`** - tip sa devet vrijednosti iz paketa `ieee.std_logic_1164` i vektor takvih vrijednosti.
- **Konkurentna naredba** - naredba u tijelu arhitekture; sve se izvršavaju istovremeno, nezavisno od redoslijeda u kodu.
- **Strukturni opis** - opis dizajna povezivanjem instanci komponenti (`component`, `port map`).
- **Konfiguracija** (`configuration`) - deklaracija kojom se bira arhitektura entiteta.
- **Biblioteka `work`** - biblioteka u koju se prevode fajlovi trenutnog projekta; uključena je podrazumijevano.

### Objašnjenje

#### Projekat u alatu Quartus

Projekat se pravi opcijom **File &rarr; New Project Wizard** (prazan projekat). Najvažniji korak je izbor čipa: za ploču DE1-SoC to je Cyclone V **5CSEMA5F31C6** (može se izabrati preko kartice *Board*). Simulator se može podesiti i kasnije, u podešavanjima projekta. Novi VHDL fajl dodaje se opcijom **File &rarr; New &rarr; VHDL File**; fajl se čuva pod nazivom entiteta. Šabloni jezičkih konstrukcija dostupni su u **Edit &rarr; Insert Template &rarr; VHDL**.

> **Napomena:** Verzija alata i adresa za preuzimanje prikazane u videu su zastarjele. Aktuelna uputstva su u dokumentu [Instalacija alata](../tools-setup.md). Na kursu se koristi standard VHDL-2008, koji se bira u podešavanjima projekta (**Assignments &rarr; Settings &rarr; Compiler Settings &rarr; VHDL Input**).

#### Tip `std_logic`

Paket `ieee.std_logic_1164` definiše tip `std_logic` sa devet vrijednosti:

| Vrijednost | Značenje |
| :---: | ------ |
| `'0'`, `'1'` | jaka nula i jaka jedinica |
| `'L'`, `'H'` | slaba nula i slaba jedinica (npr. *pull-down* i *pull-up* otpornik) |
| `'X'`, `'W'` | jaka i slaba nepoznata vrijednost (konflikt dvije vrijednosti iste jačine) |
| `'Z'` | visoka impedansa |
| `'U'` | neinicijalizovana vrijednost (početna vrijednost u simulaciji) |
| `'-'` | *don't care* (vrijednost nije bitna) |

Vrijednosti `'U'`, `'X'` i `'W'` imaju smisla samo u simulaciji: fizički konflikt na liniji ne daje "nepoznatu" vrijednost, već može oštetiti komponente. Vektori se tipično deklarišu od najvišeg ka najnižem bitu, npr. `std_logic_vector(2 downto 0)`.

#### Entitet i arhitektura

Detektor parnog broja jedinica ima trobitni ulaz `a` i izlaz `even`, koji je `'1'` kada `a` sadrži paran broj jedinica (nula jedinica se smatra parnim brojem):

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity even_detector is
  port
  (
    a    : in  std_logic_vector(2 downto 0);
    even : out std_logic
  );
end even_detector;
```

Posljednji port u listi se ne završava tačkom-zarezom. Arhitektura sadrži deklaracije (npr. signala) prije `begin` i naredbe poslije njega. Opis sumom proizvoda (`sop_arch`) prepisuje tablicu istinitosti, sa jednim signalom za svaki proizvod:

```vhdl
architecture sop_arch of even_detector is
  signal p1, p2, p3, p4 : std_logic;
begin
  even <= (p1 or p2) or (p3 or p4);
  p1 <= (not a(2)) and (not a(1)) and (not a(0));
  p2 <= (not a(2)) and a(1) and a(0);
  p3 <= a(2) and (not a(1)) and a(0);
  p4 <= a(2) and a(1) and (not a(0));
end sop_arch;
```

Ovo su konkurentne naredbe: izvršavaju se istovremeno, pa njihov redoslijed u kodu nije bitan (`even` se može dodijeliti prije signala `p1`-`p4`). VHDL ne razlikuje velika i mala slova.

#### Više arhitektura i konfiguracija

Isti entitet može imati više arhitektura. Druga arhitektura koristi činjenicu da je XOR svih bita detektor neparnog broja jedinica:

```vhdl
architecture xor_arch of even_detector is
  signal odd : std_logic;
begin
  odd <= a(2) xor a(1) xor a(0);
  even <= not odd;
end xor_arch;
```

Kada entitet ima više arhitektura, alat za sintezu podrazumijevano koristi posljednju prevedenu. Željena arhitektura se bira konfiguracijom (konvencija za naziv je `<entitet>_cfg`):

```vhdl
configuration even_detector_cfg of even_detector is
  for sop_arch
  end for;
end even_detector_cfg;
```

#### Strukturni opis

Strukturni opis povezuje instance komponenti, kao šema. Komponente `xor2` i `not1` su posebni entiteti (fajlovi [`xor2.vhd`](../../video-tutorials/part-1/video-tutorial-02/xor2.vhd) i [`not1.vhd`](../../video-tutorials/part-1/video-tutorial-02/not1.vhd)). U arhitekturi se prvo deklarišu komponente (kao entitet, uz ključnu riječ `component`), a zatim se u tijelu instanciraju sa nazivom instance i mapiranjem portova (`port map`, operator `=>`):

```vhdl
architecture str_arch of even_detector is
  component xor2
    port(
      i1, i2 : in std_logic;
      o1 : out std_logic
    );
  end component;
  component not1
    port(
      i1 : in std_logic;
      o1 : out std_logic
    );
  end component;
  signal s1, s2 : std_logic;
begin
  u1: xor2
    port map(i1 => a(0), i2 => a(1), o1 => s1);
  u2: xor2
    port map(i1 => a(2), i2 => s1, o1 => s2);
  u3: not1
    port map(i1 => s2, o1 => even);
end str_arch;
```

Strukturni opis je opširniji od crtanja šeme, ali omogućava da se složen dizajn podijeli na manje funkcionalne jedinice, od kojih se svaka opisuje zasebno.

#### Kompilacija i pregled rezultata

**Processing &rarr; Start Compilation** pokreće sve faze (analiza i sinteza, *Fitter*, *Assembler*, vremenska analiza); dvoklikom na jednu fazu u prozoru *Tasks* pokreće se samo ona. Entitet koji se sintetiše mora biti postavljen kao *top-level* (desni klik na fajl ili entitet). U izvještaju (*Compilation Report*) vidi se iskorišćenost resursa (za ovaj primjer jedan ALM i četiri pina), a **Tools &rarr; Netlist Viewers &rarr; RTL Viewer** prikazuje sintetizovanu logiku. Iz prikaza se opcijom *Locate Node* može preći na mjesto u kodu ili u *Chip Planner*-u (*cross-probing*).

### Primjer

Folder [`video-tutorials/part-1/video-tutorial-02`](../../video-tutorials/part-1/video-tutorial-02) sadrži `even_detector.vhd` (arhitekture `xor_arch`, `sop_arch`, `str_arch` i konfiguraciju), `xor2.vhd` i `not1.vhd`. Provjera sintakse i elaboracija (komponente se prevode prije entiteta koji ih koristi):

```
ghdl -a --std=08 xor2.vhd not1.vhd even_detector.vhd
ghdl -e --std=08 even_detector_cfg
```

U alatu *Quartus* napravite projekat sa sva tri fajla, mijenjajte arhitekturu u konfiguraciji i uporedite prikaze u *RTL Viewer*-u: dva I/ILI nivoa za `sop_arch`, XOR i invertor za `xor_arch`, tri instance za `str_arch`.

### Česte greške

- **Tačka-zarez iza posljednjeg porta** ili nedostaje tačka-zarez iza ostalih portova.
- **Dvije arhitekture sa istim nazivom** (npr. nakon kopiranja koda): prevođenje ne uspijeva.
- **Očekivanje da se sintetiše prva arhitektura u fajlu**: bez konfiguracije alat koristi posljednju prevedenu.
- **Pogrešan čip u projektu**: za DE1-SoC mora biti 5CSEMA5F31C6, inače raspored pinova i sinteza ne odgovaraju ploči.
- **Fajl sačuvan pod nazivom koji ne odgovara entitetu**: pravila kursa zahtijevaju da se fajl zove kao entitet.
- **Pogrešno mapiranje portova u `port map`**: smjer i redoslijed se lako zamijene; koristite imenovano mapiranje (`port => signal`).
- **Shvatanje konkurentnih naredbi kao sekvencijalnih**: redoslijed u tijelu arhitekture ne utiče na rezultat.

### Provjera znanja

1. Koja je razlika između entiteta i arhitekture i zašto jedan entitet može imati više arhitektura?
2. Kada nastaju vrijednosti `'X'` i `'W'` tipa `std_logic` i da li postoje u stvarnom kolu?
3. Po čemu se signal razlikuje od porta?
4. Zašto redoslijed konkurentnih naredbi u arhitekturi ne utiče na rezultat?
5. Kako se bira arhitektura koja se sintetiše kada entitet ima više arhitektura?

<details>
<summary>Odgovori</summary>

1. Entitet opisuje interfejs (portove), a arhitektura implementaciju; isti interfejs se može realizovati na više načina (npr. sumom proizvoda, XOR kolima ili strukturno).
2. Kada se na istoj liniji nađu dvije različite vrijednosti iste jačine (`'0'` i `'1'` daju `'X'`, `'L'` i `'H'` daju `'W'`); postoje samo u simulaciji.
3. Port je dio interfejsa i ima smjer (`in`, `out`, `inout`); signal je interna veza bez smjera, koja se može i čitati i dodjeljivati.
4. Konkurentne naredbe opisuju hardver koji radi istovremeno; svaka se ponovo izračunava kada se promijeni neki signal od kojeg zavisi.
5. Konfiguracijom (`configuration ... for <arhitektura> end for;`); bez nje alat koristi posljednju prevedenu arhitekturu.

</details>

### Dodatni materijali

- Prethodni video: [1. Uvod u FPGA tehnologiju](https://www.youtube.com/watch?v=oJSAv1hhdgk)
- Sljedeći video: [3. Osnove VHDL jezika (drugi dio)](https://www.youtube.com/watch?v=-MCetuywNN4)
- Kratke teme: [VHDL configuration](https://www.youtube.com/watch?v=DP7kfX050V4), [Quartus Schematic Capture](https://www.youtube.com/watch?v=zBnPPxa0-Hw)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
