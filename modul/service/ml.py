import pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import pickle
from keras.models import load_model
import numpy as np

def bashorat(B1, B2, B3, B4, B5, B6, B7, B10, file, filenorm, is_dl):
    if is_dl == False:
        preprocessing = pickle.load(open(filenorm.path, 'rb'))
        model = pickle.load(open(file.path, 'rb'))
        data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
        pred = model.predict(data)
        return pred
    else:
        preprocessing = pickle.load(open(filenorm.path, 'rb'))
        model = load_model(file.path)
        data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
        pred = np.argmax(np.around(model.predict(data)), axis=1) + 1
        return pred




