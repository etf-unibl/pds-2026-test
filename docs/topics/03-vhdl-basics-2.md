## 3. Osnove VHDL jezika (drugi dio)

**Video:** [Osnove VHDL jezika (drugi dio)](https://www.youtube.com/watch?v=-MCetuywNN4) (53:19) · **Kod:** [`video-tutorials/part-1/video-tutorial-03`](../../video-tutorials/part-1/video-tutorial-03) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:25](https://www.youtube.com/watch?v=-MCetuywNN4&t=25s) | Modovi portova: `in`, `out`, `inout`, `buffer` |
| [01:04](https://www.youtube.com/watch?v=-MCetuywNN4&t=64s) | Čitanje izlaznog porta i rješenje pomoću signala |
| [04:33](https://www.youtube.com/watch?v=-MCetuywNN4&t=273s) | Pristup bitima i dijelovima vektora |
| [05:59](https://www.youtube.com/watch?v=-MCetuywNN4&t=359s) | Konkatenacija (`&`) i pomjeranje |
| [08:24](https://www.youtube.com/watch?v=-MCetuywNN4&t=504s) | Dodjela vrijednosti vektoru i ključna riječ `others` |
| [11:26](https://www.youtube.com/watch?v=-MCetuywNN4&t=686s) | Aritmetička kola: sabirač |
| [14:46](https://www.youtube.com/watch?v=-MCetuywNN4&t=886s) | Paket `numeric_std`, tipovi `signed` i `unsigned`, konverzije |
| [18:24](https://www.youtube.com/watch?v=-MCetuywNN4&t=1104s) | Sinteza sabirača: ALM-ovi i LUT maske |
| [21:27](https://www.youtube.com/watch?v=-MCetuywNN4&t=1287s) | Množač i DSP blok |
| [25:54](https://www.youtube.com/watch?v=-MCetuywNN4&t=1554s) | Uslovna (`when`-`else`) i selekciona (`with`-`select`) naredba |
| [26:28](https://www.youtube.com/watch?v=-MCetuywNN4&t=1588s) | Primjer: prioritetni enkoder |
| [36:16](https://www.youtube.com/watch?v=-MCetuywNN4&t=2176s) | Sinteza: kaskadni i paralelni multiplekseri |
| [39:09](https://www.youtube.com/watch?v=-MCetuywNN4&t=2349s) | Primjer: jednostavna aritmetičko-logička jedinica (ALU) |
| [45:47](https://www.youtube.com/watch?v=-MCetuywNN4&t=2747s) | Poređenje sinteze dvije ALU arhitekture |
| [51:16](https://www.youtube.com/watch?v=-MCetuywNN4&t=3076s) | Zadatak: detektor parnog broja jedinica selekcionom naredbom |

### Ključni pojmovi

- **Mod porta** - smjer porta: `in` (ulaz), `out` (izlaz), `inout` (dvosmjerni), `buffer` (izlaz koji se može čitati unutar entiteta).
- **Isječak vektora** (*slice*) - dio vektora, npr. `r(3 downto 0)`.
- **Konkatenacija** - spajanje vektora i bita operatorom `&`.
- **`others`** - zadavanje vrijednosti svim preostalim elementima vektora ili svim preostalim izborima u naredbi.
- **`numeric_std`** - IEEE paket sa tipovima `signed` i `unsigned` i aritmetičkim operacijama nad njima.
- **Kastovanje i konverzija** - promjena tipa: `unsigned(...)`, `std_logic_vector(...)`, `to_unsigned(broj, širina)`, `to_signed(broj, širina)`.
- **DSP blok** - namjenski blok FPGA sa hardverskim množačem; alat za sintezu ga koristi za množenje.
- **Uslovna naredba** (`when`-`else`) - konkurentna dodjela sa prioritetom uslova; sintetiše se kao kaskada multipleksera.
- **Selekciona naredba** (`with`-`select`) - konkurentna dodjela po vrijednosti izraza; svi izbori moraju biti navedeni; sintetiše se kao paralelni multiplekser.
- **Prioritetni enkoder** - kolo koje daje binarni kod najvišeg aktivnog ulaza.

### Objašnjenje

#### Modovi portova i čitanje izlaza

Osim `in` i `out`, portovi mogu biti `inout` (dvosmjerni) i `buffer` (izlaz čija se vrijednost može čitati unutar entiteta). U standardu VHDL-93, koji se koristi u videu, izlazni port (`out`) ne može se čitati unutar arhitekture, pa je sljedeći kod neispravan:

```vhdl
x <= a and b;
y <= not x;  -- greška u VHDL-93: port "x" je izlazni i ne može se čitati
```

Proglašavanje porta za `inout` ili `buffer` samo zbog čitanja nije dobra praksa. Uobičajeno rješenje je interni signal, koji se može i čitati i dodjeljivati:

```vhdl
architecture simple_arch of demo_mode is
  signal ab : std_logic;
begin
  ab <= a and b;
  x <= ab;
  y <= not ab;
end simple_arch;
```

Kurs koristi standard VHDL-2008, u kojem je čitanje izlaznog porta dozvoljeno, pa je i prvi primjer ispravan. Interni signal je i dalje dobar izbor kada se ista vrijednost koristi na više mjesta, a mod `buffer` nije dozvoljen pravilima stila ([Pravila za formatiranje VHDL opisa](../vhdl-code-style.md)).

#### Rad sa vektorima

Za `signal r : std_logic_vector(7 downto 0)`:

```vhdl
q <= r(3 downto 0) & r(7 downto 4);  -- zamjena gornje i donje polovine (konkatenacija)
q <= "00" & r(7 downto 2);           -- pomjeranje udesno za dva mjesta (ulaze nule)
q <= r(5 downto 0) & "00";           -- pomjeranje ulijevo za dva mjesta
```

Operator `&` je konkatenacija (za logičko I koristi se `and`). Konstantni vektori pišu se u dvostrukim navodnicima (`"00"`), a pojedinačni biti u jednostrukim (`'0'`). Pojedinim bitima vektora može se dodijeliti vrijednost navođenjem pozicija, a svim ostalim pomoću `others`:

```vhdl
q <= (7 => '1', 5 => '1', others => '0');  -- "10100000"
q <= (others => '0');                      -- sve nule, za bilo koju širinu vektora
```

Oblik `(others => '0')` se često koristi jer ne zavisi od širine vektora.

#### Aritmetika i paket `numeric_std`

Za tip `std_logic_vector` sabiranje nije definisano, jer nije poznato da li vektor predstavlja označen ili neoznačen broj. Paket `ieee.numeric_std` uvodi tipove `unsigned` i `signed` sa aritmetičkim operacijama. Kada portovi ostaju `std_logic_vector`, vrijednosti se kastuju u `unsigned` (ili `signed`), sabiraju i vraćaju u `std_logic_vector`:

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
...
sum  <= std_logic_vector(unsigned(a) + unsigned(b));  -- 8 + 8 bita -> 8 bita
prod <= std_logic_vector(unsigned(a) * unsigned(b));  -- 8 x 8 bita -> 16 bita
```

Isto važi za sabiranje sa konstantom (`unsigned(a) + 1`). Cijeli broj se pretvara u vektor sa `to_unsigned(4, 8)` ili `to_signed(-4, 8)`, gdje je drugi argument širina u bitima. Proizvod ima dvostruko veću širinu od operanada.

Sinteza 8-bitnog sabirača koristi nekoliko ALM-ova (oni sadrže sabirače), a množač se smješta u DSP blok sa hardverskim množačem. U *Technology Map Viewer*-u se u prozoru *Properties* vidi sadržaj LUT-a (*LUT mask*), a opcijom *Locate in Chip Planner* lokacija bloka u čipu.

#### Uslovna i selekciona naredba

Obje naredbe ilustruje prioritetni enkoder: za ulaz `r` daje kod najvišeg aktivnog bita i signal `active` kada je bar jedan bit aktivan.

| `r` | `code` | `active` |
| :---: | :---: | :---: |
| `1---` | `11` | 1 |
| `01--` | `10` | 1 |
| `001-` | `01` | 1 |
| `0001` | `00` | 1 |
| `0000` | `00` | 0 |

Uslovna naredba ispituje uslove redom, pa prvi ispunjen uslov ima prioritet:

```vhdl
code <= "11" when (r(3) = '1') else
        "10" when (r(2) = '1') else
        "01" when (r(1) = '1') else
        "00";
```

Selekciona naredba bira vrijednost prema vrijednosti izraza i mora pokriti sve moguće vrijednosti, zato se završava sa `others` (osim kombinacija `'0'` i `'1'`, `std_logic` ima i vrijednosti `'X'`, `'Z'`, `'U'`...):

```vhdl
with r select
  code <= "11" when "1000"|"1001"|"1010"|"1011"|
                    "1100"|"1101"|"1110"|"1111",
          "10" when "0100"|"0101"|"0110"|"0111",
          "01" when "0010"|"0011",
          "00" when others;
```

Uslovna naredba se sintetiše kao kaskada multipleksera (prioritet), a selekciona kao paralelni multiplekser. Za mali primjer broj ALM-ova je isti, ali kod većih dizajna struktura utiče na kašnjenje i zauzeće. Selekciona naredba je pogodna za funkcije zadate tablicom, a uslovna za funkcije sa prioritetom.

#### Jednostavna ALU

ALU sa dva 8-bitna operanda bira operaciju kontrolnim signalom `ctrl`:

| `ctrl` | `result` |
| :---: | ------ |
| `0--` | `src0 + 1` |
| `100` | `src0 + src1` |
| `101` | `src0 - src1` |
| `110` | `src0 and src1` |
| `111` | `src0 or src1` |

Rezultati aritmetičkih operacija računaju se u međusignalima, a izbor se radi uslovnom ili selekcionom naredbom:

```vhdl
sum  <= std_logic_vector(signed(src0) + signed(src1));
diff <= std_logic_vector(signed(src0) - signed(src1));
inc  <= std_logic_vector(signed(src0) + 1);

with ctrl select
  result <= inc           when "000"|"001"|"010"|"011",
            sum           when "100",
            diff          when "101",
            src0 and src1 when "110",
            src0 or src1  when others;  -- "111"
```

U videu je verzija sa uslovnom naredbom zauzela 11, a selekciona 10 ALM-ova. Selekciona naredba ovdje direktno prati tablicu operacija.

### Primjer

Folder [`video-tutorials/part-1/video-tutorial-03`](../../video-tutorials/part-1/video-tutorial-03) sadrži tri dizajna:

| Dizajn | Sadržaj |
| ------ | ------ |
| [`arith_demo`](../../video-tutorials/part-1/video-tutorial-03/arith_demo/arith_demo.vhd) | sabirač (zakomentarisan) i množač sa `numeric_std` |
| [`prio_encoder`](../../video-tutorials/part-1/video-tutorial-03/prio_encoder/prio_encoder.vhd) | prioritetni enkoder: `cond_arch` i `sel_arch`, izbor konfiguracijom |
| [`simple_alu`](../../video-tutorials/part-1/video-tutorial-03/simple_alu/simple_alu.vhd) | ALU: `cond_arch` i `sel_arch`, izbor konfiguracijom |

Provjera i elaboracija (iz foldera `video-tutorials/part-1/video-tutorial-03`):

```
ghdl -a --std=08 arith_demo/arith_demo.vhd prio_encoder/prio_encoder.vhd simple_alu/simple_alu.vhd
ghdl -e --std=08 prio_encoder_cfg
ghdl -e --std=08 simple_alu_cfg
```

U alatu *Quartus* sintetišite obje arhitekture prioritetnog enkodera i ALU-a (promjenom konfiguracije) i uporedite broj ALM-ova i strukturu multipleksera u *RTL Viewer*-u. Za `arith_demo` uporedite sabirač i množač: broj ALM-ova i DSP blokova u izvještaju. Kao zadatak iz videa, opišite detektor parnog broja jedinica iz [videa 2](02-vhdl-basics-1.md) selekcionom naredbom direktno iz tablice istinitosti i uporedite rezultat sinteze.

### Česte greške

- **Čitanje izlaznog porta u VHDL-93** (`y <= not x;` gdje je `x` port `out`): greška u starijim alatima i projektima podešenim na VHDL-93; kurs koristi VHDL-2008, gdje je dozvoljeno (provjerite podešavanje projekta).
- **Aritmetika nad `std_logic_vector`** bez `numeric_std`: greška "can't determine definition of operator +"; kastujte u `unsigned`/`signed`.
- **Korišćenje paketa `std_logic_arith` ili `std_logic_unsigned`**: nisu standardni; koristite `numeric_std`.
- **Pogrešna širina rezultata**: proizvod dva 8-bitna broja ima 16 bita; zbir dva 8-bitna broja bez proširenja gubi prenos.
- **Selekciona naredba bez `others`**: nisu pokrivene sve vrijednosti tipa `std_logic_vector` i prevođenje ne uspijeva.
- **Zamjena `&` i `and`**: `&` spaja vektore, `and` je logičko I.
- **Dvostruki i jednostruki navodnici**: `'1'` je bit, `"1"` je vektor dužine jedan.

### Provjera znanja

1. Šta se mijenja u VHDL-2008 u odnosu na VHDL-93 kada treba čitati izlazni port i kako se to rješavalo u VHDL-93?
2. Šta daje izraz `"0" & r(7 downto 1)` za 8-bitni vektor `r`?
3. Zašto je za sabiranje vektora potreban paket `numeric_std` i kako se sabiraju dva `std_logic_vector` signala?
4. Po čemu se razlikuju uslovna i selekciona naredba u ponašanju i u sintetizovanoj strukturi?
5. Zašto selekciona naredba nad `std_logic_vector` mora imati granu `others` i kada je pogodnija od uslovne?

<details>
<summary>Odgovori</summary>

1. U VHDL-93 mod `out` dozvoljava samo dodjelu, pa se vrijednost računa u internom signalu koji se dodjeljuje izlazu i čita gdje je potrebno; u VHDL-2008 izlazni port se može čitati direktno.
2. Vektor pomjeren udesno za jedno mjesto, sa nulom na najvišoj poziciji (logičko pomjeranje udesno).
3. Za `std_logic_vector` nije definisano da li predstavlja označen ili neoznačen broj, pa sabiranje nije definisano; npr. `std_logic_vector(unsigned(a) + unsigned(b))`.
4. Uslovna ispituje uslove redom (prioritet) i daje kaskadu multipleksera; selekciona bira po vrijednosti izraza i daje paralelni multiplekser.
5. `std_logic` ima devet vrijednosti, pa navedene binarne kombinacije ne pokrivaju sve slučajeve; selekciona je pogodnija za funkcije zadate tablicom.

</details>

### Dodatni materijali

- Prethodni video: [2. Osnove VHDL jezika (prvi dio)](https://www.youtube.com/watch?v=-5Q7YpQmU40)
- Sljedeći video: [4. Programiranje ciljne FPGA platforme](https://www.youtube.com/watch?v=D-kIoQWeO_E)
- Kratke teme: [multstyle synthesis attribute](https://www.youtube.com/watch?v=yR-qmhUA1u0), [VHDL array attributes](https://www.youtube.com/watch?v=0LVIhOMnCE8)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
