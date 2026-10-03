## Instalacija alata

Za rad na kursu potrebni su alati navedeni u tabeli ispod. Tačne verzije alata za tekuću godinu objavljuje predmetni nastavnik. Ukoliko verzija nije navedena, koristite posljednju dostupnu verziju.

| Alat | Namjena | Obavezan |
| ------ | ------ | :------: |
| [*Git*](https://git-scm.com/downloads) | rad sa repozitorijumom | da |
| *Quartus Prime Lite Edition* | sinteza dizajna i programiranje evaluacione ploče | da |
| *ModelSim* ili *Questa* (*Intel FPGA* izdanje) | simulacija | da |
| [*Python*](https://www.python.org/downloads/) (3.8 ili noviji) | alat za provjeru stila VHDL opisa | da |
| [*GHDL*](https://github.com/ghdl/ghdl) | brza provjera sintakse i simulacija iz komandne linije | ne |
| tekstualni editor (npr. *VS Code*, *Notepad++*) | pisanje VHDL opisa | preporučeno |

### Git

Na *Windows* platformi preuzmite i pokrenite [instalacioni fajl](https://git-scm.com/download/win). Instalacija uključuje i *Git Bash* konzolu, koja se pokreće iz kontekstnog menija bilo kojeg foldera (desni klik &rarr; *Open Git Bash here*). Na *Linux* platformi *Git* se instalira pomoću menadžera paketa distribucije ([instrukcije](https://git-scm.com/download/linux)), npr. za *Ubuntu*:

```
sudo apt-get install git
```

Uspješnost instalacije provjerava se komandom:

```
git --version
```

Podešavanje *Git* alata opisano je u uputstvu [Podešavanje Git okruženja](git-setup.md).

### Quartus i simulator

Alati se preuzimaju sa stranice *Intel FPGA Software Download Center* (potražite *Quartus Prime Lite Edition*). Prilikom instalacije:

- odaberite i podršku za familiju FPGA čipa na evaluacionoj ploči koja se koristi na kursu (npr. *Cyclone V* za ploču *DE1-SoC*),
- odaberite i simulator (*ModelSim* ili *Questa - Intel FPGA Starter Edition*, zavisno od verzije *Quartus* alata),
- za *Questa* simulator potrebna je (besplatna) licenca. Postupak njenog preuzimanja i podešavanja zavisi od verzije alata, pa ga provjerite na zvaničnoj *Intel* stranici za odabranu verziju.

Za programiranje ploče preko *USB-Blaster* kabla na *Windows* platformi potrebno je instalirati drajver koji se nalazi u instalacionom folderu *Quartus* alata (`<quartus>/drivers/usb-blaster` ili `usb-blaster-ii`).

Za rad iz komandne linije (preporučeno za brzu provjeru), dodajte foldere sa izvršnim fajlovima alata u varijablu okruženja `PATH`, npr. `<instalacioni folder>/quartus/bin64` i folder simulatora sa programima `vcom` i `vsim`.

### Python i alat za provjeru stila

Instalacija *Python* okruženja i alata za provjeru stila opisana je u uputstvu [Pravila za formatiranje VHDL opisa](vhdl-code-style.md). Na *Windows* platformi prilikom instalacije *Python* okruženja označite opciju *Add python.exe to PATH*.

### GHDL (opciono)

*GHDL* je simulator otvorenog koda koji omogućava brzu provjeru sintakse i pokretanje simulacije iz komandne linije, bez pravljenja projekta. Isti alat se koristi i u automatskoj provjeri na *GitHub* platformi. Gotove verzije za *Windows*, *Linux* i *macOS* dostupne su na stranici [GHDL releases](https://github.com/ghdl/ghdl/releases). Način korišćenja opisan je u uputstvu [Simulacija i testiranje](simulation-and-testing.md).
