import geojson
import json
import sys

"""Dělení adresních bodů"""


input_file= sys.argv[1] #"body_adresy.geojson"
out_file = sys.argv[2] #"body_adresy_vystup.geojson"

if len(sys.argv)!=3:
    print ("Chybný počet vstupních parametrů")
    exit(1)
try:
    if sys.argv [2][-7:]=="geojson":
        out_file = sys.argv[2]
except ValueError:
    print ("Výstupní soubor není geojson")
    exit (4)


def open_json(input_file_name):
    """otevre vstupni geojson
        vstup: input_file: soubor geojson
        výstup: načtnená data vstupního souboru"""
    try:
        with open(input_file_name, encoding='utf-8') as f:
            gj = geojson.load(f)
    except FileNotFoundError:
        print ("soubor nenalezen")
        exit (1)
    except UnicodeError:
        print ("Chybný vstupní soubor")
        exit (2)

    #adress = gj['features'][0]
    #print(adress)
    return(gj)

def create_list(gj):
    """vytvori list ze vstupních dat obsahujicí x,y souřadnice a ID bodu
        vstup: gj:načtená data vstupního souboru
        výstup: list bodu """

    points = []
    for issues in gj['features']:
        ID = issues['properties']['@id']
        coord = issues['geometry']['coordinates']
        points.append([ID, coord[0], coord[1]])
    return (points)

#print(points)


def calc_bbox(points):
    """vypocita bouding box okolo vstupních bodů
            vstup:list bodu
            vystup:list obsahující souřadnice bouding boxu"""
    minx = float("inf")
    miny = float("inf")
    maxx = float("-inf")
    maxy = float("-inf")
    for point in points:
        if point[1] < minx:
            minx = point[1] - 0.000000001 #oseteni bodu leziciho na linii bouding boxu
        if point[1] > maxx:
            maxx = point[1] + 0.000000001
        if point[2] < miny:
            miny = point[2] - 0.000000001
        if point[2] > maxy:
            maxy = point[2] + 0.000000001
    bbox = [minx, miny, maxx, maxy]
    print(minx, miny, maxx, maxy)
    return (bbox)


def processQuarter(points, box, cluster_id):
    """ rekurzivni deleni bouding boxu na čtvrtiny s omezující podmínkou počtu bodů
            vstup: points:list bodu
                    box:souradnice bouding boxu
                    cluster_id: příslušnost bodu ke čtvrtině
            výstup: list bodů s definovaným ID skupiny"""
    pointsInThisBox = pointsInBox(points, box)
    if (len(pointsInThisBox) < 50):
        for point in pointsInThisBox:
            point.append(int(cluster_id))
        return
    else:
        processQuarter(pointsInThisBox, topLeft(box), cluster_id + "1")
        processQuarter(pointsInThisBox, topRight(box), cluster_id + "2")
        processQuarter(pointsInThisBox, bottomLeft(box), cluster_id + "3")
        processQuarter(pointsInThisBox, bottomRight(box), cluster_id + "4")


def pointsInBox(body, bbox):
    """pocet bodu v danem bounding boxu
        vstup:  body:list vstupích bodů
                bbox:souřadnice bouding boxu
        výstup: body příslušící danému bouding boxu"""
    return [point for point in body if bbox[0] <= point[1] < bbox[2] and bbox[1] <= point[2] < bbox[3]] #ošetření bodu ležícího na dělících čárách


def topLeft(box):
    """definice leveho horniho boxu
        vstup:  box: list souradnic puvodniho boxu
        výstup: list souřadnic levého horního boxu"""
    middle = [(box[2] + box[0]) / 2, (box[3] + box[1]) / 2]
    qbox = [box[0], middle[1], middle[0], box[3]]
    return qbox


def topRight(box):
    """definice pravého horniho boxu
        vstup:  box: list souradnic puvodniho boxu
        výstup: list souřadnic pravého horního boxu"""
    middle = [(box[2] + box[0]) / 2, (box[3] + box[1]) / 2]
    qbox = [middle[0], middle[1], box[2], box[3]]
    return qbox


def bottomLeft(box):
    """definice levého dolního boxu
        vstup:  box: list souradnic puvodniho boxu
        výstup: list souřadnic pravého levého dolního"""
    middle = [(box[2] + box[0]) / 2, (box[3] + box[1]) / 2]
    qbox = [box[0], box[1], middle[0], middle[1]]
    return qbox


def bottomRight(box):
    """definice pravého dolního boxu
        vstup:  box: list souradnic puvodniho boxu
        výstup: list souřadnic pravého pravého dolního"""
    middle = [(box[2] + box[0]) / 2, (box[3] + box[1]) / 2]
    qbox = [middle[0], box[1], box[2], middle[1]]
    return qbox


def create_output(gj,points):
    """spáruje list a vstupní json a vytvoří výstupní json
            vstup: gj: vstupní json
                    points: list rozdelených bodů"""
    for feature in gj['features']:
        for point in points:
            if feature['properties']['@id'] == point[0]:
                feature['properties']['cluster_id'] = point[3]
                break
    try:
        with open(out_file, 'w') as out:
            json.dump(gj, out)
    except FileNotFoundError:
        print("chyba zápisu, soubor nenalezen")
        exit (5)
    except PermissionError:
        print ("není povolený zápis do souboru")
        exit (6)


gj=open_json(input_file)
points=create_list(gj)
box = calc_bbox(points)
processQuarter(points, box, "")
print(points)
create_output(gj,points)