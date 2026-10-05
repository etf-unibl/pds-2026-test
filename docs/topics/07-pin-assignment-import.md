## 7. Dodjeljivanje pinova (alternativni način)

**Video:** [Dodjeljivanje pinova (alternativni način)](https://www.youtube.com/watch?v=xWWVBNAbvGg) (10:12) · **Kod:** [`video-tutorials/part-2/video-tutorial-07`](../../video-tutorials/part-2/video-tutorial-07) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md#testiranje-na-evaluacionoj-ploči), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:17](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=17s) | Fajl `.qsf` i naredbe `set_location_assignment` |
| [01:29](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=89s) | *Export Assignments* |
| [01:46](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=106s) | CSV fajl sa pinovima ploče |
| [02:20](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=140s) | *Import Assignments* |
| [03:14](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=194s) | Usklađivanje naziva portova sa nazivima iz fajla |
| [03:51](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=231s) | Vektor dužine jedan: `std_logic_vector(0 downto 0)` |
| [05:14](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=314s) | Interni signali umjesto preimenovanja u cijelom kodu |
| [07:09](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=429s) | Kompilacija i provjera u *Pin Planner*-u |
| [07:51](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=471s) | Zaostale dodjele koje *Fitter* ignoriše |
| [09:19](https://www.youtube.com/watch?v=xWWVBNAbvGg&t=559s) | Tcl naredbe u `.qsf` fajlu |

### Ključni pojmovi

- **Fajl `.qsf`** (*Quartus Settings File*) - tekstualni fajl sa podešavanjima projekta, uključujući dodjelu pinova.
- **`set_location_assignment`** - Tcl naredba u `.qsf` fajlu koja dodjeljuje pin portu, npr. `set_location_assignment PIN_AB12 -to SW[0]`.
- **Import Assignments** - uvoz dodjela (npr. pinova) iz CSV ili `.qsf` fajla (**Assignments &rarr; Import Assignments**).
- **Export Assignments** - izvoz dodjela projekta radi korišćenja u drugim projektima.
- **CSV fajl sa pinovima** - tabela sa kolonama `To` (naziv signala) i `Location` (pin).
- **Tcl** - skript jezik koji koriste alati za projektovanje FPGA sistema, uključujući *Quartus*.

### Objašnjenje

#### Gdje se čuva dodjela pinova

Pinovi dodijeljeni u *Pin Planner*-u ([video 4](04-programming-the-board.md)) upisuju se u fajl `<projekat>.qsf` u folderu projekta, kao Tcl naredbe:

```
set_location_assignment PIN_AB12 -to a[0]
set_location_assignment PIN_V16 -to even
```

Fajl se može otvoriti u tekstualnom editoru; dodjele se mogu i izvesti (**Assignments &rarr; Export Assignments**) i koristiti u drugim projektima.

#### Uvoz pinova iz CSV fajla

Fajl [`DE1_SoC_pin_assigments.csv`](../../video-tutorials/part-2/video-tutorial-07/DE1_SoC_pin_assigments.csv) sadrži lokacije svih periferija ploče DE1-SoC: `SW[0]`-`SW[9]`, `KEY[0]`-`KEY[3]`, `LEDR[0]`-`LEDR[9]`, `HEX0`-`HEX5` (po sedam segmenata), `CLOCK_50`, `GPIO_0`, `GPIO_1` i druge. Uvozi se preko **Assignments &rarr; Import Assignments**; preporučuje se opcija za rezervnu kopiju postojećih dodjela.

Uvoz sam po sebi ne povezuje dizajn sa periferijama: *Fitter* koristi samo dodjele čiji naziv odgovara nazivu porta *top-level* entiteta. Zato portovi moraju da se zovu kao u fajlu, npr. `SW` i `LEDR`, a ne `a` i `even`.

#### Usklađivanje naziva portova

U fajlu su `SW` i `LEDR` vektori, pa i portovi moraju biti vektori. Za jednu LED diodu koristi se vektor dužine jedan, `std_logic_vector(0 downto 0)`. On nosi istu informaciju kao `std_logic`, ali to su **različiti tipovi**: `LEDR <= even;` je greška, a ispravno je `LEDR(0) <= even;`.

Da ne bi mijenjali nazive u cijeloj arhitekturi, portovi se preimenuju, a stari nazivi postaju interni signali povezani sa portovima:

```vhdl
entity even_detector is
  port
  (
    SW   : in  std_logic_vector(2 downto 0);
    LEDR : out std_logic_vector(0 downto 0)
  );
end even_detector;

architecture sop_arch of even_detector is
  signal a : std_logic_vector(2 downto 0);
  signal even : std_logic;
  signal p1, p2, p3, p4 : std_logic;
begin
  a <= SW;
  LEDR(0) <= even;
  even <= (p1 or p2) or (p3 or p4);
  p1 <= (not a(2)) and (not a(1)) and (not a(0));
  p2 <= (not a(2)) and a(1) and a(0);
  p3 <= a(2) and (not a(1)) and a(0);
  p4 <= a(2) and a(1) and (not a(0));
end sop_arch;
```

Dodjele `a <= SW;` i `LEDR(0) <= even;` su samo veze (žice) i ne dodaju logiku.

#### Provjera nakon kompilacije

U *Pin Planner*-u se nakon kompilacije vidi da su `SW[0]`-`SW[2]` (*Input*) i `LEDR[0]` (*Output*) povezani na `PIN_AB12`, `PIN_AC12`, `PIN_AF9` i `PIN_V16`. Ostale uvezene periferije (npr. `SW[3]`) imaju smjer *Unknown*: nisu portovi dizajna, pa ih *Fitter* ignoriše. Isto važi za zaostale ručne dodjele starih portova (`a[0]`, `even`); mogu ostati u `.qsf` fajlu ili se obrisati.

### Primjer

1. Otvorite projekat detektora iz [videa 4](04-programming-the-board.md) i uvezite [`DE1_SoC_pin_assigments.csv`](../../video-tutorials/part-2/video-tutorial-07/DE1_SoC_pin_assigments.csv) (**Assignments &rarr; Import Assignments**).
2. Preimenujte portove u `SW` i `LEDR` kao u primjeru iznad i prevedite dizajn.
3. U *Pin Planner*-u i u izvještaju *Fitter*-a provjerite lokacije pinova, pa programirajte ploču.
4. Otvorite `.qsf` fajl u tekstualnom editoru i pronađite naredbe `set_location_assignment`.

### Česte greške

- **Port se ne zove kao u fajlu** (npr. `sw` umjesto `SW` nije problem jer VHDL ne razlikuje velika i mala slova, ali `switch` jeste): pin ostaje nedodijeljen i *Fitter* ga sam raspoređuje.
- **`std_logic` umjesto vektora** za `LEDR`: naziv u fajlu je `LEDR[0]`, pa port mora biti vektor.
- **Dodjela `std_logic` vrijednosti vektoru** (`LEDR <= even;`): različiti tipovi; koristite `LEDR(0)`.
- **Očekivanje da uvoz mijenja dizajn**: uvoz samo dodaje dodjele; dizajn mora koristiti iste nazive.

### Provjera znanja

1. Gdje *Quartus* čuva dodjelu pinova i u kom obliku?
2. Šta je uslov da *Fitter* iskoristi pin uvezen iz CSV fajla?
3. Zašto `LEDR <= even;` ne prolazi analizu ako je `LEDR` tipa `std_logic_vector(0 downto 0)`?
4. Zašto se uvode interni signali `a` i `even` umjesto preimenovanja u cijeloj arhitekturi?
5. Šta se dešava sa uvezenim pinovima periferija koje dizajn ne koristi?

<details>
<summary>Odgovori</summary>

1. U `.qsf` fajlu projekta, kao Tcl naredbe `set_location_assignment PIN_... -to <signal>`.
2. Port *top-level* entiteta mora imati isti naziv (i indeks) kao signal u fajlu.
3. `even` je `std_logic`, a `LEDR` je vektor; to su različiti tipovi, pa se dodjeljuje element `LEDR(0)`.
4. Logika ostaje nepromijenjena; dodaju se samo dvije dodjele koje povezuju portove sa signalima.
5. *Fitter* ih ignoriše (smjer *Unknown*); ne utiču na dizajn.

</details>

### Dodatni materijali

- Prethodni video: [6. Simulacija i testbench koncept](https://www.youtube.com/watch?v=8juBrOcO_d4)
- Sljedeći video: [8. Optimizacija kombinacionih mreža](https://www.youtube.com/watch?v=hhH37OIjS3U)
- Kratke teme: [chip_pin synthesis attribute](https://www.youtube.com/watch?v=wc1b0oMM1H8), [Project scripting with Tcl](https://www.youtube.com/watch?v=9OHjjzXgLS0)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
