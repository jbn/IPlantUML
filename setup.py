import os
from distutils.core import setup


README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name="IPlantUML",
    version="0.0.2",
    packages=["iplantuml"],
    license="License :: OSI Approved :: MIT License",
    description="Python package defining PlantUML cell magic for IPython.",
    long_description=open(README_FILE).read(),
    data_files=['README.md']
)
