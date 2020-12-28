import nltk
from smartly import Text, Button, Card
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
lemmatizer = WordNetLemmatizer()
sender_ids = []
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random


def create_model(dataset, name):
    words = []
    classes = []
    documents = []
    ignore_words = ['?', '!', ',']
    data_file = open(dataset).read()
    intents = json.loads(data_file)

    for intent in intents['intents']:
        for pattern in intent['patterns']:

            # tokenize each word
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            # add documents in the corpus
            documents.append((w, intent['tag']))

            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # lemmaztize and lower each word and remove duplicates
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    # sort classes
    classes = sorted(list(set(classes)))
    # documents = combination between patterns and intents
    print(len(documents), "documents")
    # classes = intents
    print(len(classes), "classes", classes)
    # words = all words, vocabulary
    print(len(words), "unique lemmatized words", words)

    pickle.dump(words, open('models/{}_words.pkl'.format(name), 'wb'))
    pickle.dump(classes, open('models/{}_classes.pkl'.format(name), 'wb'))

    # create our training data
    training = []
    # create an empty array for our output
    output_empty = [0] * len(classes)
    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # lemmatize each word - create base word, in attempt to represent related words
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # create our bag of words array with 1, if word match found in current pattern
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    # create train and test lists. X - patterns, Y - intents
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    print("Training data created")

    # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
    # equal to number of intents to predict output intent with softmax
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))
    # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    print(model.summary())
    # fitting and saving the model
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=300, batch_size=7, verbose=1)
    model.save('/home/amazing/Documents/Smartly-chatbot/Models/models/{}.h5'.format(name), hist)

    print("model created")


class Tagger:
    def __init__(self, dataset, model):
        words = []
        classes = []
        documents = []
        ignore_words = ['?', '!', ',']
        intents = dataset
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                # add documents in the corpus
                documents.append((w, intent['tag']))

                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        # lemmaztize and lower each word and remove duplicates
        words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))
        # sort classes
        classes = sorted(list(set(classes)))
        # documents = combination between patterns and intents
        print(len(documents), "documents")
        # classes = intents
        print(len(classes), "classes", classes)
        # words = all words, vocabulary
        print(len(words), "unique lemmatized words", words)

        pickle.dump(words, open('/home/amazing/Documents/Smartly-chatbot/Models/models/{}_words.pkl'.format("_"), 'wb'))
        pickle.dump(classes, open('/home/amazing/Documents/Smartly-chatbot/Models/models/{}_classes.pkl'.format("_"), 'wb'))

        self.words = pickle.load(open('/home/amazing/Documents/Smartly-chatbot/Models/models/__words.pkl', 'rb'))
        self.classes = pickle.load(
            open('/home/amazing/Documents/Smartly-chatbot/Models/models/__classes.pkl', 'rb'))
        self.model = model
        self.intents_dataset = dataset


    def clean_up_sentence(self, sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self, sentence, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return (np.array(bag))

    def predict_class(self, sentence):
        # filter out predictions below a threshold
        p = self.bow(sentence,  show_details=True)
        print(p)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        for i,r in enumerate(res):
            print(self.classes[i], r)
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints, sender=None):
        tag = ints[0]['intent']
        list_of_intents = self.intents_dataset['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                r = Text(random.choice(i['responses'])).message()
                break
        return r



class Flow:
    def __init__(self, dataset, model):
        self.trigger = model
        self.datset = dataset
        self.sates = {"active": False, "count": 0, "sender": ""}

    def launch_flow(self, flow, sender=None):
        global flow_active, flow_count
        flow_active = True
        print("flow found!")
        # return first content
        content_count = len(flow)
        if flow_count <= (content_count - 1):
            r = flow[flow_count]
            flow_count = flow_count + 1
        # reach end of list
        else:
            flow_active = False
            r = None
        return r

    def add(self, objects):
        for obj in objects:
            self.contents.append(obj)
            self.lenght = len(self.contents)


    def addFlow(self, flows):
        for flow in flows:
            self.flows.update({flow.trigger:flow.contents})

    def startFlows(self, trigger):
        for trig, flow in self.flows.items():
            if trig == trigger:
                self.activeFlows.update({trig:flow})



