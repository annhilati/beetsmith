from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme:
    description = readme.read() 
   
setup(
    name="beetsmith",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "beet"
        ],
    author="Annhilati",
    description="",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/annhilati/beetsmith"
)