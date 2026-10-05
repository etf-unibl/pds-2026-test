## 5. Sekvencijalne VHDL naredbe

**Video:** [Sekvencijalne VHDL naredbe](https://www.youtube.com/watch?v=oH_dKclt0WU) (59:41) · **Kod:** [`video-tutorials/part-2/video-tutorial-05`](../../video-tutorials/part-2/video-tutorial-05) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [01:17](https://www.youtube.com/watch?v=oH_dKclt0WU&t=77s) | Kašnjenje u simulaciji: ključna riječ `after` |
| [04:25](https://www.youtube.com/watch?v=oH_dKclt0WU&t=265s) | Proces kao složena konkurentna naredba |
| [07:38](https://www.youtube.com/watch?v=oH_dKclt0WU&t=458s) | Podrazumijevana vrijednost porta |
| [10:36](https://www.youtube.com/watch?v=oH_dKclt0WU&t=636s) | Šablon kombinacionog procesa |
| [13:21](https://www.youtube.com/watch?v=oH_dKclt0WU&t=801s) | Lista osjetljivosti |
| [15:44](https://www.youtube.com/watch?v=oH_dKclt0WU&t=944s) | Nepotpuna lista osjetljivosti |
| [17:26](https://www.youtube.com/watch?v=oH_dKclt0WU&t=1046s) | Proces bez liste osjetljivosti: `wait on`, `wait for`, `wait until` |
| [21:27](https://www.youtube.com/watch?v=oH_dKclt0WU&t=1287s) | Više dodjela istom signalu: proces i konkurentne naredbe |
| [26:54](https://www.youtube.com/watch?v=oH_dKclt0WU&t=1614s) | Varijable |
| [31:03](https://www.youtube.com/watch?v=oH_dKclt0WU&t=1863s) | Naredba `if` i komparator |
| [33:27](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2007s) | Upozorenje *inferring latch* |
| [36:19](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2179s) | Nepotpuna dodjela izlaza |
| [39:27](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2367s) | Stil sa podrazumijevanim dodjelama |
| [41:22](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2482s) | `if` u odnosu na `when-else` |
| [43:15](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2595s) | Naredba `case` |
| [45:42](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2742s) | Pokrivanje svih vrijednosti i `when others` |
| [47:12](https://www.youtube.com/watch?v=oH_dKclt0WU&t=2832s) | Leč kola u `case` naredbi |
| [50:31](https://www.youtube.com/watch?v=oH_dKclt0WU&t=3031s) | Petlja `for`: redukovano XOR kolo |
| [54:14](https://www.youtube.com/watch?v=oH_dKclt0WU&t=3254s) | Replikacija hardvera i `for generate` |
| [58:03](https://www.youtube.com/watch?v=oH_dKclt0WU&t=3483s) | Rezime |

### Ključni pojmovi

- **`after`** - kašnjenje dodjele signalu; koristi se samo u simulaciji, alat za sintezu ga ignoriše.
- **Proces** (`process`) - konkurentna naredba koja sadrži niz sekvencijalnih naredbi.
- **Sekvencijalna naredba** - naredba unutar procesa koja se izvršava redom (`if`, `case`, `for`, `wait`, dodjele).
- **Lista osjetljivosti** (*sensitivity list*) - signali čija promjena pokreće proces.
- **Naredba `wait`** - suspenduje proces bez liste osjetljivosti (`wait on`, `wait for`, `wait until`).
- **Varijabla** (`variable`) - objekat lokalan za proces; dodjela (`:=`) djeluje odmah.
- **Leč** (*latch*) - memorijski element koji sinteza nepoželjno generiše kada izlaz kombinacionog procesa nije dodijeljen u svim granama.
- **Podrazumijevana dodjela** - dodjela vrijednosti svim izlazima na početku procesa, prije `if` ili `case`.

### Objašnjenje

#### Kašnjenje u simulaciji

Ključna riječ `after` zadaje kašnjenje dodjele signalu, na primjer za detektor parnog broja jedinica iz [videa 2](02-vhdl-basics-1.md):

```vhdl
even <= (p1 or p2 or p3 or p4) after 20 ns;
p1 <= (not a(2) and not a(1) and not a(0)) after 15 ns;
p2 <= (not a(2) and a(1) and a(0)) after 12 ns;
```

Vrijeme se navodi sa jedinicom (`fs`, `ps`, `ns`, `us`, `ms`, `sec`). Kašnjenje utiče samo na simulaciju: alat za sintezu ga ignoriše, a stvarno kašnjenje kola zavisi od rasporeda logike na čipu i dobija se vremenskom analizom.

#### Proces i lista osjetljivosti

Proces je jedna konkurentna naredba koja sadrži niz sekvencijalnih naredbi:

```vhdl
process(a, b, c)
begin
  y <= a and b and c;
end process;
```

Promjena signala iz liste osjetljivosti pokreće proces; naredbe se izvrše redom, proces se suspenduje i čeka sljedeću promjenu. Ovaj proces je ekvivalentan konkurentnoj naredbi `y <= a and b and c;`, koju pokreće promjena bilo kojeg signala sa desne strane.

U kombinacionom procesu lista osjetljivosti mora sadržati **sve signale koji se čitaju**. Sa `process(a)` simulator ne bi pokrenuo proces pri promjeni `b` ili `c`, pa bi `y` zadržao staru vrijednost. Alat za sintezu obično ignoriše listu i napravi ispravno I kolo (uz upozorenje o nepotpunoj listi), pa se rezultati simulacije i sinteze ne poklapaju.

Port ili signal može imati podrazumijevanu (početnu) vrijednost, npr. `y : out std_logic := '0'`; ona važi u simulaciji.

#### Proces bez liste osjetljivosti

Proces bez liste osjetljivosti mora sadržati naredbu `wait`:

| Naredba | Značenje |
| ------ | ------ |
| `wait on a, b, c;` | čeka promjenu nekog od signala (implicitna lista osjetljivosti) |
| `wait for 100 ns;` | čeka zadato vrijeme |
| `wait until uslov;` | čeka da uslov postane tačan (npr. ivica takta) |

Naredba `wait for` se koristi u *testbench*-u za generisanje pobudnih signala:

```vhdl
signal a : std_logic := '0';
...
process
begin
  a <= '1';
  wait for 100 ns;
  a <= '0';
  wait for 200 ns;
end process;
```

Nakon posljednje naredbe proces počinje ispočetka, pa se dobija periodičan signal (100 ns jedinica, 200 ns nula).

> **Napomena o grešci u videu:** U videu (od [18:44](https://www.youtube.com/watch?v=oH_dKclt0WU&t=1124s)) se u procesu sa `wait for` dodjeljuje vrijednost signalu `a`, koji je ulazni port entiteta. Ulaznom portu se ne može dodijeliti vrijednost (GHDL: `port "a" can't be assigned`). U *testbench*-u je `a` interni signal arhitekture (kao u primjeru iznad), koji se povezuje na ulaz dizajna koji se testira; vidi [video 6](https://www.youtube.com/watch?v=8juBrOcO_d4).

#### Više dodjela istom signalu

```vhdl
process(a, b, c, d)
begin
  y <= a or c;
  y <= a and b;
  y <= c and d;
end process;
```

Dodjela signalu u procesu se ne obavlja odmah, nego tek kada se proces suspenduje, i to **posljednja** dodijeljena vrijednost. Ovaj proces je zato ekvivalentan naredbi `y <= c and d;`. Iste tri dodjele kao konkurentne naredbe opisuju tri izvora (*driver*) za isti signal: sinteza prijavljuje grešku (više izvora za jedan signal), a simulacija sa `std_logic` daje razriješenu vrijednost (npr. `'X'` za `'0'` i `'1'`).

#### Varijable

Varijabla se deklariše u procesu (prije `begin`), lokalna je za taj proces i dodjela vrijednosti (`:=`) djeluje odmah:

```vhdl
process(a, b)
  variable temp : std_logic;
begin
  temp := '0';
  temp := temp or a;
  temp := temp or b;
  y <= temp;
end process;
```

Sinteza daje ILI kolo sa ulazima `a` i `b`. Rezultat varijable mora se dodijeliti signalu da bi bio vidljiv izvan procesa.

| | Signal | Varijabla |
| ------ | ------ | ------ |
| Deklaracija | u arhitekturi | u procesu |
| Vidljivost | svi procesi arhitekture | samo taj proces |
| Dodjela | `<=`, na kraju procesa | `:=`, odmah |
| Lista osjetljivosti | da (ako se čita) | ne |

Varijable koristite umjereno, kada nema prirodnijeg opisa signalima.

#### Naredba `if` i leč kola

[`process_demo.vhd`](../../video-tutorials/part-2/video-tutorial-05/process_demo/process_demo.vhd) poredi dva osmobitna broja. Bez grane `else` izlaz `eq` nije dodijeljen kada brojevi nisu jednaki, pa sinteza zaključuje da on čuva staru vrijednost i generiše leč, uz upozorenje:

```
Warning (10631): VHDL Process Statement warning at process_demo.vhd(16): inferring latch(es) for signal or variable "eq", which holds its previous value in one or more paths through the process
```

U kombinacionom procesu ovo upozorenje uvijek označava grešku. Drugi uzrok iste greške je izlaz koji nije dodijeljen u nekoj grani, iako `if` ima sve grane (npr. `gt` nije dodijeljen u granama `elsif` i `else`). Najjednostavnije rješenje su podrazumijevane dodjele na početku procesa:

```vhdl
process(a, b)
begin
  gt <= '0';
  eq <= '0';
  lt <= '0';
  if (a > b) then
    gt <= '1';
  elsif (a = b) then
    eq <= '1';
  else
    lt <= '1';
  end if;
end process;
```

Pošto važi posljednja dodjela, svaki izlaz je dodijeljen u svakom prolazu kroz proces. Relacioni operatori na `std_logic_vector` vektorima iste dužine porede element po element, što za brojeve bez znaka daje ispravan rezultat; za brojeve sa znakom koristite tipove `signed`/`unsigned` iz paketa `ieee.numeric_std`.

`if` odgovara konkurentnoj naredbi `when-else`, ali je fleksibilnija: naredbe se mogu ugnijezditi, a u jednoj grani može se dodijeliti više signala.

#### Naredba `case`

`case` je sekvencijalni pandan naredbi `with-select-when`. [`case_demo.vhd`](../../video-tutorials/part-2/video-tutorial-05/case_demo/case_demo.vhd) postavlja jedan od izlaza `hi`, `mid`, `lo` prema najvišem postavljenom bitu zahtjeva `a`:

```vhdl
process(a)
begin
  hi <= '0';
  mid <= '0';
  lo <= '0';
  case a is
    when "100" | "101" | "110" | "111" =>
      hi <= '1';
    when "010" | "011" =>
      mid <= '1';
    when "001" =>
      lo <= '1';
    when others =>
      null;
  end case;
end process;
```

Izbori moraju pokriti sve vrijednosti izraza; pošto `std_logic` ima devet vrijednosti, potrebna je grana `when others` (inače: `Case Statement choices must cover all possible values of expression`). Naredba `null` ne radi ništa. Kao i kod `if`, izlaz koji nije dodijeljen u svim granama daje leč; podrazumijevane dodjele na početku procesa to sprečavaju.

> **Napomena o grešci u videu:** Kod u repozitorijumu je u grani `when others` dodjeljivao `lo <= '1'`, pa je `lo` bio postavljen i za `"000"` (nema zahtjeva) i za nedefinisane vrijednosti, suprotno opisu iz videa (`lo` samo kada je postavljen najniži bit). Kod je ispravljen kao u primjeru iznad i označen komentarom `NOTE`.

#### Petlja `for`

[`reduced_xor.vhd`](../../video-tutorials/part-2/video-tutorial-05/reduced_xor/reduced_xor.vhd) računa XOR svih bita vektora:

```vhdl
architecture demo_arch of reduced_xor is
  constant WIDTH : integer := 4;
  signal tmp : std_logic_vector(WIDTH-1 downto 0);
begin
  process(a, tmp)
  begin
    tmp(0) <= a(0);
    for i in 1 to (WIDTH-1) loop
      tmp(i) <= a(i) xor tmp(i-1);
    end loop;
  end process;
  y <= tmp(WIDTH-1);
end demo_arch;
```

Petlja `for` u procesu ne opisuje ponavljanje u vremenu, nego replikaciju hardvera: sinteza je razvija u lanac XOR kola. Ekvivalentan opis bez petlje:

```vhdl
tmp(0) <= a(0);
tmp(1) <= a(1) xor tmp(0);
tmp(2) <= a(2) xor tmp(1);
tmp(3) <= a(3) xor tmp(2);
y <= tmp(3);
```

Prednost petlje je skalabilnost: za drugu širinu mijenja se samo konstanta `WIDTH` (ili generička konstanta entiteta). Signal `tmp` se čita u procesu, pa je u listi osjetljivosti. Za replikaciju instanci komponenti koristi se konkurentna naredba `for generate`.

### Primjer

Folder [`video-tutorials/part-2/video-tutorial-05`](../../video-tutorials/part-2/video-tutorial-05) sadrži `process_demo`, `case_demo` i `reduced_xor`. Provjera sintakse i elaboracija:

```
ghdl -a --std=08 process_demo/process_demo.vhd case_demo/case_demo.vhd reduced_xor/reduced_xor.vhd
ghdl -e --std=08 case_demo
```

U *Quartus*-u uklonite granu `else` iz `process_demo` ili podrazumijevane dodjele iz `case_demo`, prevedite dizajn i pronađite upozorenje *inferring latch* i leč u *RTL Viewer*-u. Zatim promijenite `WIDTH` u `reduced_xor` na 8 (i širinu porta `a`) i uporedite rezultat sinteze.

### Česte greške

- **Nepotpuna lista osjetljivosti**: simulacija se ne poklapa sa sintezom; u kombinacionom procesu navedite sve signale koji se čitaju.
- **`if` bez `else`** ili **izlaz koji nije dodijeljen u svim granama**: sinteza generiše leč; koristite podrazumijevane dodjele na početku procesa.
- **`case` bez `when others`**: greška pri analizi, jer `std_logic_vector` ima i nedefinisane vrijednosti.
- **Očekivanje da se signal promijeni odmah**: dodjela signalu u procesu važi tek kada se proces suspenduje; za međurezultate koristite varijable.
- **Više dodjela istom signalu iz konkurentnih naredbi ili iz više procesa**: više izvora za jedan signal.
- **Dodjela ulaznom portu**: ulazni port se samo čita; pobudu u *testbench*-u generišite na internim signalima.
- **Očekivanje da `after` utiče na sintezu**: kašnjenje važi samo u simulaciji.

### Provjera znanja

1. Kada se pokreće proces sa listom osjetljivosti i šta se dešava ako neki signal koji se čita nije u listi?
2. Koju vrijednost dobija `y` nakon procesa sa dodjelama `y <= a or c; y <= a and b; y <= c and d;`?
3. Po čemu se varijabla razlikuje od signala?
4. Zašto sinteza generiše leč za `if (a = b) then eq <= '1'; end if;` i kako se to ispravlja?
5. Zašto naredba `case` nad `std_logic_vector` zahtijeva granu `when others`?

<details>
<summary>Odgovori</summary>

1. Pri promjeni nekog signala iz liste. Ako signal koji se čita nije u listi, simulacija ne reaguje na njegovu promjenu (izlaz zadržava staru vrijednost), dok sinteza obično napravi kombinaciono kolo, pa se rezultati ne poklapaju.
2. `c and d`: u procesu važi posljednja dodjela, a signal se ažurira kada se proces suspenduje.
3. Varijabla je lokalna za proces, dodjela (`:=`) djeluje odmah i ne stavlja se u listu osjetljivosti; signal je vidljiv u cijeloj arhitekturi i ažurira se na kraju procesa.
4. Kada `a /= b`, `eq` nije dodijeljen, pa mora zadržati staru vrijednost. Ispravka je grana `else eq <= '0';` ili podrazumijevana dodjela `eq <= '0';` na početku procesa.
5. Izbori moraju pokriti sve vrijednosti izraza, a `std_logic` ima devet vrijednosti (`'U'`, `'X'`, `'Z'`...), koje se ne mogu sve nabrojati.

</details>

### Dodatni materijali

- Prethodni video: [4. Programiranje ciljne FPGA platforme](https://www.youtube.com/watch?v=D-kIoQWeO_E)
- Sljedeći video: [6. Simulacija i testbench koncept](https://www.youtube.com/watch?v=8juBrOcO_d4)
- Kratke teme: [Transport and inertial delay in VHDL](https://www.youtube.com/watch?v=W5rptHuuIQc), [VHDL generics](https://www.youtube.com/watch?v=YIIg2CprQ3s), [if-generate](https://www.youtube.com/watch?v=uMoDe54J7GE)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
