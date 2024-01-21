# define the triangular membership function
def trimf(val:int, vector:list[int]) -> float:
    """
    Triangular Membership Function
        This function calculates the fuzzy value of a crisp input using a triangular membership function.  
    
    Arguments:
        val:int
            crisp value to be fuzzified
            
        vector:list[int]
            a vector with 3 values pertaining to the left base, peak, and right base of the triangular membership function.
            the vector shoul satisfy the following property:
            a < b < c
        
    Returns
        fuzzy_value: float
            fuzzified value from the crisp value
    """
    
    # check if the vector is of length 3
    assert len(vector) == 3, "the length of the vector must be equal to 3"
    
    # unpack and check the values of the vector if it statisfies the property a <= b <= c
    a, b, c = vector
    assert a < b, "a must be less than to b"
    assert b < c, "b must be less than to c"
    
    
    # compute for the fuzzy value from the crisp value
    if val <= a:
        return  0.0
    elif (val >= a) and (val <= b):
        return (val - a)/(b - a)
    elif (val >= b) and (val <= c):
        return (c - val)/(c - b) 
    elif val >= c:
        return 0.0
    
# define the linear membership function
def linearf(val:int, vector:list[int], positive_slope:bool = True) -> float:
    """
    This function computes for th1e degree of membership of a crisp value to its fuzzy counterpart through a linear membership function
    Arguments
        val:int
            The value to be fuzzified; it a should be less than be, i.e. a < b
        
        vector:list[int]
            A length 2 vector that defines the linear boundaries of the 
            linear membership function
    
        positive_slope:bool
            boolean paramater that checks if the slope to be used is positive or negative

    Returns
        fuzzy_value:float
            The fuzzified value from the crisp input
    """

    # check if the input vector is of length 2
    assert len(vector) == 2, "The vector must of of length 2"
    
    # unpack the vector and check if it statisfies the property a < b
    a, b = vector
    assert a < b, "a must be less than b"
    
    # compute for the fuzzy value from the crisp value
    # if the linear membership function has a positive slope
    if positive_slope:
       if val < a:
           return 0
       elif val > b:
           return 1
       else:
           return (val - a)/(b - a)
    
    # if the linear membership function has a negative slope
    else:
       if val < a:
           return 1
       elif val > b:
           return 0
       else:
           return  (b - val)/(b - a)