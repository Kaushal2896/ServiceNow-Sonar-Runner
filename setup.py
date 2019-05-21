import setuptools
setuptools.setup(
    name="sonar-uploader",
    version="0.0.1",
    author="kaushal28",
    author_email="kaushal.shah95@gmail.com",
    description="A small example package",
    long_description_content_type="text/markdown",
    install_requires=[
        'argparse',
        'paramiko == 2.4.2',
        'scp == 0.13.2'
   ],
)