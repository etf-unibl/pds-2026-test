## Automatske provjere

Svaki *pull request* prema grani `assignments` automatski se provjerava pomoću *GitHub Actions* servisa. Provjere se pokreću kada se *pull request* otvori, ponovo otvori, kada mu se izmijeni naslov ili opis i nakon svakog `git push` na granu zadatka.

Koji zadatak se provjerava određuje se na osnovu **prvog broja u naslovu** *pull request*-a (npr. `55` u naslovu `Issue #55 : Create NAND2 circuit`). Provjerava se sadržaj foldera `assignments/55`. Zbog toga je naslov u propisanom formatu ([Pravila prilikom predaje rješenja zadataka](assignment-submission.md)) preduslov za ispravan rad provjera.

### Poslovi (*jobs*)

Provjere su organizovane kao *workflow* `verification` sa sljedećim poslovima:

| Posao | Šta provjerava | Izvršava se za |
| ------ | ------ | ------ |
| `classify` | da li naslov sadrži broj postojećeg zadatka i vrstu zadatka na osnovu labele: probni (`good first issue`) ili zadatak koji se ocjenjuje (labela teme zadataka `assignment-1` do `assignment-4`) | sve zadatke |
| `pr-checks` | pravila predaje: naslov *pull request*-a jednak `Issue #<N> : <naslov zadatka>`, naziv grane počinje brojem zadatka, zadatak je dodijeljen autoru *pull request*-a, izmijenjeni su samo fajlovi u folderu `assignments/<N>`, svi komiti su potpisani, poruke komita prate propisani format i opis *pull request*-a prati šablon | sve zadatke |
| `linter` | stil VHDL opisa i usklađenost sa standardom VHDL-2008 (opisano u uputstvu [Pravila za formatiranje VHDL opisa](vhdl-code-style.md)) | sve zadatke |
| `basic-test` | da li fajl `assignments/<N>/test.vhd` postoji i prevodi se bez grešaka | probni zadatak |
| `testbench` | simulaciju predatih *testbench* fajlova (`*_tb.vhd`) alatom *GHDL* ([Simulacija i testiranje](simulation-and-testing.md#automatsko-pokretanje-testbench-fajlova)) | zadatke uz koje je predat *testbench* |
| `verif-setup` | određuje zadatak za testove nastavnika | sve zadatke |
| `verif` | simulaciju sa testovima nastavnika i sintezu dizajna u *Quartus* alatu | zadatke koji se ocjenjuju |

Poslovi koji se ne odnose na dati zadatak prikazuju se kao preskočeni (*skipped*, siva ikona), što ne utiče na rezultat provjere. Ako posao `classify` ne prođe, ostali poslovi se ne izvršavaju.

Posao `pr-checks` prijavljuje sva prekršena pravila odjednom, svako u zasebnoj poruci, pa je dovoljno pročitati njegov izvještaj da biste znali šta treba ispraviti.

Poslovi `verif-setup`, `pr-checks` i `verif` pripadaju zasebnom *workflow*-u `verification-tests`. On se uvijek izvršava u verziji sa grane `main`, pa izmjene fajlova *workflow*-a u *pull request*-u na njega ne utiču, i ne izvršava se za *pull request*-ove iz kopija repozitorijuma (*fork*). Posao `verif` pokreće testove predmetnog nastavnika koji nisu dio repozitorijuma kursa. Test za svaki zadatak zna koje fajlove i entitete očekuje, pa pogrešni nazivi fajlova, entiteta ili portova dovode do neuspjeha, iako je dizajn možda funkcionalno ispravan.

Probni zadatak i njegove provjere opisani su u uputstvu [Probni zadatak](test-assignment.md).

### Praćenje rezultata

Status provjera prikazuje se na dnu stranice *pull request*-a (tabulator **Conversation**):

- žuti krug - provjera je u toku (ili čeka slobodan računar za izvršavanje),
- zelena kvačica - provjera je prošla,
- crveni krstić - provjera nije prošla,
- siva ikona - posao je preskočen, jer se ne odnosi na dati zadatak.

Poruka *All checks have passed* znači da su prošle sve provjere. Ista informacija dostupna je u tabulatoru **Checks** *pull request*-a, kao i u tabulatoru **Actions** repozitorijuma, gdje su izlistana sva pokretanja.

### Analiza neuspješne provjere

1. Kliknite na **Details** pored neuspješne provjere (ili otvorite pokretanje u tabulatoru **Actions** i odaberite posao označen crvenom bojom).
2. Proširite korak označen crvenom bojom. Uzrok greške je obično opisan u posljednjim linijama ispisa tog koraka.
3. Greške poslova `linter` i `testbench` označene su i direktno u pregledu izmijenjenih fajlova (tabulator **Files changed**).
4. Rezultati se čuvaju kao artifakti, koji se preuzimaju kao ZIP arhive sa dna stranice pokretanja (sekcija **Artifacts**):
   - artifakt `verif-artifacts` (posao `verif`) sadrži foldere `sim` (rezultati testova) i `synth` (izvještaji sinteze),
   - artifakt `testbench-waveforms` (posao `testbench`) sadrži talasne oblike simulacije (`.ghw` fajlovi, koji se pregledaju alatom *GTKWave*).

   Artifakti se čuvaju ograničen broj dana.
5. Ispravite grešku lokalno, provjerite je ([Simulacija i testiranje](simulation-and-testing.md)) i pošaljite izmjenu sa `git push`. Provjere se pokreću automatski.

### Ponovno pokretanje provjera

Provjere se ponovo pokreću:

- svakim novim `git push` na granu zadatka,
- izmjenom naslova ili opisa *pull request*-a,
- dugmetom **Re-run jobs** na stranici pokretanja (ako imate potrebna prava), npr. kada je greška nastala zbog privremenog problema u infrastrukturi.

Ako provjera dugo stoji u stanju čekanja (*Queued*), moguće je da računar za izvršavanje posla `verif` nije dostupan. U tom slučaju obavijestite predmetnog nastavnika, a ne pokrećite provjere više puta.

### Dokumentacija na GitHub Pages

Nakon svake integracije u granu `assignments`, iz komentara u VHDL opisima automatski se generiše dokumentacija alatom *Doxygen* i objavljuje na adresi `https://etf-unibl.github.io/pds-2026-test/`. Dokumentovanje dizajna je obavezno i ocjenjuje se, a postupak je opisan u uputstvu [Dokumentovanje dizajna](design-documentation.md). Na objavljenoj stranici provjerite da li je dokumentacija vašeg dizajna potpuna i ispravno prikazana.
