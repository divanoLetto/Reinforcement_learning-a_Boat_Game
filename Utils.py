import numpy


def isClose(a, b, allowed_error):
    return abs(a - b) <= allowed_error


def print_matrix(matrix, verbose):
    matrix = numpy.array(matrix)
    rotated_matrix = numpy.rot90(matrix, 1)
    if verbose:
        print(rotated_matrix)
    return rotated_matrix



