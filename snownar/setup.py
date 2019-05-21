import setuptools
setuptools.setup(
    name="snownar",
    packages=['snownar'],
    package_dir={'snownar': 'src'},
    version="0.0.2",
    author="kaushal28",
    entry_points={'console_scripts': ['snownar = src.__main__:main' ]},
    author_email="shah.kaushal95@gmail.com",
    description="ServiceNow sonar uploader package",
    install_requires=[
        'argparse',
        'paramiko == 2.4.2',
        'scp == 0.13.2'
   ],
)