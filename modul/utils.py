import ee
import json


def namlik_predict(b5, b6):
    t = (b5 - b6) / (b5 + b6)
    if -1 <= t < -0.6:
        return 1
    elif -0.6 <= t < -0.2:
        return 2
    elif -0.2 <= t < 0.2:
        return 3
    elif 0.2 <= t < 0.6:
        return 4
    elif 0.6 <= t <= 1:
        return 5


def ml_predict(model, data):
    return model.predict(data)


def dl_predict(model, data):
    return model.predict(data)
