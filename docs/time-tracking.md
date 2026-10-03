## Evidencija utrošenog vremena

Za svaki zadatak na radnoj ploči evidentira se procijenjeno i stvarno utrošeno vrijeme. Evidencija je dio ocjene radnog procesa (segment *Workflow*: adekvatno i ažurno vođenje evidencije o zadacima), pa je treba voditi redovno, a ne naknadno na kraju kursa.

### Polja na radnoj ploči

Svaki zadatak na radnoj ploči ima sljedeća polja:

| Polje | Ko ga popunjava | Značenje |
| ------ | ------ | ------ |
| `Estimate (h)` | student | procjena potrebnog vremena u satima, unosi se na početku rada na zadatku |
| `Time spent (h)` | student | ručno unijeto utrošeno vrijeme u satima (ukupno, ne po danu) |
| `Time logged (h)` | automatski | zbir unosa iz komentara `/spent` |
| `Time total (h)` | automatski | `Time spent (h)` + `Time logged (h)` |

Polja se prikazuju u desnom dijelu prozora zadatka, u sekciji projekta (**Projects**), a mogu se mijenjati i direktno u tabelarnom prikazu radne ploče. Polja `Time logged (h)` i `Time total (h)` popunjava *workflow* i ne treba ih mijenjati ručno, jer se njihove vrijednosti pri sljedećem ažuriranju ponovo izračunavaju.

### Dva načina evidentiranja

Vrijeme se može evidentirati na jedan od dva načina, po izboru. Načini se mogu i kombinovati, ali **svaki period rada evidentira se samo jednom**, jer se oba izvora sabiraju.

**1. Ručni unos u polje `Time spent (h)`**

Nakon rada na zadatku povećajte vrijednost polja `Time spent (h)` za utrošeno vrijeme (npr. sa `3` na `4.5`). Ovaj način je najjednostavniji, ali ne čuva informaciju o tome kada je vrijeme utrošeno.

**2. Komentari `/spent`**

Nakon rada na zadatku dodajte komentar u zadatku, u kojem svaka linija oblika `/spent <trajanje> <opis>` predstavlja jedan unos:

```
/spent 1h30m implemented the state machine
/spent 45m testbench for the reset sequence
```

- Trajanje se zadaje u satima i/ili minutama: `2h`, `1.5h`, `1,5h`, `1h30m`, `1h 30m`, `90m`, `45min`. Broj bez jedinice (npr. `/spent 2`) nije dozvoljen, a jedan unos može iznositi najviše 24 sata.
- Opis nakon trajanja nije obavezan, ali se preporučuje.
- Svi unosi iz svih komentara u zadatku se sabiraju i upisuju u polje `Time logged (h)`, obično u roku od minut.
- Ispravan komentar dobija reakciju 👍, a komentar sa neispravnim unosom reakciju 😕. Neispravan unos se ne računa; ispravite ga izmjenom komentara.
- Greška se ispravlja izmjenom ili brisanjem komentara: zbir se svaki put izračunava ponovo iz svih komentara.
- Unos se pripisuje autoru komentara, pa je ovaj način pogodan za zadatke na kojima radi više članova tima.
- Komentari `/spent` uzimaju se u obzir samo u zadacima (*issues*), ne i u *pull request*-ovima, i to samo komentari osoba kojima je zadatak dodijeljen i učesnika kursa (studenata i nastavnika).

### Izvještaj

Jednom sedmično (ponedjeljkom ujutro) *workflow* `Time tracking` ponovo izračunava polja svih zadataka sa radne ploče i ažurira izvještaj u zakačenom (*pinned*) zadatku **Izvještaj o utrošenom vremenu** na vrhu liste zadataka. Izvještaj sadrži zbir po studentu i po zadatku:

- ručno unijeto vrijeme i procjena zadatka sa više dodijeljenih studenata dijele se na jednake dijelove,
- vrijeme iz komentara `/spent` pripisuje se autoru komentara.

Repozitorijum je javan, pa je i izvještaj, kao i ostatak repozitorijuma, vidljiv svima.

Ručno unijete vrijednosti ulaze u polje `Time total (h)` i u izvještaj pri sljedećem sedmičnom ažuriranju (ili ranije, ako nastavnik ručno pokrene izvještaj), jer izmjene polja na ploči ne pokreću *workflow*.
