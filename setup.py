from __future__ import print_function
import codecs
import re
import os
import os.path
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import fileinput

###############################################################################

NAME = 'IPlantUML'

PACKAGES = find_packages(where=".")

META_PATH = os.path.join("iplantuml", "__init__.py")

KEYWORDS = ["jupyter", "ipython", "uml", "plantuml"]

CLASSIFIERS = [
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
]

INSTALL_REQUIRES = ['plantweb']

###############################################################################

SELF_DIR = os.path.abspath(os.path.dirname(__file__))


def read_file_safely(*path_parts):
    with codecs.open(os.path.join(SELF_DIR, *path_parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read_file_safely(META_PATH)

META_VARS_RE = re.compile(r"^__([_a-zA-Z0-9]+)__ = ['\"]([^'\"]*)['\"]", re.M)

META_VARS = dict(META_VARS_RE.findall(META_FILE))

###############################################################################


def search_and_replace(jarpath):
    filename = os.path.join('iplantuml', '__init__.py')

    # rewrite __init__.py in place modifying the PLANTUMLPATH on the go.
    f = fileinput.FileInput(filename, inplace=True)

    for line in f:
        if line[:12] == 'PLANTUMLPATH':
            print('PLANTUMLPATH = \'{}\''.format(jarpath))
        else:
            # suppress endline with end='', line already has one
            print(line, end='')

    f.close()


class InstallCommand(_install):
    user_options = (_install.user_options +
                    [('jarpath=', None, 'path of plantuml.jar')])

    def initialize_options(self):
        _install.initialize_options(self)
        self.jarpath = None

    def finalize_options(self):
        _install.finalize_options(self)
        if self.jarpath is not None:
            search_and_replace(self.jarpath)

    def run(self):
        _install.run(self)


if __name__ == "__main__":
    setup(
        name=NAME,
        entry_points={'console_scripts': ['nbmerge = nbmerge:main']},
        description=META_VARS["description"],
        license=META_VARS["license"],
        url=META_VARS["uri"],
        version=META_VARS["version"],
        author=META_VARS["author"],
        author_email=META_VARS["email"],
        maintainer=META_VARS["author"],
        maintainer_email=META_VARS["email"],
        keywords=KEYWORDS,
        long_description=read_file_safely("README.rst"),
        packages=PACKAGES,
        package_dir={"": "."},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        cmdclass={'install': InstallCommand},
    )
