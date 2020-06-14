# Convert checkpoints from Chapter 7 to the right format for this chapter

import h5py
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from keras.models import load_model

model = load_model('checkpoints/small_model_epoch_5.h5')
encoder = OnePlaneEncoder((19, 19))
agent = DeepLearningAgent(model, encoder)
agent.serialize(h5py.File('agents/test.h5', 'w'))
