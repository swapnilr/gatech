import sys
import os
import numpy as np
import cv2

import assignment10

def test_normalizeImage():
    """ This script will robustly test the normalizeImage function.
    """
    matrix_1 = np.array([[  0,   0],
                         [128, 128]], dtype=np.float)
    matrix_1_answer = np.array([[  0,   0],
                                [255, 255]], dtype=np.uint8)
    matrix_2 = np.array([[-3,   0],
                         [ 0,   3]], dtype=np.float)
    matrix_2_answer = np.array([[  0,   127],
                                [127,   255]], dtype=np.uint8)
    matrix_3 = np.array([[-10, -80],
                         [100, 200]], dtype=np.float)
    matrix_3_answer = np.array([[ 63,   0],
                                [163, 255]], dtype=np.uint8)
    matrix_4 = np.array([[  -3.5,   2.12],
                         [4.12, 5.4]], dtype=np.float)
    matrix_4_answer = np.array([[  0,   161],
                                [218, 255]], dtype=np.uint8)
    matrices = [matrix_1, matrix_2, matrix_3, matrix_4]
    matrices_ans = [matrix_1_answer, matrix_2_answer,
                    matrix_3_answer, matrix_4_answer]
    print "Evaluating normalizeImage."

    for matrix_idx in range(len(matrices)):
        normalized = assignment10.normalizeImage(matrices[matrix_idx])
        ans = matrices_ans[matrix_idx]

        # Test for type.
        if type(normalized) != type(ans):
            raise TypeError(
                ("Error - normalized has type {}." + 
                 " Expected type is {}.").format(type(normalized), type(ans)))

        # Test for shape.
        if normalized.shape != ans.shape:
            raise ValueError(
                ("Error - normalized has shape {}." +
                 " Expected shape is {}.").format(normalized.shape, ans.shape))

        # Test for type of values in matrix.
        if type(normalized[0, 0]) != type(ans[0, 0]):
            raise TypeError(
                ("Error - normalized values have type {}." +
                 "Expected type is {}.").format(type(normalized[0, 0]),
                                                type(ans[0, 0])))

        # Assert values are identical.
        np.testing.assert_array_equal(normalized, ans)
    print "normalizeImage tests passed."
    return True

def test_linearWeight():
    """ This script will perform a unit test on the linear weight function.
    """

    test_input = [0, 1, 127, 128, 255]
    exp_output = np.array([0, 1, 127, 127, 0], dtype=float)

    print "Evaluating linearWeight."

    for val_idx in xrange(len(test_input)):
        weight = assignment10.linearWeight(test_input[val_idx])
        ans = exp_output[val_idx]
        if type(weight) != type(ans) and type(weight) != float:
            raise ValueError(
                ("Error - weight has type {}." +
                 " Expected type is {}.").format(type(weight), type(ans)))

        if ans != weight:
            raise ValueError(
                ("Error - linearWeight returned {} for input {}." +
                 " Expected output is {}.").format(weight, test_input[val_idx],
                                                   ans))
    print "linearWeight testing passed."
    return True

def test_getYXLocations():

    test_input = np.array([[ 41, 200,  190,  41],
                           [ 98, 151,   41, 182],
                           [128, 190,   98, 209],
                           [ 41,  27,  129, 190]], dtype=np.uint8)
    test_intensities = [41, 190, 98, 182]

    test_answers = [[np.array([0, 0, 1, 3], dtype=np.int64),
                     np.array([0, 3, 2, 0], dtype=np.int64)], # 41
                    [np.array([0, 2, 3], dtype=np.int64),
                     np.array([2, 1, 3], dtype=np.int64)], # 190
                    [np.array([1, 2], dtype=np.int64),
                     np.array([0, 2], dtype=np.int64)], # 98
                    [np.array([1], dtype=np.int64),
                     np.array([3], dtype=np.int64)]] # 182
            

    for test_idx in xrange(len(test_intensities)):
        x_locs, y_locs = assignment10.getYXLocations(test_input,
                                                     test_intensities[test_idx])
        x_ans, y_ans = test_answers[test_idx]
        
        
        # Test type.
        if type(x_locs) != type(x_ans):
            raise ValueError(
                ("Error - x_locs has type {}." +
                 " Expected type is {}.").format(type(x_locs), type(x_ans)))
        if type(x_locs[0]) != type(x_ans[0]):
            raise ValueError(
                ("Error - x_locs values have type {}." +
                 " Expected value type is {}.").format(type(x_locs[0]),
                                                       type(x_ans[0])))

        # Test length (did you find the right amount of points).
        if len(x_locs) != len(x_ans):
            raise ValueError(
                ("Error - x_locs has len {}." +
                 " Expected len is {}.").format(len(x_locs), len(x_ans)))

        if len(x_locs) != len(y_locs):
            raise ValueError(
                ("The length of your outputs is not the same." +
                 "x_locs length: {} | y_locs length: {}.").format(len(x_locs),
                                                                  len(y_locs)))


        np.testing.assert_array_equal(y_locs, y_ans)
        np.testing.assert_array_equal(x_locs, x_ans)
        
    print "getYXLocations testing passed."
    return True

if __name__ == "__main__":
    print "Performing unit test."
    if not test_normalizeImage():
        print "normalizeImage function failed. Halting testing."
        sys.exit()
    if not test_linearWeight():
        print "linearWeight function failed. Halting testing."
        sys.exit()
    if not test_getYXLocations():
        print "getYXLocations function failed. Halting testing."
        sys.exit()
    print "Unit tests passed."

    print "We do not run a unit test for computeResponseCurve so make sure " + \
          "you look at the HDR output (or see why the function isn't " + \
          "running) to assess your progress."

    image_dir = "input"
    output_dir = "output"
    exposure_times = np.float64([1/160.0, 1/125.0, 1/80.0, 1/60.0, 1/40.0,
                                 1/15.0])
    log_exposure_times = np.log(exposure_times)

    np.random.seed()
    hdr = assignment10.computeHDR(image_dir, log_exposure_times)
    cv2.imwrite(output_dir + "/hdr.jpg", hdr)

