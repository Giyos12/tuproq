import pickle
from sklearn.svm import SVC
from uath.models import Model


# preprocessing = pickle.load(open("pre_humus.pkl", 'rb'))
# model = pickle.load(open("humus.pkl", 'rb'))

def bashorat(B1, B2, B3, B4, B5, B6, B7, B10):
    m1 = Model.objects.get(order=0)
    preprocessing = pickle.load(open(m1.file1norm.path, 'rb'))
    model = pickle.load(open(m1.file1.path, 'rb'))
    data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
    pred = model.predict(data)
    return pred
