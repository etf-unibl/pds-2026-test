## Proces rada u GitHub okruženju

Rad na kursu organizovan je kroz zadatke (*issues*) koji se prate na radnoj ploči projekta (*GitHub Projects*). Svaki zadatak prolazi isti životni vijek:

```
zadatak (issue) -> grana (branch) -> komiti (commits) -> pull request -> automatske provjere -> pregled -> integracija (merge)
```

U uputstvu se nazivi elemenata korisničkog interfejsa *GitHub* platforme navode na engleskom jeziku, onako kako se prikazuju. Raspored elemenata se s vremenom mijenja, pa ako neki element ne nađete na opisanom mjestu, potražite ga po nazivu.

### Radna ploča

Radna ploča projekta dostupna je u tabulatoru **Projects** repozitorijuma. Zadaci su raspoređeni u kolone koje opisuju njihov status:

| Kolona | Značenje |
| ------ | ------ |
| *Backlog* | zadaci koji su definisani, ali još nisu planirani |
| *To Do* | zadaci planirani za tekuću sedmicu |
| *In Progress* | zadaci na kojima se trenutno radi |
| *In Review* | zadaci za koje je otvoren *pull request* i koji čekaju pregled |
| *Done* | pregledani i integrisani zadaci |

Status zadatka se mijenja prevlačenjem kartice u odgovarajuću kolonu ili izborom vrijednosti u polju *Status* unutar zadatka. Važno je da status na ploči uvijek odgovara stvarnom stanju, jer se ažurnost ploče ocjenjuje (segment *Workflow*).

### Kreiranje zadatka

Zadatke za prvi dio kursa kreira predmetni nastavnik. U radu na projektu zadatke kreiraju članovi tima, na sljedeći način:

1. Na radnoj ploči, na dnu željene kolone (tipično *Backlog*), kliknite na **Add item** i unesite naziv zadatka. Zadatak se kreira kao nacrt (*draft*).
2. Kliknite na naziv zadatka i dodajte opis (**Edit**, a zatim **Update comment**). Opis treba da bude dovoljno jasan da bilo koji član tima može da razumije šta je cilj zadatka i kada se smatra završenim.
3. U desnom dijelu prozora dodijelite zadatak članu tima (**Assignees**) i konvertujte ga u *issue* (**Convert to issue**), pri čemu birate repozitorijum kursa. Tek nakon konverzije zadatak dobija broj (npr. `#55`) i vidljiv je u tabulatoru **Issues**.
4. Dodajte labelu (**Labels**, tipično `task`) i odgovarajući *milestone* (**Milestone**).
5. U sekciji projekta unesite procjenu potrebnog vremena u polje `Estimate (h)`. Utrošeno vrijeme evidentira se tokom rada, kako je opisano u uputstvu [Evidencija utrošenog vremena](time-tracking.md).

### Kreiranje grane za zadatak

Za svaki zadatak radi se na zasebnoj grani, koja se najjednostavnije kreira iz samog zadatka:

1. Otvorite zadatak (tabulator **Issues**) i u desnom dijelu prozora, u sekciji **Development**, kliknite na **Create a branch**.
2. Kliknite na **Change branch source** i u polju **Branch source** odaberite granu `assignments` (ili drugu granu koju definiše nastavnik, npr. za projekat).
3. Po potrebi promijenite naziv grane u polju **Branch name**. Podrazumijevani naziv počinje brojem zadatka i preporučuje se da se zadrži. Naziv grane **mora** počinjati brojem zadatka i crticom (npr. `55-create-nand2-circuit`), što se automatski provjerava. Ako više članova tima radi na istom zadatku, svako koristi svoju granu sa različitim nazivom (npr. `55-create-nand2-circuit-ana`).
4. Odaberite opciju **Checkout locally** i kliknite na **Create branch**.

Nakon kreiranja grane, *GitHub* prikazuje komande kojima se lokalno prebacujete na nju. One su oblika:

```
git fetch origin
git checkout <naziv-grane>
```

Zadatak prebacite u kolonu *In Progress*.

**Napomena:** Grana se može kreirati i lokalno (`git checkout -b <N>-<opis> origin/assignments`, gdje je `<N>` broj zadatka) i poslati na *GitHub* (`git push -u origin <naziv-grane>`). U tom slučaju se povezuje sa zadatkom u sekciji **Development** (ikona zupčanika), odabirom repozitorijuma i grane.

### Predaja izmjena

Tokom rada izmjene se predaju sljedećom sekvencom komandi:

```
git status
git add <putanja>
git commit -s
git push
```

- `git status` prikazuje izmijenjene i nove fajlove i trenutnu granu. Prije svakog komita provjerite da ste na grani zadatka.
- `git add <putanja>` dodaje fajl ili cijeli folder (npr. `git add assignments/55`) u sljedeći komit. Oblik `git add .` dodaje sve izmjene u tekućem folderu, pa ga koristite samo ako ste provjerili da nema neželjenih fajlova.
- `git commit -s` otvara editor za unos poruke komita, a opcija `-s` na kraj poruke dodaje potpis autora (`Signed-off-by: ...`), koji je obavezan za svaki komit. Format poruke je propisan u uputstvu [Pravila prilikom predaje rješenja zadataka](assignment-submission.md). Kraća poruka može se zadati i direktno, npr. `git commit -s -m "Issue #55 : Create NAND2 circuit" -m "- Added entity and architecture"`.
- `git push` šalje komite na *GitHub*. Prvi put, ako grana još ne postoji na *GitHub* platformi, koristi se `git push -u origin <naziv-grane>`.

Komitujte i šaljite izmjene često, a ne samo na kraju rada.

### Otvaranje *pull request*-a

Kada je rješenje spremno za pregled i sve izmjene su poslate (`git push`):

1. Na početnoj stranici repozitorijuma kliknite na **Compare & pull request** u obavještenju o nedavno poslatoj grani. Alternativno, u tabulatoru **Pull requests** kliknite na **New pull request**.
2. Za odredišnu granu (**base**) odaberite `assignments`, a za izvornu granu (**compare**) granu zadatka.
3. Provjerite naslov: mora biti tačno `Issue #<N> : <naslov zadatka>`. Ako grana sadrži jedan komit, *GitHub* kao naslov predlaže prvi red njegove poruke, pa je naslov već ispravan ako je i poruka komita ispravna. Ako komita ima više, *GitHub* predlaže naslov napravljen od naziva grane (npr. `55 create nand2 circuit`), koji je potrebno zamijeniti.
4. Polje za opis je automatski popunjeno šablonom *pull request*-a. U njemu:
   - u sekciju *Opis* upišite kratak opis rješenja (šta dizajn radi i kako je realizovan),
   - u sekciju *Izmjene* upišite listu izmjena, po jednu u liniji koja počinje sa `- ` (mogu se prepisati stavke iz poruka komita),
   - u sekciji *Provjera* označite stavke ([x]), i to tek kada su zaista provjerene. Stavke se mogu označiti i klikom na kvadratić, nakon kreiranja *pull request*-a.

   Komentare oblika `<!-- ... -->` ne brišite: po njima automatska provjera prepoznaje sekcije, a na stranici *pull request*-a se ne prikazuju.
5. Kliknite na **Create pull request**.
6. Prebacite zadatak u kolonu *In Review*.

Predmetni nastavnik se automatski dodaje kao recenzent (**Reviewers**). Na projektu dodajte i članove tima. Pravila za naslov i opis navedena su u uputstvu [Pravila prilikom predaje rješenja zadataka](assignment-submission.md#naslov-i-opis-pull-request-a).

### Automatske provjere i pregled

Otvaranjem *pull request*-a, kao i svakim novim `git push` na granu zadatka, pokreću se automatske provjere. Njihov status se prikazuje na dnu stranice *pull request*-a, a detaljno su opisane u uputstvu [Automatske provjere](automated-checks.md).

Predmetni nastavnik pregleda rješenje i ostavlja komentare u tabulatoru **Files changed** ili **Conversation**. Ako su potrebne izmjene, ispravke se rade na istoj grani i šalju sa `git push`: *pull request* se automatski ažurira i nije potrebno otvarati novi. Nakon ispravke odgovorite na komentar ili kliknite na **Resolve conversation**.

### Integracija

Kada rješenje zadovolji kriterijume, predmetni nastavnik integriše granu u granu `assignments` (**Merge pull request**) i zadatak se prebacuje u kolonu *Done*. Zadatak se zatim zatvara dugmetom **Close issue** na dnu stranice zadatka. Automatsko zatvaranje zadatka ključnim riječima (npr. `Closes #55`) ne radi, jer grana `assignments` nije podrazumijevana grana repozitorijuma.

**Napomena:** Integraciju izmjena obavlja isključivo predmetni nastavnik (ukoliko nije drugačije dogovoreno). Studenti ne integrišu svoja rješenja samostalno.

Nakon integracije, grana zadatka se može obrisati (dugme **Delete branch** na stranici *pull request*-a), a lokalno:

```
git checkout assignments
git pull
git branch -d <naziv-grane>
```
