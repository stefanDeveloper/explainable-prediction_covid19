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
