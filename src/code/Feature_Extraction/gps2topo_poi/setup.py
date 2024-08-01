from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3 :: Only",  # Specify Python 3 only
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
]

setup(
    name="gps2topo_poi",
    packages=find_packages(),
    version="0.1.3",
    description="A Python package to use GPS data of public transit routes and append topographical and Points of Interests (POI) related features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavindu-w/Explainable-Bus-Arrival-Time-Prediction-Model-with-Improved-Features-Related-to-Topography-and-POIs",
    keywords=['Topolographical data', 'Elevation', 'Points of Interest', 'POI', 'GPS', 'Travel Time', 'Public Transit', 'Heterogeneous Traffic Conditions'],
    author="kavindu-w",
    author_email='akwarnakulasuriya@gmail.com',
    license='MIT',
    classifiers=classifiers,
    python_requires=">=3.6",
    install_requires=['pandas', 'numpy', 'osmnx', 'tqdm'],
    project_urls={
        "Homepage": "https://github.com/kavindu-w/Explainable-Bus-Arrival-Time-Prediction-Model-with-Improved-Features-Related-to-Topography-and-POIs",
        "Source": "https://github.com/kavindu-w/Explainable-Bus-Arrival-Time-Prediction-Model-with-Improved-Features-Related-to-Topography-and-POIs/tree/main/src/code/Feature_Extraction/gps2topo_poi",
        "Download": "https://pypi.org/project/gps2topo-poi/",
    }
)