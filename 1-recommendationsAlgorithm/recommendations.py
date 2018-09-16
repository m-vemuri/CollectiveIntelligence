from math import sqrt

# Calculation of Euclidean distance between two points.
# Here, each person has preference data in prefs
# the preference data is the point in the euclidean space.
def sim_distance(prefs, person1, person2):
    
    si = {}

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si)==0: 
        return 0
    
    sum_of_squares = sum([ pow( prefs[person1][item] - prefs[person2][item], 2 ) for item in si ])

    return 1/(1 + sqrt(sum_of_squares))

# Calculation of the pearson correlation between two points
# The pearson correlation gives a value between -1 and +1. 
# A value of 0 implies no change with changes to either variable.
# A value of -1 implies as one var increase, the other decreases.
# A value of +1 implies as one var increases, the other increases.
def pearson_cor(prefs, person1, person2):

    si={}

    # first find the common items in each
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    if len(si) == 0: return 0

    # number of elements
    n = len(si)

    sumOfProduct = sum([ (prefs[person1][item]*prefs[person2][item]) for item in si ])

    sumOfX = sum( [ prefs[person1][item] for item in si ] )
    sumOfY = sum( [ prefs[person2][item] for item in si ] )
    
    
    sumOfSqX = sum( [ pow(prefs[person1][item],2) for item in si ] )
    sumOfSqY = sum( [ pow(prefs[person2][item],2) for item in si ] )

    sqOfSumX = pow(sumOfX,2)
    sqOfSumY = pow(sumOfY,2)

    numerator = ((n * sumOfProduct) - (sumOfX * sumOfY))
    denominator = sqrt( ((n * sumOfSqX) - sqOfSumX ) * ( (n * sumOfSqY) - sqOfSumY ) )

    return numerator/denominator


def topMatches(prefs, person):

    similars=[ (pearson_cor(prefs, person, item ), item)  for item in prefs if item != person ]

    similars.sort()
    similars.reverse()

    print("\n\nTop 5 similar matches:\n")
    
    return similars[0:5]


critics={
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        #'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        #'You, Me and Dupree': 2.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        #'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.0,
        'The Night Listener': 3.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        #'Just My Luck': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Mukund Vemuri': {
        #'Lady in the Water': 4.0,
        'Snakes on a Plane': 4.5,
        #'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 1.0,
        #'The Night Listener': 3.0
    }
}       