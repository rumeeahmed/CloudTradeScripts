# Python Directory
This directory will contain all the Python scripts and programs for CloudTrade use only. Below is a detailed
explanation on the structure and usage of this directory.

## Installation & Usage
To execute any of these Python scripts an installation of `Python 3` is required which can be found from the following
[link](https://www.python.org/downloads/). An IDE is also required to make editing and executing Python code locally
easier. The standard to use is `Pycharm` which can be found [here](https://www.jetbrains.com/pycharm/). Alternatively,
scripts can be executed using `Visual Studio Code` but note that the Python module must be downloaded and installed
from the marketplace. Both applications have a green play button in the top right corner that will allow execution of
the file in question.

## Directory Structure
### Structure
The main directory will contain all the folders for each Python script which can then be opened and worked on as an
individual project in `PyCharm` or `Visual Studio Code`. The `Customer Based Scripts` directory will contain any code
that has been deployed in production. There will be sub-folders on a per-customer basis. The outer directory will
contain various scripts that may be useful for manual tasks experienced by the Operations team.

### Read Me Files
This file will contain the basic instructions to get started with the Python script in question. This will be a 
markdown, so it can be opened up using `Visual Stuidio Code` and to view the file in its native format use the command 
`Ctrl+Shift+V`.

### Requirements Files
Each project may contain a `requirements.txt` file which documents which external libraries and packages are required
for the script to function properly, if these dependencies are not installed then the program will most likely crash
and will not achieve its intended purpose.

To install any dependencies open up the terminal and type in package name using the command `pip install`. Look at the 
example below for the `requests` package. If the command is ambiguous then search for the package in PyPi, an online 
index for Python packages and there will be a copy icon for the exact command to paste into the terminal. The link to this
can be found [here](https://pypi.org/)

```python
pip install requests
```
