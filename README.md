Kaylesi mängureeglid

Mäng algab ühe rea pulkadega.

Ühe käiguga võib eemaldada ühe pulga.
Samuti võib eemaldada kaks kõrvuti olevat pulka.
Eemaldatud pulkade tõttu võivad allesjäänud pulgad moodustada eraldi gruppe.
Mängijad käivad kordamööda.
Võidab mängija, kes eemaldab viimase allesjäänud pulga.

Programmis alustatakse 10 pulgaga.



Kuidas programm töötab

Mänguseis on programmis esitatud True ja False väärtuste listina.

Näiteks:

[True, True, False, True]

True tähendab, et pulk on veel alles, ja False tähendab, et pulk on eemaldatud.

Selline lahendus võimaldab lihtsalt kujutada ka olukordi, kus pulkade rida on jagunenud mitmeks grupiks.

Olulisemad funktsioonid on näiteks:

valid_move() – kontrollib, kas valitud käik on lubatud;
legal_moves() – leiab kõik võimalikud käigud;
new_game_state() – loob käigu järel uue mänguseisu;
game_over() – kontrollib, kas mäng on lõppenud;
minimax() – hindab rekursiivselt mänguseise;
best_computer_move() – valib arvuti jaoks parima käigu;
print_minimax_tree() – kuvab väikese näite minimaxi mängupuust.



Programmi käivitamine

Käivitamiseks:

python kayles.py

Programmi alguses kuvatakse mõned näited võimalikest käikudest ning 3 pulgaga minimaxi mängupuu. Seejärel algab mäng inimese ja arvuti vahel.



Arendusprotsess ja tegevuste logi
1. etapp – lihtne Kaylesi mäng

Esimese viiba eesmärk oli luua lihtne käsureal töötav Kaylesi mäng kahe inimese jaoks.

Olulisemad piirangud olid:

kasutada Pythonit;
hoida kood lihtne ja algajale arusaadav;
minimaxi veel mitte kasutada;
vältida ebavajalikke teeke;
eraldada mänguloogika ja kasutaja sisend.

Codex valis mänguseisu esitamiseks True/False väärtustega listi. Samuti loodi eraldi funktsioonid mänguseisu kuvamiseks, käikude kontrollimiseks ja pulkade eemaldamiseks.

Codex tegi pärast koodi loomist süntaksikontrolli ja lihtsad mänguloogika kontrollid. Esimene etapp töötas edukalt.


2. etapp – mänguseisu funktsioonid

Teises etapis palusin lisada funktsioonid:

kõigi lubatud käikude genereerimiseks;
uue mänguseisu loomiseks;
mängu lõpu tuvastamiseks.

Lisati funktsioonid legal_moves(), new_game_state() ja game_over().

Oluline muudatus oli see, et new_game_state() loob mänguseisust koopia ega muuda vana seisu. See on hilisema minimaxi jaoks oluline, sest erinevad mängupuu harud ei tohi üksteise mänguseisu muuta.

Codex kontrollis funktsioone mitme erineva näidisseisuga.


3. etapp – minimax ja arvutimängija

Kolmandas etapis lisati minimax-algoritm.

Minimax vaatab läbi võimalikud tulevased käigud ja hindab, kas seis viib arvuti võidu või kaotuseni.

Terminalseisudes kasutatakse väärtusi:

+1 – arvuti jaoks võitev seis;
-1 – arvuti jaoks kaotav seis.

Arvuti proovib valida maksimaalse väärtusega käigu ja inimese puhul eeldatakse, et ta valib arvuti jaoks halvima võimaliku käigu.

Lisati ka debug-võimalus, millega saab näha, kui mitu minimaxi funktsioonikutset ühe käigu otsimiseks tehti.


4. etapp – minimaxi mängupuu

Neljandas etapis lisati väike mängupuu näide.

Funktsioon print_minimax_tree() näitab:

algseisu;
võimalikke käike;
järgnevaid mänguseise;
terminalseise;
minimaxi väärtusi.

Näites kasutatakse kolme pulka, sest suurema arvu puhul muutuks puu väga kiiresti liiga suureks.

Selles etapis tekkis ka üks ebaõnnestunud test. Codex proovis käivitada kontrolli ühe rea Python-käsuna, kuid with lauset ei saanud selles vormis kasutada. Codex tuvastas, et probleem oli testkäsus, mitte programmis, ning tegi uue kontrolli teisel viisil.


5. etapp – jõudluse mõõtmine ja memoization

Viiendas etapis uurisin minimaxi jõudlust.

Codex leidis, et tavaline minimax arvutab samu mänguseise väga palju kordi uuesti.

Selle parandamiseks lisati memoization ehk cache.

Cache'i võti on:

(tuple(pins), computer_turn)

See tähendab, et juba arvutatud mänguseisu väärtus salvestatakse ning sama seisuni uuesti jõudes ei pea kogu mängupuud uuesti läbi arvutama.

Mõõtmistulemused
Pulkade arv	Tavaline minimax	Memoization
6	3495 kutset, 0.0127 s	411 kutset, 0.0007 s
8	214115 kutset, 1.0618 s	2467 kutset, 0.0058 s

Ajad on ligikaudsed ja sõltuvad arvutist.

8 pulga puhul vähenes minimaxi funktsioonikutsete arv rohkem kui 200 000 kutse pealt umbes 2500 kutseni.

Selles etapis tekkis kaks huvitavat ebaõnnestumist.

Esimeses kontrollis kasutas Codex kogemata defineerimata assert_equal funktsiooni. See test ei töötanud ning Codex asendas selle tavaliste assert kontrollidega.

Olulisem probleem tekkis esimese cache-versiooniga. Cache oli küll minimaxi funktsioonile lisatud, kuid seda ei edastatud rekursiivsetesse väljakutsetesse. Seetõttu ei töötanud memoization alguses nii nagu vaja. Codex märkas seda mõõtmistulemuste põhjal, parandas rekursiivse väljakutse ning tegi mõõtmised uuesti.


6. etapp – alpha-beta pruning

Viimases etapis uurisin, kas memoization'ile oleks mõistlik lisada ka alpha-beta pruning.

Codex lõi ajutiselt alpha-beta versiooni ja võrdles kolme lahendust:

tavaline minimax;
minimax koos memoization'iga;
minimax koos memoization'i ja alpha-beta pruning'uga.

Näiteks 8 pulga korral:

Meetod	Funktsioonikutsed	Aeg
Tavaline minimax	214115	1.0618 s
Memoization	2467	0.0058 s
Memoization + alpha-beta	2154	0.0082 s

Alpha-beta vähendas mõnel juhul läbivaadatavate seisude arvu, kuid programmi tööaeg oli siiski suurem kui ainult memoization'i kasutades.

10 ja 12 pulga puhul oli alpha-beta versioon samuti memoization'ist aeglasem.

Seetõttu otsustas Codex alpha-beta lahendust lõplikku programmi mitte jätta.

See oli minu jaoks üks olulisemaid tähelepanekuid: keerulisema optimeerimise lisamine ei tähenda automaatselt, et programm muutub kiiremaks.


Arvutus- ja mäluresurss

Tavalise minimaxi peamine probleem oli suur korduvate arvutuste hulk.

Erinevad käikude järjestused võivad jõuda sama mänguseisuni. Ilma cache'ita arvutab minimax sellise seisu iga kord uuesti.

Memoization vähendas oluliselt arvutusmahtu ja programmi tööaega.

Samas kasutab memoization rohkem mälu, sest juba arvutatud mänguseisud ja nende väärtused salvestatakse cache sõnastikku.

Seega tekkis kompromiss:

rohkem mälukasutust;
oluliselt vähem korduvat arvutamist;
palju väiksem tööaeg.

Täpset mälukasutust baitides selles projektis ei mõõdetud, kuid cache'i lisamine suurendab mälukasutust vastavalt salvestatud mänguseisude arvule.
