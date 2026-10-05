## 4. Programiranje ciljne FPGA platforme

**Video:** [Programiranje ciljne FPGA platforme](https://www.youtube.com/watch?v=D-kIoQWeO_E) (12:17) · **Kod:** - (koristi se primjer iz [videa 2](02-vhdl-basics-1.md)) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md#testiranje-na-evaluacionoj-ploči), [Instalacija alata](../tools-setup.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:00](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=0s) | Razvojna ploča DE1-SoC i njene periferije |
| [00:54](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=54s) | Povezivanje ploče: napajanje, *USB-Blaster* priključak, prekidač za način programiranja |
| [02:53](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=173s) | Primjer: detektor parnog broja jedinica |
| [03:23](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=203s) | Dodjela pinova: prekidači i LED diode iz korisničkog uputstva |
| [05:25](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=325s) | *Pin Planner* i ponovno prevođenje |
| [07:50](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=470s) | *Programmer*: izbor hardvera, JTAG, fajl `.sof` |
| [10:00](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=600s) | Testiranje na ploči |
| [10:38](https://www.youtube.com/watch?v=D-kIoQWeO_E&t=638s) | Uvoz dodjele pinova iz fajla |

### Ključni pojmovi

- **DE1-SoC** - razvojna ploča kursa sa čipom Cyclone V (5CSEMA5F31C6) i periferijama: prekidači, tasteri, LED diode, sedmosegmentni displeji, memorija, VGA, USB, PS/2, GPIO konektori.
- **USB-Blaster** - interfejs za programiranje FPGA preko USB kabla; na ploči je priključak označen sa *USB Blaster*.
- **Dodjela pinova** (*pin assignment*) - povezivanje portova *top-level* entiteta sa fizičkim pinovima čipa.
- **Pin Planner** - alat u *Quartus*-u za ručnu dodjelu pinova (**Assignments &rarr; Pin Planner**).
- **JTAG** - standardni interfejs preko kojeg se čip programira.
- **Fajl `.sof`** (*SRAM Object File*) - konfiguracioni fajl koji generiše *Assembler*, u folderu `output_files` projekta.

### Objašnjenje

#### Povezivanje ploče

Ploča se napaja preko posebnog priključka i uključuje prekidačem za napajanje. Za programiranje se USB kabl povezuje na priključak označen sa *USB Blaster* (ne na ostale USB priključke). Pri prvom povezivanju instaliraju se USB drajveri (vidi [Instalacija alata](../tools-setup.md)). Na ploči postoji prekidač kojim se bira da li se FPGA programira iz alata *Quartus* (JTAG) ili iz Linux-a koji radi na HPS procesoru; podesite ga prema korisničkom uputstvu ploče (*DE1-SoC User Manual*).

#### Dodjela pinova

Nakon uspješne sinteze, portovi entiteta se povezuju sa pinovima na koje su vezane periferije. Lokacije pinova nalaze se u korisničkom uputstvu ploče. Za detektor parnog broja jedinica ulazi `a(0)`-`a(2)` vežu se na prekidače `SW0`-`SW2`, a izlaz `even` na crvenu LED diodu `LEDR0`:

| Port | Periferija | Pin |
| ------ | ------ | ------ |
| `a(0)` | `SW[0]` | `PIN_AB12` |
| `a(1)` | `SW[1]` | `PIN_AC12` |
| `a(2)` | `SW[2]` | `PIN_AF9` |
| `even` | `LEDR[0]` | `PIN_V16` |

U **Assignments &rarr; Pin Planner** za svaki port se u koloni *Location* upiše pin. Dodjela se primjenjuje tek nakon ponovnog prevođenja (**Processing &rarr; Start Compilation**); tada se u koloni *Fitter Location* vidi da je *Fitter* povezao portove sa zadatim pinovima.

Pinovi najčešće korišćenih periferija (iz fajla [`DE1_SoC_pin_assigments.csv`](../../video-tutorials/part-2/video-tutorial-07/DE1_SoC_pin_assigments.csv)):

| Periferija | Pinovi |
| ------ | ------ |
| `SW[0]`-`SW[9]` | AB12, AC12, AF9, AF10, AD11, AD12, AE11, AC9, AD10, AE12 |
| `KEY[0]`-`KEY[3]` | AA14, AA15, W15, Y16 |
| `LEDR[0]`-`LEDR[9]` | V16, W16, V17, V18, W17, W19, Y19, W20, W21, Y21 |
| `HEX0[0]`-`HEX0[6]` | AE26, AE27, AE28, AG27, AF28, AG28, AH28 |
| `CLOCK_50` | AF14 |

Tasteri `KEY` i segmenti sedmosegmentnih displeja su aktivni na nuli (pritisnut taster daje `'0'`, segment svijetli za `'0'`).

#### Programiranje

1. Otvorite **Tools &rarr; Programmer**. Ako piše *No Hardware*, uključite ploču, kliknite **Hardware Setup** i izaberite *DE-SoC [USB-1]*.
2. Mod je **JTAG**. Kliknite **Auto Detect** i izaberite čip 5CSEMA5 (u lancu su dva uređaja: FPGA i HPS; programira se FPGA).
3. Za FPGA uređaj izaberite fajl (**Change File**) `output_files/<projekat>.sof`.
4. Označite **Program/Configure** i kliknite **Start**.

Nakon programiranja dizajn odmah radi: za detektor, `LEDR0` svijetli kada je uključen paran broj prekidača `SW0`-`SW2` (i kada nijedan nije uključen).

#### Uvoz dodjele pinova iz fajla

Ručna dodjela je spora i podložna greškama za veći broj pinova. Brže je uvesti gotov fajl sa dodjelom svih periferija ploče (**Assignments &rarr; Import Assignments**), što je prikazano u [videu 7](https://www.youtube.com/watch?v=xWWVBNAbvGg). Uslov je da se portovi *top-level* entiteta zovu kao periferije u fajlu (npr. `SW`, `KEY`, `LEDR`, `HEX0`).

> **Napomena:** U videu se fajl sa dodjelom pinova naziva Excel fajl; to je CSV fajl (vrijednosti razdvojene zarezima) u formatu koji *Quartus* uvozi, koji se može otvoriti i u Excel-u.

### Primjer

Testiranje dizajna iz [videa 2](02-vhdl-basics-1.md) na ploči:

1. Napravite projekat sa fajlovima iz [`video-tutorials/part-1/video-tutorial-02`](../../video-tutorials/part-1/video-tutorial-02) za čip 5CSEMA5F31C6 i izaberite arhitekturu u konfiguraciji.
2. Pokrenite **Analysis & Synthesis**, a zatim u *Pin Planner*-u dodijelite pinove prema tabeli iznad.
3. Pokrenite kompletno prevođenje i provjerite kolonu *Fitter Location*.
4. Programirajte ploču i provjerite rad za svih osam kombinacija prekidača.

Za vježbu proširite ulaz na prekidače `SW0`-`SW3` (četvorobitni ulaz) ili dodajte izlaz detektora neparnog broja jedinica na `LEDR1`.

### Česte greške

- **USB kabl na pogrešnom priključku**: za programiranje se koristi priključak *USB Blaster*.
- **Prekidač za način programiranja u pogrešnom položaju**: *Programmer* ne vidi FPGA; podesite ga prema korisničkom uputstvu.
- **Programiranje bez ponovnog prevođenja** nakon izmjene pinova: dodjela važi tek nakon kompilacije.
- **Pogrešan uređaj u lancu**: nakon *Auto Detect* fajl se dodjeljuje FPGA čipu (5CSEMA5), ne HPS-u.
- **Nedodijeljeni pinovi**: *Quartus* ih raspoređuje sam, pa dizajn radi na pogrešnim pinovima; provjerite upozorenja o pinovima u izvještaju.
- **Zaboravljena aktivna nula**: tasteri `KEY` daju `'0'` kada su pritisnuti, a segmenti displeja svijetle za `'0'`.

### Provjera znanja

1. Na koji priključak ploče se povezuje USB kabl za programiranje i šta još treba podesiti na ploči?
2. Gdje se nalaze lokacije pinova periferija i kako se dodjeljuju u alatu *Quartus*?
3. Zašto je nakon dodjele pinova potrebno ponovo prevesti dizajn?
4. Koji fajl se učitava u FPGA i gdje se nalazi?
5. Šta je uslov za uvoz dodjele pinova iz gotovog fajla?

<details>
<summary>Odgovori</summary>

1. Na priključak *USB Blaster*; prekidač za način programiranja treba podesiti tako da se FPGA programira iz alata *Quartus* (JTAG).
2. U korisničkom uputstvu ploče (i u fajlu sa dodjelom pinova kursa); dodjeljuju se u *Pin Planner*-u (kolona *Location*) ili uvozom fajla.
3. Dodjela pinova je ograničenje za *Fitter*; raspored na pinove se primjenjuje tek pri ponovnom razmještanju i povezivanju.
4. Fajl `.sof` koji generiše *Assembler*, u folderu `output_files` projekta.
5. Portovi *top-level* entiteta moraju se zvati kao periferije u fajlu (npr. `SW`, `LEDR`).

</details>

### Dodatni materijali

- Prethodni video: [3. Osnove VHDL jezika (drugi dio)](https://www.youtube.com/watch?v=-MCetuywNN4)
- Sljedeći video: [5. Sekvencijalne VHDL naredbe](https://www.youtube.com/watch?v=oH_dKclt0WU)
- [7. Dodjeljivanje pinova (alternativni način)](https://www.youtube.com/watch?v=xWWVBNAbvGg)
- Kratke teme: [chip_pin synthesis attribute](https://www.youtube.com/watch?v=wc1b0oMM1H8), [Programming the device from Linux on HPS](https://www.youtube.com/watch?v=SP8fCZdNxkE)
- [DE1-SoC: dokumentacija proizvođača](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=167&No=836&PartNo=4) (korisničko uputstvo, *System Builder*)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
