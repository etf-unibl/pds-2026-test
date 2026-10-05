## 15. Primjena procedura pri pisanju testbench fajlova

**Video:** [Primjena procedura pri pisanju testbench fajlova](https://www.youtube.com/watch?v=mw2XPHItJM8) (16:24) · **Kod:** [`video-tutorials/part-4/video-tutorial-15`](../../video-tutorials/part-4/video-tutorial-15) · **Vezana uputstva:** [Simulacija i testiranje](../simulation-and-testing.md), [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:17](https://www.youtube.com/watch?v=mw2XPHItJM8&t=17s) | Memorija iz [videa 9](09-regular-sequential-circuits.md) |
| [01:23](https://www.youtube.com/watch?v=mw2XPHItJM8&t=83s) | Atribut `ramstyle` u simulaciji |
| [01:37](https://www.youtube.com/watch?v=mw2XPHItJM8&t=97s) | Struktura testbench-a |
| [02:53](https://www.youtube.com/watch?v=mw2XPHItJM8&t=173s) | Takt sa zadatim brojem perioda |
| [03:13](https://www.youtube.com/watch?v=mw2XPHItJM8&t=193s) | Upis i čitanje postavljanjem signala |
| [05:39](https://www.youtube.com/watch?v=mw2XPHItJM8&t=339s) | Zašto apstrahovati operacije na magistrali |
| [06:13](https://www.youtube.com/watch?v=mw2XPHItJM8&t=373s) | Procedure i funkcije |
| [07:15](https://www.youtube.com/watch?v=mw2XPHItJM8&t=435s) | Gdje se deklarišu procedure |
| [08:29](https://www.youtube.com/watch?v=mw2XPHItJM8&t=509s) | Procedura `readmem` |
| [10:11](https://www.youtube.com/watch?v=mw2XPHItJM8&t=611s) | Procedura `writemem` |
| [10:56](https://www.youtube.com/watch?v=mw2XPHItJM8&t=656s) | Pozivanje procedura |
| [11:32](https://www.youtube.com/watch?v=mw2XPHItJM8&t=692s) | Primjer: serijski interfejs |
| [13:52](https://www.youtube.com/watch?v=mw2XPHItJM8&t=832s) | Provjera da test otkriva grešku |
| [15:20](https://www.youtube.com/watch?v=mw2XPHItJM8&t=920s) | Trenutak provjere u odnosu na takt |

### Ključni pojmovi

- **Potprogram** - funkcija ili procedura.
- **Funkcija** (`function`) - vraća vrijednost i ne smije sadržati `wait`.
- **Procedura** (`procedure`) - ne vraća vrijednost (rezultat se vraća kroz `out` parametre), može sadržati `wait` i dodjeljivati signale.
- **Apstrakcija transakcije** - operacija na magistrali (upis, čitanje, slanje serijskog podatka) upakovana u jednu proceduru.
- **Paket** (`package`) - mjesto za procedure koje se koriste u više testbench-eva.

### Objašnjenje

#### Testbench za memoriju

[`memory_tb.vhd`](../../video-tutorials/part-4/video-tutorial-15/memory/memory_tb.vhd) testira memoriju iz [videa 9](09-regular-sequential-circuits.md) (64 riječi od 8 bita; [`memory.vhd`](../../video-tutorials/part-4/video-tutorial-15/memory/memory.vhd)). Atribut `ramstyle` utiče samo na sintezu i nema uticaja na simulaciju. Takt se generiše zadati broj perioda, nakon čega se proces zaustavlja (`wait;`), pa se simulacija završava sama:

```vhdl
  process
  begin
    for i in 1 to num_cycles loop
      clk <= '0';
      wait for T/2;
      clk <= '1';
      wait for T/2;
    end loop;
    wait;
  end process;
```

Upis se izvodi postavljanjem `we`, `addr` i `data` i čekanjem jednog takta, a čitanje postavljanjem `we <= '0'`. Kod složenijih interfejsa (*handshake* signali, serijski protokoli) ovakvo ručno postavljanje signala se ponavlja i lako se pogriješi.

#### Procedure

Procedura je potprogram koji, za razliku od funkcije, ne vraća vrijednost, ali može sadržati naredbe `wait`, pa može opisati cijelu transakciju na magistrali. Procedure deklarisane u procesu mogu direktno dodjeljivati signale arhitekture; procedure deklarisane u arhitekturi ili u paketu dobijaju signale kao parametre, ali se mogu koristiti u više procesa i testbench-eva.

```vhdl
    procedure readmem(
      constant addr_in : in natural;
      constant expect : in std_logic_vector
    ) is
    begin
      we <= '0';
      addr <= addr_in;
      wait for 20 ns;
      assert (q = expect)
        report "Test failed!"
        severity Error;
    end readmem;

    procedure writemem(
      constant addr_in : in natural;
      constant data_in : in std_logic_vector
    ) is
    begin
      we <= '1';
      addr <= addr_in;
      data <= data_in;
      wait for 20 ns;
    end writemem;
```

Parametar tipa `std_logic_vector` ne mora imati zadatu dužinu; dužinu dobija od stvarnog argumenta. Testni scenario se tada piše kao niz transakcija:

```vhdl
    writemem(22, "00001111");
    readmem(22, "00001111");
```

Isti princip je još korisniji za serijske interfejse: procedura dobija podatak, pa ga sama šalje bit po bit sa odgovarajućim `wait for`.

> **Napomena o grešci u videu:** U videu (i ranije u kodu) `readmem` poredi signal `data` sa očekivanom vrijednošću ([09:24](https://www.youtube.com/watch?v=mw2XPHItJM8&t=564s)). `data` je ulaz memorije koji postavlja sam testbench, pa provjera ne zavisi od memorije i nikad ne bi otkrila neispravnu memoriju; demonstracija na [13:52](https://www.youtube.com/watch?v=mw2XPHItJM8&t=832s) prijavljuje grešku samo zato što se razlikuju upisana i očekivana vrijednost. Izlaz memorije je `q`; kod je ispravljen (`assert (q = expect)`) i označen komentarom `NOTE`.

#### Trenutak provjere

`readmem` postavlja adresu i čeka 20 ns (jedan takt): memorija pamti adresu na rastuću ivicu, pa je `q` važeći tek nakon nje. Provjera mora biti nakon ivice na kojoj se rezultat pojavljuje, a prije sljedeće promjene ulaza; inače test prijavljuje lažnu grešku ili propušta stvarnu. U videu se zato greška prijavljuje na 80 ns, na opadajućoj ivici takta.

### Primjer

U folderu [`video-tutorials/part-4/video-tutorial-15/memory`](../../video-tutorials/part-4/video-tutorial-15/memory) pokrenite testbench:

```
ghdl -i --std=08 *.vhd
ghdl -m --std=08 memory_tb
ghdl -r --std=08 memory_tb --assert-level=error
```

Zatim provjerite da test zaista otkriva grešku: promijenite očekivanu vrijednost u `readmem(22, "00001111")`, ili u `memory.vhd` privremeno izbacite upis (`ram(addr) <= data;`), i provjerite da se simulacija završava sa `Test failed!`. Za vježbu prebacite procedure u paket i dodajte proceduru koja upisuje i provjerava sve adrese.

### Česte greške

- **Provjera ulaza umjesto izlaza dizajna**: test ne zavisi od dizajna i uvijek prolazi.
- **Provjera u pogrešnom trenutku**: prije nego što se izlaz ažurira ili nakon sljedeće promjene ulaza.
- **Procedura van procesa koja dodjeljuje signale koji nisu parametri**: greška pri analizi; signale treba proslijediti kao parametre.
- **`wait` u funkciji**: nije dozvoljeno; koristite proceduru.
- **Testbench koji nije provjeren**: provjerite da test pada za namjerno neispravan dizajn.

### Provjera znanja

1. Po čemu se procedura razlikuje od funkcije?
2. Zašto su procedure pogodne za testbench-eve?
3. Šta je potrebno da bi procedura deklarisana van procesa mogla mijenjati signale?
4. Zašto provjera `data = expect` ne testira memoriju?
5. Kako se provjerava da testbench zaista otkriva grešku?

<details>
<summary>Odgovori</summary>

1. Funkcija vraća vrijednost i ne smije sadržati `wait`; procedura ne vraća vrijednost (može imati `out` parametre), a može sadržati `wait` i dodjeljivati signale.
2. Ponovljene transakcije (upis, čitanje, serijsko slanje) pišu se jednom, a scenario testa postaje kratak i čitljiv niz poziva.
3. Signali joj se moraju proslijediti kao parametri (klase `signal`).
4. `data` je ulaz koji postavlja sam testbench; provjera ne zavisi od izlaza memorije `q`.
5. Namjerno se pokvari dizajn ili očekivana vrijednost i provjeri se da simulacija prijavljuje grešku.

</details>

### Dodatni materijali

- Prethodni video: [14. Smanjenje kašnjenja mreža primjenom pipeline tehnike](https://www.youtube.com/watch?v=K7ENW7DFjXg)
- Kratke teme: [VHDL funkcije](https://www.youtube.com/watch?v=Ki51447L1SU), [VHDL Packages](https://www.youtube.com/watch?v=bKRCJ3X5dsM), [Fajl za inicijalizaciju memorije](https://www.youtube.com/watch?v=ScZWPQ2UmE4)
- [12. Napredni aspekti pisanja Testbench fajlova](12-advanced-testbench.md)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
