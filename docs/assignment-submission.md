## Pravila prilikom predaje rješenja zadataka

Rješenja zadataka se predaju preko *GitHub* platforme, a većina pravila opisanih u nastavku provjerava se automatski (posao `pr-checks`, [Automatske provjere](automated-checks.md)). Rješenje koje ne poštuje pravila neće proći automatsku provjeru. Postupak rada na *GitHub* platformi opisan je u uputstvu [Proces rada u GitHub okruženju](github-workflow.md). Ista pravila važe i za [probni zadatak](test-assignment.md).

### Grana

- Za svaki zadatak kreira se zasebna grana. Izvorna grana (**Branch source**) je obavezno `assignments`.
- Naziv grane **mora** počinjati brojem zadatka i crticom, nakon čega slijedi kratak opis (npr. `55-create-nand2-circuit`). Takav naziv predlaže *GitHub* kada se grana kreira iz zadatka i preporučuje se da se zadrži.
- Na zadatku se radi isključivo na njegovoj grani. Nikada ne komitujte direktno na granu `assignments`.
- Zadatak na koji se rješenje odnosi mora biti dodijeljen autoru *pull request*-a (**Assignees**).
- Ne pravite kopiju repozitorijuma (*fork*). Grane se šalju direktno u repozitorijum kursa, jer automatske provjere nemaju pristup potrebnim resursima za *pull request* iz kopije.

### Struktura foldera

Svi fajlovi rješenja smještaju se u folder `assignments/<N>`, gdje je `<N>` broj zadatka. Na primjer, za zadatak `#55`:

```
assignments/
└── 55/
    ├── nand2.vhd
    └── nand2_tb.vhd
```

- Naziv foldera sadrži samo broj zadatka, bez znaka `#` i drugih dodataka.
- Nazivi fajlova, entiteta i portova moraju biti tačno onakvi kako su navedeni u postavci zadatka, jer ih automatski testovi koriste za pokretanje simulacije i sinteze.
- *Testbench* za dizajn `<dizajn>` nalazi se u fajlu `<dizajn>_tb.vhd`, a njegov entitet se zove `<dizajn>_tb` (npr. `nand2_tb` u fajlu `nand2_tb.vhd`). Svaki takav fajl se automatski simulira ([Simulacija i testiranje](simulation-and-testing.md#automatsko-pokretanje-testbench-fajlova)).
- U folder se smještaju samo izvorni fajlovi (VHDL opisi, *testbench* fajlovi, fajlovi sa testnim podacima i ograničenjima, npr. `.sdc`, ako ih zadatak zahtijeva). Fajlovi koje generišu alati (folderi `db`, `simulation`, `work`, `html`, talasni oblici, izvještaji i sl.) se ne predaju. Većina ih je već navedena u fajlu `.gitignore`.
- Izmjene izvan foldera `assignments/<N>` (dodavanje, izmjena, brisanje ili premještanje fajlova) nisu dozvoljene i automatska provjera ih odbija.
- Formatiranje sadržaja fajlova propisano je uputstvom [Pravila za formatiranje VHDL opisa](vhdl-code-style.md).
- Dizajn mora biti dokumentovan komentarima prema uputstvu [Dokumentovanje dizajna](design-documentation.md). Dokumentacija je obavezna i ocjenjuje se.

### Poruka komita

Svaki komit ima jednoobraznu poruku koja sadrži:

- u prvom redu naslov u formatu `Issue #<N> : <naslov zadatka>`, gdje je `<N>` broj, a `<naslov zadatka>` naslov zadatka na *GitHub* platformi,
- prazan red,
- u narednim redovima listu stavki koje opisuju šta je urađeno u tom komitu,
- prazan red i potpis (*sign-off*) autora u obliku `Signed-off-by: Ime Prezime <email>`.

Primjer:

```
Issue #55 : Create NAND2 circuit

- Added entity definition for the design
- Added initial code for architecture
- Created an initial testbench for the design

Signed-off-by: Ime Prezime <12345678+imeprezime@users.noreply.github.com>
```

Potpis se ne piše ručno, već ga dodaje opcija `-s` komande `git commit` (`git commit -s`), na osnovu imena i email adrese podešenih u *Git* alatu ([Podešavanje Git okruženja](git-setup.md#osnovna-podešavanja)). Kako je repozitorijum javan, tu koristite privatnu *GitHub* adresu. Potpisom autor potvrđuje da je rješenje njegov samostalan rad. **Svaki** komit u *pull request*-u mora biti potpisan, a ime i email adresa u potpisu moraju biti jednaki imenu i email adresi autora komita. Kako se potpisuje komit koji je već napravljen bez potpisa, opisano je u uputstvu [Rješavanje čestih problema](troubleshooting.md).

Preporučuje se korišćenje engleskog jezika u poruci komita, ali to nije obavezno. Rješenje se može predati kroz više komita (npr. prvo osnovna verzija, zatim dopune), a svaki komit prati isti format.

Format poruke svakog komita u *pull request*-u provjerava se automatski: prvi red mora biti tačno `Issue #<N> : <naslov zadatka>`, drugi red prazan, a u nastavku mora postojati bar jedna stavka liste (linija koja počinje sa `- `). Komitovi integracije (*merge*) se ne provjeravaju. Uključeni *Git hook*-ovi ([Podešavanje Git okruženja](git-setup.md#uključivanje-git-hook-ova-preporučeno)) provjeravaju isto već prilikom komitovanja i popunjavaju prvi red poruke.

#### Korišćenje AI alata

Ako je bilo koji dio koda u komitu generisao AI alat (uključujući kod preuzet iz odgovora AI asistenta), to se navodi u poruci tog komita, uz objašnjenje kako je alat korišćen: posebna linija `AI-assisted-by: <alat> - <kako je korišćen>` iznad potpisa, po jedna za svaki alat. Primjer:

```
Issue #55 : Create NAND2 circuit

- Added entity definition for the design
- Added a testbench that checks all input combinations

AI-assisted-by: GitHub Copilot CLI - generated the testbench loop over all input combinations; I wrote the checks and verified the results
Signed-off-by: Ime Prezime <12345678+imeprezime@users.noreply.github.com>
```

Liniju upišite sami (na kraj poruke, iza prazne linije); `git commit -s` potpis dodaje ispod nje. Ako je AI alat samo objašnjavao, a kod ste pisali sami, linija nije potrebna. Automatska provjera ovu liniju ne provjerava, ali je nastavnik pregleda; potpisom i dalje potvrđujete da razumijete i odgovarate za cijelo rješenje. Dodatak `pds-git` (komit) pita da li je AI generisao kod i pomaže da se linija napiše.

### Naslov i opis *pull request*-a

- Naslov *pull request*-a je identičan prvom redu poruke komita: `Issue #<N> : <naslov zadatka>`.
- Koriste se tačan broj i originalni naslov zadatka, bez ikakvih dodataka. Automatska provjera poredi naslov sa naslovom zadatka (razlike u broju razmaka se zanemaruju).
- Odredišna grana (**base**) je `assignments`.
- Opis prati šablon *pull request*-a: sekcija *Opis* (kratak opis rješenja) je popunjena, a sve stavke u sekciji *Provjera* su označene ([x]). Sekciju *Izmjene* automatska provjera popunjava iz poruka komita. Komentari sa oznakama sekcija (npr. `<!-- section:summary -->`, `<!-- check:style -->`) ne smiju se brisati, jer po njima automatska provjera prepoznaje sekcije; ostali komentari mogu se obrisati.
- Stavka provjere označava se tek kada je ono što opisuje zaista provjereno.

Postupak otvaranja *pull request*-a i popunjavanja šablona opisan je u uputstvu [Proces rada u GitHub okruženju](github-workflow.md#otvaranje-pull-request-a). Ako su naslov ili opis pogrešni, ispravite ih na stranici *pull request*-a (**Edit** pored naslova, odnosno **...** &rarr; **Edit** na opisu): izmjena automatski ponovo pokreće provjere.

### Završetak rada na zadatku

1. Prije otvaranja *pull request*-a lokalno provjerite sintaksu i simulaciju ([Simulacija i testiranje](simulation-and-testing.md)), stil (`vhdl-style <N>`) i dokumentaciju ([Dokumentovanje dizajna](design-documentation.md)).
2. Otvorite *pull request*, popunite opis prema šablonu i označite stavke provjere. Predmetni nastavnik se automatski dodaje kao recenzent.
3. Sačekajte rezultate automatskih provjera ([Automatske provjere](automated-checks.md)). Kada sve provjere prođu, prebacite zadatak u kolonu *In Review*.
4. Ako nastavnik vrati zadatak na doradu, ispravke radite na istoj grani i šaljite sa `git push`.
5. Zadatak je završen kada ga nastavnik integriše u granu `assignments`. Tada se zadatak prebacuje u kolonu *Done*.

### Rokovi

Rok za predaju zadatka je naveden u samom zadatku ili u *milestone*-u kojem zadatak pripada.

<!-- TODO (nastavnik): definisati šta se smatra trenutkom predaje (npr. otvaranje pull request-a ili posljednji komit prije roka) i kako se tretira zakašnjela predaja. -->
