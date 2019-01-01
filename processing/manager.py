import cv2
from image_preprocesing import image_tresholding as tresh
from image_preprocesing import image_enhancment as ie
from processing.first_stage.first_stage import FirstStage
from metrics import utilityNumbers as un
from metrics import uitility as util


def get_most_likely_rois_from_image(image):
    adjusted = ie.adjust_gamma(image, 1.5)
    image_gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

    first_stage_processor = FirstStage(image)
    first_stage_processor.crop_image()
    first_stage_processor.apply_filtering_and_tresholding()

    #1. nadji konture na zabluranoj morphanoj slici
    #2. izostri osnovnu sliku i stavi bound rectangle od zablurane slike na izostrenu sliku
    #3. od bound rectanglova iz zablurane slike nadji 5 onih koji imaju slicnu povrsinu
    #4. ako smo isprano uzeli znamenke iz ROi-ja dobiveni 1 korakom, opet nadji konture u ROI-u i uzmi konturu s najvecom povrsinom

    #1. nadji konture na zabluranoj morphanoj slici
    (cnts, hierarchy) = first_stage_processor.getCountoursAndHierachy()

    #2. izostri osnovnu sliku i stavi bound rectangle od zablurane slike na izostrenu sliku
    #sharpened = ie.getHighBoostSharpImage(adjusted)
    #treshed = tresh.treshImageOtsuWithCorrection(sharpened, -16)

    #sharpened = ie.remove_noise_and_get_grey_img(adjusted)
    sharpened = ie.factory_method_processing(adjusted, 'homomorphic')
    treshed = tresh.treshImageOtsuWithCorrection(sharpened, -15)
    #cv2.imshow("Digit ROI", treshed)
    #cv2.waitKey(0)

    #cnts = list(filter(lambda x: (x[1][2] > 20 and x[1][3] > 20 and x[1][2] < 150 and x[1][3] < 150), cnts))
    cnts = list(filter(lambda x: (x[1][2] > 45 and x[1][3] > 45 and x[1][2] < 200 and x[1][3] < 200), cnts))
    roisAndCordinates = util.getRoiAndCourdinatesInWholeImageFromCnts(cnts, treshed)

    #3. od bound rectanglova iz zablurane slike nadji 5 onih koji su unutar Y grupe i imaju najslicnu povrsinu
    most_likely_roisAndCordinates = un.getMostLikelyRois(roisAndCordinates)

    most_likely_digits = []

    if not most_likely_roisAndCordinates:
        raise ValueError('Ne mogu pronaci znamenke na slici')

    for roidAndCordinate in most_likely_roisAndCordinates:
        most_likely_digits.append(roidAndCordinate.roi)

    return most_likely_digits


def get_most_likely_digits_from_image(most_likely_digits):
    digits = []
    for most_likely_digit in most_likely_digits:
        cnts = cv2.findContours(most_likely_digit.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        digit_roi = most_likely_digit[y: y + h, x: x + w]
        #cv2.imshow("Digit ROI", digit_roi)
        #cv2.waitKey(0)
        #digit_roi = transform.deskew2(digit_roi)
        #digit_roi = transform.center_extent(digit_roi,(28,28))
        digit_roi = cv2.resize(digit_roi, (28, 28), interpolation=cv2.INTER_AREA)
        digits.append(digit_roi)
        cv2.imshow('Digit ', digit_roi)
        cv2.waitKey()
    return digits
