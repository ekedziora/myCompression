import collections, re

def codeNotInText(code, text):
    if(code in text):
        return False
    return True

def convertStringToAsciiValues(string):
    return [ord(c) for c in string]

def convertAsciiValuesToString(asciiValues):
    return ''.join(chr(i) for i in asciiValues)

def findNextAvailableCode(startCode, text):
    asciiValues = convertStringToAsciiValues(startCode)
    asciiValues[-1] += 1
    while True:
        lastChar = asciiValues[-1]
        for ch in range(lastChar, 256):
            asciiValues[-1] = ch
            newCode = convertAsciiValuesToString(asciiValues)
            if codeNotInText(newCode, text):
                return newCode
        asciiValues = [0] * len(asciiValues)
        asciiValues.append(0)


def compress(text):
    dictionary = {}
    alphanumericWords = re.findall(r'\w+', text)
    punctuationWords = re.findall(r'\W+', text)
    allWords = alphanumericWords + punctuationWords
    list = sorted(collections.Counter(allWords).items(), key=lambda x: x[1], reverse = True)
    allWordsOrdered = [x[0] for x in list]

    dictionaryDelimiter = findNextAvailableCode(chr(32), text)
    replacementDelimiter = findNextAvailableCode(dictionaryDelimiter, text)

    lastReplacement = replacementDelimiter
    skipFindingNextCode = False
    for word in allWordsOrdered:
        if not skipFindingNextCode:
            lastReplacement = findNextAvailableCode(lastReplacement, text)
        if(len(lastReplacement) < len(word)):
            dictionary[word] = lastReplacement
            skipFindingNextCode = False
        else:
            skipFindingNextCode = True

    print(dictionary)
    print(len(dictionary))
    dictionaryString = ''
    for word, replacement in dictionary.items():
        if(len(word) <= len(replacement)):
            print(word + '->' + replacement)
        text = text.replace(word, replacement)
        dictionaryString += word + replacement + replacementDelimiter

    print('dictionary string len:' + str(len(dictionaryString)))
    print('text len:' + str(len(text)))
    dictionaryString = dictionaryDelimiter + dictionaryString
    print(dictionaryString)
    return dictionaryDelimiter + replacementDelimiter + text + dictionaryString


def extractDictionary(dictionaryString, replacementDelimiter):
    dictionary = {}
    lastDelimiterPos = 0
    for i in range(0, len(dictionaryString)):
        if (dictionaryString[i] == replacementDelimiter):
            word = dictionaryString[lastDelimiterPos: i-1]
            replacement = dictionaryString[i-1: i]
            dictionary[replacement] = word
            lastDelimiterPos = i+1
    return dictionary

def uncompress(text):
    dictionaryDelimiter = text[0]
    replacementDelimiter = text[1]
    text = text[2:]
    dictionaryStart = text.index(dictionaryDelimiter) + 1
    dictionaryString = text[dictionaryStart:]
    text = text[:dictionaryStart - 1]
    dictionary = extractDictionary(dictionaryString, replacementDelimiter)
    for replacement, word in dictionary.items():
        text = text.replace(replacement, word)
    return text

s = str(open('lifeisfine.txt', 'rb').read())
# s = 'Hello. Today hello just hello. Here: hello or just now; Thankyou hello just now.'
originalLength = len(s)
print(originalLength)

compressed = compress(s)
compressedLength = len(compressed)
print(compressedLength)

print("Stopień kompresji: " + str(float(compressedLength)/float(originalLength)))
# uncompressed = uncompress(compressed)