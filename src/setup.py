"""droid_backends: the DROID-SLAM CUDA extension (strapsai mirror).

Built and installed on its own, image-side (dtc-dockerfiles 08b-reid:
`pip install --no-build-isolation ./src`). The python package next door
(../droid_slam) is NOT part of this install; it colcon-builds from reid_ws.
lietorch (../thirdparty/lietorch) installs separately, also image-side.
"""
import os.path as osp

from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

HERE = osp.dirname(osp.abspath(__file__))
ROOT = osp.dirname(HERE)

setup(
    name='droid_backends',
    version='0.1.0',
    ext_modules=[
        CUDAExtension('droid_backends',
            include_dirs=[osp.join(ROOT, 'thirdparty/lietorch/eigen')],
            sources=[
                'droid.cpp',
                'droid_kernels.cu',
                'correlation_kernels.cu',
                'altcorr_kernel.cu',
            ],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': ['-O3'],
            }),
    ],
    cmdclass={'build_ext': BuildExtension},
)
