import os
import subprocess

from IPython.core.magic import register_cell_magic
from IPython.display import SVG

PLANTUMLPATH = '/usr/local/bin/plantuml.jar'

def plantuml_exec(*file_names, **kwargs):
    """
    Given a list of UML documents, generate corresponding SVG diagrams.

    :param file_names: the filenames of the documents for parsing by PlantUML.
    :param kwargs: optionally `plantuml_path`, indicating where the PlantUML
        jar file resides.
    :return: the path to the generated SVG UML diagram.
    """
    plantuml_path = kwargs.get('plantuml_path', PLANTUMLPATH)

    cmd = ["java",
           "-splash:no",
           "-jar", plantuml_path,
           "-tsvg"] + list(file_names)

    subprocess.check_call(cmd, shell=False, stderr=subprocess.STDOUT)

    return [os.path.splitext(f)[0] + ".svg" for f in file_names]


@register_cell_magic
def plantuml(line, cell):
    """
    Generate and inline the SVG portrayal of the given PlantUML UML spec.

    :param line: if not empty, it is the base file name to give to the
        serialized cell contents and the generated SVG files.
    :param cell: the PlantUML language UML specification.
    :return: a IPython SVG object for the diagram or None given error.
    """
    if line:
        retain, base_name = True, os.path.splitext(line)[0]
    else:
        retain, base_name = False, "tmp"

    uml_path = base_name + ".uml"
    with open(uml_path, 'w') as fp:
        fp.write(cell)

    try:
        svg_name = plantuml_exec(uml_path)[0]
        return SVG(filename=svg_name)
    finally:
        if not retain:
            os.unlink(uml_path)

            svg_path = base_name + ".svg"
            if os.path.exists(svg_path):
                os.unlink(svg_path)
