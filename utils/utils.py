from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from keras.models import load_model
from config.config import Config

class Helpers:

    model = load_model('Food_Classification_Model.h5')

    def prepare_image(self, img_path):
        img = load_img(img_path, target_size=(224, 224, 3))
        img = img_to_array(img)
        img = img / 255
        img = np.expand_dims(img, [0])
        predictions = self.model.predict(img)
        max_probability = np.max(predictions)
        print(max_probability)
        threshold = 0.9  # Adjust as needed based on model's performance

        # Check if the maximum probability is above the threshold
        if max_probability >= threshold:
            print("valid image")  # Image contains food in the dataset
        else:
            print("Not a valid image")
        y_class = predictions.argmax(axis=-1)
        print(y_class)
        y = " ".join(str(x) for x in y_class)
        return int(y)

    def allowed_image_format(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS