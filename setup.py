from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
from gml.settings import auto_config as cfg
import os

with open("README.md", 'r') as f:
    long_description = f.read()


project_dir = os.path.dirname(os.path.realpath(__file__))
requirements_path = project_dir + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()


class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        install.run(self)


setup(
    name = cfg.NAME,
    version = cfg.VERSION[1:],
    description = cfg.DESCRIPTION,
    license = "MIT",
    long_description = long_description,
    author = cfg.AUTHOR,
    author_email = "maher.laaroussi@gmail.com",
    url = "https://maherlaaroussi.com/",
    packages = [cfg.NAME, cfg.NAME + ".settings"],
    install_requires = install_requires,
    cmdclass = {
        'install': PreInstallCommand,
    },
)
