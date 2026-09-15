"""The DROID-SLAM python package (strapsai mirror, CHIRON reid mapping).

Pure python: the bare top-level modules exactly as upstream imports them
(`from droid import Droid`, `from factor_graph import FactorGraph`) plus the
geom / modules / data_readers / visualizer packages. No CUDA build here: the
droid_backends extension is built from ../src (src/setup.py) and lives in the
reid image; this package colcon-builds from reid_ws/src (version_control/
reid.yaml), so the workspace overlay is the one importable copy of the code.

colcon's --symlink-install (setup.py develop) puts THIS directory's build
mirror on PYTHONPATH, which is why the package root is droid_slam/ itself and
not the repository root: the flat module names must sit directly under it.
"""
import os.path as osp
from glob import glob

from setuptools import find_packages, setup

HERE = osp.dirname(osp.abspath(__file__))

setup(
    name='droid_slam',
    version='0.1.0',
    packages=find_packages(where=HERE),
    py_modules=[osp.splitext(osp.basename(p))[0]
                for p in sorted(glob(osp.join(HERE, '*.py')))
                if osp.basename(p) != 'setup.py'],
)
