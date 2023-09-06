import os
from pathlib import Path
from qgis.core import *

# on save, the name will be file name, and 'builtins' while running
print(__name__)

if __name__ == "builtins":
    # path of QGIS project file
    project_file_path = Path(QgsProject.instance().absoluteFilePath())
    project_directory_path = project_file_path.parent

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
