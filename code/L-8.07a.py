from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.httpfrontend.server import get_web_app
from keras.models import load_model

model = load_model('checkpoints/small_model_epoch_5.h5')
encoder = OnePlaneEncoder((19, 19))
agent = DeepLearningAgent(model, encoder)
web_app = get_web_app({'predict': agent})
web_app.run()
