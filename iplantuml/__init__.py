import argparse
import os
import subprocess
import uuid

from IPython.core.magic import register_cell_magic
from IPython.display import SVG

import plantweb  # dummy import to ensure plantweb module is present


__title__ = "iplantuml"
__description__ = "Package which adds a PlantUML cell magic to IPython."
__uri__ = "https://github.com/jbn/iplantuml"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 John Bjorn Nelson"
__version__ = "0.1.0"
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"

###############################################################################
# If you install with `setup.py`, it can overwrite this path. But, bitaxis's
# PR is better for most cases. Launching the JVM each time is slow and
# resource intensivel. Web requests are better. You don't need Java anymore.
###############################################################################

PLANTUMLPATH = '/usr/local/bin/plantuml.jar'


def _exec_and_get_paths(cmd, file_names):
    subprocess.check_call(cmd, shell=False, stderr=subprocess.STDOUT)

    return [os.path.splitext(f)[0] + ".svg" for f in file_names]


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

    return _exec_and_get_paths(cmd, file_names)


def plantuml_web(*file_names, **kwargs):
    """
    Given a list of UML documents, generate corresponding SVG diagrams, using
    PlantUML's web service via the plantweb module.

    :param file_names: the filenames of the documents for parsing by PlantUML.
    :return: the path to the generated SVG UML diagram.
    """
    cmd = ["plantweb",
           "--format",
           "auto"] + list(file_names)

    return _exec_and_get_paths(cmd, file_names)


@register_cell_magic
def plantuml(line, cell):
    """
    Generate and inline the SVG portrayal of the given PlantUML UML spec.

    :param line: if not empty, it is the base file name to give to the
        serialized cell contents and the generated SVG files.
    :param cell: the PlantUML language UML specification.
    :return: a IPython SVG object for the diagram or None given error.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jar", action="store_true",
                        help="render using plantuml.jar (default is plantweb)")
    parser.add_argument("-n", "--name", type=str, default=None,
                        help="persist as <name>.uml and <name>.svg after rendering")
    parser.add_argument("-p", "--plantuml-path", default=None,
                        help="specify PlantUML jar path (default={})".format(PLANTUMLPATH))
    args = parser.parse_args(line.split() if line else "")
    retain = args.name is not None
    base_name = args.name or str(uuid.uuid4())
    use_web = not (args.jar or args.plantuml_path)

    uml_path = base_name + ".uml"
    with open(uml_path, 'w') as fp:
        fp.write(cell)

    try:
        output = None
        if use_web:
            output = plantuml_web(uml_path)
        else:
            plantuml_path = os.path.abspath(args.plantuml_path or PLANTUMLPATH)
            plantuml_exec(uml_path, plantuml_path=plantuml_path)
        svg_name = output[0]
        return SVG(filename=svg_name)
    finally:
        if not retain:
            if os.path.exists(uml_path):
                os.unlink(uml_path)
            svg_path = base_name + ".svg"
            if os.path.exists(svg_path):
                os.unlink(svg_path)
