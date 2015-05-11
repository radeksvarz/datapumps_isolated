# coding=utf-8

from setuptools import setup

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
    # http://stackoverflow.com/a/23265673/752142
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
setup(
    name='dataviso_sequencer',
    version='0.0.1',
    description='TODO Add description',

    # ########################################################################
    #
    # README.rst is generated from README.md:
    #
    # $ pandoc --from=markdown --to=rst README.md -o .tmp/README.rst
    #
    # ~ OR ~
    #
    # $ fab build
    # ########################################################################
    long_description=read_md('README.md'),

    url='https://github.com/radeksvarz/datapumps_isolated',
    license='MIT',
    author='TBA',
    author_email='example@example.com',

    # The exclude makes sure that a top-level tests package doesn’t get
    # installed (it’s still part of the source distribution)
    # since that would wreak havoc.
    # find_packages(exclude=['tests*'])
    packages=[
        "dataviso_sequencer",
        "dataviso_sequencer.lib",
        "dataviso_sequencer.lib_impl",
        "dataviso_sequencer.types"
    ],


    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
)
