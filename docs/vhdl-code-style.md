## Primjena pravila formatiranja opisa u VHDL jeziku

Opis svakog dizajna u VHDL jeziku treba da bude uniformno stilizovan prema pravilima kursa. Pravila su zasnovana na smjernicama *VHDL coding style* koje su dio [*Open Hardware Repository*](https://gitlab.com/ohwr/project/vhdl-style/-/wikis/home) projekta (dostupne i kao [HTML stranica](https://gitlab.com/ohwr/project/vhdl-style/blob/master/doc/vhdl-coding-style.adoc)), a dopunjena su pravilima alata [*VHDL Style Guide* (VSG)](https://github.com/jeremiah-c-leary/vhdl-style-guide) kojim se stil provjerava. Alat za provjeru stila kursa održava se u zasebnom repozitorijumu [vhdl-style-tools](https://github.com/etf-unibl/vhdl-style-tools). Sva pravila su objedinjena u dokumentu [Pravila stila za VHDL opise](https://github.com/etf-unibl/vhdl-style-tools/blob/v1.1.0/docs/vhdl-style-rules.md) (dostupan i kao [PDF](https://github.com/etf-unibl/vhdl-style-tools/blob/v1.1.0/docs/vhdl-style-rules.pdf)). Ova pravila je potrebno striktno pratiti za svaki modul koji čini neki projekat opisan VHDL jezikom (uključujući *testbench* fajlove).

### Zaglavlje fajla

Jedan od propisanih elemenata, koji se obavezno mora zadovoljiti, je zaglavlje fajla (pravilo `F-03 [FileHeader]`). Zaglavlje treba da ima izgled ekvivalentan zaglavlju datom ispod, s tim da elementi `unit name` i `description` trebaju da budu prilagođeni samom dizajnu:

```
-----------------------------------------------------------------------------
--
-- unit name:     NAND2
--
-- description:
--
--   This file implements a simple NAND2 logic.
--
-----------------------------------------------------------------------------
-- The MIT License
-----------------------------------------------------------------------------
-- Copyright (c) 2026 Faculty of Electrical Engineering
--
-- Permission is hereby granted, free of charge, to any person obtaining a
-- copy of this software and associated documentation files (the "Software"),
-- to deal in the Software without restriction, including without limitation
-- the rights to use, copy, modify, merge, publish, distribute, sublicense,
-- and/or sell copies of the Software, and to permit persons to whom
-- the Software is furnished to do so, subject to the following conditions:
--
-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
-- THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
-- ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
-- OTHER DEALINGS IN THE SOFTWARE
-----------------------------------------------------------------------------
```

**Napomena:** U napomeni o autorskim pravima (`-- Copyright (c) ...`) mora biti upisana **tekuća godina**. Alat odbacuje fajl sa bilo kojom drugom godinom, pa pri preuzimanju fajlova iz ranijih godina (npr. iz video tutorijala) godinu treba ažurirati. Naziv jedinice (`unit name`) mora odgovarati nazivu entiteta (ili paketa) opisanog u fajlu.

### Instalacija alata

Za provjeru stila potrebni su [*Python*](https://www.python.org/downloads/) (verzija 3.8 ili novija) i [*Git*](https://git-scm.com/downloads). Alat se instalira iz foldera repozitorijuma kursa (uz pretpostavku da smo otvorili *Command Prompt*, *PowerShell* ili terminal u tom folderu):

```
python -m pip install -r requirements.txt
```

Fajl `requirements.txt` sadrži verziju alata `vhdl-style-tools` koja se koristi u kursu; *pip* ga preuzima sa *GitHub* platforme zajedno sa alatom VSG i instalira komandu `vhdl-style`. Na *Linux* i *macOS* platformama umjesto `python` se obično koristi `python3`. Ako ne želite da instalirate pakete u sistemsku *Python* instalaciju, možete prethodno napraviti i aktivirati virtuelno okruženje:

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

(na *Linux* i *macOS* platformama okruženje se aktivira komandom `source .venv/bin/activate`). Komanda `vhdl-style` je dostupna samo u okruženju u kojem je alat instaliran, pa virtuelno okruženje treba aktivirati u svakom novom terminalu.

Opciono, ako je instaliran simulator [GHDL](https://github.com/ghdl/ghdl), alat dodatno provjerava da li su opisi u skladu sa standardom VHDL-2008 (pravilo `S-01 [VHDLVersion]`). Na *GitHub* platformi ova provjera se izvršava uvijek.

### Provjera stila

Provjera se pokreće iz foldera repozitorijuma kursa komandom `vhdl-style`, kojoj se prosljeđuje broj zadatka (iz *GitHub* platforme). Komanda provjerava sve `.vhd` fajlove u folderu `assignments/<broj_zadatka>`. Na primjer, za zadatak čiji je broj 55:

```
vhdl-style 55
```

Umjesto broja zadatka može se navesti i putanja do foldera ili do pojedinačnih fajlova:

```
vhdl-style assignments/55
vhdl-style assignments/55/nand2.vhd
```

Ako komanda `vhdl-style` nije pronađena (npr. folder sa *Python* skriptama nije u putanji), ista provjera se pokreće i sa `python -m vhdl_style_tools 55`.

Za svaki fajl alat ispisuje pronađene greške u obliku `fajl:linija: pravilo -- opis`, na primjer:

```
==> assignments\55\counter_ctrl.vhd: 5 violation(s)
  assignments\55\counter_ctrl.vhd:12: pds_001 -- [FileHeader] header line 12: copyright year 2025 must be the current year 2026
  assignments\55\counter_ctrl.vhd:43: entity_017 -- Move : 2 columns
  assignments\55\counter_ctrl.vhd:43: pds_015 -- [PortsName] in port 'en' must end with '_i'
  assignments\55\counter_ctrl.vhd:43: port_025 -- Suffix en with one of the following: _i, _o, _b
  assignments\55\counter_ctrl.vhd:79: if_002 -- Remove enclosing ()'s

1 file(s) checked, 5 violation(s).
Rules: https://github.com/etf-unibl/vhdl-style-tools/blob/v1.1.0/docs/vhdl-style-rules.en.md
Hint: many violations can be fixed automatically with --fix.
```

Oznaka pravila (npr. `port_025` ili `pds_001`) može se potražiti u dokumentu [Pravila stila za VHDL opise](https://github.com/etf-unibl/vhdl-style-tools/blob/v1.1.0/docs/vhdl-style-rules.md). Pravila čija oznaka počinje sa `pds_` su pravila kursa, a njihov opis počinje nazivom OHWR pravila u uglastim zagradama (npr. `[FileHeader]`). Oznake ostalih pravila su oznake VSG pravila, detaljno opisanih (sa primjerima) u [VSG dokumentaciji](https://vhdl-style-guide.readthedocs.io/en/latest/rules.html).

### Automatska ispravka

Veliki dio grešaka (uvlačenje, razmaci, prazne linije, velika i mala slova, završeci linija, ...) alat može da ispravi automatski:

```
vhdl-style --fix 55
```

Opcija `--fix` **mijenja fajlove**, pa je preporučljivo da prije toga komitujete (ili sačuvate kopiju) svoje izmjene. Poslije ispravke alat ponovo provjerava fajlove i ispisuje greške koje je potrebno ispraviti ručno (npr. zaglavlje, nazivi signala i portova). Kako se ispravke izvršavaju u fazama, preporučuje se da se provjera ponovi dok ne prođe bez grešaka.

### Provjera na *GitHub* platformi

Prilikom otvaranja ili ažuriranja *pull request*-a, *GitHub Actions* automatski pokreće istu provjeru za zadatak čiji je broj naveden u naslovu *pull request*-a (npr. `Issue #55 : Create NAND2 circuit`). Greške se prikazuju u izvještaju posla `linter`, a označene su i direktno u pregledu izmijenjenih fajlova (*Files changed*). Provjera stila mora da prođe bez grešaka prije nego što se *pull request* prihvati.

### Završeci linija

Pravilom `F-05 [EndOfLine]` propisano je da se svaka linija završava samo `<LF>` karakterom (*Unix* konvencija), dok *Windows* konvencija podrazumijeva kombinaciju karaktera `<CR><LF>`. Repozitorijum sadrži fajl `.gitattributes` koji *Git* alatu nalaže da u repozitorijum upisuje fajlove sa `<LF>` završecima linija i da ih takve i preuzima, bez obzira na podešavanje `core.autocrlf`. Pored toga:

- opcija `--fix` pretvara `<CR><LF>` završetke u `<LF>`,
- repozitorijum sadrži i fajl `.editorconfig`, koji editori sa podrškom za [EditorConfig](https://editorconfig.org) (npr. *IntelliJ*, a *VS Code* i *Notepad++* uz odgovarajući dodatak) koriste da automatski podese `<LF>` završetke, uvlačenje od dva razmaka i uklanjanje razmaka na kraju linija,
- u editoru *Notepad++* završeci linija se mogu promijeniti i ručno, u meniju **Edit&rarr;EOL Conversion&rarr;Unix (LF)**.

Više o drugim opcijama konfiguracije, možete pročitati u dokumentu [GitHub line endings configuration](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings).
