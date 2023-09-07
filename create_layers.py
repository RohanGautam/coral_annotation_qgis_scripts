# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *


class CreateLayersAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm creates relavant temporary scratch layers for coral annotation.

    All Processing algorithms should extend the QgsProcessingAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    # INPUT = "INPUT"
    OVERGROWTH = "OVERGROWTH"
    EROSION = "EROSION"
    UNCERTAIN = "UNCERTAIN"
    WHOLE_CORAL = "WHOLE_CORAL"
    MIN_RING_NUM = "MIN_RING_NUM"
    MAX_RING_NUM = "MAX_RING_NUM"
    OUTPUT = "OUTPUT"

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return CreateLayersAlgorithm()

    def name(self):
        return "coral_annotation_create_layers"

    def displayName(self):
        return self.tr("Create layers")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Coral annotation")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "coralannotation"

    def shortHelpString(self):
        return self.tr(
            "Create relavant temporary vector layers for coral annotation purposes"
        )

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.WHOLE_CORAL, self.tr("Whole coral"), True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.OVERGROWTH, self.tr("Overgrowth"), True)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.UNCERTAIN, self.tr("Uncertain"), True)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.EROSION, self.tr("Erosion"), True)
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_RING_NUM,
                self.tr("Minimum ring number"),
                defaultValue=0,
                minValue=0,
                maxValue=30,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_RING_NUM,
                self.tr("Maximum ring number"),
                defaultValue=10,
                minValue=0,
                maxValue=30,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        min_ring_num = self.parameterAsInt(parameters, self.MIN_RING_NUM, context)
        max_ring_num = self.parameterAsInt(parameters, self.MAX_RING_NUM, context)
        overgrowth = self.parameterAsBool(parameters, self.OVERGROWTH, context)
        erosion = self.parameterAsBool(parameters, self.EROSION, context)
        uncertain = self.parameterAsBool(parameters, self.UNCERTAIN, context)
        whole_coral = self.parameterAsBool(parameters, self.WHOLE_CORAL, context)

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

        return {self.OUTPUT: True}
