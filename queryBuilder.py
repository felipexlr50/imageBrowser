import re

REGEX_STRING = '[^-"\w]'


def getSearchStringArray(queryString):
    return re.sub(REGEX_STRING, " ",  queryString).split()


def parseCompoundString(queryString):
    wordlist = getSearchStringArray(queryString)
    compoundQuerryWord = []
    newWordList = []
    isCompound = False
    for word in wordlist:

        if('"' in word or isCompound):
            isCompound = not word.endswith('"')
            compoundQuerryWord.append(word)

        else:
            newWordList.append(word)

        if(len(compoundQuerryWord) > 1 and ('"' in compoundQuerryWord[0] and '"' in compoundQuerryWord[-1])):
            newWordList.append(" ".join(compoundQuerryWord))

    return newWordList


def parseQueryWordList(queryString):
    wordlist = parseCompoundString(queryString)

    result = []

    for word in wordlist:
        if("-" in word):
            result.append({'word': word, 'sign': "-"})
        else:
            result.append({'word': word, 'sign': "+"})

    return result


def filterResultsDb(queryString):
    wordlist = parseQueryWordList(queryString)
    posWords = list(map(lambda word: word['word'], list(
        filter(lambda item: '+' in item['sign'], wordlist))))

    negWords = list(map(lambda word: str(word['word']).replace('-', ''), list(
        filter(lambda item: '-' in item['sign'], wordlist))))

    return posWords, negWords


def filterResults(queryString, db_results):
    wordlist = parseQueryWordList(queryString)
    posWords = list(map(lambda word: word['word'], list(
        filter(lambda item: '+' in item['sign'], wordlist))))

    negWords = list(map(lambda word: str(word['word']).replace('-', ''), list(
        filter(lambda item: '-' in item['sign'], wordlist))))

    posResults = set()
    posWords = set(posWords)
    finalResult = list()

    isNeg = False

    for i in range(0, len(db_results)):
        resultName = db_results[i][1]
        resultTag = db_results[i][0]
        try:
            if(isNeg or resultTag in negWords):
                isNeg = True
                if(resultName != db_results[i+1][1]):
                    isNeg = False
                    posResults = set()

                continue
        except:
            pass

        if(resultTag in posWords):
            posResults.add(resultTag)
        try:
            if(resultName != db_results[i+1][1]):

                if(posResults == posWords):
                    finalResult.append(resultName)

                posResults = set()
        except:
            pass

    return finalResult
