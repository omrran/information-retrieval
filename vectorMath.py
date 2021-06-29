import math


# to calculate inner product between to vectors
def inner_product(v1, v2):
    elNum = len(v1)
    result = 0
    for i in range(elNum):
        result += v1[i] * v2[i]
    return result



#################################################
# calculate a length of vector
# v is a list like that : [1,3,4,-9] .....
def length_vector(v):
    result = 0
    for i in range(len(v)):
        result += math.pow(v[i], 2)
    return math.sqrt(result)


#####################################################
# calculate angle between two vector
def angle_between_two_vector(v1, v2):
    cos_theta = inner_product(v1, v2) / (length_vector(v1) * length_vector(v2))
    theta = math.acos(cos_theta)
    # theta by Radian so we will convert it to Degrees
    theta = 180 * theta / math.pi
    return theta



