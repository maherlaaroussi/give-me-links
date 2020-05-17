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
        check_call("wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz".split())
        check_call("tar -xzvf geckodriver-v0.26.0-linux64.tar.gz".split())
        check_call("rm geckodriver-v0.26.0-linux64.tar.gz".split())
        check_call("sudo mv geckodriver /usr/local/bin".split())
        check_call("pip install -r requirements.txt --user".split())
        install.run(self)


setup(
    name = cfg.NAME,
    version = cfg.VERSION,
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
