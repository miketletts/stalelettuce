from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='stalelettuce',
    version='0.1',
    description='A package for making data analysis at LeafLink easier.',
    long_description=readme(),
    classifiers=[
        'Operating System :: MacOS',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    url='https://github.com/miketletts/stalelettuce',
    author='Michael Letts',
    author_email='michael.letts@leaflink.com',
    license='MIT',
    packages=['stalelettuce'],
    install_requires=[
        'pandas',
        'psycopg2-binary',
        'SQLalchemy'
    ],
    include_package_data=True,
    zip_safe=False)
