from qgis.core import *

# on save, the name will be file name, and 'builtins' while running
print(__name__)

if __name__ == "builtins":
    root = QgsProject.instance().layerTreeRoot()
    annotation_group = root.addGroup("annotations")

    def addTmpLayer(name):
        layer = QgsVectorLayer("Polygon", name, "memory")
        QgsProject.instance().addMapLayer(layer, False)
        annotation_group.addLayer(layer)

    # add ring layers
    [addTmpLayer(f"R{i}") for i in range(10)]
    # add other layers
    addTmpLayer("overgrowth")
    addTmpLayer("uncertain")
    addTmpLayer("erosion")
