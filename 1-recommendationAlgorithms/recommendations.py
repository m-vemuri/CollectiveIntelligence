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
    if denominator == 0: return 0

    return numerator/denominator

# returns top 5 similar matches 
def topMatches(prefs, person):

    similars=[ (pearson_cor(prefs, person, item ), item)  for item in prefs if item != person ]

    similars.sort()
    similars.reverse()

    # print("\n\nTop 5 similar matches:\n")
    
    return similars[0:5]


# get top recommendations for critics, 
# or if you trasform the prefs, then it will give you items.
def getRecommendations(prefs, person):

    skip=[]

    for item in prefs[person]:
        skip.append(item)

    # find the top 5 similar critics
    similars = topMatches(prefs, person)

    if len(similars) == 0:
        return []
    
    # this dictionary will store the ratings
    ratings = {}
    # simultaneously, keep track of the similarity sum
    similaritySum = {}

    # loop on the similar items that you have got
    # and then create a weighted rating to recommend an item
    for similarity, critic in similars:
        # as long as the critic rating is +ve
        if similarity >= 0:
            for movie in prefs[critic]:
                if movie not in skip:
                    if movie not in ratings:
                        ratings[movie]=0
                    ratings[movie] += similarity*prefs[critic][movie]
                    if movie not in similaritySum:
                        similaritySum[movie] = 0
                    similaritySum[movie] += similarity
    
    recommend = [ ( (ratings[movie]/similaritySum[movie]), movie) for movie in ratings]

    recommend.sort()
    recommend.reverse()

    print("\n\nTop 5 similar matches:\n")

    return recommend

# This is almost like a transpose of the prefs.
# i.e. the inner becomes the outer and the outer
# becomes the inner.
def transformPrefs(prefs):

    transformed = {}
    
    for key, value in prefs.items():
        for inner, val in value.items():
            if inner not in transformed:
                transformed[inner] = {}
            transformed[inner].update({key : val})

    return transformed

# creates a dataset of similar items for each item. 
def calculateSimilarItems(prefs):

    transformed = transformPrefs(prefs)

    result = {}

    for item in transformed:
        result[item] = topMatches(transformed, item)

    return result

def getRecommendedItems(prefs, person):
    
    similarItems = calculateSimilarItems(prefs)

    totalSimilarity={}
    totalRating={}

    skip = []
    for item in prefs[person]:
        skip.append(item)

    for movie in prefs[person]:
        for similarity, similarMovie in similarItems[movie]:
            if similarMovie not in skip:
                if similarMovie not in totalSimilarity:
                    totalSimilarity[similarMovie]=0
                totalSimilarity[similarMovie]+=similarity
                if similarMovie not in totalRating:
                    totalRating[similarMovie]=0
                totalRating[similarMovie]+=(prefs[person][movie]*similarity)
    
    recommended = [ (totalRating[movie]/totalSimilarity[movie], movie) for movie in totalRating if totalSimilarity[movie] != 0]

    recommended.sort()
    recommended.reverse()

    return recommended

def loadMovieLens():

    movies = {}
    for line in open("./data/u.item", encoding = "ISO-8859-1"):
        (id, title) = line.split('|')[0:2]
        movies[id]=title
    
    prefs = {}
    for line in open("./data/u.data", encoding = "ISO-8859-1"):
        (userid, movieid, rating) = line.split("\t")[0:3]
        if userid not in prefs:
            prefs[userid]={}
        prefs[userid][movies[movieid]] = float(rating)

    return prefs

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