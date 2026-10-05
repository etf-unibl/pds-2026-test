## 13. Vremenska analiza sinhronih digitalnih sistema

**Video:** [Vremenska analiza sinhronih digitalnih sistema](https://www.youtube.com/watch?v=DVF86jV4JMo) (1:19:02) · **Kod:** [`video-tutorials/part-4/video-tutorial-13`](../../video-tutorials/part-4/video-tutorial-13) · **Vezana uputstva:** [Video tutorijali](../video-tutorials.md)

### Sadržaj

| Vrijeme | Tema |
| ---: | ------ |
| [00:23](https://www.youtube.com/watch?v=DVF86jV4JMo&t=23s) | Kašnjenje flip-flopa `Tcq` |
| [01:13](https://www.youtube.com/watch?v=DVF86jV4JMo&t=73s) | Vrijeme uspostavljanja (*setup*) i zadržavanja (*hold*) |
| [02:30](https://www.youtube.com/watch?v=DVF86jV4JMo&t=150s) | Registar, logika narednog stanja, registar |
| [05:28](https://www.youtube.com/watch?v=DVF86jV4JMo&t=328s) | Vremenski dijagram: `Tnext(min)` i `Tnext(max)` |
| [11:56](https://www.youtube.com/watch?v=DVF86jV4JMo&t=716s) | Uslov za *setup* i najveća frekvencija takta |
| [14:39](https://www.youtube.com/watch?v=DVF86jV4JMo&t=879s) | *Launch* i *latch* ivica |
| [16:29](https://www.youtube.com/watch?v=DVF86jV4JMo&t=989s) | Uslov za *hold* |
| [20:31](https://www.youtube.com/watch?v=DVF86jV4JMo&t=1231s) | Kašnjenje takta i narušavanje *hold* uslova |
| [21:58](https://www.youtube.com/watch?v=DVF86jV4JMo&t=1318s) | Kašnjenje izlaza `Tco` |
| [24:03](https://www.youtube.com/watch?v=DVF86jV4JMo&t=1443s) | Povezani podsistemi |
| [26:49](https://www.youtube.com/watch?v=DVF86jV4JMo&t=1609s) | Kritična putanja |
| [29:32](https://www.youtube.com/watch?v=DVF86jV4JMo&t=1772s) | Lažna putanja (*false path*) |
| [34:04](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2044s) | Izvještaj vremenske analize za sekvencijalni množač |
| [36:36](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2196s) | *Unconstrained Paths* |
| [37:16](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2236s) | *Slack* |
| [39:13](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2353s) | Podrazumijevani takt od 1 GHz |
| [40:39](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2439s) | *Timing Analyzer*: četiri koraka |
| [44:11](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2651s) | SDC fajl |
| [47:13](https://www.youtube.com/watch?v=DVF86jV4JMo&t=2833s) | Meni *Constraints* |
| [53:16](https://www.youtube.com/watch?v=DVF86jV4JMo&t=3196s) | `create_clock` |
| [57:16](https://www.youtube.com/watch?v=DVF86jV4JMo&t=3436s) | Ponovna analiza i modeli radnih uslova |
| [1:01:02](https://www.youtube.com/watch?v=DVF86jV4JMo&t=3662s) | *Fmax Summary* |
| [1:02:35](https://www.youtube.com/watch?v=DVF86jV4JMo&t=3755s) | Ulazna i izlazna kašnjenja i virtuelni takt |
| [1:07:11](https://www.youtube.com/watch?v=DVF86jV4JMo&t=4031s) | `set_input_delay` i `set_output_delay` |
| [1:11:46](https://www.youtube.com/watch?v=DVF86jV4JMo&t=4306s) | *Report Timing* i *Locate Path* |
| [1:14:25](https://www.youtube.com/watch?v=DVF86jV4JMo&t=4465s) | Lažna putanja za asinhroni reset |
| [1:17:59](https://www.youtube.com/watch?v=DVF86jV4JMo&t=4679s) | Analiza bez *unconstrained* putanja |

### Ključni pojmovi

- **`Tcq`** - kašnjenje od aktivne ivice takta do promjene izlaza flip-flopa.
- **`Tsetup` / `Thold`** - vrijeme prije / poslije aktivne ivice takta tokom kojeg ulaz flip-flopa mora biti stabilan.
- **`Tnext(max)` / `Tnext(min)`** - najduže / najkraće kašnjenje kombinacione logike između dva registra.
- **Launch / latch ivica** - ivica koja pokreće promjenu na izlazu prvog registra / ivica na kojoj drugi registar pamti rezultat.
- **Slack** - razlika između vremena kada podatak treba da stigne i vremena kada zaista stigne; negativan *slack* znači da uslov nije ispunjen.
- **Kritična putanja** - putanja sa najvećim kašnjenjem; određuje najveću frekvenciju takta.
- **Lažna putanja** (*false path*) - putanja koja postoji u strukturi, ali se logički nikad ne aktivira, ili asinhrona putanja koja se isključuje iz analize.
- **SDC** (*Synopsys Design Constraints*) - fajl sa vremenskim ograničenjima dizajna (Tcl komande).
- **Virtuelni takt** - takt spoljnog uređaja koji nije port dizajna; referenca za ulazna i izlazna kašnjenja.

### Objašnjenje

#### Vremenski parametri flip-flopa

Flip-flop karakterišu tri vremena koja zavise od tehnologije i na koja projektant ne može da utiče: `Tcq`, `Tsetup` i `Thold`. Ulaz `D` ne smije da se mijenja u prozoru od `Tsetup` prije do `Thold` poslije aktivne ivice takta.

#### Uslov za setup i najveća frekvencija

Između dva registra sa istim taktom podatak kreće sa izlaza prvog registra na *launch* ivicu, prolazi kroz kombinacionu logiku i mora da se ustali na ulazu drugog registra najkasnije `Tsetup` prije sljedeće (*latch*) ivice:

```
Tcq + Tnext(max) + Tsetup < Tc
fmax = 1 / (Tcq + Tnext(max) + Tsetup)
```

Pošto su `Tcq` i `Tsetup` zadati tehnologijom, frekvencija se povećava samo smanjenjem kašnjenja logike `Tnext(max)`, npr. optimizacijom kombinacione mreže ([video 8](08-combinational-optimization.md)) ili *pipeline* tehnikom ([video 14](https://www.youtube.com/watch?v=K7ENW7DFjXg)).

#### Uslov za hold

Prva promjena na ulazu drugog registra ne smije nastupiti prije isteka `Thold` nakon iste ivice:

```
Thold < Tcq + Tnext(min)
```

Flip-flopovi se projektuju tako da je `Thold < Tcq`, pa je uslov ispunjen čak i kada između registara nema logike. Narušavanje *hold* uslova moguće je kada takt kasni različito do dva registra (*clock skew*), što alat za vremensku analizu takođe provjerava.

#### Izlazi, povezani podsistemi i kritična putanja

Kašnjenje izlaza je `Tco = Tcq + Toutput` (kod Mealy mašine i od ulaza). Kada izlaz jednog podsistema ulazi u logiku narednog stanja drugog, u uslov za *setup* ulazi cijeli lanac: `Tco(podsistem 1) + Tnext(max) + Tsetup < Tc`.

Alat analizira strukturu (topologiju) kola i prijavljuje najdužu putanju kao kritičnu. Neke putanje se logički nikad ne aktiviraju: na primjer, ako dva multipleksera sa zajedničkim selekcionim signalom biraju između blokova od 10 ns i 40 ns, a zatim od 60 ns i 20 ns, strukturno najduža putanja (40 + 60 = 100 ns) nije moguća, a stvarna kritična putanja je 10 + 60 = 70 ns. Takve lažne putanje projektant mora sam da prijavi alatu.

#### Timing Analyzer u alatu Quartus

> **Napomena:** U videu se koristi *Quartus* 16.1, gdje se alat zove *TimeQuest Timing Analyzer*. U novijim verzijama zove se *Timing Analyzer* (**Tools &rarr; Timing Analyzer**); koraci, izvještaji i SDC komande su isti.

Vremenska analiza je posljednji korak kompilacije. Bez SDC fajla alat pretpostavlja takt od 1 GHz (period 1 ns), pa izvještaj prijavljuje negativan *slack*, a ulazi i izlazi su prijavljeni kao *Unconstrained Paths*. U *Timing Analyzer*-u postupak ima četiri koraka:

1. **Create Timing Netlist** - proračun kašnjenja svih putanja nakon *Fitter*-a.
2. **Read SDC File** - učitavanje ograničenja (podrazumijevano `<projekat>.sdc`).
3. **Update Timing Netlist** - primjena ograničenja.
4. Izvještaji (*Report Setup/Hold Summary*, *Report Top Failing Paths*, *Report Unconstrained Paths*, histogrami...).

Svaka akcija u grafičkom interfejsu izvršava Tcl komandu (npr. `create_timing_netlist -model slow`, `read_sdc`, `update_timing_netlist`), pa se postupak može automatizovati skriptom. Modeli *Slow* i *Fast* (na 85 °C i 0 °C) odgovaraju najsporijem i najbržem primjerku čipa.

#### SDC fajl

[`seq_mult.sdc`](../../video-tutorials/part-4/video-tutorial-13/seq_mult/seq_mult.sdc) ograničava sekvencijalni množač iz [videa 11](11-register-transfer-methodology.md):

```tcl
create_clock -name clk -period 8 [get_ports {clk}]
create_clock -name clk_virt -period 8

derive_clock_uncertainty

set_input_delay -clock clk_virt -max 0.550 [get_ports {start}]
set_input_delay -clock clk_virt -min 0.350 [get_ports {start}]
set_input_delay -clock clk_virt -max 0.550 [get_ports {a_in[*]}]
set_input_delay -clock clk_virt -min 0.350 [get_ports {a_in[*]}]
...
set_output_delay -clock clk_virt -max 0.550 [get_ports {r[*]}]
set_output_delay -clock clk_virt -min 0.350 [get_ports {r[*]}]
...
set_false_path -from [get_ports {reset}] -to [all_registers]
```

| Komanda | Značenje |
| ------ | ------ |
| `create_clock -period 8 [get_ports {clk}]` | stvarni takt na portu `clk`, 125 MHz |
| `create_clock -name clk_virt -period 8` | virtuelni takt (bez porta) spoljnih uređaja |
| `derive_clock_uncertainty` | automatska nesigurnost (*jitter*) takta |
| `set_input_delay` | kašnjenje ulaza u odnosu na virtuelni takt: `Tco` spoljnog flip-flopa i kašnjenje na ploči |
| `set_output_delay` | vrijeme koje izlazu treba do spoljnog flip-flopa, uključujući njegov `Tsetup` |
| `set_false_path -from [get_ports {reset}]` | asinhroni reset se isključuje iz analize |

Ograničenja se mogu unijeti i preko menija **Constraints** u *Timing Analyzer*-u (*Create Clock*, *Set Input Delay*, *Set False Path*...), koji prikazuje odgovarajuću SDC komandu. `[get_ports {a_in[*]}]` bira sve bite vektora. Za taktove iz PLL-a koristi se `derive_pll_clocks`; nezavisni takt domeni se razdvajaju sa `set_clock_groups`, a putanje koje imaju više taktova na raspolaganju sa `set_multicycle_path`.

Nakon dodavanja ograničenja dizajn treba ponovo prevesti, jer i *Fitter* koristi SDC fajl. Putanja koja ne zadovoljava uslov analizira se desnim klikom: **Report Timing** prikazuje *launch* i *latch* vremena i talasni oblik, a **Locate Path** pokazuje putanju u *Technology Map Viewer*-u ili *Chip Planner*-u. Analiza je kompletna kada nijedan port nije *unconstrained* i kada je *slack* pozitivan za sve modele. U videu *Fmax Summary* za ovaj dizajn pokazuje oko 300 MHz.

### Primjer

Folder [`video-tutorials/part-4/video-tutorial-13/seq_mult`](../../video-tutorials/part-4/video-tutorial-13/seq_mult) sadrži `seq_mult.vhd` i `seq_mult.sdc`.

1. Napravite projekat za 5CSEMA5F31C6 sa `seq_mult.vhd` (bez SDC fajla), prevedite ga i pogledajte izvještaj vremenske analize: takt od 1 GHz, negativan *slack*, *Unconstrained Paths*.
2. Dodajte `seq_mult.sdc` u projekat (**Project &rarr; Add/Remove Files in Project**), ponovo prevedite i provjerite da je *slack* pozitivan i da nema *unconstrained* putanja.
3. U *Fmax Summary* pročitajte najveću frekvenciju, smanjite period u `create_clock` ispod te vrijednosti i provjerite da se pojavljuju *failing paths*; analizirajte ih sa *Report Timing*.
4. Uklonite `set_false_path` za `reset` i pogledajte *Report Unconstrained Paths*.

### Česte greške

- **Projekat bez SDC fajla**: analiza sa podrazumijevanim taktom od 1 GHz nema smisla.
- **Nedefinisana ulazna i izlazna kašnjenja**: putanje do portova ostaju *unconstrained*.
- **Ograničenje asinhronog signala** (reset, tasteri): takvi ulazi se proglašavaju lažnim putanjama.
- **Analiza bez ponovnog prevođenja**: *Fitter* raspoređuje logiku prema ograničenjima tek pri novoj kompilaciji.
- **Brkanje imena takta i porta**: `-name` je logičko ime ograničenja, a port se zadaje sa `get_ports`; bez `get_ports` takt je virtuelan.
- **Izvedeni takt iz logike** bez `create_generated_clock`: alat ne zna njegovu vezu sa osnovnim taktom (bolje je koristiti *enable*, [video 9](09-regular-sequential-circuits.md)).

### Provjera znanja

1. Napišite uslov za *setup* između dva registra i objasnite na koju veličinu projektant može da utiče.
2. Zašto je *hold* uslov obično ispunjen i kada može biti narušen?
3. Šta je *slack* i šta znači negativna vrijednost?
4. Čemu služi virtuelni takt i zašto se ulazna i izlazna kašnjenja zadaju u odnosu na njega?
5. Zašto se za asinhroni `reset` zadaje `set_false_path`?

<details>
<summary>Odgovori</summary>

1. `Tcq + Tnext(max) + Tsetup < Tc`; `Tcq` i `Tsetup` zavise od tehnologije, pa projektant može da smanji samo kašnjenje logike `Tnext(max)` (ili da poveća period takta).
2. Flip-flopovi su projektovani tako da je `Thold < Tcq`, pa se ulaz drugog registra ne mijenja prerano; uslov može biti narušen kada takt stiže do registara sa različitim kašnjenjem (*clock skew*).
3. *Slack* je razlika između zahtijevanog i stvarnog vremena dolaska podatka; negativan *slack* znači da podatak stiže prekasno (ili prerano, za *hold*) i da dizajn ne zadovoljava ograničenja.
4. Virtuelni takt predstavlja takt spoljnog uređaja koji šalje ili prima podatke, a nije port dizajna; kašnjenja ulaza i izlaza (`Tco` spoljnog flip-flopa, kašnjenje na ploči, `Tsetup` prijemnika) opisuju se u odnosu na taj takt.
5. Asinhroni reset ne zavisi od ivice takta, pa vremenska analiza za njega nema smisla; bez `set_false_path` njegove putanje do svih registara ostaju *unconstrained*.

</details>

### Dodatni materijali

- Prethodni video: [12. Napredni aspekti pisanja Testbench fajlova](https://www.youtube.com/watch?v=PCvCYeHhEFw)
- Sljedeći video: [14. Smanjenje kašnjenja mreža primjenom pipeline tehnike](https://www.youtube.com/watch?v=K7ENW7DFjXg)
- Kratke teme: [Clock skew and timing analysis with clock skew](https://www.youtube.com/watch?v=VQlkn-XPkd4), [Adding PLL to Quartus design](https://www.youtube.com/watch?v=V6xj6NznBdY), [Project scripting with Tcl](https://www.youtube.com/watch?v=9OHjjzXgLS0), [SignalTap II Logic Analyzator](https://www.youtube.com/watch?v=Ag3d9Dem_cs)
- [Video tutorijali](../video-tutorials.md) - pregled svih videa
