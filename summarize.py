# TextRank project
import random
import math
import nltk

class Node:
    def __init__(self, index, text, significant_words):
        self.index = index
        self.sentence = text
        self.words = significant_words
        self.neighbors = []
        self.edges = {}
        self.score = random.randint(1, 10)

class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight

def Similarity(v1, v2):
    commonWords = 0
    for w in v1.words:
        if w in v2.words:
            commonWords += 1
    return commonWords/(math.log(len(v1.words)) + math.log(len(v2.words)))

def BuildGraph(graph, listOfSentences):
    nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')

    for s in listOfSentences:
        good_words = []
        for i in s.lower().split():
            if i not in stop_words:
                good_words.append(i)
        newNode = Node(len(graph), s, good_words)
        for n in graph:
            sim = Similarity(newNode, n)
            if sim != 0:
                newEdge = Edge(s, n, sim)
                newNode.neighbors.append(n)
                newNode.edges[n] = newEdge
                n.neighbors.append(newNode)
                n.edges[newNode] = newEdge
        graph.append(newNode)

def CalculateNodeScores(graph):
    d = 0.85
    thresh = 0.0001
    done = False

    if len(graph) == 0:
        return

    while not done:
        for i in graph:
            old = i.score
            sum = 0
            for j in i.neighbors:
                denom = 0
                for k in j.neighbors:
                    denom += j.edges[k].weight
                sum += j.score * j.edges[i].weight / denom
            i.score = (1 - d) + (d * sum)
            if abs(old - i.score) < thresh:
                done = True

def PrintSummary(graph, sentence_count):
    sorted_graph = sorted(graph, key=lambda node: node.score)

    count = 0

    if len(sorted_graph) < sentence_count:
        selected_nodes = sorted_graph
    else:
        selected_nodes = []
        while count < sentence_count:
            newSentence = sorted_graph.pop()
            selected_nodes.append(newSentence)
            count += 1

    for s in sorted(selected_nodes, key=lambda node: node.index):
        print s.sentence

def Summarize():
    nltk.download('punkt')

    graph = [] # list of nodes in the graph

    F = open('sample.txt', 'r')
    fileText = F.read()
    listOfSentences = nltk.tokenize.sent_tokenize(fileText)

    BuildGraph(graph, listOfSentences)

    CalculateNodeScores(graph)

    PrintSummary(graph, 10)


# start of main program
random.seed()
Summarize()
