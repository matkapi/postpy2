from distutils.core import setup

setup(
    name='postpy2',
    packages=['postpy2'],
    version='0.0.1',
    description='A library to use postman collection V2 in python. Inspired by https://github.com/k3rn3l-p4n1c/postpython Bardia Heydari nejad',
    author='Martin Kapinos',
    author_email='matkapi19@gmail.com',
    url='https://github.com/matkapi/postpy2',
    # I'll explain this in a second
    download_url='https://codeload.github.com/matkapi/postpy2/zip/master',
    keywords=['postman', 'rest', 'api'],  # arbitrary keywords
    install_requires=[
        'requests',
    ],
    classifiers=[],
)
