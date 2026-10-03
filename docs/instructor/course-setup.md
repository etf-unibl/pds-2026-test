## Priprema repozitorijuma kursa (uputstvo za nastavnika)

Ovo uputstvo navodi sve što je potrebno za pokretanje nove generacije kursa iz ovog šablonskog repozitorijuma (*template*). Uputstvo postoji samo u šablonu: *workflow* za inicijalizaciju ga uklanja iz kreiranog repozitorijuma, pa ga tokom pripreme kursa čitajte u šablonskom repozitorijumu. Uputstva za studente nalaze se u folderu `docs/` i ne zavise od godine izvođenja, a sve što se mijenja od generacije do generacije navedeno je u odjeljku [Vrijednosti koje se mijenjaju svake godine](#2-vrijednosti-koje-se-mijenjaju-svake-godine).

Oznake: `<organizacija>` je *GitHub* organizacija, `<repozitorijum>` repozitorijum kursa, a `<godina>` godina izvođenja kursa.

### 1. Kreiranje repozitorijuma

1. Kreirajte `<organizacija>/<repozitorijum>` iz šablona (**Use this template &rarr; Create a new repository**) i označite opciju **Include all branches**, kako bi bile kopirane grane `main`, `assignments` i `gh-pages`. Repozitorijum nazovite prema kursu i godini (npr. `pds-2026`), jer se na osnovu naziva popunjavaju oznake (vidi [Automatska inicijalizacija](#automatska-inicijalizacija)).
2. Grana `main` ostaje podrazumijevana grana. Ona sadrži dokumentaciju (`README.md`, `docs/`), koju studenti prvu vide, *workflow*-e koji koriste tajne ili ne smiju biti izmijenjeni *pull request*-om: `verif-tests.yml` (pravila predaje i testovi nastavnika) i `time-tracking.yml`, sa njihovim skriptama, kao i šablon *pull request*-a `.github/pull_request_template.md`. *GitHub* izvršava `pull_request_target`, *workflow*-e za komentare i rasporede samo sa podrazumijevane grane.
3. Grana `assignments` je nezavisna od grane `main` (nemaju zajedničku istoriju) i ne sadrži dokumentaciju, već samo foldere `.github/workflows/`, `.github/scripts/` (`classify.sh`), `.githooks/` (*Git hook*-ovi za studente) i `assignments/` (sa fajlovima `Doxyfile` i `read-me-first.txt`), fajlove `.github/CODEOWNERS`, `requirements.txt` i `LICENSE`, kao i `.gitignore`, `.gitattributes` i `.editorconfig`. *Workflow* za *pull request* izvršava se iz odredišne grane *pull request*-a, pa se *workflow*-i koji se izvršavaju u verziji iz *pull request*-a (`verif.yml`, `gh-pages.yml`) nalaze na grani `assignments`.
4. Grana `gh-pages` je prazna (jedan prazan komit). *Workflow* `GitHub Pages` je popunjava *Doxygen* dokumentacijom nakon svake integracije u granu `assignments`.
5. Svaki fajl se mijenja samo na svojoj grani: dokumentacija i `verif-tests.yml` / `time-tracking.yml` na grani `main`, a `verif.yml` i `gh-pages.yml` na grani `assignments`. Skripta `.github/scripts/classify.sh` postoji na obje grane (koriste je `verif-tests.yml` i `verif.yml`), pa dvije kopije držite jednakim. Grane se nikada ne integrišu jedna u drugu.

#### Automatska inicijalizacija

Kreiranjem repozitorijuma početni komit se šalje na granu `main`, čime se pokreće *workflow* `Initialize course repository` (`.github/workflows/init-course.yml`, skripta `.github/template/init_course.py`). Vrijednosti se određuju na osnovu novog repozitorijuma:

| Vrijednost | Izvor | Primjer |
| ------ | ------ | ------ |
| organizacija | vlasnik repozitorijuma | `etf-unibl` |
| repozitorijum | naziv repozitorijuma | `pds-2026` |
| godina | prvi broj oblika `20xx` u nazivu repozitorijuma, a ako ga nema, tekuća godina | `2026` |
| naziv kursa | naziv repozitorijuma velikim slovima | `PDS-2026` |

*Workflow* pravi dva komita kao `github-actions[bot]`:

- `main`: zamjenjuje oznake organizacije i repozitorijuma u fajlu `README.md` i folderu `docs/`, postavlja naziv kursa kao naslov u `README.md` i godinu u `LICENSE`, i uklanja obavještenje o šablonu iz `README.md`, ovo uputstvo (`docs/instructor/`) i skriptu (`.github/template/`),
- `assignments`: postavlja godinu u `LICENSE`, naziv kursa kao `PROJECT_NAME` u `assignments/Doxyfile` i nalog koji je kreirao repozitorijum kao vlasnika koda u `.github/CODEOWNERS` (tako svaki *pull request* automatski od njega traži pregled; po potrebi tu dodajte i ostale nastavnike ili tim).

Na kraju *workflow* trećim komitom briše sopstveni fajl, tako da u kreiranom repozitorijumu ne ostaje ništa od mehanizma šablona. Ako *GitHub* to odbije (fajlovi *workflow*-a mogu biti zaštićeni od izmjena ugrađenim tokenom), korak se završava obavještenjem; tada fajl `.github/workflows/init-course.yml` na grani `main` obrišite ručno. Kada skripta više ne postoji, *workflow* ništa ne radi, pa ni zaostali fajl ne smeta.

Rezultat provjerite u tabulatoru **Actions**. Ako se *workflow* nije pokrenuo (npr. *Actions* su isključene u organizaciji), uključite *Actions* i pokrenite ga ručno (**Actions &rarr; Initialize course repository &rarr; Run workflow**). Oznake koje nije uspio da zamijeni navedene su kao upozorenja u izvještaju.

### 2. Vrijednosti koje se mijenjaju svake godine

| Gdje | Vrijednost | Postaviti na |
| ------ | ------ | ------ |
| `README.md` (`main`) | raspodjela bodova, ako se mijenja; naslov se postavlja automatski | tekuća generacija |
| `README.md`, `docs/*.md` (`main`) | preostali `TODO` komentari (gdje se objavljuju bodovi, rokovi, lokacija projekta, zahtjevi za dokumentaciju) | tekuća generacija |
| repozitorijum za verifikaciju | `lookup/pds_<godina>_issues.lookup` | brojevi zadataka tekuće generacije i odgovarajući testovi, uključujući stavku `0` (NAND2 primjer, korak 7) |
| `requirements.txt` (`assignments`) | oznaka (*tag*) verzije `vhdl-style-tools` | verzija koja se koristi te godine (vidi uputstvo o stilu) |

Organizacija, repozitorijum, godina, naslov u `README.md`, `LICENSE` i `Doxyfile` postavljaju se [automatskom inicijalizacijom](#automatska-inicijalizacija). Prije početka kursa provjerite preostale stavke: `git grep -n TODO` na grani `main`.

*Workflow* pronalazi okruženje za verifikaciju bez dodatnih podešavanja (vidi korak 4). Podrazumijevane vrijednosti mogu se promijeniti opcionim varijablama repozitorijuma:

| Varijabla | Podrazumijevana vrijednost | Mijenja se kada |
| ------ | ------ | ------ |
| `PDS_LOOKUP_TABLE` | `pds_<godina>_issues.lookup`, gdje je `<godina>` prvi broj oblika `20xx` u nazivu repozitorijuma (a ako ga nema, tekuća godina) | *lookup* tabela ima drugačiji naziv |
| `PDS_VERIF_REPO` | `knezicm/pds-2022-verification` | okruženje za verifikaciju se premjesti u drugi repozitorijum |

### 3. Pristup i dozvole

1. Dodajte studente sa ulogom **Write** (najbolje kroz tim u organizaciji), kako bi mogli da šalju grane. Kopije repozitorijuma (*fork*) nisu podržane: testovi nastavnika se ne izvršavaju za *pull request* iz kopije.
2. Kreirajte *ruleset* (ili *branch protection rule*) za granu `assignments`:
   - integracija je moguća samo kroz *pull request* (direktno slanje izmjena je blokirano),
   - obavezne provjere: `classify`, `pr-checks`, `linter`, `basic-test`, `testbench`, `verif-setup` i `verif` (posao koji je preskočen zbog uslova računa se kao uspješan),
   - zabraniti *force push* i brisanje grane,
   - opciono, zahtijevati pregled vlasnika koda (nastavnika navedenih u `.github/CODEOWNERS`),
   - integraciju i zaobilaženje pravila dozvoliti samo nastavnicima.
3. Granu `main` zaštitite na isti način ili ograničite slanje izmjena samo na nastavnike. Ova pravila štite i tajne: okruženja iz koraka 4 daju ih samo *workflow*-ima sa grane `main`, pa granu `main` (kao i granu `assignments`, čiji se sadržaj testira) ne smije moći da mijenja niko osim nastavnika (vidi [Bezbjednost](#9-bezbjednost)).
4. **Settings &rarr; Actions &rarr; General &rarr; Approval for running fork pull request workflows from contributors**: odaberite **Require approval for all external contributors**. U javnom repozitorijumu bilo ko može otvoriti *pull request* iz kopije; uz ovo podešavanje njegovi *workflow*-i čekaju odobrenje nastavnika.

### 4. Actions, tajne, varijable i *runner*

1. **Settings &rarr; Actions &rarr; General**: dozvolite *Actions* i postavite **Workflow permissions** na *Read and write* (potrebno za objavljivanje na grani `gh-pages`).
2. **Settings &rarr; Environments**: kreirajte dva okruženja (*environment*) i svako ograničite na jednu granu (**Deployment branches and tags &rarr; Selected branches and tags &rarr; Add deployment branch or tag rule**):
   - `verification`, grana `main`, sa tajnom `PDS_PAT`: *fine-grained personal access token* sa dozvolom *Contents: Read* za (privatni) repozitorijum za verifikaciju,
   - `time-tracking`, grana `main`, sa tajnom `PDS_PROJECT_TOKEN` (vidi [Evidencija utrošenog vremena](#evidencija-utrošenog-vremena)).

   Tokene **ne** dodajte kao tajne repozitorijuma (**Settings &rarr; Secrets and variables &rarr; Actions**): tajna repozitorijuma dostupna je *workflow*-ima sa svih grana, uključujući grane koje šalju studenti, dok se tajna okruženja daje samo poslovima koji se izvršavaju na dozvoljenoj grani. Zabilježite datume isteka tokena i obnovite ih prije kraja kursa. Svaki posao koji koristi okruženje prikazuje se kao *deployment* tog okruženja, što je očekivano.
3. **Settings &rarr; Secrets and variables &rarr; Actions &rarr; Variables**: samo ako podrazumijevana vrijednost iz odjeljka [Vrijednosti koje se mijenjaju svake godine](#2-vrijednosti-koje-se-mijenjaju-svake-godine) ne odgovara, dodajte `PDS_LOOKUP_TABLE` i/ili `PDS_VERIF_REPO`. *Lookup* tabela koja se koristi ispisuje se u poslovima `classify` i `verif-setup`.
4. **Settings &rarr; Actions &rarr; Runners &rarr; New self-hosted runner**: registrujte računar na kojem se izvršava posao `verif` i instalirajte *runner* kao servis, uz mjere opisane u odjeljku [Bezbjednost](#9-bezbjednost). Na računaru su potrebni `python3`, *ModelSim* i *Quartus* na putanjama koje koristi `verif-tests.yml` (`$HOME/intelFPGA_lite/<verzija>/...`). Ako se verzija alata promijeni, ažurirajte putanje. *Workflow*-i koriste akcije koje se izvršavaju na *Node.js 24*, za šta je potrebna verzija *runner*-a 2.327.1 ili novija; *runner* se podrazumijevano sam ažurira, pa automatsko ažuriranje ostavite uključeno.
5. **Settings &rarr; Pages**: postavite **Source** na *Deploy from a branch*, grana `gh-pages`, folder `/ (root)`. Stranica (`https://<organizacija>.github.io/<repozitorijum>/`) ostaje prazna dok se u granu `assignments` ne integrišu prvi VHDL fajlovi.
6. Ako *self-hosted runner* nije dostupan, umjesto njega se može koristiti posao `pds-verification` (samo simulacija, *ModelSim* se instalira tokom izvršavanja): u fajlu `verif-tests.yml` u njegovom uslovu zamijenite `false &&` sa `true &&`, a uslov posla `verif` postavite na `false`.

### 5. *Workflow* za verifikaciju

Za svaki *pull request* prema grani `assignments` izvršavaju se dva *workflow*-a sa grane `assignments`:

- `verification` (`.github/workflows/verif.yml`, okidač `pull_request`): provjere koje izvršavaju studentski kod, ali im nisu potrebne tajne (stil, `test.vhd`, *testbench* fajlovi). Izvršava se u verziji iz *pull request*-a, pa bi ga student mogao oslabiti u svom *pull request*-u; nema tajni koje bi se mogle otkriti, a takva izmjena ne prolazi `pr-checks` (fajlovi izvan foldera `assignments/<N>`) i vidljiva je u tabulatoru **Files changed**.
- `verification-tests` (`.github/workflows/verif-tests.yml`, okidač `pull_request_target`): pravila predaje (`pr-checks`) i testovi nastavnika sa tokenom `PDS_PAT`. Uvijek se izvršava u verziji *workflow*-a i skripti sa podrazumijevane grane `main` (pravilo *GitHub* platforme za `pull_request_target`), iz *pull request*-a preuzima samo folder `assignments/<N>`, kao podatke i bez pristupnih podataka, i preskače *pull request*-ove iz kopija repozitorijuma.

Oba određuju zadatak zajedničkom skriptom `.github/scripts/classify.sh`.

| Posao | Namjena | Izvršava se za |
| ------ | ------ | ------ |
| `classify` | broj zadatka (prvi broj u naslovu *pull request*-a), vrsta zadatka na osnovu labela, postojanje *testbench* fajlova, naziv *lookup* tabele | uvijek |
| `pr-checks` | pravila predaje (vidi ispod; `verification-tests`) | *pull request*-ove |
| `linter` | stil opisa (`vhdl-style`) | probne zadatke i zadatke koji se ocjenjuju |
| `basic-test` | `assignments/<N>/test.vhd` postoji i prevodi se | probne zadatke |
| `testbench` | *GHDL* simulacija svakog fajla `assignments/<N>/*_tb.vhd` (entitet nazvan kao fajl, VHDL-93, neuspjeh za `assert` nivoa `error`/`failure`, prekid nakon 10 ms simuliranog vremena, talasni oblici u artifaktu `testbench-waveforms`) | zadatke uz koje je predat *testbench* |
| `verif-setup` | broj i vrsta zadatka za testove nastavnika (`verification-tests`) | *pull request*-ove sa grana repozitorijuma, ručna pokretanja |
| `verif` | testovi nastavnika (simulacija i sinteza) na *self-hosted runner*-u (`verification-tests`, okruženje `verification`) | zadatke koji se ocjenjuju i NAND2 primjer |

Posao `pr-checks` upoređuje *pull request* sa zadatkom i prijavljuje svako prekršeno pravilo:

1. naslov je jednak `Issue #<N> : <naslov zadatka>` (razlike u razmacima se zanemaruju),
2. naziv izvorne grane počinje sa `<N>-`,
3. autor *pull request*-a je među osobama kojima je zadatak `<N>` dodijeljen,
4. dodati, izmijenjeni, obrisani ili premješteni su samo fajlovi u folderu `assignments/<N>/`,
5. svaki komit osim komita integracije (*merge*) sadrži `Signed-off-by: <ime autora> <email autora>` koji odgovara autoru komita (`git commit -s`),
6. poruka svakog komita osim komita integracije ima oblik `Issue #<N> : <naslov zadatka>`, prazan red i bar jednu stavku liste `- `,
7. opis prati šablon *pull request*-a: sekcije označene sa `<!-- section:summary -->` i `<!-- section:changes -->` su popunjene, a svaka linija označena sa `<!-- check:... -->` je označena ([x]).

Zajedno, ove provjere sprečavaju da se rješenje greškom preda za pogrešan zadatak, iako više zadataka dijeli istu labelu grupe. Pravila su realizovana u skripti `.github/scripts/pr_rules.py` na grani `main`; skripta samo čita podatke preko API-ja.

Studenti za ova pravila imaju dva pomoćna alata (opisana u uputstvima za studente):

- ***Git hook*-ovi** u folderu `.githooks/` na grani `assignments`, koji se uključuju jednom komandom `git config core.hooksPath .githooks`: `prepare-commit-msg` popunjava `Issue #<N> : <naslov zadatka>` (broj iz naziva grane, naslov preko javnog API-ja), `commit-msg` provjerava pravila 5 i 6 (i da broj odgovara grani), a `pre-commit` pravilo 4. *Hook*-ovi se mogu zaobići, pa je `pr-checks` i dalje ono što pravila sprovodi.
- **Šablon *pull request*-a** `.github/pull_request_template.md` na grani `main` (*GitHub* čita šablone sa podrazumijevane grane) automatski popunjava opis svakog *pull request*-a. Oznake `section:` i `check:` u šablonu koristi `pr_rules.py`, pa ih pri izmjenama šablona zadržite (ili uskladite skriptu). Kao naslov *GitHub* predlaže prvi red poruke komita ako grana ima jedan komit, a inače naziv grane.

#### Labele: probni zadaci i zadaci koji se ocjenjuju

| | Probni zadatak | Zadatak koji se ocjenjuje |
| ------ | ------ | ------ |
| labela | `good first issue` (podrazumijevana *GitHub* labela) | tačno jedna labela grupe zadataka, `assignment-1` do `assignment-4`, zajednička za sve zadatke te grupe |
| očekivani fajlovi | `assignments/<N>/test.vhd` | prema postavci zadatka |
| poslovi | `classify`, `pr-checks`, `linter`, `basic-test` (+ `testbench`) | `classify`, `pr-checks`, `linter`, `verif` (+ `testbench`) |
| *lookup* tabela | nije potrebna | mora sadržati broj zadatka |

Ostale labele zadatka (npr. `task`, `bug`) se zanemaruju, pa zadatak može imati proizvoljan broj dodatnih labela. Posao `classify` ne prolazi ako zadatak nema ni labelu `good first issue` ni labelu `assignment-<n>`, ako ima obje vrste ili ako ima više labela `assignment-<n>`. Zbog toga se zadaci koji imaju samo druge labele, npr. projektni zadaci sa labelom `task`, ne mogu predati na granu `assignments`; *pull request*-ovi projekta treba da budu usmjereni na granu projekta. Izmjena labele ne pokreće *workflow* ponovo; ponovno pokretanje se postiže izmjenom naslova ili opisa *pull request*-a ili opcijom **Re-run jobs**.

<!-- TODO (nastavnik): opisati kako se predaje zadatak recenzije na kraju kursa (labela i grana), ako prolazi kroz ovaj workflow. -->

Ako ne želite provjeru stila za probne zadatke, uslov posla `linter` promijenite u `${{ needs.classify.outputs.kind == 'assignment' }}`.

### 6. Radna ploča, labele, *milestone*-ovi i zadaci

1. Kreirajte projekat (**Projects &rarr; New project &rarr; Board**) sa kolonama *Backlog*, *To Do*, *In Progress*, *In Review*, *Done* i povežite ga sa repozitorijumom (tabulator **Projects** repozitorijuma &rarr; **Link a project**).
2. Labele koje koristi *workflow* (vidi korak 5): `good first issue` (postoji podrazumijevano u novim repozitorijumima; ako je obrisana, kreirajte je ponovo) i četiri labele grupa zadataka `assignment-1` &hellip; `assignment-4`. Za projekat: `task`, a po potrebi i `bug`, `documentation`.
3. *Milestone*-ovi: po jedan za svaki dio kursa ili sedmicu, sa postavljenim rokom (to je rok koji studenti vide). Probni zadaci pripadaju istom *milestone*-u kao i zadaci prvog dijela kursa.
4. Kreirajte po jedan probni zadatak za svakog studenta (labela `good first issue`, dodijeljen studentu, povezan sa pločom). U opisu zadatka dovoljno je uputiti na `docs/test-assignment.md`.
5. Kreirajte zadatke koji se ocjenjuju, po jedan za svakog studenta i svaki zadatak, svaki sa labelom odgovarajuće grupe (`assignment-1` &hellip; `assignment-4`) i **dodijeljen studentu** (to zahtijeva posao `pr-checks`). Brojeve zadataka dodjeljuje *GitHub*, pa zadatke treba **prvo** kreirati, a zatim *lookup* tabelu u repozitorijumu za verifikaciju popuniti stvarnim brojevima. Svaki zadatak mora navesti tražene nazive fajlova, entiteta i portova, jer ih testovi za verifikaciju koriste.

#### Evidencija utrošenog vremena

Studenti evidentiraju vrijeme po zadatku ručno, u polju projekta `Time spent (h)`, ili komentarima `/spent` ([docs/time-tracking.md](../time-tracking.md)). *Workflow* `Time tracking` (`.github/workflows/time-tracking.yml` i `.github/scripts/time_tracking.py` na grani `main`) sabira oba izvora:

- komentar `/spent` (dodat, izmijenjen ili obrisan) odmah ponovo izračunava polja `Time logged (h)` i `Time total (h)` zadatka i označava komentar reakcijom 👍 (ispravan) ili 😕 (neispravan unos),
- svakog ponedjeljka u 05:00 UTC, kao i pri svakom ručnom pokretanju (**Actions &rarr; Time tracking &rarr; Run workflow**), ponovo izračunava sve zadatke sa radne ploče i pravi izvještaj: zakačeni (*pinned*) zadatak *Izvještaj o utrošenom vremenu* (labela `time-report`), sažetak pokretanja i CSV fajlove `time-per-student.csv`, `time-per-issue.csv` i `time-entries.csv` (artifakt `time-report`, čuva se 90 dana). Ručno unijeto vrijeme i procjena zadatka sa više dodijeljenih studenata dijele se na jednake dijelove, a unosi `/spent` pripisuju se autoru komentara.

Podešavanje:

1. Kreirajte *fine-grained personal access token* (**avatar &rarr; Settings &rarr; Developer settings &rarr; Personal access tokens &rarr; Fine-grained tokens**). Koristite zaseban token, a ne `PDS_PAT`:
   - **Resource owner**: organizacija (`<organizacija>`); ako organizacija zahtijeva odobravanje *fine-grained* tokena, odobrite zahtjev u podešavanjima organizacije,
   - **Repository access**: samo repozitorijum kursa, sa dozvolom **Issues: Read and write** (komentari, reakcije, labele i zadatak sa izvještajem),
   - **Organization permissions**: **Projects: Read and write**,
   - rok važenja: do kraja kursa.
2. Sačuvajte ga kao tajnu `PDS_PROJECT_TOKEN` okruženja `time-tracking` (korak 4.2), a ne kao tajnu repozitorijuma. Reakcije, zadatak sa izvještajem i izmjene na projektu prikazuju se pod nalogom vlasnika tokena. Uzimaju se u obzir samo komentari `/spent` osoba kojima je zadatak dodijeljen i saradnika repozitorijuma / članova organizacije, pa se komentari osoba izvan kursa u javnom repozitorijumu zanemaruju.
3. *Workflow* koristi jedini otvoreni projekat povezan sa repozitorijumom. Ako je povezano više projekata, postavite varijablu repozitorijuma `PDS_PROJECT_NUMBER` na broj projekta kursa (iz njegove adrese).
4. Brojčana polja `Estimate (h)`, `Time spent (h)`, `Time logged (h)` i `Time total (h)` kreiraju se automatski pri prvom pokretanju, a mogu se kreirati i ručno, sa tačno ovim nazivima. Prije početka kursa jednom ručno pokrenite *workflow*, kako bi polja bila kreirana.
5. Preporuka: dodajte tabelarni prikaz projekta sa ova četiri polja kao kolonama, grupisan po polju **Assignees**, sa uključenim zbirom (**Field sum**) za `Time total (h)`.

Repozitorijum može imati najviše tri zakačena zadatka, a zadatak sa izvještajem zauzima jedno mjesto.

### 7. Provjera okruženja za verifikaciju

Repozitorijum za verifikaciju sadrži NAND2 primjer, koji je u *lookup* tabeli registrovan kao zadatak `0`. Njime se provjerava kompletan posao `verif` (*runner*, putanje do *ModelSim* i *Quartus* alata, `PDS_PAT`, *lookup* tabela) bez ikakvog studentskog rješenja. Primjer pokrenite:

- prije prvog zadatka, nakon svake izmjene na računaru sa *runner*-om ili verzijama alata, kao i kad god posao `verif` ne prolazi iz razloga koji nisu povezani sa predatim rješenjem,
- opcijom **Actions &rarr; verification-tests &rarr; Run workflow**, grana `main`, broj zadatka `0` (ručno pokretanje testira granu `assignments`).

Za zadatak `0` izvršavaju se samo poslovi `verif-setup` i `verif`; posao `verif` mora proći, a artifakt `verif-artifacts` mora sadržati rezultate simulacije i sinteze primjera. Provjerite da *lookup* tabela tekuće generacije sadrži stavku `0`.

### 8. Provjera prije početka kursa

Sa probnim nalogom (ili sopstvenim) prođite kompletno uputstvo `docs/getting-started.md`:

- [ ] NAND2 primjer (zadatak `0`, korak 7) prolazi posao `verif` i artifakt `verif-artifacts` sadrži njegove rezultate,
- [ ] kloniranje preko SSH, kreiranje grane iz probnog zadatka, dodavanje `assignments/<N>/test.vhd` potpisanim komitom i otvaranje *pull request*-a sa propisanim naslovom: izvršavaju se `classify`, `pr-checks`, `linter` i `basic-test`, a `verif` je preskočen,
- [ ] dodavanje *testbench* fajla `*_tb.vhd`: izvršava se posao `testbench`, koji ne prolazi kada *testbench* prijavi grešku naredbom `assert`,
- [ ] isto za zadatak koji se ocjenjuje: `verif` se izvršava na *self-hosted runner*-u i artifakt `verif-artifacts` se može preuzeti,
- [ ] `pr-checks` ne prolazi za pogrešan naslov, granu čiji naziv ne počinje brojem zadatka, zadatak koji nije dodijeljen autoru, fajl izmijenjen izvan foldera `assignments/<N>/`, komit bez potpisa, poruku komita u pogrešnom formatu i opis sa praznom sekcijom ili neoznačenom stavkom provjere,
- [ ] sa uključenim *Git hook*-ovima (`git config core.hooksPath .githooks`) komanda `git commit -s` na grani zadatka popunjava naslov zadatka, a novi *pull request* dobija opis iz šablona i prolazi `pr-checks` kada se popune sekcije i označe stavke provjere; nastavnik se automatski dodaje kao recenzent,
- [ ] *pull request* sa pogrešnim brojem zadatka u naslovu ne prolazi posao `classify`,
- [ ] neuspješne obavezne provjere blokiraju integraciju,
- [ ] integracija u granu `assignments` objavljuje *Doxygen* dokumentaciju na adresi `https://<organizacija>.github.io/<repozitorijum>/`,
- [ ] komentar `/spent 1h` u zadatku ažurira njegova polja `Time logged (h)` i `Time total (h)` i dobija reakciju 👍; ručno pokretanje *workflow*-a **Time tracking** ažurira zakačeni zadatak sa izvještajem i prilaže CSV fajlove,
- [ ] bezbjednost ([Bezbjednost](#9-bezbjednost)): oba tokena postoje samo kao tajne okruženja; probna grana sa *workflow*-om koji koristi okruženje `verification` biva odbijena (*Branch is not allowed to deploy*); podešeno je odobravanje *workflow*-a iz kopija; *self-hosted runner* prihvata samo `verif-tests.yml` sa grane `assignments` (ako su dostupne grupe *runner*-a).

### 9. Bezbjednost

Repozitorijum kursa je javan, a svaki student ima pravo pisanja. Ovaj odjeljak opisuje prijetnje i mjere ugrađene u šablon, kao i šta je potrebno uraditi za *self-hosted runner*.

#### Ko može izvršiti kod sa tajnama

Svako ko ima pravo pisanja može poslati granu sa sopstvenim fajlom *workflow*-a (slanje preko SSH ne ograničava izmjene fajlova *workflow*-a) i može izmijeniti fajlove *workflow*-a u *pull request*-u. Takvi *workflow*-i se izvršavaju sa svim tajnama **repozitorijuma**. Zato šablon ne koristi tajne repozitorijuma:

- `PDS_PAT` je tajna okruženja `verification`, ograničenog na granu `main`; koristi je samo `verif-tests.yml`, koji se izvršava na okidač `pull_request_target`, tj. uvijek u verziji sa podrazumijevane grane `main`, i od studenta preuzima samo folder `assignments/<N>`, kao podatke i bez pristupnih podataka,
- `PDS_PROJECT_TOKEN` je tajna okruženja `time-tracking`, ograničenog na granu `main`; *workflow* za evidenciju vremena izvršava se samo sa grane `main` (događaji komentara i rasporedi uvijek koriste podrazumijevanu granu),
- `verif.yml`, koji se izvršava u verziji iz *pull request*-a, koristi samo `GITHUB_TOKEN` sa pravom čitanja.

Ovo važi samo dok studenti ne mogu mijenjati granu `main` (i granu `assignments`): zadržite pravila iz [koraka 3](#3-pristup-i-dozvole) (obavezan *pull request*, bez *force push*-a i brisanja, zaobilaženje samo za nastavnike) i povremeno provjerite da nisu dodate nove tajne repozitorijuma.

Preostali rizik: simulator na *runner*-u i dalje izvršava studentski VHDL opis. VHDL može čitati i pisati fajlove (`std.textio`) kojima korisnik *runner*-a ima pristup, pa se na *runner*-u ne smije nalaziti ništa što studenti ne smiju vidjeti (vidi ispod).

#### *Self-hosted runner*

*Self-hosted runner* je najosjetljiviji dio: **bilo koji** *workflow* repozitorijuma može zatražiti `runs-on: self-hosted`, uključujući *workflow* na grani koju je poslao student, i zatim izvršiti proizvoljne komande na računaru. Okruženja to ne sprečavaju. *GitHub* ne preporučuje *self-hosted runner*-e za javne repozitorijume, pa primijenite što više sljedećih mjera:

1. **Ograničite *runner* na zvanični *workflow* (preporučeno).** Grupe *runner*-a u organizaciji mogu se ograničiti na odabrane *workflow*-e: **podešavanja organizacije &rarr; Actions &rarr; Runner groups &rarr; New runner group**, pristup samo repozitorijumu kursa, uključena opcija **Allow public repositories**, i **Workflow access &rarr; Selected workflows** sa `<organizacija>/<repozitorijum>/.github/workflows/verif-tests.yml@refs/heads/main`. *Runner* registrujte u ovoj grupi. Tada *runner* ne prihvata poslove drugih *workflow*-a, drugih grana ni izmijenjenog `verif-tests.yml` iz *pull request*-a, dok `pull_request_target` i ručna pokretanja sa grane `main` zadovoljavaju pravilo. Grupe *runner*-a sa odabranim *workflow*-ima zahtijevaju *GitHub Team* ili *Enterprise* plan; obrazovne ustanove mogu besplatno dobiti *GitHub Team* kroz *GitHub Education*, pa provjerite plan organizacije (**podešavanja organizacije &rarr; Billing and plans**).
2. ***Runner* za jednokratnu upotrebu.** Registrujte ga komandom `./config.sh --ephemeral`: *runner* prihvata samo jedan posao i zatim se odjavljuje. U kombinaciji sa virtuelnom mašinom ili kontejnerom koji se nakon svakog posla vraća u čisto stanje (i skriptom ponovo registruje), ništa što posao ostavi ne prelazi na sljedeći posao.
3. **Zaštitite računar.**
   - *Runner* izvršavajte kao zaseban korisnik bez administratorskih (`sudo`) prava.
   - Na računaru ne držite ništa drugo: SSH ključeve, tokene, sesije pregledača, druge repozitorijume ni lične podatke. Repozitorijum za verifikaciju preuzima se za svaki posao i ne smije trajno ostati na računaru.
   - Računar smjestite u zaseban mrežni segment, bez pristupa internoj mreži fakulteta, po mogućnosti sa odlaznim saobraćajem ograničenim na *GitHub* i adrese koje alati zahtijevaju.
   - Redovno ažurirajte operativni sistem i alate i povremeno pregledajte zapise *runner*-a (folder `_diag`).
4. **Ograničite vrijeme dostupnosti.** Ako nijedna od navedenih mjera nije moguća, zaustavite servis *runner*-a izvan perioda predaje zadataka ili umjesto njega koristite posao `pds-verification` na *GitHub* infrastrukturi (samo simulacija, bez sinteze; vidi korak 4.6).

#### *Pull request*-ovi iz kopija

U javnom repozitorijumu bilo ko može otvoriti *pull request* iz kopije. *Pull request* iz kopije nikada ne dobija tajne, `verif-tests.yml` ga preskače, a uz podešavanje odobravanja iz [koraka 3](#3-pristup-i-dozvole) ostale provjere čekaju odobrenje nastavnika. Ne odobravajte pokretanja *workflow*-a nepoznatih osoba.

#### Javni podaci

- **Bodovi:** šablon ne sadrži tabele sa bodovima; bodove čuvajte izvan repozitorijuma (npr. u sistemu za učenje na daljinu fakulteta) i u `README.md` navedite gdje ih studenti mogu vidjeti.
- **Email adrese:** svaki komit sadrži email adresu autora, i to i u obaveznom potpisu. Uputstvo za studente preporučuje privatnu *GitHub* adresu (`...@users.noreply.github.com`).
- **Izvještaj o vremenu:** zakačeni zadatak sa izvještajem, CSV artifakti i polja projekta (ako je projekat javan) prikazuju broj sati po studentu. O tome obavijestite studente na početku kursa, a ako polja ne treba da budu javna, postavite vidljivost projekta na privatnu.
- **Artifakti:** artifakte pokretanja u javnom repozitorijumu (npr. `verif-artifacts`) može preuzeti svaki prijavljeni korisnik *GitHub* platforme. Provjerite da rezultati simulacije ne otkrivaju testne vektore iz repozitorijuma za verifikaciju ili skratite `retention-days`.

#### Tokeni

- Koristite *fine-grained* tokene sa minimalnim dozvolama navedenim iznad, samo za repozitorijum kursa (i repozitorijum za verifikaciju), sa rokom važenja do kraja kursa.
- `PDS_PAT` i `PDS_PROJECT_TOKEN` držite odvojeno, tako da otkrivanje jednog ne ugrožava drugi. Dozvola *Projects* ne može se ograničiti na jedan projekat, već obuhvata sve projekte organizacije.
- Oba tokena djeluju u ime svog vlasnika; umjesto njih može se koristiti *GitHub App*, ali to ne smanjuje dozvolu *Projects*.
- Ako postoji sumnja da je token otkriven, odmah ga opozovite (**Settings &rarr; Developer settings &rarr; Personal access tokens**) i kreirajte novi.

### 10. Završetak kursa

- Preuzmite konačni izvještaj o utrošenom vremenu (ručno pokrenite **Time tracking** i preuzmite artifakt `time-report`).
- Uklonite studentima pravo pisanja (ili arhivirajte repozitorijum: **Settings &rarr; Archive this repository**).
- Zaustavite ili uklonite *self-hosted runner* i opozovite `PDS_PAT` i `PDS_PROJECT_TOKEN`.
- Poboljšanja dokumentacije i *workflow*-a prenesite i u šablonski repozitorijum, a ne samo u repozitorijum tekuće generacije.
