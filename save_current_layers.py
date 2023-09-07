# -*- coding: utf-8 -*-
import os
from pathlib import Path
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *
from qgis.processing import alg


# @alg(name='savecorallayersalg', label='Buffer and export to raster (alg)',
#      group='examplescripts', group_label='Example scripts')
# # 'INPUT' is the recommended name for the main input parameter
# @alg.input(type=alg.SOURCE, name='INPUT', label='Input vector layer')
# # 'OUTPUT' is the recommended name for the main output parameter
# @alg.input(type=alg.RASTER_LAYER_DEST, name='OUTPUT',
#            label='Raster output')
# @alg.input(type=alg.VECTOR_LAYER_DEST, name='BUFFER_OUTPUT',
#            label='Buffer output')
# @alg.input(type=alg.DISTANCE, name='BUFFERDIST', label='BUFFER DISTANCE',
#            default=1.0)
# @alg.input(type=alg.DISTANCE, name='CELLSIZE', label='RASTER CELL SIZE',
#            default=10.0)
# @alg.output(type=alg.NUMBER, name='NUMBEROFFEATURES',
#             label='Number of features processed')

# def bufferrasteralg(instance, parameters, context, feedback, inputs):
#     """
#     Description of the algorithm.
#     (If there is no comment here, you will get an error)
#     """


class SaveLayersAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm saves temporary scratch layers after coral annotation, and linkes them with locations on an annotations folder.

    All Processing algorithms should extend the QgsProcessingAlgorithm class.
    """

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return SaveLayersAlgorithm()

    def name(self):
        return "coral_annotation_save_layers"

    def displayName(self):
        return self.tr("Save vector layers")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Coral annotation2")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "coralannotation2"

    def shortHelpString(self):
        return self.tr(
            "Save temporary vector layers after/during coral annotation in an `annotations/` folder at the project root."
        )

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        return None

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        feedback.pushInfo("here")

        # path of QGIS project file
        project_file_path = Path(QgsProject.instance().absoluteFilePath())
        project_directory_path = project_file_path.parent

        feedback.pushInfo(f"Project root directory: {str(project_directory_path)}")
        # create annotations directory if needed
        annotations_dir_path = project_directory_path.joinpath("annotations")
        if not os.path.exists(annotations_dir_path):
            os.mkdir(annotations_dir_path)

        # Get current layers
        layers = list(QgsProject.instance().mapLayers().values())

        # save vector layers
        for l in layers:
            if l.type() == QgsMapLayer.VectorLayer:
                layer_name = l.name()
                path_to_save = str(annotations_dir_path.joinpath(f"{layer_name}.shp"))
                # save as shapefile
                _writer = QgsVectorFileWriter.writeAsVectorFormat(
                    l, path_to_save, "utf-8", driverName="ESRI Shapefile"
                )
                # update data source of current layer to be from memory to file contents
                l.setDataSource(
                    path_to_save + f"|layername={layer_name}", layer_name, "ogr"
                )
        return {"output": True}
