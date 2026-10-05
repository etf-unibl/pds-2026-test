## Simulacija i testiranje

Prije predaje, svako rješenje je potrebno provjeriti lokalno. Automatske provjere na *GitHub* platformi pokreću iste korake (analiza, simulacija, sinteza), pa rješenje koje lokalno ne prolazi neće proći ni tamo, a lokalna provjera traje znatno kraće. Instalacija potrebnih alata opisana je u uputstvu [Instalacija alata](tools-setup.md).

Primjeri u nastavku koriste dizajn `nand2` iz fajla `nand2.vhd` i njegov *testbench* `nand2_tb` iz fajla `nand2_tb.vhd`, smještene u folderu `assignments/55`.

### Preporučeni redoslijed provjere

1. **Sintaksa** - svi fajlovi se prevode bez grešaka (standard VHDL-2008).
2. **Simulacija** - *testbench* potvrđuje ispravno ponašanje dizajna.
3. **Sinteza** - dizajn se uspješno sintetiše u *Quartus* alatu (dizajn koji se simulira ne mora nužno biti sintetizabilan).
4. **Stil** - `vhdl-style 55` ne prijavljuje greške ([Pravila za formatiranje VHDL opisa](vhdl-code-style.md)).

### Simulacija iz komandne linije (ModelSim / Questa)

Komande se pokreću iz foldera sa fajlovima. Fajlovi se prevode redoslijedom zavisnosti (prvo komponente, zatim dizajn koji ih koristi, na kraju *testbench*):

```
vlib work
vcom -2008 nand2.vhd nand2_tb.vhd
vsim -c nand2_tb -do "run -all; quit -f"
```

Opcija `-c` pokreće simulaciju bez grafičkog interfejsa. Za pregled talasnih oblika simulacija se pokreće u grafičkom interfejsu:

```
vsim nand2_tb -do "add wave -r /*; run -all"
```

Folder `work` i fajl `transcript` koje simulator generiše se ne predaju.

### Simulacija iz komandne linije (GHDL)

```
ghdl -a --std=08 nand2.vhd nand2_tb.vhd
ghdl -e --std=08 nand2_tb
ghdl -r --std=08 nand2_tb --wave=nand2_tb.ghw
```

Komanda `ghdl -a` provjerava sintaksu i analizira fajlove, `ghdl -e` elaborira *testbench*, a `ghdl -r` pokreće simulaciju. Talasni oblici iz fajla `nand2_tb.ghw` pregledaju se alatom [GTKWave](https://gtkwave.sourceforge.net). Ako simulacija ne završava sama (npr. *testbench* sa taktnim signalom koji se ne zaustavlja), dodajte opciju `--stop-time=1us`.

Opcija `--std=08` prevodi kod po standardu VHDL-2008, koji se koristi na kursu. Iste opcije koristi i automatska provjera na *GitHub*-u. U *Quartus* projektu standard se bira u podešavanjima projekta (vidi [Instalacija alata](tools-setup.md#quartus-i-simulator)).

### Sinteza u Quartus alatu

1. Napravite projekat (**File &rarr; New Project Wizard**). Preporučuje se da radni folder projekta bude **izvan** repozitorijuma, kako fajlovi koje *Quartus* generiše ne bi završili u komitu.
2. U koraku *Add Files* dodajte VHDL fajlove iz foldera `assignments/<N>` (bez *testbench* fajla). Fajlovi ostaju u repozitorijumu, a projekat ih samo referencira.
3. Odaberite FPGA čip na evaluacionoj ploči koja se koristi na kursu.
4. Postavite *top-level* entitet (**Project &rarr; Set as Top-Level Entity** nad fajlom dizajna) i pokrenite **Processing &rarr; Start &rarr; Start Analysis & Synthesis**.
5. Provjerite izvještaj o greškama i upozorenjima. Posebnu pažnju obratite na upozorenja o nenamjerno generisanim lečevima (*inferred latch*).

Rezultat sinteze se može pregledati kao šema u **Tools &rarr; Netlist Viewers &rarr; RTL Viewer**.

### Vrste testova

**Manuelni test** - *testbench* generiše pobude, a ispravnost se procjenjuje pregledom talasnih oblika. Pogodan je za prve korake i otkrivanje grešaka, ali se rezultat ne može automatski provjeriti.

**Automatizovani (samoprovjeravajući) test** - *testbench* sam poredi izlaze dizajna sa očekivanim vrijednostima i prijavljuje razlike naredbom `assert`. Rezultat je jasno vidljiv u ispisu simulatora, a test se može ponavljati nakon svake izmjene. Pri ocjenjivanju projekta (segment QA) automatizovani testovi nose više bodova.

Primjer samoprovjeravajućeg procesa za kolo `nand2` (prikazan je samo proces; zaglavlje fajla, entitet i deklaracije signala `a`, `b` i `y` su izostavljeni, a potrebna je i biblioteka `ieee.numeric_std`):

```vhdl
  check : process is
    variable v_in : std_logic_vector(1 downto 0);
  begin
    for i in 0 to 3 loop
      v_in := std_logic_vector(to_unsigned(i, 2));
      a    <= v_in(1);
      b    <= v_in(0);
      wait for 10 ns;
      assert y = (v_in(1) nand v_in(0))
        report "Wrong output for input combination " & integer'image(i)
        severity error;
    end loop;
    report "Test finished";
    wait;
  end process check;
```

Nakon simulacije provjerite da ispis ne sadrži poruke nivoa `Error` (u *ModelSim* / *Questa* simulatoru sažetak se vidi u liniji `Errors: 0, Warnings: 0` na kraju simulacije).

Za veći broj test vektora, ulazne pobude i očekivani izlazi mogu se čitati iz tekstualnih fajlova pomoću paketa `std.textio`. Fajlovi sa podacima se predaju zajedno sa *testbench* fajlom. Primjeri su dati u materijalima uz video tutorijale kursa.

### Automatsko pokretanje *testbench* fajlova

Svaki *testbench* predat uz zadatak automatski se simulira u poslu `testbench` ([Automatske provjere](automated-checks.md)). Da bi to bilo moguće, potrebno je poštovati sljedeća pravila:

- *testbench* za dizajn `<dizajn>` nalazi se u fajlu `<dizajn>_tb.vhd` u folderu `assignments/<N>`, a njegov entitet se zove `<dizajn>_tb` (isto kao fajl, bez ekstenzije),
- svi fajlovi koje *testbench* koristi nalaze se u istom folderu,
- greške se prijavljuju naredbom `assert` sa nivoom `error` ili `failure`, jer posao ne prolazi samo ako se prijavi takva poruka (ili ako se *testbench* ne može prevesti),
- simulacija se završava sama (npr. zaustavljanjem takta nakon posljednjeg testa i naredbom `wait;` u procesu sa pobudama). Simulacija se u svakom slučaju prekida nakon 10 ms simuliranog vremena.

Posao izvršava iste komande koje možete pokrenuti i lokalno, iz foldera `assignments/<N>`:

```
ghdl -i --std=08 *.vhd
ghdl -m --std=08 nand2_tb
ghdl -r --std=08 nand2_tb --stop-time=10ms --assert-level=error --wave=nand2_tb.ghw
```

Komanda `ghdl -i` učitava sve fajlove iz foldera, a `ghdl -m` ih prevodi potrebnim redoslijedom. Talasni oblici iz simulacije dostupni su i kao artifakt `testbench-waveforms` na stranici pokretanja provjera.

Uspješno izvršen posao `testbench` znači samo da *testbench* nije prijavio grešku. Koliko dobro *testbench* provjerava dizajn zavisi od toga koje slučajeve pokriva, pa testove pišite tako da obuhvate sve značajne kombinacije ulaza i granične slučajeve.

### Testiranje na evaluacionoj ploči

1. U *Quartus* projektu dodijelite pinove FPGA čipa portovima dizajna. Za ploču kursa dostupan je fajl sa dodjelom pinova koji se uvozi opcijom **Assignments &rarr; Import Assignments**, a pojedinačni pinovi se mogu podesiti u **Assignments &rarr; Pin Planner**.
2. Pokrenite kompletno prevođenje (**Processing &rarr; Start Compilation**).
3. Povežite ploču *USB-Blaster* kablom, otvorite **Tools &rarr; Programmer**, u **Hardware Setup** odaberite *USB-Blaster*, a zatim pokrenite programiranje dugmetom **Start** (fajl `.sof` iz foldera `output_files`).

Ako *Programmer* ne prepoznaje ploču, provjerite da li je instaliran drajver za *USB-Blaster* ([Instalacija alata](tools-setup.md)).
