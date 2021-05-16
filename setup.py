import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Replace relative image path with github-hosted one
long_description = long_description.replace(
    "docs/cmd-example.gif",
    "https://raw.githubusercontent.com/amykyta3/git-me-the-url/master/docs/cmd-example.gif?sanitize=true"
)

with open(os.path.join("gitmetheurl", "__about__.py")) as f:
    v_dict = {}
    exec(f.read(), v_dict)
    version = v_dict['__version__']

setuptools.setup(
    name="git-me-the-url",
    version=version,
    author="Alex Mykyta",
    author_email="amykyta3@github.com",
    description="Generate sharable links to your Git source",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amykyta3/git-me-the-url",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ['gitmetheurl = gitmetheurl.cmd:main']
    },
    include_package_data=True,
    install_requires=[
        "gitpython",
    ],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
    ),
    project_urls={
        "Source": "https://github.com/amykyta3/git-me-the-url",
        "Tracker": "https://github.com/amykyta3/git-me-the-url/issues",
    },
)
