# Replication of Explainable Predictions of COVID-19 Infection from Chest X-rays

> Replication of Explainable Predictions of COVID-19 Infection from Chest X-rays. We want to reproduce and validate the findings that are listed in [COVID-CXR](https://github.com/aildnont/covid-cxr) repository. Furthermore, we want to apply the model on the [Kaggle Challenge](https://www.kaggle.com/c/siim-covid19-detection) dataset.

## Getting Started

Run COVID-CXR with Python<=3.7:

> Be careful: If you run it Python higher than 3.7, you might run into problems with `opencv` or `tensorflow_gpu`. If you want to use a higher version, you are on your own.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
after that follow the instructions in the [Getting Started of COVID-CXR](https://github.com/aildnont/covid-cxr#getting-started). Additionally, we have a [Colab Notebook](https://github.com/stefanDeveloper/explainable-prediction_covid19/blob/main/colab/covid-cxr.ipynb)

## Notes on this project

The folder `covid-cxr` is originally the [COVID-CXR project](https://github.com/aildnont/covid-cxr.git).
To work with it, we cloned it (commit [`bf79a5c62bdc9b58666056e31893c02515d550c7`](https://github.com/aildnont/covid-cxr/commit/bf79a5c62bdc9b58666056e31893c02515d550c7)) and modified it so that it works with a larger dataset.

This is how we set up the folder:

```sh
git clone https://github.com/aildnont/covid-cxr.git covid-cxr
# Remove git folder and docs
rm -rf covid-cxr/.git covid-cxr/.github covid-cxr/docs
```

## Run in Colab

