from setuptools import find_packages, setup

setup(
    name='recyclus',
    version='0.3.0',
    license='BSD',
    maintainer='Yarden Livnat',
    description='Client for Recyclus remote services',
    url='https://github.com/yarden-livnat/recyclus',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pp-ez',
        'pprintpp',
        'requests',
        'requests_jwt',
        'pyyaml'
    ],
    extras_require={
        # 'test': [
        #     'pytest',
        #     'coverage',
        # ],
    },
)
