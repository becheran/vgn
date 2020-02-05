import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vgn",
    version="0.0.1",
    author="Armin Becher",
    author_email="becherarmin@gmail.com",
    description="VGN API for python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/becheran/vgn",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.6.2,<3',
    ],
    setup_requires=['wheel'],
)
