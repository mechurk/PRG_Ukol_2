Dokumentace úkol_2

Dělení adresních bodů

Program na dělení vstupních bodů do skupin podle polohy bodů a počtu bodů ve skupině.

Vstupní parametry:
   Vstupní json: soubor ve formátu json obsahující mimo jiné souřadnice x,y a specifické ID bodu
   
Výstupní parametry: 
    Výstupní json: soubor ve formátu json obsahující všehny paramatetry vstupního souboru a navíc sloupec cluster_id
    
    
Běh programu:
    Program vytvoří box kolem vstupní množiny bodů, pokud je bodů v daném boxu více, jak definované číslo, program
    rozdělí box na čtvrtiny a znovu se zeptá na počet bodů v daném boxu. Tak je tomu až do doby, kdy jsou všchny body
    rozděleny na skupiny, které obsahují maximálně padesát bodů. Poté je z daných bodů vytvořen nový soubor ve formátu json 
    který obsahuje atribut cluster_id. 
    
   Cluster_id= délka čísla znázorňuje hloubku zanoření daného boxu, číslo v každé hloubce značí příslušnost dané čtvrtině.
               číslo 1 = levá horní čtvrtina,
               číslo 2 = pravá horní čtvrtina,
               číslo 3 = levá dolní čtvrtina,
               číslo 4 = pravá dolní čtvrtina
               
   př: cluster_id: 142 - hloubka boxu 3, v prním boxu příslušnost k 1. čtvrtině, v druhém boxu(hloubka 2)
   příslušnost k čtvrté čtvrtině atd.
    
    