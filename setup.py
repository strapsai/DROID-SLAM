"""Dual-mode packaging for the strapsai mirror (CHIRON reid mapping).

Default (colcon / plain pip in reid_ws): installs the droid_slam python
modules ONLY — bare top-level modules exactly as upstream imports them
(`from droid import Droid`), no CUDA compilation. The image keeps code out
(UFM pattern); the workspace overlay provides it.

DROID_BUILD_EXTENSIONS=1 (the 08b-reid dockerfile): builds and installs ONLY
the droid_backends CUDA extension — the image bakes deps, never code.
lietorch is installed separately from thirdparty/lietorch (also image-side).
"""
import os
import os.path as osp
from glob import glob

from setuptools import setup, find_packages

ROOT = osp.dirname(osp.abspath(__file__))

if os.environ.get('DROID_BUILD_EXTENSIONS') == '1':
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension
    setup(
        name='droid_backends',
        version='0.1.0',
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
else:
    setup(
        name='droid_slam',
        version='0.1.0',
        package_dir={'': 'droid_slam'},
        packages=find_packages(where='droid_slam'),
        py_modules=[osp.splitext(osp.basename(p))[0]
                    for p in glob(osp.join(ROOT, 'droid_slam', '*.py'))],
    )
