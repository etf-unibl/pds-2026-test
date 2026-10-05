## 6. Simulacija i testbench koncept

**Video:** [Simulacija i testbench koncept](https://www.youtube.com/watch?v=8juBrOcO_d4) (1:00:21) · **Kod:** [`video-tutorials/part-2/video-tutorial-06`](../../video-tutorials/part-2/video-tutorial-06) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md), [Instalacija alata](../tools-setup.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:21](https://www.youtube.com/watch?v=8juBrOcO_d4&t=21s) | Simulator uz *Quartus* |
| [01:14](https://www.youtube.com/watch?v=8juBrOcO_d4&t=74s) | Projekat i izbor simulatora (*EDA Tool Settings*) |
| [02:17](https://www.youtube.com/watch?v=8juBrOcO_d4&t=137s) | Jednostavan dizajn: I kolo sa kašnjenjem |
| [05:24](https://www.youtube.com/watch?v=8juBrOcO_d4&t=324s) | *Test Bench Template Writer* |
| [08:15](https://www.youtube.com/watch?v=8juBrOcO_d4&t=495s) | Struktura testbench-a |
| [09:04](https://www.youtube.com/watch?v=8juBrOcO_d4&t=544s) | Pobudni signali |
| [11:28](https://www.youtube.com/watch?v=8juBrOcO_d4&t=688s) | Putanja do simulatora i podešavanje testbench-a u projektu |
| [13:54](https://www.youtube.com/watch?v=8juBrOcO_d4&t=834s) | *RTL* i *Gate Level* simulacija |
| [14:21](https://www.youtube.com/watch?v=8juBrOcO_d4&t=861s) | Prozori simulatora, *Run -All*, talasni oblici |
| [17:22](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1042s) | Prevođenje u simulatoru i biblioteka `work` |
| [18:51](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1131s) | Samoprovjeravajući testbench |
| [23:06](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1386s) | `assert`, `report`, `severity` |
| [25:31](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1531s) | Proces bez `wait` naredbe |
| [26:32](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1592s) | Trenutak provjere: `wait on`, `wait for` |
| [30:15](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1815s) | Testbench otkriva grešku u dizajnu |
| [32:25](https://www.youtube.com/watch?v=8juBrOcO_d4&t=1945s) | Generički sabirač i generičke konstante |
| [36:28](https://www.youtube.com/watch?v=8juBrOcO_d4&t=2188s) | `for generate` |
| [40:36](https://www.youtube.com/watch?v=8juBrOcO_d4&t=2436s) | Bihevioralni sabirač: `numeric_std` umjesto `std_logic_arith` |
| [44:42](https://www.youtube.com/watch?v=8juBrOcO_d4&t=2682s) | Testbench sa petljama |
| [50:54](https://www.youtube.com/watch?v=8juBrOcO_d4&t=3054s) | Greška u povezivanju otkrivena simulacijom |
| [52:42](https://www.youtube.com/watch?v=8juBrOcO_d4&t=3162s) | Greška u testbench-u: poređenje preko `to_integer` |
| [58:31](https://www.youtube.com/watch?v=8juBrOcO_d4&t=3511s) | I testbench može biti neispravan |

### Ključni pojmovi

- **Testbench** - VHDL opis bez portova koji generiše pobudne signale za dizajn koji se testira i posmatra ili provjerava njegove izlaze.
- **UUT** (*unit under test*) - instanca dizajna koji se testira.
- **Samoprovjeravajući testbench** (*self-checking*) - testbench koji sam poredi izlaze sa očekivanim vrijednostima.
- **`assert` / `report` / `severity`** - provjera uslova, poruka i nivo ozbiljnosti (`note`, `warning`, `error`, `failure`).
- **RTL simulacija** - funkcionalna simulacija VHDL opisa; **gate-level** simulacija koristi rezultat sinteze sa kašnjenjima.
- **Generička konstanta** (`generic`) - parametar entiteta koji se zadaje pri instanciranju (`generic map`).
- **`for generate`** - konkurentna naredba koja replicira instance ili naredbe.

### Objašnjenje

#### Simulator i projekat

Uz *Quartus* se instalira simulator *Intel FPGA* izdanja (*ModelSim* u starijim, *Questa* u novijim verzijama). Simulator se bira u **Assignments &rarr; Settings &rarr; EDA Tool Settings &rarr; Simulation**, sa formatom izlaza **VHDL**, a putanja do simulatora se provjerava u **Tools &rarr; Options &rarr; EDA Tool Options**.

> **Napomena:** U videu se koriste *Quartus* 16.1 i *ModelSim-Altera*. U novijim verzijama simulator je *Questa - Intel FPGA Starter Edition* i za njega je potrebna besplatna licenca; vidi [Instalacija alata](../tools-setup.md). Postupak u alatu je isti.

**Processing &rarr; Start &rarr; Start Test Bench Template Writer** (nakon analize i sinteze) generiše šablon testbench-a (`.vht`) u folderu `simulation/<simulator>`. Testbench se zatim dodaje u **Settings &rarr; Simulation &rarr; Compile test bench** (naziv, *top-level* entitet testbench-a i fajl), a simulacija se pokreće sa **Tools &rarr; Run Simulation Tool &rarr; RTL Simulation**. U simulatoru se signali prevlače u prozor *Wave*, a **Run -All** izvršava simulaciju dok ima događaja.

Iz komandne linije isti testbench se pokreće alatom GHDL (kao u CI provjeri kursa):

```
ghdl -a --std=08 even_detector.vhd even_detector_tb.vhd
ghdl -e --std=08 even_detector_tb
ghdl -r --std=08 even_detector_tb --stop-time=10ms --assert-level=error --wave=even_detector_tb.ghw
```

#### Struktura testbench-a

[`even_detector_tb.vhd`](../../video-tutorials/part-2/video-tutorial-06/even_detector/even_detector_tb.vhd) ima entitet bez portova, a arhitektura sadrži deklaraciju komponente, signale za povezivanje, instancu dizajna i dva procesa:

```vhdl
entity even_detector_tb is
end even_detector_tb;

architecture tb_arch of even_detector_tb is
  component even_detector
    port(
      a : in std_logic_vector(2 downto 0);
      even : out std_logic
    );
  end component;
  signal test_in : std_logic_vector(2 downto 0);
  signal test_out : std_logic;
begin
  -- uut instantiation
  uut: even_detector
    port map(a => test_in, even => test_out);
  ...
```

Generator pobude postavlja sve kombinacije ulaza, svaku na 200 ns, i na kraju se zaustavlja naredbom `wait;` (čeka zauvijek):

```vhdl
  process
  begin
    test_in <= "000";
    wait for 200 ns;
    test_in <= "001";
    wait for 200 ns;
    ...
    test_in <= "111";
    wait for 200 ns;
    wait;
  end process;
```

Proces bez liste osjetljivosti i bez `wait` naredbe nikada se ne suspenduje: simulator prijavljuje beskonačnu petlju (*process contains no WAIT statement*).

#### Provjera rezultata

Provjera se pokreće pri svakoj promjeni ulaza (`wait on test_in`), a izlaz se čita tek nakon `wait for 100 ns`, kada se ustale kašnjenja dizajna (ovdje 32-35 ns) i prije sljedeće promjene ulaza (200 ns):

```vhdl
  process
    variable error_status : boolean;
  begin
    wait on test_in;
    wait for 100 ns;
    if ((test_in = "000" and test_out = '1') or
        ...
        (test_in = "111" and test_out = '0'))
    then
      error_status := false;
    else
      error_status := true;
    end if;

    -- report an error
    assert not error_status
      report "Test failed!"
      severity error;
  end process;
```

`assert` ispisuje poruku iz `report` kada uslov **nije** ispunjen. Nivo `severity` određuje ozbiljnost: `note` i `warning` su informativni, a `error` (i `failure`) označavaju neuspješan test. CI provjera kursa pokreće simulaciju sa `--assert-level=error`, pa samo poruke nivoa `error` i više obaraju test.

> **Napomena o grešci u videu:** U videu (i ranije u kodu) verifikator prijavljuje grešku sa `severity note`. Poruka nivoa `note` ne označava neuspješan test, pa bi neispravan dizajn prošao provjeru u simulatoru i u CI-ju. Kod je ispravljen na `severity error` i označen komentarom `NOTE`.

#### Generički sabirač i `for generate`

[`generic_adder.vhd`](../../video-tutorials/part-2/video-tutorial-06/generic_adder/generic_adder.vhd) ima generičku konstantu `width` sa podrazumijevanom vrijednošću 4; širina se zadaje pri instanciranju (`generic map (width => 8)`). Strukturna arhitektura povezuje `width` potpunih sabirača ([`fulladder.vhd`](../../video-tutorials/part-2/video-tutorial-06/generic_adder/fulladder.vhd)) u lanac prenosa:

```vhdl
architecture str_arch of generic_adder is
  ...
  signal wire : std_logic_vector(0 to width);
begin
  wire(0) <= carry_in;
  carry_out <= wire(width);

  g1:
  for i in 0 to width-1 generate
    f_add: fulladder port map (a(i), b(i), wire(i), sum(i), wire(i+1));
  end generate;
end str_arch;
```

`for generate` instancira sabirač za svako `i`, što je isto kao `width` ručno napisanih instanci, ali se za drugu širinu ništa ne mijenja. Pozicione veze u `port map` prate redoslijed portova komponente (`a`, `b`, `cin`, `s`, `cout`); zamjena dvije pozicije (npr. `s` i `cout`) daje sintaksno ispravan, ali pogrešan dizajn, što se u videu otkriva simulacijom. Imenovane veze (`cin => wire(i)`) su sigurnije.

Isti sabirač može se opisati bihevioralno pomoću paketa `ieee.numeric_std`:

```vhdl
architecture num_arch of generic_adder is
  signal result : unsigned(width downto 0);
begin
  result <= ('0' & unsigned(a)) + ('0' & unsigned(b)) + unsigned'(0 => carry_in);
  sum <= std_logic_vector(result(width-1 downto 0));
  carry_out <= result(width);
end num_arch;
```

Operandi se proširuju za jedan bit (`'0' &`) da bi rezultat sadržao prenos. Paketi `std_logic_arith` i `std_logic_unsigned` (zakomentarisani u kodu) nisu standardni i ne preporučuju se; koristite `numeric_std`.

#### Testbench sa petljama

[`generic_adder_tb.vhd`](../../video-tutorials/part-2/video-tutorial-06/generic_adder/generic_adder_tb.vhd) u jednom procesu generiše i provjerava sve kombinacije ulaza pomoću dvije ugniježđene petlje. Rezultat se poredi kao cijeli broj, jer su `sum_test` (5 bita) i ulazi (4 bita) različite dužine:

```vhdl
assert (to_integer(unsigned(sum_test)) =
        (to_integer(unsigned(a_test)) + to_integer(unsigned(b_test))))
  report "Error, sum incorrect! Expected sum of " &
    integer'image((to_integer(unsigned(a_test)) + to_integer(unsigned(b_test)))) & ...
  severity error;
```

`std_logic_vector` se prvo pretvara u `unsigned`, pa u `integer`; `integer'image` pretvara broj u string za poruku. Na kraju proces ispisuje `Test completed.` i zaustavlja se sa `wait;`.

> **Napomena o grešci u videu:** U videu se kaže da petlje prolaze kroz 15 vrijednosti za `b` i ukupno 15 &times; 15 kombinacija. Petlje `for i in 0 to 15` imaju 16 iteracija, pa se testira 16 &times; 16 = 256 kombinacija (simulacija traje 2560 ns). Takođe se kaže da RTL prikaz sadrži četiri polusabirača; to su potpuni sabirači (`fulladder`).

Testbench takođe može imati greške: u videu je pogrešno poređenje vektora različitih dužina prijavljivalo greške ispravnog dizajna. Za složenije dizajne testni vektori i očekivani rezultati često se generišu drugim alatom (npr. Python) i čitaju iz fajla.

### Primjer

Folder [`video-tutorials/part-2/video-tutorial-06`](../../video-tutorials/part-2/video-tutorial-06) sadrži `even_detector` i `generic_adder` sa testbench-evima. Simulacija alatom GHDL:

```
ghdl -a --std=08 generic_adder/fulladder.vhd generic_adder/generic_adder.vhd generic_adder/generic_adder_tb.vhd
ghdl -e --std=08 generic_adder_tb
ghdl -r --std=08 generic_adder_tb --assert-level=error
```

Očekivani ispis je `Test completed.` bez poruka o grešci. Zatim namjerno pokvarite dizajn (npr. zamijenite `wire(i+1)` i `sum(i)` u `port map`) i provjerite da testbench prijavljuje greške i da se simulacija završava neuspješno.

### Česte greške

- **Proces bez `wait` naredbe** u testbench-u: beskonačna petlja na početku simulacije.
- **Generator pobude bez `wait;` na kraju**: pobuda se ponavlja ispočetka.
- **Provjera odmah nakon promjene ulaza**: izlaz još nije ažuriran zbog kašnjenja; sačekajte (`wait for`) prije provjere.
- **`severity note` za neuspješnu provjeru**: test ne pada; koristite `severity error`.
- **Poređenje vektora različitih dužina**: rezultat je uvijek `false`; poredite cijele brojeve (`to_integer`).
- **Pozicione veze u `port map` pogrešnim redoslijedom**: dizajn se prevodi, ali radi pogrešno.
- **`std_logic_arith` / `std_logic_unsigned`**: nestandardni paketi; koristite `numeric_std`.
- **Testbench koji nije provjeren**: provjerite da testbench zaista prijavljuje grešku za namjerno neispravan dizajn.

### Provjera znanja

1. Zašto entitet testbench-a nema portove?
2. Šta se dešava u simulaciji ako proces bez liste osjetljivosti nema nijednu `wait` naredbu?
3. Zašto verifikator čeka 100 ns nakon promjene ulaza prije provjere?
4. Kada `assert` ispisuje poruku i zašto je za neuspješnu provjeru potreban nivo `error`?
5. Šta omogućavaju generička konstanta `width` i naredba `for generate` u generičkom sabiraču?

<details>
<summary>Odgovori</summary>

1. Testbench je najviši nivo simulacije: sam generiše ulaze i čita izlaze dizajna preko internih signala, pa nema veza sa okruženjem.
2. Proces se nikada ne suspenduje, pa vrijeme simulacije ne napreduje; simulator prijavljuje beskonačnu petlju.
3. Izlaz se mijenja sa kašnjenjem dizajna (do 35 ns); provjera mora biti nakon što se izlaz ustali, a prije sljedeće promjene ulaza (200 ns).
4. Kada uslov nije ispunjen. Nivoi `note` i `warning` ne označavaju neuspjeh, pa simulacija (i CI sa `--assert-level=error`) prolazi i kada je dizajn neispravan.
5. `width` određuje širinu sabirača pri instanciranju, a `for generate` instancira odgovarajući broj potpunih sabirača, pa se kod ne mijenja za drugu širinu.

</details>

### Dodatni materijali

- Prethodni video: [5. Sekvencijalne VHDL naredbe](https://www.youtube.com/watch?v=oH_dKclt0WU)
- Sljedeći video: [7. Dodjeljivanje pinova (alternativni način)](https://www.youtube.com/watch?v=xWWVBNAbvGg)
- Kratke teme: [VHDL generics](https://www.youtube.com/watch?v=YIIg2CprQ3s), [if-generate](https://www.youtube.com/watch?v=uMoDe54J7GE), [VHDL configuration](https://www.youtube.com/watch?v=DP7kfX050V4)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
