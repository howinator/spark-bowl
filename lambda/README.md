# Development && Deployment Guide

## Setting up local development

* Create a virtualenv with python version 3.6
    * `pyenv virtualenv 3.6.1 spark-bowl && pyenv activate spark-bowl`
* Install requirements in `lambda/infra/requirements`
    * `pip install -r lambda/infra/requirements/base.txt`

## Testing local code

* To run tests, `python lambda/src/tests.py`
