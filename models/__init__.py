import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random


class Create:
    def __init__(self, **kwargs):
        model = Sequential()
        model.add(Dense(128, input_shape=(len(kwargs['train_x'][0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(kwargs['train_y'][0]), activation='softmax'))
        
        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        # fitting and saving the model

        hist = model.fit(np.array(kwargs["train_x"]), np.array(kwargs["train_y"]), epochs=200, batch_size=5, verbose=1)
        model.save(kwargs['name'], hist)
        print("model created")
