import math
import shapely

class autoKartierunterlagen:
    def __init__(self, layer, scale, paper, overlap):
        self.layer = QgsProject.instance().mapLayersByName(layer)[0]
        self.angle = None
        self.centroid = None
        self.scale = scale
        self.paper = paper
        self.paper_x = None
        self.paper_y = None
        self.overlap = overlap
        
        self.get_scale(self.scale, self.paper)
        self.ombb(self.layer)
        self.calc_centroid(self.layer)
        self.rotate(self.layer, self.angle)
        self.gitter(self.layer, self.paper_x, self.paper_y, self.overlap)
        self.rotate(self.layer, -self.angle)
        QgsProject.instance().addMapLayer(self.layer)
        
        
    def ombb(self, layer):
        result = processing.run('native:orientedminimumboundingbox',
        { 'INPUT' : layer.source(),
        'OUTPUT' : 'TEMPORARY_OUTPUT' })
        
        output = result['OUTPUT']
        
        features = output.getFeatures()
        
        for feat in features:
            attrs = feat.attributes()
            self.angle = int(attrs[10])
            
        self.layer = output
        
    def rotate(self, layer, angle):
        provider = layer.dataProvider()


        couples_id_geom = []
        for feature in layer.getFeatures():
            geom = feature.geometry()
            centroid = self.centroid
            geom.rotate(angle, centroid)
            # accumulate args to avoid rotation feature by feature
            couples_id_geom.append([feature.id(), geom])

        # Change the layer features rotation in one go
        provider.changeGeometryValues({
        couple_id_geom[0]: couple_id_geom[1] for couple_id_geom in couples_id_geom
        })

        # Refresh to see the changes
        layer.triggerRepaint()
        
        self.layer = layer
        
    def gitter(self, layer, x, y, overlap):
        result = processing.run('native:creategrid',
        { 'CRS' : layer.crs(),
        'EXTENT' : layer.extent(),
        'HOVERLAY' : overlap,
        'HSPACING' : x,
        'OUTPUT' : 'TEMPORARY_OUTPUT',
        'TYPE' : 2, 
        'VOVERLAY' : overlap,
        'VSPACING' : y })
        
        self.layer = result['OUTPUT']
        
    def calc_centroid(self, layer):
        for feature in layer.getFeatures():
            geom = feature.geometry()
            self.centroid = feature.geometry().centroid().asPoint()
        
    def get_scale(self, scale, paper):
        if paper == 'A3':
            self.paper_x = 39 * 2000 / 100
            self.paper_y = 28 * 2000 / 100
        
        
layer = 'Uraum UVS'
scale = 2000
paper = 'A3'
overlap = 100

autoKartierunterlagen(layer, scale, paper, overlap)