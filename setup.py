"""strapsai mirror packaging (CHIRON reid mapping, E5 streaming odometry).

One ordinary install, GroundingDINO-style: the droid_backends CUDA extension
plus the droid_slam python modules (bare top-level names, exactly as upstream
imports them: `from droid import Droid`). Installed fully in the 08b-reid
image; lietorch installs separately from thirdparty/lietorch.
"""
import os.path as osp
from glob import glob

from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

ROOT = osp.dirname(osp.abspath(__file__))

setup(
    name='droid_slam',
    version='0.1.0',
    package_dir={'': 'droid_slam'},
    packages=find_packages(where='droid_slam'),
    py_modules=[osp.splitext(osp.basename(p))[0]
                for p in glob(osp.join(ROOT, 'droid_slam', '*.py'))],
    ext_modules=[
        CUDAExtension('droid_backends',
            include_dirs=[osp.join(ROOT, 'thirdparty/lietorch/eigen')],
            sources=[
                'src/droid.cpp',
                'src/droid_kernels.cu',
                'src/correlation_kernels.cu',
                'src/altcorr_kernel.cu',
            ],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': ['-O3'],
            }),
    ],
    cmdclass={'build_ext': BuildExtension},
)
