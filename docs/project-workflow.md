## Rad na projektu

U drugom dijelu kursa studenti rade u timovima na projektnom zadatku. Proces rada je isti kao kod zadataka (zadatak &rarr; grana &rarr; *pull request* &rarr; pregled &rarr; integracija, [Proces rada u GitHub okruženju](github-workflow.md)), uz razlike opisane u nastavku.

<!-- TODO (nastavnik): navesti gdje se nalazi kod projekta (zaseban repozitorijum tima ili folder/grana u repozitorijumu kursa), naziv odredišne grane i rokove za pojedine faze projekta. -->

### Organizacija tima

- Tim na početku projekta dijeli projektni zadatak na manje, jasno definisane zadatke (*issues*) i raspoređuje ih po *milestone*-ovima.
- Svaki zadatak ima opis sa kriterijumom završetka (šta mora biti urađeno da bi se zadatak smatrao završenim) i dodijeljenog člana tima (**Assignees**).
- Zadatak treba da bude dovoljno mali da se završi u toku jedne sedmice. Veći zadaci se dijele na podzadatke.
- Ploča projekta se ažurira redovno, najmanje jednom sedmično, tako da u svakom trenutku odražava stvarno stanje.
- Za svaki zadatak se unosi procjena i evidentira utrošeno vrijeme ([Evidencija utrošenog vremena](time-tracking.md)). Na zadacima na kojima radi više članova tima preporučuje se evidencija komentarima `/spent`, jer se vrijeme tada pripisuje svakom članu pojedinačno.
- Rad treba ravnomjerno rasporediti među članovima tima. Doprinos svakog člana vidljiv je iz dodijeljenih zadataka, komita i pregleda *pull request*-ova.

### Grane i integracija

- Svaki član radi na granama svojih zadataka, a nikada direktno na glavnoj grani projekta.
- Svaki *pull request* pregleda najmanje jedan drugi član tima (**Reviewers**), uz predmetnog nastavnika.
- Pregled podrazumijeva čitanje izmjena, lokalno pokretanje simulacije i komentare u tabulatoru **Files changed**. Odobrenje se daje opcijom **Review changes &rarr; Approve**, a zahtjev za izmjenama opcijom **Request changes**.
- Prije otvaranja *pull request*-a grana zadatka se usklađuje sa glavnom granom projekta, kako bi se konflikti riješili prije pregleda:

```
git fetch origin
git merge origin/<glavna-grana-projekta>
```

Ako dođe do konflikta, *Git* označava sporne dijelove fajlova oznakama `<<<<<<<`, `=======` i `>>>>>>>`. Konflikt se rješava ručnom izmjenom fajla (zadržavanjem ispravnog sadržaja i brisanjem oznaka), nakon čega slijede `git add <fajl>` i `git commit -s`. I u radu na projektu svaki komit mora biti potpisan.

### Kvalitet (QA)

- Za svaki modul dizajna piše se *testbench*. Prednost imaju automatizovani (samoprovjeravajući) testovi ([Simulacija i testiranje](simulation-and-testing.md)).
- Testovi se predaju zajedno sa modulom koji testiraju, u istom *pull request*-u.
- Dizajn se na kraju testira i na evaluacionoj ploči. Postupak i rezultate testiranja (npr. fotografije ili kratak video) treba dokumentovati u zadatku ili *pull request*-u.

### Završetak projekta

- Kompletan kod projekta je integrisan u glavnu granu i sve automatske provjere prolaze.
- Tim priprema video prezentaciju rezultata projekta i dostavlja je na način koji definiše predmetni nastavnik.
- Svi zadaci na ploči su zatvoreni ili je jasno označeno šta nije završeno.

Način bodovanja projekta opisan je na početnoj stranici repozitorijuma.
