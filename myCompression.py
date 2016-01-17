import collections, re, sys, codecs

def replaceAllWords(text, wordDict):
    rc = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, wordDict)))
    def translate(match):
        return wordDict[match.group(0)]
    return rc.sub(translate, text)

def charUsableForCompression(char, text):
    if(char <= sys.maxunicode and chr(char) in text):
        return False
    return True


def findNextAvailableDelimiter(start, text):
    for ch in range(start, sys.maxunicode + 1):
        if chr(ch) not in text:
            return ch


def compress(text):
    dictionary = {}
    alphanumericWords = re.findall(r'\w+', text)
    punctuationWords = re.findall(r'\W+', text)
    allWords = alphanumericWords + punctuationWords
    wordsOccurences = collections.Counter(allWords)
    wordsOccuredMoreThanOnce = {word: count for word, count in wordsOccurences.items() if count > 1}
    list = sorted(wordsOccuredMoreThanOnce.items(), key=lambda x: x[1], reverse = True)
    allWordsOrdered = [x[0] for x in list]

    dictionaryDelimiter = findNextAvailableDelimiter(32, text)
    replacementDelimiter = findNextAvailableDelimiter(dictionaryDelimiter + 1, text)

    replacementChar = replacementDelimiter + 1

    i = 0
    for ch in range(replacementChar, sys.maxunicode + 1):
        if i >= len(allWordsOrdered):
            break
        if charUsableForCompression(ch, text):
            word = allWordsOrdered[i]
            dictionary[word] = chr(ch)
            i += 1

    print(dictionary)
    print(len(dictionary))
    text = replaceAllWords(text, dictionary)
    dictionaryString = ''
    for word, replacement in dictionary.items():
        dictionaryString += word + replacement + chr(replacementDelimiter)

    dictionaryString = chr(dictionaryDelimiter) + dictionaryString
    print('dictionary string len:' + str(len(dictionaryString)))
    print('text len:' + str(len(text)))
    return chr(dictionaryDelimiter) + chr(replacementDelimiter) + text + dictionaryString


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

s = str(codecs.open( "pantadeuszksiega1utf.txt", "r", "utf-8" ).read())
# s = 'Hello. Today hello just hello. Here: hello or just now; Thankyou hello just now.'
originalLength = len(s)
print(originalLength)

compressed = compress(s)
compressedLength = len(compressed)
print(compressedLength)

print("Stopień kompresji: " + str(float(compressedLength)/float(originalLength)))
uncompressed = uncompress(compressed)
# print(uncompressed)