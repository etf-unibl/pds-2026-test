## 12. Napredni aspekti pisanja Testbench fajlova

**Video:** [Napredni aspekti pisanja Testbench fajlova](https://www.youtube.com/watch?v=PCvCYeHhEFw) (36:34) · **Kod:** [`video-tutorials/part-3/video-tutorial-12`](../../video-tutorials/part-3/video-tutorial-12) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:32](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=32s) | Lookup tabela testnih vektora |
| [01:11](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=71s) | Tip `record` |
| [02:44](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=164s) | Niz zapisa bez zadatog opsega |
| [03:30](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=210s) | Konstanta sa testnim vektorima: poziciono i imenovano navođenje |
| [04:47](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=287s) | Petlja kroz `test_vectors'range` i provjera |
| [07:58](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=478s) | Testbench otkriva grešku u dizajnu |
| [08:59](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=539s) | Testni vektori iz fajla i skript jezici |
| [10:37](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=637s) | Paket `std.textio` |
| [12:52](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=772s) | Tipovi `file` i `line` |
| [14:09](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=849s) | `file_open` za čitanje i upis |
| [16:25](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=985s) | Čitanje liniju po liniju: `endfile`, `readline`, `read` |
| [18:42](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1122s) | Upis rezultata: `write`, `writeline` |
| [20:00](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1200s) | Gdje se nalaze fajlovi sa podacima |
| [22:12](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1332s) | Greške u izlaznom fajlu |
| [23:42](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1422s) | Testbench za binarni brojač |
| [26:16](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1576s) | Reset impuls i generator takta |
| [28:27](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1707s) | Upis odbiraka na ivicu takta |
| [31:29](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1889s) | Rezultat: `max_pulse` kasni jedan takt |
| [33:17](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1997s) | Prikaz signala u simulatoru: *Radix* i *Analog* format |

### Ključni pojmovi

- **Lookup tabela** - konstanta koja sadrži ulaze i očekivane izlaze za sve testne slučajeve.
- **`record`** - složeni tip sa imenovanim poljima, kao `struct` u jeziku C.
- **Niz bez zadatog opsega** (`array (natural range <>) of ...`) - dužina se određuje pri inicijalizaciji.
- **`std.textio`** - paket za rad sa tekstualnim fajlovima u simulaciji (tipovi `text` i `line`, procedure `readline`, `read`, `write`, `writeline`).
- **`ieee.std_logic_textio`** - paket sa `read`/`write` za `std_logic` i `std_logic_vector`; u VHDL-2008 te procedure su dio paketa `std_logic_1164`, a paket je zadržan radi kompatibilnosti.
- **Fajl sa testnim vektorima** - CSV fajl koji generiše i provjerava skript jezik (Python, MATLAB...).

### Objašnjenje

#### Lookup tabela testnih vektora

Testni vektori mogu se zadati unaprijed, kao konstanta niza zapisa ([`even_detector_tb.vhd`](../../video-tutorials/part-3/video-tutorial-12/even_detector/even_detector_tb.vhd)):

```vhdl
  type test_vector is record
    a : std_logic_vector(2 downto 0);
    even : std_logic;
  end record;

  type test_vector_array is array (natural range <>) of test_vector;
  constant test_vectors : test_vector_array := (
    -- a,  even    -- positional method is used here
    ("000", '1'),  -- alternatively, you can use (a => "000", even => '1')
    ("001", '0'),
    ...
    ("111", '0')
  );
```

Jedan proces postavlja ulaz, čeka da se izlaz ustali i provjerava ga:

```vhdl
  process
  begin
    for i in test_vectors'range loop
      test_in <= test_vectors(i).a;
      wait for 200 ns;

      assert (test_out = test_vectors(i).even)
        report "Test vector " & integer'image(i) & " failed " & ...
        severity error;
    end loop;
    wait;
  end process;
```

`test_vectors'range` je opseg indeksa niza (ovdje `0 to 7`), pa petlja prolazi kroz sve vektore bez obzira na njihov broj. Polja zapisa se čitaju tačkom (`test_vectors(i).a`).

> **Napomena o grešci u videu:** Na [05:09](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=309s) se kaže da atribut `'range` daje veličinu niza. `'range` daje opseg indeksa (pogodan za petlju), a broj elemenata daje atribut `'length`.

#### Testni vektori iz fajla

Ulazi i očekivani izlazi mogu biti u CSV fajlu koji generiše skript jezik, a testbench upisuje rezultate u drugi fajl koji skript zatim provjerava. Zakomentarisani dio istog testbench-a to radi pomoću paketa `std.textio`:

```vhdl
    file_open(input_buf, "data_files/even_detector_input.csv", read_mode);
    file_open(output_buf, "data_files/even_detector_output.csv", write_mode);
    ...
    while not endfile(input_buf) loop
      readline(input_buf, read_col_from_input_buf);
      read(read_col_from_input_buf, val_a, good_num);
      next when not good_num;  -- skip the header lines

      read(read_col_from_input_buf, val_comma);
      read(read_col_from_input_buf, val_even, good_num);
      ...
      test_in <= val_a;
      even_actual <= val_even;
      wait for 200 ns;

      write(write_col_to_output_buf, test_in);
      write(write_col_to_output_buf, string'(","));
      ...
      writeline(output_buf, write_col_to_output_buf);
    end loop;
```

`readline` čita jednu liniju fajla u promjenljivu tipa `line`, a `read` iz nje redom čita vrijednosti; treći argument (`good_num`) je `false` ako vrijednost nije pročitana, što se koristi za preskakanje linije zaglavlja (`#a,even`). Upis ide obrnutim redom: `write` dodaje vrijednosti u liniju, a `writeline` upisuje liniju u fajl. Ulazni fajl [`even_detector_input.csv`](../../video-tutorials/part-3/video-tutorial-12/even_detector/data_files/even_detector_input.csv):

```
#a,even
000,1
001,0
...
```

Putanja fajla je relativna u odnosu na direktorijum iz kojeg se pokreće simulacija (u *Quartus*-u folder `simulation/<simulator>` projekta), pa tamo mora postojati folder `data_files`. Izlaz za ispravan dizajn:

```
#a,even_actual,even,even_test_results
000,1,1,OK
001,0,0,OK
...
```

> **Napomena o grešci u videu:** Na [14:59](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=899s) se kaže da i izlazni fajl mora unaprijed postojati. Fajl otvoren u `write_mode` simulator sam kreira (ili briše postojeći sadržaj); mora postojati samo folder `data_files` i, naravno, ulazni fajl.

Ovaj testbench neispravan rezultat samo upisuje u fajl (`Error`), bez `assert` naredbe, pa simulacija prolazi i za neispravan dizajn (kao što se vidi na [22:34](https://www.youtube.com/watch?v=PCvCYeHhEFw&t=1354s)). Ako testbench treba sam da prijavi grešku (npr. u CI provjeri), uz upis u fajl dodajte i `assert test_out = even_actual ... severity error;`.

`ieee.std_logic_textio` nije dio standarda VHDL-93 (to je *Synopsys* paket), pa ga stariji alati u režimu VHDL-93 ne prihvataju uvijek. Kurs koristi VHDL-2008, u kojem su `read`/`write` za `std_logic` dio paketa `std_logic_1164`; linija `use ieee.std_logic_textio.all;` je tada nepotrebna, ali dozvoljena.

#### Testbench za sekvencijalnu mrežu

[`binary_counter_tb.vhd`](../../video-tutorials/part-3/video-tutorial-12/binary_counter/binary_counter_tb.vhd) testira jednosegmentni binarni brojač iz [videa 9](09-regular-sequential-circuits.md). Reset impuls i takt su tipični za svaki testbench sekvencijalne mreže:

```vhdl
  constant T : time := 20 ns;
  ...
  reset <= '1', '0' after T/2;

  process
  begin
    clk <= '0';
    wait for T/2;
    clk <= '1';
    wait for T/2;
    ...
  end process;
```

Dodjela `reset <= '1', '0' after T/2;` je talasni oblik: `'1'` od početka, `'0'` nakon pola periode. Drugi proces na svaku rastuću ivicu (nakon reseta) upisuje `max_pulse` i `q` (pretvoren u `integer`) u `data_files/binary_counter_data.csv`, a nakon 30 taktova generator takta zatvara fajl i zaustavlja se (`wait;`). U rezultatu se vidi greška jednosegmentnog opisa: `max_pulse` je `'1'` kada je `q = 0`, a ne kada je `q = 15`, a prvi red je `U`, jer se `max_pulse` ne postavlja resetom.

```
max_pulse,q
U,0
0,1
...
0,15
1,0
```

#### Prikaz signala u simulatoru

U prozoru *Wave* desnim klikom na signal bira se **Radix** (binarni, heksadecimalni, `unsigned`, `signed`...) i **Format &rarr; Analog**, koji vektor prikazuje kao analogni signal (npr. testerasti signal brojača). To je korisno za vizuelnu provjeru signala koji predstavljaju odbirke.

### Primjer

U folderu [`video-tutorials/part-3/video-tutorial-12`](../../video-tutorials/part-3/video-tutorial-12) pokrenite testbench sa lookup tabelom:

```
ghdl -a --std=08 even_detector.vhd even_detector_tb.vhd
ghdl -e --std=08 even_detector_tb
ghdl -r --std=08 even_detector_tb --assert-level=error
```

Zatim uključite varijantu sa fajlovima (odkomentarišite dijelove označene sa *Uncomment for file-based testbench*, zakomentarišite one označene sa *Comment for file-based testbench*) i pokrenite simulaciju istim komandama iz foldera `even_detector`. Provjerite `data_files/even_detector_output.csv`, pa obrišite jedno `not` u dizajnu i ponovite. Za vježbu napišite Python skriptu koja generiše ulazni fajl i provjerava kolonu `even_test_results`.

### Česte greške

- **Testbench sa fajlovima bez `assert`**: greške su samo u fajlu, a simulacija prolazi.
- **Pogrešna relativna putanja**: fajl se traži u odnosu na direktorijum simulacije, ne u odnosu na VHDL fajl.
- **Nepostojeći folder `data_files`**: `file_open` ne može da kreira folder.
- **Fajl koji se ne zatvori**: dio upisanih linija može ostati u baferu; zatvorite fajlove sa `file_close`.
- **Upis tipa `unsigned` direktno**: `write` ga ne podržava; pretvorite u `integer` ili `std_logic_vector`.

### Provjera znanja

1. Kako se definiše niz zapisa bez unaprijed zadate dužine i kako se određuje njegova dužina?
2. Šta je razlika između atributa `'range` i `'length`?
3. Kako testbench sa fajlovima preskače liniju zaglavlja u ulaznom CSV fajlu?
4. Zašto testbench sa fajlovima iz videa ne prijavljuje grešku u simulaciji i kako se to popravlja?
5. Kako se u rezultatu testbench-a za brojač vidi da jednosegmentni opis kasni jedan takt?

<details>
<summary>Odgovori</summary>

1. `type test_vector_array is array (natural range <>) of test_vector;` - dužina niza se određuje brojem elemenata u inicijalizaciji konstante.
2. `'range` daje opseg indeksa (npr. `0 to 7`), pogodan za petlju; `'length` daje broj elemenata (8).
3. `read` sa trećim argumentom vraća `false` kada linija ne počinje vrijednošću tipa `std_logic_vector` (zaglavlje počinje sa `#`), a `next when not good_num;` prelazi na sljedeću liniju.
4. Rezultat poređenja se samo upisuje u fajl kao `Error`; potrebno je dodati `assert` sa `severity error` (ili provjeriti fajl skriptom).
5. `max_pulse` je `'1'` u redu u kojem je `q = 0`, a trebalo bi da bude u redu u kojem je `q = 15`.

</details>

### Dodatni materijali

- Prethodni video: [11. Projektovanje sekvencijalnih mreža Register-Transfer metodologijom](https://www.youtube.com/watch?v=39Tch03-rAU)
- Sljedeći video: [13. Vremenska analiza sinhronih digitalnih sistema](https://www.youtube.com/watch?v=DVF86jV4JMo)
- Kratke teme: [VHDL funkcije](https://www.youtube.com/watch?v=Ki51447L1SU), [VHDL Packages](https://www.youtube.com/watch?v=bKRCJ3X5dsM), [Unconstrained array in VHDL](https://www.youtube.com/watch?v=Curgf6K1Row)
- [15. Primjena procedura pri pisanju testbench fajlova](https://www.youtube.com/watch?v=mw2XPHItJM8)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
