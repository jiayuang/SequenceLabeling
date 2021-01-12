import io
import sys

def processTrainingFile(file):
    vocabList = set()
    tagList = set()
    sentenceList = []
    train_data = io.open(file, 'r', encoding='utf-8')
    for line in train_data:
        line = line.strip()
        combos = line.split(' ')
        sentenceList.append(combos)
        for combo in combos:
            index = combo.rfind('/') #index of last occurrence of a substring
            word = combo[:index]
            tag = combo[(index+1):]

            vocabList.add(word)
            tagList.add(tag)


    return vocabList, tagList, sentenceList


def transitionProb(sentences, tags):
    denominator = {}
    numerator = {}
    for tag in tags:
        denominator[tag] = dict.fromkeys(tags, 0)
        numerator[tag] = dict.fromkeys(tags, 0)

    counter = 0
    q0 = dict.fromkeys(tags, 0)
    for sentence in sentences:
        index = sentence[0].rfind('/')
        tag = sentence[0][(index+1):]
        q0[tag] += 1
        counter += 1
    for tag in tags:
        q0[tag] = q0[tag] / counter


    for sentence in sentences:
        for i in range(len(sentence)-1):
            indexCur = sentence[i].rfind('/')
            tagCur = sentence[i][(indexCur+1):]

            for tag in tags:
                denominator[tagCur][tag] += 1

            indexNext = sentence[i+1].rfind('/')
            tagNext = sentence[i+1][(indexNext+1):]
            numerator[tagCur][tagNext] += 1


    transitionRes = {}
    for tag in tags:
        transitionRes[tag] = dict.fromkeys(tags, 0)

    tagNum = len(tags)
    for tagDe, tagNu in zip(denominator.keys(), numerator.keys()):
        for tagDeSub, tagNuSub in zip(denominator[tagDe].keys(), numerator[tagNu].keys()):

            transitionRes[tagDe][tagDeSub] = (numerator[tagNu][tagNuSub]+1) / (denominator[tagDe][tagDeSub] + tagNum ** 2)

    return q0, transitionRes


def emissionProb(sentences, vocabs, tags):
    emissionProbRes = {}
    for vocab in vocabs:
        emissionProbRes[vocab] = dict.fromkeys(tags, 0)

    posTagCounter = dict.fromkeys(tags, 0)

    for sentence in sentences:
        for combo in sentence:
            index = combo.rfind('/')
            tag = combo[(index+1):]
            word = combo[:index]

            emissionProbRes[word][tag] += 1
            posTagCounter[tag] += 1


    for vocab in vocabs:
        for tag in tags:
            emissionProbRes[vocab][tag] = emissionProbRes[vocab][tag] / posTagCounter[tag]

    return emissionProbRes


if __name__ == "__main__":
    testFile  = sys.argv[1]
    vocabs, tags, sentences = processTrainingFile(testFile)
    q0, transition = transitionProb(sentences, tags)
    emission = emissionProb(sentences, vocabs, tags)


    with open('hmmmodel.txt', 'w') as output:
        output.write('Training Stats\n')
        output.write('Transition Probabilities\n')

        output.write('Number of tags\n')
        output.write(str(len(tags))+'\n')
        output.write('Number of vocabs\n')
        output.write(str(len(vocabs))+'\n')

        for tag in tags:
            output.write('q0 '+tag+' '+str(q0[tag])+'\n')
        for tag1 in tags:
            for tag2 in tags:
                output.write(tag1+' '+tag2+' '+str(transition[tag1][tag2])+'\n')


        output.write('Emission Probabilities\n')
        for v in vocabs:
            for tag in tags:
                output.write(v+' '+tag+' '+str(emission[v][tag])+'\n')







