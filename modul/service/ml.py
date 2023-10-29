import pickle
from sklearn.svm import SVC
from uath.models import Model


# preprocessing = pickle.load(open("pre_humus.pkl", 'rb'))
# model = pickle.load(open("humus.pkl", 'rb'))

def bashorat(B1, B2, B3, B4, B5, B6, B7, B10,file,filenorm):
    preprocessing = pickle.load(open(filenorm.path, 'rb'))
    model = pickle.load(open(file.path, 'rb'))
    data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
    pred = model.predict(data)
    return pred
