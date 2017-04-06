# Update Version Numbers
Update `exa/_version.py` and `meta.yaml` version numbers.


# Commit and Push Changes
Push changes to your repository (fork).
```bash
git add -A
git commit -m "message"
git push
```
Make a pull request (PR). Once accepted the organization will be tag a new release.
```bash
git tag -a X.X.X -m "message"
git push --tags
```


# Release on PyPI Testing
Publish to `TestPyPI`_ (~/.pypirc required).
```bash
python setup.py register -r pypitest    # run once
python setup.py sdist upload -r pypitest
python setup.py bdist_wheel upload -r pypitest
```


# Release on PyPI
Publish to `PyPI`_ (~/.pypirc required).
```bash
python setup.py register -r pypi     # run once
python setup.py sdist upload -r pypi
python setup.py bdist_wheel upload -r pypi
```


# Release on Anaconda
Publish to the `exa-analytics`_ channel on  `Anaconda`_
```bash
conda install conda-build    # may also need anaconda-client (run `anaconda login` in shell)
conda build .
conda convert -f --platform all /path/to/conda-bld/pltfrm/exa-...tar.bz2 -o /path/to/outputdir/
conda upload /path/to/build/build.tar.bz2    # For each build
```


# Release on NPM
Creates a new release of the JavaScript package jupyter-exa

```bash
git clean -fdx
cd js
npm install
npm publish
```

.. _PyPI: https://pypi.python.org/pypi
.. _TestPyPI: https://testpypi.python.org/pypi
.. _exa-analytics: https://anaconda.org/exaanalytics
.. _Anaconda: https://anaconda.org/
