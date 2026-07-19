from setuptools import setup, find_packages

setup(
    name="image2stl",
    version="0.1.0",
    description="Convert 2D images to 3D STL files",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "image2stl=cli.main:cli",
        ],
    },
    install_requires=[
        "Pillow==10.1.0",
        "numpy==1.26.2",
        "scipy==1.11.4",
        "trimesh==4.0.0",
        "Click==8.1.7",
    ],
    python_requires=">=3.8",
)
