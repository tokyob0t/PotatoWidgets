from setuptools import find_packages, setup

setup(
    name="PotatoWidgets",
    version="1.0.6",
    packages=find_packages(),
    install_requires=["PyGObject"],
    entry_points={
        "console_scripts": [
            "potato_widgets = PotatoWidgets.main:main",
        ],
    },
    author="T0kyoB0y",
    description="Widget system based on Python, using GTK+ and GtkLayerShell.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/T0kyoB0y/PotatoWidgets",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="GTK+ GtkLayerShell widget python",
    project_urls={
        "Source": "https://github.com/T0kyoB0y/PotatoWidgets",
    },
)
