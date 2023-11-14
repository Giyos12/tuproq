import json
from modul.models import Counter
import ee
import pandas as pd

# Counter.objects.all()
ee.Initialize()
# geoJSON = {"type": "Feature", "id": 0, "geometry": {"type": "Polygon", "coordinates": [
#     [[68.49709718800005, 40.46856120900003], [68.49712098900005, 40.468605688000025],
#      [68.49713266100008, 40.468627498000046], [68.49675517400004, 40.468771805000074],
#      [68.49669780700003, 40.468793736000066], [68.49580535700005, 40.469134894000035],
#      [68.49560320100005, 40.469212173000074], [68.49535139900007, 40.469308427000044],
#      [68.49528174400007, 40.469335053000066], [68.49521997600004, 40.46935866500007],
#      [68.49469711600005, 40.469558531000075], [68.49423922600005, 40.469733560000066],
#      [68.49418804200008, 40.46975312400008], [68.49405950700003, 40.46980225600004],
#      [68.49401973700003, 40.46981745900007], [68.49393918600003, 40.46984824900005],
#      [68.49390308700004, 40.46986204700005], [68.49388060400008, 40.469870642000046],
#      [68.49375265600008, 40.469919548000064], [68.49368504300003, 40.46994291400006],
#      [68.49362837900003, 40.46996249700004], [68.49361260500007, 40.46996794800003],
#      [68.49315654200007, 40.469137655000054], [68.49314947900007, 40.46912479800005],
#      [68.49281608000007, 40.46851780800006], [68.49183392100008, 40.46881803700006],
#      [68.49182253300006, 40.46879694300003], [68.49168726500005, 40.468546375000074],
#      [68.49158929500004, 40.46835900100007], [68.49138856200005, 40.467975082000066],
#      [68.49120299400005, 40.46762016300005], [68.49103371700005, 40.467296401000056],
#      [68.49093995700008, 40.467117073000054], [68.49087851500008, 40.46699776400004],
#      [68.49086840700005, 40.46697813900005], [68.49083089900006, 40.46690530700005],
#      [68.49077458200003, 40.46679595100005], [68.49069529500008, 40.46664199500003],
#      [68.49069091600006, 40.46663349000005], [68.49066343400006, 40.46655474100004],
#      [68.49066375800004, 40.46651185500008], [68.49071090200005, 40.46646560100004],
#      [68.49074871400006, 40.466415733000076], [68.49093331600005, 40.466355219000036],
#      [68.49127820300004, 40.46624216400005], [68.49157619500005, 40.466144479000036],
#      [68.49219734800005, 40.46594085500004], [68.49237158600005, 40.46588373600008],
#      [68.49270528500006, 40.46577434200003], [68.49308122700006, 40.46565109800008],
#      [68.49316929000008, 40.46562222800003], [68.49326203900006, 40.465589273000035],
#      [68.49396660100007, 40.46538774700008], [68.49396243100006, 40.46531982400006],
#      [68.49384610500005, 40.46509952200006], [68.49428768300004, 40.464957782000056],
#      [68.49436918500004, 40.46493162000007], [68.49449797700004, 40.464891446000024],
#      [68.49450486000006, 40.46488929900005], [68.49475816700004, 40.464810285000056],
#      [68.49480862100006, 40.464794547000054], [68.49496798100006, 40.46474483600008],
#      [68.49503303700004, 40.46472454900004], [68.49517719500005, 40.464973077000025],
#      [68.49518815500005, 40.46499356100003], [68.49521336700008, 40.46504068000007],
#      [68.49526230000004, 40.465132132000065], [68.49531855900005, 40.46523727600004],
#      [68.49541806000008, 40.46542323500006], [68.49549627100004, 40.465569403000075],
#      [68.49577649000008, 40.46609310000008], [68.49585683000004, 40.466243242000075],
#      [68.49610901000005, 40.46671452900006], [68.49618503900007, 40.46685661300006],
#      [68.49628581100006, 40.46704493800007], [68.49631449400005, 40.46709854000005],
#      [68.49647534400003, 40.46739913700003], [68.49650591500006, 40.467456267000046],
#      [68.49654003800003, 40.46752003600005], [68.49667050900007, 40.46776385600003],
#      [68.49685468600006, 40.468108037000036], [68.49693151900004, 40.46825161900006],
#      [68.49706254800003, 40.46849647500005], [68.49706283100005, 40.468497006000064],
#      [68.49709718800005, 40.46856120900003]]]}, "properties": {"massiv": "Barlos", "Kontur_raq": 6947}}

# read json file konturlar.json
geoJSON = json.load(open('konturlar.json'))
print(geoJSON['features'])

for i in Counter.objects.all():
    count = 0
    id = i.counter_id
    l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    coors = geoJSON['features'][count]['geometry']['coordinates']
    aoi = ee.Geometry.Polygon(coors)
    ffa_db = ee.Image(ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
                      .filterBounds(aoi)
                      .filterDate('2021-01-01', '2021-03-02')
                      .first()
                      .clip(aoi))
    json = ffa_db.getInfo()
    print(json)
    count += 1

geoJSON = geoJSON['features'][0]
l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
coords = geoJSON['geometry']['coordinates']
aoi = ee.Geometry.Polygon(coords)

ffa_db = ee.Image(ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
                  .filterBounds(aoi)
                  .filterDate('2021-01-01', '2021-03-02')
                  .first()
                  .clip(aoi))

print(type(ffa_db.getInfo()))
# write json file

if __name__ == '__main__':
    pass
