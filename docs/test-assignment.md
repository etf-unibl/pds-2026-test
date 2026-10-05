## Probni zadatak

Probni zadatak služi da se cijeli postupak predaje (grana, komit, *pull request*, automatske provjere, pregled) prođe jednom prije prvog zadatka koji se ocjenjuje. Probni zadatak se ne boduje, ali je njegovo uspješno završavanje preduslov za predaju ostalih zadataka.

### Kako prepoznati probni zadatak

Predmetni nastavnik na početku kursa svakom studentu kreira zaseban probni zadatak (*issue*) i dodjeljuje mu ga. Probni zadatak se od ostalih razlikuje po sljedećem:

- označen je labelom `good first issue`, dok su zadaci koji se ocjenjuju označeni labelom grupe zadataka kojoj pripadaju (`assignment-1` do `assignment-4`),
- automatske provjere za njega ne pokreću testove nastavnika (simulaciju i sintezu), već provjeravaju da li fajl `test.vhd` postoji i da li se prevodi bez grešaka, stil opisa i poštovanje pravila predaje.

Na osnovu labele automatske provjere određuju da li se radi o probnom zadatku ili zadatku koji se ocjenjuje. Labele postavlja nastavnik i studenti ih ne mijenjaju.

### Šta je potrebno predati

U folderu `assignments/<N>`, gdje je `<N>` broj probnog zadatka, potrebno je predati fajl `test.vhd` sa opisom jednostavnog kola po izboru (npr. NAND kolo sa dva ulaza). Entitet se obavezno zove `test` (a u zaglavlju fajla naziv jedinice `TEST`), jer pravila stila zahtijevaju da naziv fajla bude jednak nazivu entiteta. Fajl treba da sadrži deklaraciju entiteta i arhitekturu, da se prevodi bez grešaka (standard VHDL-2008), da bude formatiran u skladu sa uputstvom [Pravila za formatiranje VHDL opisa](vhdl-code-style.md) i dokumentovan prema uputstvu [Dokumentovanje dizajna](design-documentation.md).

```
assignments/
└── <N>/
    └── test.vhd
```

Opciono, uz dizajn se može predati i *testbench* (npr. `test_tb.vhd` sa entitetom `test_tb`), koji se tada automatski simulira ([Simulacija i testiranje](simulation-and-testing.md#automatsko-pokretanje-testbench-fajlova)).

### Postupak

Postupak je identičan postupku za zadatke koji se ocjenjuju, pa se ovdje navode samo koraci sa referencama na detaljna uputstva:

1. Otvorite probni zadatak u tabulatoru **Issues** i prebacite ga u kolonu *In Progress* na radnoj ploči.
2. Iz zadatka kreirajte granu sa izvornom granom `assignments` ([Proces rada u GitHub okruženju](github-workflow.md#kreiranje-grane-za-zadatak)) i lokalno se prebacite na nju. Naziv grane mora počinjati brojem zadatka (npr. `<N>-test-pull-request`), što je podrazumijevani naziv koji predlaže *GitHub*.

   ```
   git fetch origin
   git checkout <naziv-grane>
   ```

3. Napravite folder `assignments/<N>` i u njemu fajl `test.vhd`.
4. Lokalno provjerite fajl:

   ```
   ghdl -a --std=08 assignments/<N>/test.vhd
   vhdl-style <N>
   ```

   Umjesto *GHDL* alata može se koristiti i `vcom -2008` ([Simulacija i testiranje](simulation-and-testing.md)).
5. Komitujte (obavezno sa opcijom `-s`, koja dodaje potpis) i pošaljite izmjene ([Pravila prilikom predaje rješenja zadataka](assignment-submission.md#poruka-komita)):

   ```
   git add assignments/<N>
   git commit -s
   git push -u origin <naziv-grane>
   ```

6. Otvorite *pull request* prema grani `assignments` sa naslovom `Issue #<N> : <naslov zadatka>` i popunite opis prema šablonu koji se automatski prikazuje: kratak opis, lista izmjena i označene stavke provjere ([Proces rada u GitHub okruženju](github-workflow.md#otvaranje-pull-request-a)). Predmetni nastavnik se automatski dodaje kao recenzent.
7. Pratite automatske provjere ([Automatske provjere](automated-checks.md)). Za probni zadatak izvršavaju se poslovi `classify`, `pr-checks`, `linter` i `basic-test` (i `testbench`, ako ste predali *testbench*), dok je posao `verif` preskočen (označen sivom ikonom), što je očekivano.
8. Kada sve provjere prođu, prebacite zadatak u kolonu *In Review*. Ako provjera ne prođe, ispravite grešku na istoj grani i ponovo pošaljite izmjene.

Probni zadatak je završen kada ga nastavnik pregleda i integriše. Nakon toga ste spremni za rad na zadacima koji se ocjenjuju.

### Česte greške u probnom zadatku

- Naziv foldera ne odgovara broju zadatka ili sadrži znak `#`.
- Fajl nije nazvan tačno `test.vhd` (npr. `Test.vhd` ili `test.vhdl`) ili se entitet ne zove `test` (posao `linter` tada prijavljuje grešku `pds_002 [FileName]`).
- Naslov *pull request*-a nije identičan obliku `Issue #<N> : <naslov zadatka>`.
- Grana je kreirana iz grane `main` umjesto iz grane `assignments` ili njen naziv ne počinje brojem zadatka.
- Komit nije potpisan (izostavljena je opcija `-s`).

Ostali problemi i njihova rješenja opisani su u uputstvu [Rješavanje čestih problema](troubleshooting.md).
