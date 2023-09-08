# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *
from qgis.processing import alg


@alg(
    name="createcorallayers",
    label="Create layers",
    group="coralannotation",
    group_label="Coral annotation",
)
@alg.input(type=alg.BOOL, name="OVERGROWTH", label="Overgrowth", default=True)
@alg.input(type=alg.BOOL, name="EROSION", label="Erosion", default=True)
@alg.input(type=alg.BOOL, name="UNCERTAIN", label="Uncertain", default=True)
@alg.input(type=alg.BOOL, name="WHOLE_CORAL", label="Whole Coral", default=True)
@alg.input(type=alg.BOOL, name="CENTER", label="Center", default=True)
@alg.input(
    type=alg.INT,
    name="MIN_RING_NUM",
    label="Minimum ring number",
    default=0,
    minValue=0,
    maxValue=30,
)
@alg.input(
    type=alg.INT,
    name="MAX_RING_NUM",
    label="Maximum ring number",
    default=10,
    minValue=0,
    maxValue=30,
)
@alg.output(type=alg.BOOL, name="indicator", label="indicator")
def processAlgorithm(instance, parameters, context, feedback, inputs):
    """
    Here is where the processing itself takes place.
    """
    min_ring_num = instance.parameterAsInt(parameters, "MIN_RING_NUM", context)
    max_ring_num = instance.parameterAsInt(parameters, "MAX_RING_NUM", context)
    overgrowth = instance.parameterAsBool(parameters, "OVERGROWTH", context)
    erosion = instance.parameterAsBool(parameters, "EROSION", context)
    uncertain = instance.parameterAsBool(parameters, "UNCERTAIN", context)
    whole_coral = instance.parameterAsBool(parameters, "WHOLE_CORAL", context)
    center = instance.parameterAsBool(parameters, "CENTER", context)

    feedback.pushInfo(f"Min ring num: {min_ring_num}, type {type(min_ring_num)}")
    feedback.pushInfo(f"og: {overgrowth}, type {type(overgrowth)}")

    root = QgsProject.instance().layerTreeRoot()
    annotation_group = root.addGroup("annotations")

    def addTmpLayer(name):
        layer = QgsVectorLayer("Polygon", name, "memory")
        QgsProject.instance().addMapLayer(layer, False)
        annotation_group.addLayer(layer)

    # add ring layers
    [addTmpLayer(f"R{i}") for i in range(min_ring_num, max_ring_num)]
    # add other layers
    if overgrowth:
        addTmpLayer("overgrowth")
    if uncertain:
        addTmpLayer("uncertain")
    if erosion:
        addTmpLayer("erosion")
    if whole_coral:
        addTmpLayer("whole_coral")
    if center:
        addTmpLayer("center")

    return {"OUTPUT": True}
