import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='library',
    version='0.1',
    author='Simply Equipped LLC',
    author_email='howard@simplyequipped.com',
    description='Python package for running local library services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simplyequipped/library',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.6.1'
)
