import collections, re, sys, codecs, os.path, time

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

def preformDictionaryPrefixesExtraction(dictionary):
    for word, replacement in dictionary.items():
        for word2, replacement2 in dictionary.items():
            if word2 != word and word2.startswith(word):
                prefixedKey = word2.replace(word, replacement)
                dictionary[prefixedKey] = dictionary.pop(word2)
    return dictionary

def replacePrefixes(dictionary):
    for replacement, word in dictionary.items():
        for replacement2, word2 in dictionary.items():
            if replacement != replacement2 and replacement in word2:
                dictionary[replacement2] = word2.replace(replacement, word)
    return dictionary

def compress(text, prefixing):
    dictionary = {}
    alphanumericWords = re.findall(r'\w+', text)
    punctuationWords = re.findall(r'\W+', text)
    allWords = alphanumericWords + punctuationWords
    print("Wszystkich słów: " + str(len(allWords)))
    wordsOccurences = collections.Counter(allWords)
    wordsOccuredMoreThanOnce = {word: count for word, count in wordsOccurences.items() if count > 1 and len(word) > 1}
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

    text = replaceAllWords(text, dictionary)
    if prefixing:
        dictionary = preformDictionaryPrefixesExtraction(dictionary)

    dictionaryString = ''
    for word, replacement in dictionary.items():
        dictionaryString += word + replacement + chr(replacementDelimiter)

    dictionaryString = chr(dictionaryDelimiter) + dictionaryString
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

def uncompress(text, prefixing):
    dictionaryDelimiter = text[0]
    replacementDelimiter = text[1]
    text = text[2:]
    dictionaryStart = text.index(dictionaryDelimiter) + 1
    dictionaryString = text[dictionaryStart:]
    text = text[:dictionaryStart - 1]
    dictionary = extractDictionary(dictionaryString, replacementDelimiter)
    if prefixing:
        dictionary = replacePrefixes(dictionary)
    for replacement, word in dictionary.items():
        text = text.replace(replacement, word)
    return text

if(len(sys.argv) < 2):
    print("Nie podano pliku do skompresowania")
    exit(1)

filepath = sys.argv[1]
if(not os.path.isfile(filepath)):
    print("Podana ścieżka do pliku jest nieprawidłowa")
    exit(1)

try:
    text = str(codecs.open(filepath, "r", "utf-8").read())
except UnicodeDecodeError:
    print("Podany plik nie jest plikiem UTF-8")
    exit(1)

if(len(sys.argv) > 2 and sys.argv[2] == "-prefix"):
    prefixing = True
else:
    prefixing = False

startCompression = time.time()
compressed = compress(text, prefixing)
stopCompression = time.time()
originalLength = len(text)
compressedLength = len(compressed)
originalBytesLength = len(text.encode())
compressedBytesLength = len(compressed.encode())
print("Długość oryginalnego tekstu: " + str(originalLength))
print("Długość skompresowanego tekstu: " + str(compressedLength))
print("Długość orginalnego tekstu w bajtach: " + str(originalBytesLength))
print("Długość skompresowanego tekstu w bajtach: " + str(compressedBytesLength))
print("Stopień kompresji: " + str(float(compressedBytesLength) / float(originalBytesLength)))

startUncompression = time.time()
uncompressed = uncompress(compressed, prefixing)
stopUncompression = time.time()

print("Czas wykonania: " + str(stopUncompression - startCompression))
print("Czas kompresji: "+ str(stopCompression - startCompression))
print("Czas dekompresji: "+ str(stopUncompression - startUncompression))

out = codecs.open("uncompressed.txt", "w", "utf-8")
out.write(uncompressed)
out.close()