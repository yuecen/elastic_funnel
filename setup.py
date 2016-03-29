
from setuptools import setup, find_packages

description = open('README.md').read()
requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='elastic_funnel',
    description='Analysis tool for funnel visualization with log from Elasticsearch',
    version='0.0.1',

    # Author details
    author='yuecen',
    author_email='yuecendev@gmail.com',
    long_description=description,
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    keywords='elasticsearch log funnel',
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'elastic_funnel = elastic_funnel.cli:main'
        ]
    }
)