setup(
    name="comPylador",
    version="1.0.0",
    description="Compilador del lenguaje ensamblado la máquina diseñada en clase a binario",
    long_description="None",
    long_description_content_type="text/markdown",
    url="",
    author="DdFa92",
    author_email="ddfa92ii@gmail.com",
    license="None",
    classifiers=[
        "License :: None",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["compilador"],
    include_package_data=True,
    install_requires=[
        "feedparser", "html2text", "importlib_resources", "typing"
    ],
    entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)