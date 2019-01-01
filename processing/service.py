import manager
import cv2
from classifier import svm


def get_predicted_numbers_from_image(image):
    most_likely_rois = manager.get_most_likely_rois_from_image(image)
    digits = manager.get_most_likely_digits_from_image(most_likely_rois)
    predicted_numbers = svm.predict_digits(digits)

    return predicted_numbers


def get_predicted_numbers_as_string_from_image(image):
    predicted_numbers = get_predicted_numbers_from_image(image)
    predicted_numbers_as_string = __convert_np_array_to_string(predicted_numbers)
    return predicted_numbers_as_string


def __convert_np_array_to_string(array):
    string = ''
    for i in range(int(array.shape[0])):
        print array[i]
        string += str(int(array[i]))
    return string


if __name__ == "__main__":
    image = cv2.imread('../resources/watermeter2.png')
    print get_predicted_numbers_from_image(image)
