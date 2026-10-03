<!-- template:begin -->
> **Šablonski repozitorijum.** Repozitorijum kursa se kreira opcijom **Use this template &rarr; Create a new repository** (uz označenu opciju **Include all branches**). Oznake (organizacija, repozitorijum, godina, naziv kursa) se popunjavaju automatski prilikom kreiranja, a ovo obavještenje i uputstvo za nastavnika se uklanjaju. Postupak je opisan u uputstvu [Priprema repozitorijuma kursa](docs/instructor/course-setup.md).
<!-- template:end -->

<!-- TODO (nastavnik): naziv kursa i godina izvođenja -->
# <Naziv kursa>

**Uputstva:**

- [Prvi koraci](docs/getting-started.md)
- [Instalacija alata](docs/tools-setup.md)
- [Podešavanje Git okruženja](docs/git-setup.md)
- [Proces rada u GitHub okruženju](docs/github-workflow.md)
- [Pravila prilikom predaje rješenja zadataka](docs/assignment-submission.md)
- [Probni zadatak](docs/test-assignment.md)
- [Pravila za formatiranje VHDL opisa](docs/vhdl-code-style.md)
- [Dokumentovanje dizajna](docs/design-documentation.md)
- [Simulacija i testiranje](docs/simulation-and-testing.md)
- [Automatske provjere](docs/automated-checks.md)
- [Rad na projektu](docs/project-workflow.md)
- [Evidencija utrošenog vremena](docs/time-tracking.md)
- [Rješavanje čestih problema](docs/troubleshooting.md)

Novi studenti počinju od uputstva [Prvi koraci](docs/getting-started.md).

**Informacije o kursu:**

Ispit se polaže kroz dvije cjeline:
1. priprema za izradu projekta i
2. rad na projektu.

Raspodjela bodova za navedene dvije cjeline je data u tabeli ispod.

| Priprema (50%) || Projekat (50%) |||
| :------: | :------: | :------: | :------: | :------: |
| Zadaci | Test | Dizajn | QA | Workflow |
| 25% | 25% | 20% | 20% | 10% |

Bodovi se ne objavljuju u ovom repozitorijumu, jer je javan.
<!-- TODO (nastavnik): navesti gdje studenti mogu vidjeti svoje bodove (npr. sistem za učenje na daljinu fakulteta). -->

**Zadaci:** Student radi četiri zadatka tokom prvog dijela kursa i jedan zadatak recenzije (*review*) na kraju kursa. Svaki zadatak nosi 5% ocjene. Svaki student se ocjenjuje individualno. Način predaje zadataka opisan je u uputstvu [Pravila prilikom predaje rješenja zadataka](docs/assignment-submission.md).

**Test:** Test se radi po završetku prvog dijela kursa (tačan datum će biti pravovremeno definisan) i čini ga 25 pitanja iz oblasti koje su obrađene u prvom dijelu kursa. Svaki student se ocjenjuje individualno.

**Dizajn:** Bodovi se određuju na osnovu procentualne ispunjenosti postavljenih zahtjeva i ciljeva projektnog zadatka. Svaki član tima dobija isti broj bodova.

**Quality Assurance (QA):** Boduje se pokrivenost dizajna odgovarajućim testovima ([Simulacija i testiranje](docs/simulation-and-testing.md)). Više bodova će ostvariti timovi koji budu koristili automatizovane testove. Ovaj segment takođe uključuje testiranje dizajna na stvarnom hardveru (evaluacionoj ploči). Svaki član tima dobija isti broj bodova.

| Pokrivenost testovima | Broj bodova |
| ------ | :------: |
| - dizajn ne sadrži manuelne testove <br> - dizajn ne sadrži automatizovane testove <br> - dizajn nije testiran na evaluacionoj ploči | 0% |
| - dizajn ne sadrži manuelne testove <br> - dizajn ne sadrži automatizovane testove <br> - dizajn je testiran na evaluacionoj ploči | 5% |
| - dizajn sadrži manuelne testove sa simulacijama <br> - dizajn ne sadrži automatizovane testove <br> - dizajn nije testiran na evaluacionoj ploči | 5% |
| - dizajn sadrži manuelne testove sa simulacijama <br> - dizajn ne sadrži automatizovane testove <br> - dizajn je testiran na evaluacionoj ploči | 10% |
| - dizajn sadrži automatizovane testove <br> - dizajn nije testiran na evaluacionoj ploči | 10% |
| - dizajn sadrži automatizovane testove <br> - dizajn je testiran na evaluacionoj ploči | 20% |

**Workflow:** Podrazumijeva bodove ostvarene na osnovu ocjene poštovanja radnog procesa ([Rad na projektu](docs/project-workflow.md)), tj. adekvatno i redovno ažuriranje liste radnih zadataka, ravnomjerna distribucija opterećenja u smislu rada na projektnim aktivnostima, korišćenje Git infrastrukture i prezentacija rezultata projekta (priprema video prezentacije na kraju projekta). Svaki student se ocjenjuje individualno osim u segmentu prezentacije rezultata projekta.

| Segment | Broj bodova |
| ------ | :------: |
| Adekvatno i ažurno vođenje evidencije o zadacima | 3% |
| Korišćenje Git infrastrukture | 3% |
| Ravnomjerna distribucija opterećenja | 2% |
| Prezentacija rezultata projekta | 2% |
