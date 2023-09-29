# -*- coding: utf-8 -*-
import os
from pathlib import Path
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import *
from qgis.processing import alg
from qgis.utils import iface


@alg(
    name="savecorallayersalg",
    label="Save vector layers",
    group="coralannotation",
    group_label="Coral annotation",
)
@alg.input(type=alg.BOOL, name="run", label="Save vector layers", default=True)
@alg.output(type=alg.BOOL, name="indicator", label="Success indicator")
def save_layers_alg(instance, parameters, context, feedback, inputs):
    """
    Saves vector layers to an annotations directory.
    """
    to_save = instance.parameterAsBool(parameters, "run", context)
    feedback.pushInfo("here")

    if to_save:
        # path of QGIS project file
        if QgsProject.instance().absoluteFilePath() == "":
            raise QgsProcessingException(
                "The project file is not saved. Save the project file before saving the layers"
            )

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
    else:
        return {"output": False}
