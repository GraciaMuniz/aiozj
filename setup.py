from setuptools import setup, find_packages


setup(
    name='aiozj',
    version='0.1',
    description='Asyncio-based client for ByteDance Platform',
    author='Rocky Feng',
    author_email='folowing@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['aiohttp>=3.6.2'],
    python_requires='>3.8.0',
    zip_safe=False,
)
