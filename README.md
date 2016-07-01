![Alt test](doc/source/_static/logo.png)

# Installation
**Note** conda build coming soon! 
The typical Python data stack is required (example using the **conda** package manager).
```
conda install numpy scipy pandas seaborn scikit-learn jupyter notebook ipywidgets sphinx
```
Currently there are some growing pains associated with our dependencies. Ensure that
you have identical version numbers on ipywidgets and jupyter-client (eg. ipywidgets=4.1.1 
and jupyter-client=4.1.1).

From inside the git repository, exa can be installed using:
```
pip install .
```


# Getting Started


# Documentation
Documentation is generated using [sphinx](http://sphinx-doc.org "Sphinx")
```
cd doc
make html
or
cd doc
.\make.bat html
```
and open in your favorite browser.
