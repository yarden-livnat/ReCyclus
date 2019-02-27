from setuptools import find_packages, setup

setup(
    name='recyclus',
    version='0.1.0',
    license='BSD',
    maintainer='Yarden Livnat',
    description='Client for Recyclus remote services',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
