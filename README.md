# geomine

## Ülevaade
Programm on mõeldud Geopeitus.ee lehelt aardeinfo lugemiseks ja salvestamiseks GPX formaati. Salvestatud failid võimaldavad Garmini seadmetes kasutada sisseehitatud geopeituse funktsionaalsust. 
Töötab Python 3.6 keskkonnas. 

## Kasutamine

### Aardeinfo GPX formaati salvestamine
Käivita käsurealt **geomine_gpx** :  
`python3 geomine_gpx.py`  
Seejärel sisesta geopeituse kasutajanimi ja parool
Seejärel sisesta aarde ID number või URL, misjärel salvestatakse aardeinfo ####.gpx faili  
Programmist väljumiseks sisesta:  
`exit`

### Aardeinfo salvestamine tekstireana - 
Käivita käsurealt **geomine_oneline** koos argumendiga aarde ID numbriga või URL-iga:  
`python3 geomine_oneline.py ####` kus `####` on aarde ID või URL
Seejärel sisesta geopeituse kasutajanimi ja parool.  
Programm väljastab käsureale kopeeritaval kujul aarde põhiinfo.

## Testitud seadmed
* Garmin Etrex 30 (Software v 2.90)

## Changelog
* 0.4.0 - Lisatud sisselogimine kuna koordinaadid on peidetud, samuti on muutunud kuupäevaformaat
* 0.3.1 - Täpsustatud logitüüpe.
* 0.3.0 - lisatud geomine_oneline, mis salvestab aarde põhiinfo tekstireana
* 0.2.0 - koodibaas viidud üle Python 3.6-le
* 0.1.0 - esimene versioon (Python 2.7)
