from typing import Optional

from setuptools import setup, find_packages


package_name = 'vuakhter'


def get_version() -> Optional[str]:
    with open('vuakhter/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='Package to count usage statistics from ELK logs.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='kibana statistics',
    version=get_version(),
    author='BestDoctor',
    author_email='s.butkin@bestdoctor.ru',
    install_requires=[
        'setuptools',
        'elasticsearch>=7.0.0,<8.0.0',
        'elasticsearch-dsl>=7.0.0,<8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'vuakhter = vuakhter.scripts.process:main',
        ],
    },
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
