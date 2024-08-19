# nrl

## Running an existing project
Navigate to the root of the repository where the poetry.toml file is.

You must first install the required version of python with pyenv and set that to the local for the repository.



$ pyenv install $PYTHON_VERSION
$ pyenv local $PYTHON_VERSION
After running this command, .python-version will be in the root of the repository.

Then explicitly tell poetry to use the new version of python that has been installed.



$ poetry env use ~/.pyenv/versions/$PYTHON_VERSION/bin/python
After this, there will be a .venv folder that contains the python environment that poetry will use.

Now that poetry has been explicitly told what environment to use, you can install the rest of the dependencies in the toml file.



$ poetry install
We have had issues with poetry in the past, this is the best way to ensure that the correct version of python is used for the environment.

To activate the environment in the shell.

$poetry shell

To deactivate the environment.

$exit

