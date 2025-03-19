HEADLINE=       "Bisection Method"
ROOT_FINDING=   "is a root finding algorithm"
WHICH_MEANS1=    "... Which means for a function f it finds"
WHICH_MEANS2=   "f of x equal to 0"
TWOCONDITION=   "It has to obey 2 condition.They are"
CONDITION1=     "Knowing 2 values of function say a and b of function f such that f of a and f of b are two different sign.So if one is                     positive than other is negative."
CONDITION2=     "The 2nd condition is,the function has to be continious from a to b"
FOCUS=          r"Let's focus on the second condition." 

##Scene 2
CONTINIOUS_DES= r"""What is a continious function?Is simple term
                    ,If you can draw a graph of a function 
                    without picking up the pen,in range a to b then it is called a continious
                    function from a to b"""

CONTI_EXAMPLE=  r"""So this is a continious function"""
CONTI_REASON=   "Because you can draw the graph without picking up the pen"
NOT_CONTI   =   "And this is not a continious function"
NOT_CONTI2 =   "As there is no way to draw the function without picking up the pen"



#Scene 3

THINK_ABOUT=  "Let's think about it for a moment."
POINT_A=    "Given a point A which is over the x axis"
POINT_B=    "and B which is under the x axis."
A_TO_B=     """Can you plot a graph that goes from point A to B that doesn't intersect the x axis? .... 
                On hintsight,It feel like not possible and it isn't"""
THERE_EXIST= """So for a continious function f,if we know two values of the function,and they are of diffenret sign,
we know there exist atleast one  root between the two values."""

FOR_A_FUNCTION= """So for a continious function,if for input a and b 
if the function returns a positive value than,There exist atleast a root in the middle of a,b"""



## Scene 4
ROOT_RENAME=        """Let's denote the root to x"""
ROOT_IS=            """Now that the x is in inside of range a and b 
                    we can say the x is average of a and b"""
WITH_ERROR=         """With an error of plus minus b minus a divided by 2."""
ERROR_EXP=          """Let's recap a few things.When I say a+-b it means The value resides between a-b and a+b,a being the average"""
ERROR_EXP2=         """So the value a+b/2 +- b-a/2 means the value is between a and b"""
CELEBRATE=          """Yeah we found the value of the root"""
NOT_SATISFACTORY=   """What!!! Not satisfied with the result"""

SATIFY_IF=          """Well the result would have been satisfying if the values of a and b are close enough.
                        Close enough so the error a minus b by 2 will be miniscule"""
ERROR_LESS=         """Because if a abd b are close together than their error a-b/2 is small as well"""
MAKE_SMALL=         """So a quesiton is,can we make the range of a and b smaller.Maybe be finding new a and b"""
MORE_INFOR=         """We need more information about the function.We can check more values of the function."""
CHOOSE_MIDDLE=       """We can choose the middle a,b say x and 
                    checks the the output of the function is means what f of x is."""
THREE_STATE=        """Now the value of f in x can be positive or negative,zero,If it is zero we found out the root."""

NEW_RANGE_POS=          """If functon of x is positive than you found a new range 
                    x and b for which one is positive and other is negative,So x became the new a"""
NEW_RANGE_NEG=      """If x is negative than we found range a,
                    x for which we can found the root,x become the new b"""
RANGE_HALF=         """Using the previous range a,b,We found the new a,b where the distance between them cut in                      half."""
TWO_THINGS=         """We can do two things,1,We can take the new root of the range
which also have an error of a-b divided by 2,which is half the error we have before,"""
SECOND_THING=       """or if you are not satisfied with the current error,even after reducing the error in half,you can generate new a b range,they are half distance apart between each other."""
REPEAT=             """Repeat the process enough time to get error you desire."""


    
