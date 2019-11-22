import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='postpy2',
    packages=['postpy2'],
    version='0.0.2',
    author='Martin Kapinos',
    author_email='matkapi19@gmail.com',
    description='A library to use postman collection V2 in python. Inspired by https://github.com/k3rn3l-p4n1c/postpython Bardia Heydari nejad',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/matkapi/postpy2',
    download_url='https://codeload.github.com/matkapi/postpy2/zip/master',
    keywords=['postman', 'rest', 'api'],  # arbitrary keywords
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
