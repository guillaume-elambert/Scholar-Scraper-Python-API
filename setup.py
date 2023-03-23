from setuptools import setup, find_packages

setup(
    name='scholar-scraper',
    version='1.0.11',
    description='A python API to get publications from specific users on Google Scholar.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/guillaume-elambert/ScholarPythonAPI',
    keywords=['Google Scholar', 'academics', 'citations'],
    author='Guillaume ELAMBERT',
    author_email='guillaume.elambert@yahoo.fr',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=[
        'scholarly~=1.7.9',
    ],
    python_requires='>=3',
    license='GPLv3+',
)
