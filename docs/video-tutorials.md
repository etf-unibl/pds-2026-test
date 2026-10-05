## Video tutorijali

Video tutorijali kursa objavljeni su na *YouTube* kanalu [Projektovanje digitalnih sistema](https://www.youtube.com/@%D0%9F%D1%80%D0%BE%D1%98%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%D0%B0%D1%9A%D0%B5%D0%B4%D0%B8%D0%B3%D0%B8%D1%82%D0%B0%D0%BB%D0%BD%D0%B8%D1%85%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0/videos). Kod primjera iz tutorijala nalazi se u folderu [`video-tutorials`](../video-tutorials) repozitorijuma, organizovan po djelovima kursa i rednom broju videa.

**Napomena:** Kod u folderu `video-tutorials` odgovara kodu prikazanom u videima (greške uočene u videima su ispravljene u kodu, označene komentarom `NOTE` i opisane na stranici teme) i ne prati u potpunosti pravila iz uputstva [Pravila za formatiranje VHDL opisa](vhdl-code-style.md) (npr. nema zaglavlja fajla, a nazivi portova nemaju sufikse `_i`/`_o`). Kada dio koda koristite u rješenju zadatka, dodajte zaglavlje, prilagodite nazive i formatiranje i provjerite ga komandom `vhdl-style <N>`.

### Predavanja

| # | Dio | Video | Trajanje | Sažetak | Kod | Primjeri |
| ---: | :---: | ------ | ---: | :---: | ------ | ------ |
| 1 | 1 | [Uvod u FPGA tehnologiju](https://www.youtube.com/watch?v=oJSAv1hhdgk) | 22:26 | [stranica](topics/01-fpga-introduction.md) | – | – |
| 2 | 1 | [Osnove VHDL jezika (prvi dio)](https://www.youtube.com/watch?v=-5Q7YpQmU40) | 48:25 | [stranica](topics/02-vhdl-basics-1.md) | [`part-1/video-tutorial-02`](../video-tutorials/part-1/video-tutorial-02) | `even_detector`, `not1`, `xor2` |
| 3 | 1 | [Osnove VHDL jezika (drugi dio)](https://www.youtube.com/watch?v=-MCetuywNN4) | 53:19 | [stranica](topics/03-vhdl-basics-2.md) | [`part-1/video-tutorial-03`](../video-tutorials/part-1/video-tutorial-03) | `arith_demo`, `prio_encoder`, `simple_alu` |
| 4 | 2 | [Programiranje ciljne FPGA platforme](https://www.youtube.com/watch?v=D-kIoQWeO_E) | 12:17 | [stranica](topics/04-programming-the-board.md) | – | – |
| 5 | 2 | [Sekvencijalne VHDL naredbe](https://www.youtube.com/watch?v=oH_dKclt0WU) | 59:41 | [stranica](topics/05-sequential-statements.md) | [`part-2/video-tutorial-05`](../video-tutorials/part-2/video-tutorial-05) | `case_demo`, `process_demo`, `reduced_xor` |
| 6 | 2 | [Simulacija i testbench koncept](https://www.youtube.com/watch?v=8juBrOcO_d4) | 1:00:21 | [stranica](topics/06-simulation-testbench.md) | [`part-2/video-tutorial-06`](../video-tutorials/part-2/video-tutorial-06) | `even_detector`, `generic_adder` |
| 7 | 2 | [Dodjeljivanje pinova (alternativni način)](https://www.youtube.com/watch?v=xWWVBNAbvGg) | 10:12 | [stranica](topics/07-pin-assignment-import.md) | [`part-2/video-tutorial-07`](../video-tutorials/part-2/video-tutorial-07) | `DE1_SoC_pin_assigments.csv` |
| 8 | 2 | [Optimizacija kombinacionih mreža](https://www.youtube.com/watch?v=hhH37OIjS3U) | 56:38 | [stranica](topics/08-combinational-optimization.md) | [`part-2/video-tutorial-08`](../video-tutorials/part-2/video-tutorial-08) | `addsub`, `comp2mode`, `comp3`, `diff`, `prio_encoder`, `share_operator` |
| 9 | 3 | [Projektovanje sekvencijalnih mreža sa regularnom strukturom](https://www.youtube.com/watch?v=fTYa7lhoetw) | 1:24:00 | [stranica](topics/09-regular-sequential-circuits.md) | [`part-3/video-tutorial-09`](../video-tutorials/part-3/video-tutorial-09) | `binary_counter`, `memory`, `prog_counter`, `reg`, `timer` |
| 10 | 3 | [Projektovanje sekvencijalnih mreža metodologijom mašina stanja](https://www.youtube.com/watch?v=UbAJiexhklk) | 53:59 | [stranica](topics/10-state-machines.md) | [`part-3/video-tutorial-10`](../video-tutorials/part-3/video-tutorial-10) | `mem_ctrl` |
| 11 | 3 | [Projektovanje sekvencijalnih mreža Register-Transfer metodologijom](https://www.youtube.com/watch?v=39Tch03-rAU) | 34:39 | [stranica](topics/11-register-transfer-methodology.md) | [`part-3/video-tutorial-11`](../video-tutorials/part-3/video-tutorial-11) | `seq_mult` |
| 12 | 3 | [Napredni aspekti pisanja Testbench fajlova](https://www.youtube.com/watch?v=PCvCYeHhEFw) | 36:34 | [stranica](topics/12-advanced-testbench.md) | [`part-3/video-tutorial-12`](../video-tutorials/part-3/video-tutorial-12) | `binary_counter`, `even_detector` |
| 13 | 4 | [Vremenska analiza sinhronih digitalnih sistema](https://www.youtube.com/watch?v=DVF86jV4JMo) | 1:19:02 | [stranica](topics/13-timing-analysis.md) | [`part-4/video-tutorial-13`](../video-tutorials/part-4/video-tutorial-13) | `seq_mult` |
| 14 | 4 | [Smanjenje kašnjenja mreža primjenom pipeline tehnike](https://www.youtube.com/watch?v=K7ENW7DFjXg) | 1:00:47 | [stranica](topics/14-pipelining.md) | [`part-4/video-tutorial-14`](../video-tutorials/part-4/video-tutorial-14) | `pipeline_mult` |
| 15 | 4 | [Primjena procedura pri pisanju testbench fajlova](https://www.youtube.com/watch?v=mw2XPHItJM8) | 16:24 | [stranica](topics/15-testbench-procedures.md) | [`part-4/video-tutorial-15`](../video-tutorials/part-4/video-tutorial-15) | `memory` |

### Kratke teme

Kraći videi o pojedinačnim konstrukcijama jezika VHDL i mogućnostima alata *Quartus*.

| # | Video | Trajanje |
| ---: | ------ | ---: |
| 16 | [if-generate (VHDL language construct)](https://www.youtube.com/watch?v=uMoDe54J7GE) | 9:46 |
| 17 | [chip_pin synthesis attribute](https://www.youtube.com/watch?v=wc1b0oMM1H8) | 3:17 |
| 18 | [Algorithmic State Machines (ASM)](https://www.youtube.com/watch?v=KHZtNmtEX_E) | 7:32 |
| 19 | [VHDL array attributes](https://www.youtube.com/watch?v=0LVIhOMnCE8) | 6:57 |
| 20 | [Transport and inertial delay in VHDL](https://www.youtube.com/watch?v=W5rptHuuIQc) | 10:08 |
| 21 | [VHDL funkcije](https://www.youtube.com/watch?v=Ki51447L1SU) | 4:58 |
| 22 | [Quartus Project Revision](https://www.youtube.com/watch?v=QI2TiE2XZWg) | 2:47 |
| 23 | [Programming the device from Linux on HPS](https://www.youtube.com/watch?v=SP8fCZdNxkE) | 6:20 |
| 24 | [State Machine Editor](https://www.youtube.com/watch?v=mJtIjkAMuYc) | 11:57 |
| 25 | [alias (VHDL language construct)](https://www.youtube.com/watch?v=-FPVRwsmBZ8) | 8:23 |
| 26 | [Tri-state logic circuits](https://www.youtube.com/watch?v=6KLx1YlEG7s) | 6:48 |
| 27 | [Adding PLL to Quartus design](https://www.youtube.com/watch?v=V6xj6NznBdY) | 7:01 |
| 28 | [Fajl za incijalizaciju memorije](https://www.youtube.com/watch?v=ScZWPQ2UmE4) | 8:12 |
| 29 | [Quartus Schematic Capture](https://www.youtube.com/watch?v=zBnPPxa0-Hw) | 7:17 |
| 30 | [Quartus project archive](https://www.youtube.com/watch?v=8_hd3XY3u_w) | 4:37 |
| 31 | [keep synthesis attribute](https://www.youtube.com/watch?v=G4bkaQxRiNk) | 2:02 |
| 32 | [Project scripting with Tcl](https://www.youtube.com/watch?v=9OHjjzXgLS0) | 10:00 |
| 33 | [multstyle synthesis attribute](https://www.youtube.com/watch?v=yR-qmhUA1u0) | 4:14 |
| 34 | [ALT_INBUF Altera primitive](https://www.youtube.com/watch?v=4kncJ8TlBzQ) | 5:01 |
| 35 | [VHDL Packages](https://www.youtube.com/watch?v=bKRCJ3X5dsM) | 5:34 |
| 36 | [Unconstrained array in VHDL](https://www.youtube.com/watch?v=Curgf6K1Row) | 6:13 |
| 37 | [VHDL generics](https://www.youtube.com/watch?v=YIIg2CprQ3s) | 9:56 |
| 38 | [VHDL configuration](https://www.youtube.com/watch?v=DP7kfX050V4) | 8:30 |
| 39 | [Clock skew and timing analysis with clock skew](https://www.youtube.com/watch?v=VQlkn-XPkd4) | 8:26 |
| 40 | [SignalTap II Logic Analyzator](https://www.youtube.com/watch?v=Ag3d9Dem_cs) | 5:32 |

### Plejliste

Primjeri projektnih zadataka i studentskih prezentacija iz ranijih generacija:

- [Projektni zadaci (2020)](https://www.youtube.com/playlist?list=PLYeVxS9LO0cKHWsfHqdkyYfl3DQrqVp28)
- [Studentske prezentacije (2020)](https://www.youtube.com/playlist?list=PLYeVxS9LO0cJllKucOU0O1esq76mOL6wB)
