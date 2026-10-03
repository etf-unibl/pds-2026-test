## Podešavanje Git okruženja

Ovo uputstvo opisuje jednokratna podešavanja potrebna za pristup repozitorijumu kursa: osnovna podešavanja *Git* alata, generisanje SSH ključa, njegovo dodavanje na *GitHub* i kloniranje repozitorijuma. Instalacija *Git* alata opisana je u uputstvu [Instalacija alata](tools-setup.md).

Sve komande se unose u *Git Bash* konzolu (*Windows*) ili terminal (*Linux*, *macOS*).

### Osnovna podešavanja

Svaki komit sadrži ime i email adresu autora. Repozitorijum kursa je javan, pa su ovi podaci vidljivi svima. Zato umjesto lične ili fakultetske email adrese koristite privatnu adresu koju dodjeljuje *GitHub*:

1. Na *GitHub* platformi otvorite **Settings &rarr; Emails** i uključite opciju **Keep my email addresses private**. Ispod opcije je prikazana vaša privatna adresa, oblika `<broj>+<korisničko ime>@users.noreply.github.com`.
2. Po želji uključite i opciju **Block command line pushes that expose my email**, koja odbija slanje komita sa vašom javnom adresom.
3. Podesite ime i privatnu adresu jednom, na nivou korisnika:

```
git config --global user.name "Ime Prezime"
git config --global user.email "<broj>+<korisničko ime>@users.noreply.github.com"
```

pri čemu `Ime Prezime` i adresu treba zamijeniti stvarnim podacima. Ista adresa se koristi i u obaveznom potpisu svakog komita (`Signed-off-by`), a komiti sa njom su povezani sa vašim *GitHub* nalogom.

Podešena vrijednost se provjerava komandom `git config --global --list`.

### Generisanje SSH ključa

Pristup repozitorijumu ostvaruje se preko SSH protokola, za šta je potreban par ključeva (privatni i javni). Par ključeva se generiše komandom:

```
ssh-keygen -t ed25519 -C "ime.prezime@student.etf.unibl.org"
```

Alat prvo pita za lokaciju fajla. Pritiskom na taster *Enter* prihvata se podrazumijevana lokacija (`~/.ssh/id_ed25519`, odnosno `C:\Users\<korisnik>\.ssh\id_ed25519` na *Windows* platformi), što se i preporučuje.

Zatim se traži šifra (*passphrase*) kojom se dodatno štiti privatni ključ. Šifra nije obavezna (dovoljno je pritisnuti *Enter* dva puta), ali ako je definišete, morate je zapamtiti, jer bez nje ključ nije moguće koristiti.

Rezultat su dva fajla:

- `id_ed25519` - privatni ključ, koji ostaje samo na vašem računaru i **nikome se ne dostavlja**,
- `id_ed25519.pub` - javni ključ, koji se dodaje na *GitHub*.

**Napomena:** Ako alat prijavi da tip `ed25519` nije podržan (stariji SSH klijenti), koristite `ssh-keygen -t rsa -b 4096`, pri čemu će fajlovi imati nazive `id_rsa` i `id_rsa.pub`.

### Dodavanje javnog ključa na GitHub

1. Prikažite sadržaj javnog ključa komandom `cat ~/.ssh/id_ed25519.pub` i kopirajte kompletan ispis (jedna linija koja počinje sa `ssh-ed25519`).
2. Na *GitHub* platformi otvorite meni korisničkog naloga (avatar u gornjem desnom uglu) i odaberite **Settings &rarr; SSH and GPG keys &rarr; New SSH key**.
3. U polje *Title* unesite proizvoljan naziv (npr. naziv računara), polje *Key type* ostavite na vrijednosti *Authentication Key*, a u polje *Key* prilijepite kopirani javni ključ.
4. Potvrdite klikom na dugme *Add SSH key*.

Ispravnost podešavanja provjerava se komandom:

```
ssh -T git@github.com
```

Prilikom prvog povezivanja potrebno je potvrditi identitet servera odgovorom `yes`. Ako je sve u redu, ispisuje se poruka `Hi <korisničko ime>! You've successfully authenticated, ...`.

Ako radite na više računara, postupak generisanja i dodavanja ključa ponavlja se za svaki računar.

### Kloniranje repozitorijuma

Adresa repozitorijuma za SSH pristup dobija se klikom na dugme **Code &rarr; SSH** na početnoj stranici repozitorijuma. Repozitorijum se klonira komandom:

```
git clone git@github.com:<organizacija>/<repozitorijum>.git
```

*Git* pravi folder sa nazivom repozitorijuma u folderu iz kojeg je komanda pokrenuta. Sve naredne komande izvršavaju se unutar tog foldera:

```
cd <repozitorijum>
```

Rješenja zadataka se predaju na granu `assignments`, pa se nakon kloniranja potrebno prebaciti na nju:

```
git checkout assignments
```

Trenutna grana i stanje fajlova provjeravaju se komandom `git status`.

### Uključivanje *Git hook*-ova (preporučeno)

Grana `assignments` sadrži *Git hook*-ove (folder `.githooks`), skripte koje *Git* automatski pokreće prilikom komitovanja. Uključuju se jednom, u folderu repozitorijuma:

```
git config core.hooksPath .githooks
```

Nakon toga, na grani zadatka (čiji naziv počinje brojem zadatka, npr. `55-create-nand2-circuit`):

- komanda `git commit -s` (bez opcije `-m`) otvara editor sa unaprijed popunjenim prvim redom `Issue #<N> : <naslov zadatka>` (naslov se preuzima sa *GitHub* platforme) i praznom stavkom liste, pa je potrebno samo upisati opis izmjena,
- komit čija poruka ne prati propisani format, nema potpis ili sadrži broj drugog zadatka biva odbijen, uz poruku šta treba ispraviti (poruka se čuva u fajlu `.git/COMMIT_EDITMSG`),
- komit koji mijenja fajlove izvan foldera `assignments/<N>` biva odbijen.

Ista pravila se provjeravaju i automatski, prilikom otvaranja *pull request*-a ([Automatske provjere](automated-checks.md)), pa *hook*-ovi služe da se greške uoče odmah, a ne tek na *GitHub* platformi. Za preuzimanje naslova zadatka potreban je *Python*, koji se instalira zajedno sa alatom za provjeru stila.

### Dodatni materijali

- [Pro Git](https://git-scm.com/book/en/v2) - besplatna knjiga o *Git* alatu
- [GitHub Docs: Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Serija video materijala o korišćenju Git alata](https://www.youtube.com/watch?v=qZ41BiMd1yI&list=PLwgfxpYcBNqGyUdy37jpFxAt-DdeSAHbU)
