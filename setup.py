import pathlib

from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='netbench',
    version='0.1.0',
    description='CLI utility that wraps a bunch of network benchmarks for ease of use.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/atc-casip/netbench',
    author='Víctor Vázquez',
    author_email='victorvazrod@ugr.es',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=[
        'click',
        'pandas',
        'iperf3'
    ],
    entry_points='''
        [console_scripts]
        netbench=netbench.main:netbench
    ''',
    python_requires='>=3.6'
)
