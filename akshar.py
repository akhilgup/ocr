#total=256(pixels)*23(versions of each image)=5888

from PIL import Image
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')



def createExamples():
    numberArrayExamples = open('dataset_model.txt','a')
    mylist=numberArrayExamples.read()
    numbersWeHave = range(1,31)
    versionsWeHave=range(0,23)
    for eachNum in numbersWeHave:
        for furtherNum in versionsWeHave:

            imgFilePath = 'dataset/'+str(eachNum)+'-'+str(furtherNum)+'.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiarl = str(eiar.tolist())
            #print(eiarl)

            lineToWrite = str(eachNum)+'::'+eiarl+'\n'
            mylist.write(lineToWrite)
            np.savetxt("dataset_model.txt",mylist, delimiter=",")

#createExamples()


def threshold(imageArray):
    balanceAr = []
    newAr = imageArray
    for eachPart in imageArray:
        for theParts in eachPart:
			# for the reduce(lambda x, y: x + y, theParts[:3]) / len(theParts[:3])
			# in Python 3, just use: from statistics import mean
			# then do avgNum = mean(theParts[:3])
            avgNum = reduce(lambda x, y: x + y, theParts[:3]) / len(theParts[:3])
            balanceAr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newAr



def whatIdIsThis(filePath):

    matchedAr = []
    loadExamps = open('dataset_model.txt','r').read()
    loadExamps = loadExamps.split('\n')
    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    inQuestion = str(iarl)
    for eachExample in loadExamps:
        if len(eachExample)>3:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')
            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))

                x+=1
        
                
    x = Counter(matchedAr)
    print(x)



    graphX = []
    graphY = []

    ylimi = 0

    for eachThing in x:
        graphX.append(eachThing)
        graphY.append(x[eachThing])
        ylimi = x[eachThing]



    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4),(1,0), rowspan=3,colspan=4)
    
    ax1.imshow(iar)
    ax2.bar(graphX,graphY,align='center')
    plt.ylim(200)
    
    #maximum value to be shown on x-axis
    xloc = plt.MaxNLocator(20)
    
    ax2.xaxis.set_major_locator(xloc)

    plt.show()



# whatIdIsThis("<Call any image here>")
#createExamples()   to create the dataset
#threshold("call anyany image") 
