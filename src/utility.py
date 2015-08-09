#!/usr/bin/python

class Sample:
    def __init__(self, name):
        self.name = name
        self.training = []
        self.labels = []

class Mainclass:
    def __init__(self):
        self.pos_tags = dict()
        self.pos_tag_counter = 0
        self.wordtypes = []
        i = Sample("it's vs its")
        self.wordtypes.append(i)
        y = Sample("you're vs your")
        self.wordtypes.append(y)
        th = Sample("they're vs their")
        self.wordtypes.append(th)
        l = Sample("loose vs lose")
        self.wordtypes.append(l)
        to = Sample("to vs too")
        self.wordtypes.append(to)
        self.typedict = dict()
        self.typedict["it's"] = 0
        self.typedict["its"] = 0
        self.typedict["you're"] = 1
        self.typedict["your"] = 1
        self.typedict["they're"] = 2
        self.typedict["their"] = 2
        self.typedict["loose"] = 3
        self.typedict["lose"] = 3
        self.typedict["to"] = 4
        self.typedict["too"] = 4
        self.classdict = dict()
        self.classdict["it's"] = 0
        self.classdict["its"] = 1
        self.classdict["you're"] = 0
        self.classdict["your"] = 1
        self.classdict["they're"] = 0
        self.classdict["their"] = 1
        self.classdict["loose"] = 0
        self.classdict["lose"] = 1
        self.classdict["to"] = 0
        self.classdict["too"] = 1

    def writemodel(self, filename):
        with open(filename, 'w+') as outfile:
            outfile.write("pos_tags {}\n".format(len(self.pos_tags)))
            for tag in self.pos_tags:
                outfile.write("{0} {1}\n".format(tag, self.pos_tags[tag]))
            for wtype in self.wordtypes:
                outfile.write("{0} {1}\n".format(wtype.name, len(wtype.training)))
                for sample in wtype.labels:
                    outfile.write("{0}\n".format(sample))
                for sample in wtype.training:
                    outfile.write("{0} {1} {2} {3}\n".format(sample[0], sample[1], sample[2], sample[3]))
    
    def gettagcount(self):
    	return self.pos_tag_counter
    	
    def searchword(self, wtype, wclass):
        if wtype == 0:
            if wclass == 0:
                return "it's"
            else:
                return "its"
        elif wtype == 1:
            if wclass == 0:
                return "you're"
            else:
                return "your"
        elif wtype == 2:
            if wclass == 0:
                return "they're"
            else:
                return "their"
        elif wtype == 3:
            if wclass == 0:
                return "loose"
            else:
                return "lose"
        elif wtype == 4:
            if wclass == 0:
                return "to"
            else:
                return "too"
    
    def searchtag(self, tag):
        if tag not in self.pos_tags:
            self.pos_tags[tag] = self.pos_tag_counter
            self.pos_tag_counter += 1
        return self.pos_tags[tag]
    
    def gettype(self, word):
        if word in self.typedict:
            return self.typedict[word]
        else:
            return -1;
    
    def getclass(self, word):
        if word in self.classdict:
            return self.classdict[word]
        else:
            return -1;
   
    def appendtypes(self, wtype, wclass, features):
        self.wordtypes[wtype].training.append(features)
        self.wordtypes[wtype].labels.append(wclass) 
    
    
