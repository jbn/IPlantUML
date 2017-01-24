from __future__ import print_function
import os
import os.path
from distutils.core import setup
from distutils.command.install import install as _install
import fileinput


def search_and_replace(jarpath):
    filename = os.path.join('iplantuml', '__init__.py')
    run_once = True
    # rewrite __init__.py in place modifying the PLANTUMLPATH on the go.
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            if line[:12] == 'PLANTUMLPATH':
                print('PLANTUMLPATH = \'{}\''.format(jarpath))
            else:
                # suppress endline with end='', line already has one
                print(line, end='')


class InstallCommand(_install):
    user_options = _install.user_options + [ ('jarpath=', None, 'path of plantuml.jar') ]

    def initialize_options(self):
        super().initialize_options()
        self.jarpath = None

    def finalize_options(self):
        super().finalize_options()
        if self.jarpath is not None:
            search_and_replace(self.jarpath)

    def run(self):
        super().run()


README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name="IPlantUML",
    version="0.0.4",
    packages=["iplantuml"],
    license="License :: OSI Approved :: MIT License",
    description="Python package defining PlantUML cell magic for IPython.",
    long_description=open(README_FILE).read(),
    data_files=['README.md'],
    cmdclass={'install':InstallCommand},
)
