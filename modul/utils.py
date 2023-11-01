import ee
import json


def namlik_predict(b5, b6):
    t = (float(b5) - float(b6)) / (float(b5) + float(b6))
    if -0.26 <= t < -0.16:
        return 1
    elif -0.16 <= t < - 0.06:
        return 2
    elif -0.06 <= t < 0.04:
        return 3
    elif 0.04 <= t < 0.14:
        return 4
    elif 0.14 <= t <= 0.24:
        return 5
    return 3


def ml_predict(model, data):
    return model.predict(data)


def dl_predict(model, data):
    return model.predict(data)
