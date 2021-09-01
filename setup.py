import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='postpygraphql',
    packages=['postpygraphql'],
    version='0.0.2',
    author='Dmitriy Tregubov',
    author_email='hedin358@mail.ru',
    description='A library to use postman collection V2.1 in python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dtregubov/postpygraphql',
    download_url='https://codeload.github.com/dtregubov/postpygraphql/zip/master',
    keywords=['postman', 'python', 'graphql', 'rest', 'api'],  # arbitrary keywords
    install_requires=[
        'requests',
        'python-magic'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
