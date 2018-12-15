import sys
import du2_kristyna_mechurova
from du2_kristyna_mechurova import open_json
sys.argv[1] ="body_adresy.geojson"
sys.argv[2]="body_adresy_vystup.geojson"

#def test_argv():
#    assert du2_kristyna_mechurova("body_adresy.geojson" "body_adresy_vystup.geojson")==True


def test_existopen_file():
    assert open_json("body_adresy.geojson")==gj
    #assert open_json("body_adresy_kec.geojson")==False
"""    
def test_incorrect_geojson():
    
def test_correct_geojson_imput():
    
def test_points_50():
"""

