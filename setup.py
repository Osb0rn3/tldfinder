from setuptools import setup, find_packages

setup(
    name='tldfinder',
    version='1.0.2',
    py_modules=['tldfinder'],
    author='Amirmohammad Safari',
    author_email='amirmohammad@myyahoo.com',
    description='Discover bug bounty scopes associated with star top-level domains (TLDs).',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'tldfinder=tldfinder:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
