import pickle
from sklearn.svm import SVC
from uath.models import Model
from sklearn.ensemble import RandomForestClassifier


def bashorat(B1, B2, B3, B4, B5, B6, B7, B10, file, filenorm):
    preprocessing = pickle.load(open(filenorm.path, 'rb'))
    model = pickle.load(open(file.path, 'rb'))
    data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
    pred = model.predict(data)
    return pred


def bashorat1(B1, B2, B3, B4, B5, B6, B7, B10, file, filenorm):
    preprocessing = pickle.load(open(filenorm.path, 'rb'))
    model = pickle.load(open(file.path, 'rb'))
    data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
    pred = model.predict(data)
    return pred
