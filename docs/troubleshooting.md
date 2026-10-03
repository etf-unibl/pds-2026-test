## Rješavanje čestih problema

### Pristup repozitorijumu

**`git@github.com: Permission denied (publickey)`**
SSH ključ nije dodat na *GitHub* ili se ne koristi odgovarajući ključ. Provjerite komandom `ssh -T git@github.com` i ponovite korake iz uputstva [Podešavanje Git okruženja](git-setup.md). Na *Windows* platformi provjerite da li se ključ nalazi u folderu `C:\Users\<korisnik>\.ssh`.

**`ERROR: Repository not found`**
Pozivnica za repozitorijum nije prihvaćena ili je adresa repozitorijuma pogrešna. Provjerite pozivnice na stranici `https://github.com/etf-unibl/pds-2026-test/invitations`.

**`Permission to ... denied` prilikom `git push`**
Nalog nema pravo pisanja u repozitorijum. Obratite se predmetnom nastavniku.

### Grane i komiti

**Komitovali ste na pogrešnu granu (npr. `assignments`)**
Ako komit još nije poslat na *GitHub*, prenesite ga na granu zadatka i vratite granu `assignments` u prethodno stanje:

```
git branch <naziv-grane-zadatka>
git reset --hard origin/assignments
git checkout <naziv-grane-zadatka>
```

Prva komanda pravi granu zadatka koja sadrži komit (ako grana već postoji, umjesto nje koristite `git checkout <naziv-grane-zadatka>` i `git cherry-pick assignments`, a zatim se vratite na `assignments` i izvršite `git reset --hard origin/assignments`). Komanda `git reset --hard` briše sve nekomitovane izmjene na tekućoj grani, pa je prije toga provjerite komandom `git status`.

**`git push` je odbijen (`rejected ... fetch first`)**
Na *GitHub* grani postoje komiti koji nisu lokalno (npr. drugi član tima je poslao izmjene). Preuzmite ih komandom `git pull`, riješite eventualne konflikte i ponovite `git push`.

**`git push` prijavljuje `has no upstream branch`**
Grana se prvi put šalje na *GitHub*. Koristite `git push -u origin <naziv-grane>`.

**Pogrešna poruka posljednjeg komita**
Ako komit još nije poslat, ispravlja se komandom `git commit --amend -s`. Ako je već poslat, ostavite ga i poštujte format u narednim komitima.

**Komit nije potpisan (`Signed-off-by`)**
Ako se radi o posljednjem komitu, potpis se dodaje komandom `git commit --amend -s --no-edit`. Ako nepotpisanih komita ima više, potpisuju se svi komiti grane zadatka:

```
git fetch origin
git rebase --signoff origin/assignments
```

Ako su komiti već poslati na *GitHub*, izmijenjena grana se šalje komandom `git push --force-with-lease`. Ovu komandu koristite isključivo na grani svog zadatka. Ako potpis postoji, ali posao `pr-checks` i dalje prijavljuje grešku, ime ili email adresa u potpisu se ne poklapaju sa autorom komita; provjerite podešavanja `git config --global user.name` i `user.email`.

**Naziv grane ne počinje brojem zadatka**
Naziv grane na koju se odnosi otvoreni *pull request* nije moguće promijeniti. Preimenujte granu lokalno, pošaljite je pod novim nazivom, otvorite novi *pull request* i zatvorite stari:

```
git branch -m <N>-<opis>
git push -u origin <N>-<opis>
git push origin --delete <stari-naziv>
```

**Fajl se ne pojavljuje u `git status`**
Fajl je vjerovatno obuhvaćen pravilima u fajlu `.gitignore` (npr. folderi `simulation` i `testbench` ili nazivi koji sadrže riječ `example`). Uzrok se provjerava komandom `git check-ignore -v <putanja>`. Preimenujte fajl ili folder tako da nije obuhvaćen pravilom.

**Greškom je komitovan generisani fajl ili folder**
Uklonite ga iz repozitorijuma (fajl ostaje na disku) i komitujte izmjenu:

```
git rm -r --cached <putanja>
git commit
```

**Poruka komita koji je već poslat ne prati propisani format**
Najjednostavnije je sve komite grane zadatka objediniti u jedan komit sa ispravnom porukom i poslati izmijenjenu granu:

```
git fetch origin
git reset --soft origin/assignments
git commit -s
git push --force-with-lease
```

Komanda `git reset --soft` zadržava sve izmjene fajlova, a uklanja samo komite, pa `git commit -s` pravi jedan novi komit sa svim izmjenama. Ovu komandu koristite isključivo na grani svog zadatka. Pojedinačne poruke mogu se ispraviti i komandom `git rebase -i origin/assignments` (opcija `reword`).

**Komit je odbijen porukom `Commit rejected`**
Poruku je odbio uključeni *Git hook*, a ispod poruke je navedeno šta treba ispraviti. Napisana poruka sačuvana je u fajlu `.git/COMMIT_EDITMSG`, pa se može ponovo iskoristiti komandom `git commit -s -e -F .git/COMMIT_EDITMSG`. Opcijom `--no-verify` *hook* se može zaobići, ali automatska provjera na *GitHub* platformi primjenjuje ista pravila.

**Naslov zadatka nije popunjen u poruci komita (`<issue title>`)**
*Hook* nije uspio da preuzme naslov sa *GitHub* platforme (nema mrežne veze ili *Python* nije pronađen). Upišite naslov ručno, tačno kao na *GitHub* platformi. Na *Windows* platformi provjerite da komanda `python --version` radi; ako se otvara *Microsoft Store*, *Python* nije instaliran ili nije dodat u `PATH`.

### Automatske provjere

**Provjera prijavljuje da folder ne postoji**
Folder mora imati naziv `assignments/<N>`, gdje je `<N>` broj iz naslova *pull request*-a. Provjerite naziv foldera (samo broj, bez `#`) i da je broj zadatka prvi broj u naslovu *pull request*-a.

**Posao `classify` prijavljuje `Issue #<N> does not exist` ili `is a pull request, not an issue`**
Prvi broj u naslovu *pull request*-a nije broj zadatka. Ispravite naslov (**Edit** pored naslova), čime se provjere ponovo pokreću.

**Posao `classify` prijavljuje da zadatak mora imati labelu `good first issue` ili `assignment-<n>`, ili se za probni zadatak pokreće posao `verif` (ili obrnuto)**
Zadatak nema odgovarajuću labelu ili ima pogrešnu. Obavijestite predmetnog nastavnika, koji ispravlja labelu, a zatim ponovo pokrenite provjere izmjenom naslova ili opisa *pull request*-a.

**Posao `pr-checks` prijavljuje da naslov *pull request*-a nije ispravan**
Naslov mora biti tačno `Issue #<N> : <naslov zadatka>`, sa originalnim naslovom zadatka. Ispravite ga opcijom **Edit** pored naslova, čime se provjere ponovo pokreću.

**Posao `pr-checks` prijavljuje da opis ne prati šablon**
Opis mora sadržati popunjenu sekciju *Opis* i sve označene stavke provjere, a oznake sekcija (komentari oblika `<!-- section:... -->` i `<!-- check:... -->`) ne smiju biti obrisane. Sekciju *Izmjene* provjera popunjava sama. Ispravite opis (**...** &rarr; **Edit**). Ako su oznake obrisane, kopirajte kompletan šablon iz fajla [`.github/pull_request_template.md`](https://github.com/etf-unibl/pds-2026-test/blob/main/.github/pull_request_template.md) na grani `main` (dugme **Raw** prikazuje i komentare) i ponovo upišite sadržaj sekcija.

**Posao `pr-checks` prijavljuje da zadatak nije dodijeljen autoru**
U naslovu je naveden broj tuđeg zadatka ili zadatak nije dodijeljen vama. Provjerite broj u naslovu, a ako je ispravan, obavijestite predmetnog nastavnika.

**Posao `pr-checks` prijavljuje izmjene izvan foldera `assignments/<N>`**
Vratite navedene fajlove u stanje sa grane `assignments`, a fajlove koji tamo ne postoje uklonite, pa komitujte i pošaljite izmjenu:

```
git fetch origin
git checkout origin/assignments -- <putanja>
git rm <putanja-novog-fajla>
git commit -s
git push
```

**Posao `testbench` ne prolazi**
Poruka `does not compile` znači da se *testbench* ili dizajn ne prevode ili da se entitet *testbench*-a ne zove kao njegov fajl (npr. `nand2_tb` u fajlu `nand2_tb.vhd`). Poruka `failed` znači da je *testbench* prijavio grešku naredbom `assert`. Pokrenite iste komande lokalno ([Simulacija i testiranje](simulation-and-testing.md#automatsko-pokretanje-testbench-fajlova)) i pregledajte talasne oblike iz artifakta `testbench-waveforms`.

**Provjere se ne pokreću**
Provjerite da je odredišna grana (**base**) `assignments` i da *pull request* nije otvoren iz kopije repozitorijuma (*fork*). Testovi nastavnika (`verif-setup`, `verif`) se nikada ne izvršavaju za *pull request* iz kopije, a ostale provjere za kopiju mogu čekati odobrenje nastavnika.

**Provjera dugo čeka (*Queued*)**
Računar za izvršavanje simulacije i sinteze možda nije dostupan. Obavijestite predmetnog nastavnika.

**Simulacija lokalno prolazi, a na *GitHub* platformi ne**
Najčešći uzroci su nazivi fajlova, entiteta ili portova koji ne odgovaraju postavci zadatka, fajl koji nije dodat u komit (provjerite tabulator **Files changed**) i razlike u velikim i malim slovima u nazivima fajlova (*Linux* ih razlikuje, *Windows* ne).

### Alati

**`vhdl-style`, `vsim` ili `ghdl` nije prepoznata komanda**
Folder sa izvršnim fajlovima alata nije u varijabli okruženja `PATH`, ili je terminal otvoren prije instalacije. Otvorite novi terminal, a ako problem ostane, provjerite podešavanja iz uputstva [Instalacija alata](tools-setup.md).

**Simulator prijavljuje da licenca nije pronađena**
Licenca za *Questa* simulator nije preuzeta ili nije ispravno podešena. Ponovite postupak opisan na zvaničnoj *Intel* stranici za verziju alata koju koristite.
