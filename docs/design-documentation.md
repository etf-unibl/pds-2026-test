## Dokumentovanje dizajna

Svaki dizajn mora biti dokumentovan posebnim komentarima u VHDL opisu, iz kojih alat [*Doxygen*](https://www.doxygen.nl) generiše HTML dokumentaciju. Dokumentacija se automatski generiše i objavljuje na adresi `https://<organizacija>.github.io/<repozitorijum>/` nakon svake integracije u granu `assignments` ([Automatske provjere](automated-checks.md#dokumentacija-na-github-pages)). **Dokumentovanje dizajna je obavezno i ocjenjuje se.**

Ovo uputstvo je sažetak dijela *Doxygen* dokumentacije koji se odnosi na VHDL ([Documenting the code: VHDL](https://www.doxygen.nl/manual/docblocks.html#vhdlblocks)).

### Doxygen komentari u VHDL opisu

*Doxygen* obrađuje samo komentare koji počinju sa `--!`. Obični komentari (`--`) se ignorišu, pa se mogu koristiti za napomene koje ne treba da budu dio dokumentacije.

- **Kratak opis** (*brief*): jedna linija `--!` neposredno ispred elementa koji se dokumentuje.
- **Detaljan opis** (*details*): više uzastopnih linija koje počinju sa `--!`. Ako se iza kratkog opisa ostavi prazna linija, linije koje slijede čine detaljan opis.
- Komentar se uvijek nalazi **ispred** elementa koji opisuje. Jedini izuzetak su portovi (i generici), za koje komentar može stajati i **iza** elementa, u istoj liniji, i tada predstavlja kratak opis tog porta.

Umjesto oslanjanja na prazne linije, kratak i detaljan opis mogu se eksplicitno označiti komandama `@brief` i `@details`, što se i preporučuje jer je otpornije na greške.

### Najčešće komande

| Komanda | Značenje |
| ------ | ------ |
| `@file` | označava da se komentar odnosi na cijeli fajl |
| `@brief` | kratak opis (jedna rečenica) |
| `@details` | detaljan opis |
| `@note` | napomena koja se posebno ističe |
| `@warning` | upozorenje (npr. ograničenja dizajna) |
| `@see` | referenca na povezani element (npr. drugi entitet) |

Kompletan spisak komandi dat je u [*Doxygen* dokumentaciji](https://www.doxygen.nl/manual/commands.html). Unutar opisa mogu se koristiti i liste (linije koje počinju sa `-`).

### Šta je potrebno dokumentovati

<!-- TODO (nastavnik): provjeriti minimalne zahtjeve za dokumentaciju koji se ocjenjuju. -->

Minimalno, u svakom fajlu dizajna potrebno je dokumentovati:

1. **fajl** - kratak opis sadržaja fajla (`@file` i `@brief`),
2. **entitet** - kratak opis i detaljan opis funkcionalnosti (šta kolo radi, kako se koristi, vremensko ponašanje ako je bitno),
3. **svaki generik i port** - kratak opis (značenje, jedinica ili kodovanje, aktivni nivo signala),
4. **arhitekturu** - kratak opis i detaljan opis načina realizacije,
5. **procese, značajne signale, konstante, tipove i instance komponenti** - kratak opis njihove uloge.

*Testbench* fajlovi (`*_tb.vhd`) se ne uključuju u generisanu dokumentaciju, ali i u njima treba komentarisati šta se i kako testira.

*Doxygen* komentari se pišu **pored** obaveznog zaglavlja fajla, koje je propisano uputstvom [Pravila za formatiranje VHDL opisa](vhdl-code-style.md). Nakon dodavanja komentara provjerite stil komandom `vhdl-style <N>`.

### Primjer

Primjer dokumentovanog multipleksera 2:1 (zaglavlje fajla je izostavljeno):

```vhdl
--! @file
--! @brief 2:1 multiplexer

library ieee;
use ieee.std_logic_1164.all;

--! @brief 2:1 multiplexer
--! @details Selects one of the two data inputs. When sel_i is '0'
--! the output follows a_i, otherwise it follows b_i.
entity mux2 is
  port (
    a_i   : in  std_logic; --! First data input
    b_i   : in  std_logic; --! Second data input
    sel_i : in  std_logic; --! Select input ('0' selects a_i)
    y_o   : out std_logic  --! Multiplexer output
  );
end entity mux2;

--! @brief Dataflow architecture of the multiplexer
--! @details The output is driven by a single conditional
--! signal assignment, so the circuit is purely combinational.
architecture dataflow of mux2 is
begin
  y_o <= a_i when sel_i = '0' else b_i;
end architecture dataflow;
```

Za sekvencijalna kola na isti način se dokumentuju procesi i signali, uvijek komentarom ispred elementa:

```vhdl
  --! Current value of the counter
  signal count : unsigned(3 downto 0);

  --! @brief Counter register
  --! @details Synchronous reset; the counter wraps around after 15.
  count_reg : process (clk_i) is
```

### Lokalni pregled dokumentacije

Prije predaje, izgled dokumentacije možete provjeriti lokalno:

1. Instalirajte *Doxygen* sa stranice [Doxygen download](https://www.doxygen.nl/download.html).
2. U folderu `assignments` repozitorijuma pokrenite:

   ```
   doxygen Doxyfile
   ```

3. Otvorite fajl `assignments/html/index.html` u web pregledaču i pronađite svoj dizajn (npr. u meniju **Design Units**).

Folder `html` se ne predaje (naveden je u fajlu `.gitignore`). Podešavanja u fajlu `Doxyfile` ne mijenjajte, jer se isti fajl koristi za objavljivanje dokumentacije na *GitHub Pages*.
