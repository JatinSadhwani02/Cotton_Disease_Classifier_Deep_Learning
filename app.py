#Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

#load model
model =load_model("predicted_cotton_disease_model.h5")

print('@@ Model loaded')


def pred_cot_dieas(cott_plant):
  test_image = load_img(cott_plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image).round(3) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result) # get the index of max value
  print('@@ final predicted value = ',pred)

  return pred

  # if pred == 0:
  #   return "Healthy Cotton Plant", 'healthy_plant_leaf.html' # if index 0 burned leaf
  # elif pred == 1:
  #     return 'Diseased Cotton Plant', 'disease_plant.html' # # if index 1
  # elif pred == 2:
  #     return 'Healthy Cotton Plant', 'healthy_plant.html'  # if index 2  fresh leaf
  # else:
  #   return "Healthy Cotton Plant", 'healthy_plant.html' # if index 3

#------------>>pred_cot_dieas<<--end
    

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
  return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():   
  if request.method == 'POST':
    file = request.files['image'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join('static/user uploaded', filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred = pred_cot_dieas(cott_plant=file_path)

    if pred == 0:
      return render_template('healthy_plant_leaf.html', pred_output = 'Healthy Cotton Plant', user_image = file_path)
    elif pred==1:
      return render_template('disease_plant.html', pred_output = 'Disease Cotton Plant', user_image = file_path)
    elif pred==2:
      return render_template('healthy_plant.html', pred_output = 'Healthy Cotton Plant', user_image = file_path)
    else:
      return render_template('healthy_plant.html', pred_output = 'Healthy Cotton Plant', user_image = file_path)




    
# For local system & cloud
if __name__ == "__main__":
    app.run(debug=True) 
    
    