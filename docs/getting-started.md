## Prvi koraci

Ovo uputstvo je polazna tačka za rad na kursu. Prati redoslijed koraka koji je potrebno proći od prvog dana, a za svaki korak upućuje na detaljnije uputstvo.

U uputstvima se koriste sljedeće oznake koje je potrebno zamijeniti stvarnim vrijednostima:

| Oznaka | Značenje |
| ------ | ------ |
| `<N>` | broj zadatka (*issue*) na *GitHub* platformi, npr. `55` |

### 1. Priprema naloga i pristupa

1. Napravite nalog na [*GitHub*](https://github.com) platformi (ukoliko ga već nemate) i dostavite korisničko ime predmetnom nastavniku.
2. Prihvatite pozivnicu za pristup repozitorijumu kursa. Pozivnica stiže na email adresu povezanu sa nalogom, a vidljiva je i na stranici `https://github.com/etf-unibl/pds-2026-test/invitations`.
3. Instalirajte potrebne alate prema uputstvu [Instalacija alata](tools-setup.md).
4. Podesite *Git* alat i SSH pristup, a zatim klonirajte repozitorijum prema uputstvu [Podešavanje Git okruženja](git-setup.md).

### 2. Upoznavanje sa procesom rada

5. Pročitajte uputstvo [Proces rada u GitHub okruženju](github-workflow.md) kako biste razumjeli životni vijek zadatka: zadatak (*issue*) &rarr; grana (*branch*) &rarr; komit (*commit*) &rarr; zahtjev za integraciju (*pull request*) &rarr; pregled i integracija.
6. Pročitajte [Pravila prilikom predaje rješenja zadataka](assignment-submission.md). Ova pravila se provjeravaju automatski, pa njihovo nepoštovanje dovodi do neuspješne provjere.
7. Pročitajte uputstvo o stilu VHDL opisa ([Pravila za formatiranje VHDL opisa](vhdl-code-style.md)) i instalirajte alat za provjeru stila.
8. Uradite probni zadatak (zadatak sa labelom `good first issue`) prema uputstvu [Probni zadatak](test-assignment.md). Njegova svrha je da cijeli postupak prođete jednom, bez ocjenjivanja.

### 3. Rad na zadacima

9. Dizajn dokumentujte prema uputstvu [Dokumentovanje dizajna](design-documentation.md), a prije predaje svako rješenje provjerite lokalno: sintaksa i simulacija ([Simulacija i testiranje](simulation-and-testing.md)) i stil (`vhdl-style <N>`).
10. Nakon otvaranja *pull request*-a, pratite rezultate automatske provjere ([Automatske provjere](automated-checks.md)) i ispravljajte greške dok sve provjere ne prođu.
11. Pratite komentare predmetnog nastavnika u *pull request*-u i dorađujte rješenje na istoj grani.
12. Za svaki zadatak unesite procjenu i evidentirajte utrošeno vrijeme ([Evidencija utrošenog vremena](time-tracking.md)).

### 4. Rad na projektu

13. U drugom dijelu kursa rad se odvija u timovima, prema uputstvu [Rad na projektu](project-workflow.md).

Ako nešto ne radi kako je opisano, pogledajte [Rješavanje čestih problema](troubleshooting.md), a ako tamo ne nađete odgovor, obratite se predmetnom nastavniku.

### Kontrolna lista

- [ ] *GitHub* nalog napravljen i korisničko ime dostavljeno nastavniku
- [ ] pozivnica za repozitorijum prihvaćena
- [ ] instalirani *Git*, *Quartus* sa simulatorom i *Python*
- [ ] SSH ključ dodat na *GitHub* i `ssh -T git@github.com` uspješno izvršen
- [ ] repozitorijum kloniran i izvršeno prebacivanje na granu `assignments`
- [ ] alat za provjeru stila instaliran (`vhdl-style --help` radi)
- [ ] *Git hook*-ovi uključeni (`git config core.hooksPath .githooks`)
- [ ] [probni zadatak](test-assignment.md) predat i sve automatske provjere prošle
