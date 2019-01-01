import joblib
from skimage.feature import hog
import numpy as np
from contextlib import contextmanager

clf = joblib.load("../resources/digits_all_cls-4-4.pkl")
#@contextmanager
#def __get_svm_model():
    #clf = joblib.load("../resources/digits_all_cls-3-4.pkl")
    #yield clf

def predict_digits(digits):
    predicted = np.empty(5)
    #clf = joblib.load("../resources/digits_all_cls.pkl")
    i = 0
    for digit in digits:
        hog_features = hog(digit, orientations=18, pixels_per_cell=(8, 8), cells_per_block=(1, 1), visualise=False,
                           normalise=True)
        hog_features = np.array([hog_features], 'float64')
        #print roi_hog_fd.
        predicted[i] = clf.predict(hog_features)
        i = i + 1
    return predicted
