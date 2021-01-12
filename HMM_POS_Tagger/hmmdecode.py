import io
import sys

def processTestFile(file):
    sentenceList = []
    train_data = io.open(file, 'r', encoding='utf-8')
    for line in train_data:
        line = line.strip()
        combos = line.split(' ')
        sentenceList.append(combos)

    return sentenceList


def ViterbiDecode(tags, emission, transition, q0, sentence):
    probability = {}
    backpointer = {}
    for state in tags:
      probability[state] = {}
      backpointer[state] = {}
      if sentence[0] not in emission:
          probability[state][1] = 0
      else:
          probability[state][1] = q0[state] * emission[sentence[0]][state]

    for t in range(2, (len(sentence)+1)):
        if sentence[t-1] not in emission:
            emission[sentence[t-1]] = dict.fromkeys(tags, 0)

        previousZero = True
        for tag in tags:
            if probability[tag][t-1] != 0.0:
                  previousZero = False

        for tag in tags:
              if previousZero:
                if 0 == emission[sentence[t-1]][tag]: 
                  probability[tag][t] = 0
                else:
                  probability[tag][t] = max([ transition[q1][tag] * emission[sentence[t-1]][tag] for q1 in tags])
                backpointer[tag][t] = tags[0]
                backProb = transition[tags[0]][tag]
                for i in range(1, len(tags)):
                  temp = transition[tags[i]][tag]
                  if temp > backProb:
                    backProb = temp
                    backpointer[tag][t] = tags[i]
                
              else:
                if 0 == emission[sentence[t-1]][tag]: 
                  probability[tag][t] = 0
                else:
                  probability[tag][t] = max([probability[q1][t-1] * transition[q1][tag] * emission[sentence[t-1]][tag] for q1 in tags])
                backpointer[tag][t] = tags[0]
                backProb = probability[tags[0]][t-1] * transition[tags[0]][tag]
                for i in range(1, len(tags)):
                    temp = probability[tags[i]][t-1] * transition[tags[i]][tag]
                    if temp > backProb:
                        backProb = temp
                        backpointer[tag][t] = tags[i]
                
    T = len(sentence)
    termiMostProbable = tags[0]
    highestProb = probability[tags[0]][T]
    for i in range(1, len(tags)):
        temp = probability[tags[i]][T]
        if temp > highestProb:
            highestProb = temp
            termiMostProbable = tags[i]
    res = [termiMostProbable]
    for i in range(len(sentence), 1, -1):
        res.append(backpointer[res[-1]][i])

    original = res[::-1]
    output = ''
    for word, tag in zip(sentence, original):
        output += word+'/'+tag+' '

    return output

if __name__ == "__main__":
    testFile = sys.argv[1]
    tags = []
    vocabs = set()
    q0 = {}
    emission = {}
    transition = {}
    with open('hmmmodel.txt', 'r') as inputHmm:
        fsdf = inputHmm.readline()
        fsdf = inputHmm.readline()
        dfsd = inputHmm.readline()

        tagNum = int(inputHmm.readline().strip())
        dfsd = inputHmm.readline()

        vocabNum = int(inputHmm.readline().strip())

        for i in range(tagNum):
            line = inputHmm.readline().strip()
            list_ = line.split(' ')
            tags.append(list_[1])
            q0[list_[1]] = float(list_[2])
                
        for tag in tags:
            transition[tag] = dict.fromkeys(tags, 0)
        for tag1 in tags:
            for tag2 in tags:
                line = inputHmm.readline().strip()
                list_ = line.split(' ')

                transition[list_[0]][list_[1]] = float(list_[2])
                
        fsdf = inputHmm.readline()
        for i in range(vocabNum):
          for j in range(tagNum):
            line = inputHmm.readline().strip()
            list_ = line.split(' ')
            if j == 0:
              emission[list_[0]] = dict.fromkeys(tags, 0)
           
            emission[list_[0]][list_[1]] = float(list_[2])

    
    sentences = processTestFile(testFile)
    output = open('hmmoutput.txt', 'w')
    
    for sentence in sentences:        
        tagRes = ViterbiDecode(tags, emission, transition, q0, sentence)
        output.write(tagRes+'\n')
    output.close()
    
    
    