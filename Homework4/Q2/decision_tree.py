from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        #self.tree = {}
        self.tree = []

    def build_tree(self, X, y):
        if len(X) == 1:
            leaf = np.array([[-1, y[0], -1, -1]], dtype=np.object)
            return leaf
        if y.count(y[0]) == len(y):
            leaf = np.array([[-1, y[0], -1, -1]], dtype=np.object)
            return leaf
        else:
            # determine the split point maximize the info gain
            split_attribute = 0
            #split_val = 0
            info_gain = -999
            maxGain = -999
            X_left = []
            X_right = []
            y_left = []
            y_right = []
            number = 1

            length = len(X[0])
            sets = len(X)
            for index in range (0, length):
                for value in range (0, sets):
                    split = X[value][index]
                    X_left, X_right, y_left, y_right = partition_classes(X, y, index, split)
                    current_y = []
                    current_y.append(y_left)
                    current_y.append(y_right)
                    maxGain = information_gain(y, current_y)
                    if maxGain > info_gain:
                        split_attribute = index
                        split_val = split
                        info_gain = maxGain
                    elif maxGain == info_gain:
                        number = number + 1
            if number == length*sets:
                leaf = np.array([[-1, self.majority(y), -1, -1]], dtype=np.object)
                return leaf
            X_left, X_right, y_left, y_right = partition_classes(X, y, split_attribute, split_val)
            if len(X_left) == 0 or len(X_right) == 0:
                leaf = np.array([[-1, 0, -1, -1]], dtype=np.object)
                return leaf
            leftTree = np.array(self.build_tree(X_left, y_left), dtype=np.object)
            rightTree = np.array(self.build_tree(X_right, y_right), dtype=np.object)
            root = np.array([[split_attribute, split_val, 1, leftTree.shape[0]+1]], dtype=np.object)
            return np.vstack([root, leftTree, rightTree])

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        self.tree = self.build_tree(X, y)

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        j = 0
        k = 0
        while (k != -1):
            k = self.tree[j][0]
            k = int(k)
            predictY = self.tree[j][1]
            if (k != -1):
                value = self.tree[j][1]
                if type(value) == int:
                    if (record[k] <= self.tree[j][1]):
                        j = j + self.tree[j][2]
                        j = int(j)
                    else:
                        j = j + self.tree[j][3]
                        j = int(j)
                else:
                    if (record[k] == self.tree[j][1]):
                        j = j + self.tree[j][2]
                        j = int(j)
                    else:
                        j = j + self.tree[j][3]
                        j = int(j)
        return predictY


    def majority(self, valueY):
        occurance = 0
        length = len(valueY)
        for i in valueY:
            if i == 0:
                occurance += 1
        if occurance > length - occurance:
            return 0
        else:
            return 1

if __name__=="__main__":
    tree = {}
    X = [['ee', 'aa', 10],
       ['kk', 'bb', 22],
       ['aa', 'cc', 28],
       ['aa', 'bb', 32],
       ['bb', 'cc', 32]]
    y = [1,1,0,0,1]
    learner = DecisionTree()
    learner.learn(X, y)
    record = [[10, 'aa', 2],
       [55, 'ff', 0],
       [42, 'rr', 0],
       [5, 'kk', 32],
       [4, 'dd', 32],
       [10, 'ss', 2],
       [1, 'tt', 22]]
    #predict = learner.classify(record)
    #print predict