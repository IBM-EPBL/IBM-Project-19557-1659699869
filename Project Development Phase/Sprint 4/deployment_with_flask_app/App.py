from flask import Flask, request, render_template,make_response
import pickle
import cv2
from skimage import feature
import os.path
 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file'] 
        
        basepath = os.path.dirname('__file__')
        filepath = os.path.join(basepath, "uploads", f.filename)
        f.save(filepath)
        print(str(request.form['imageType']) == 'spiral')
        if str(request.form['imageType'] == 'spiral'):
            model = pickle.loads(open('parkinson-spiral-model.pkl','rb').read())
            print("sprial")
        else:
            model = pickle.loads(open('parkinson-wave-model.pkl','rb').read())
        image = cv2.imread(filepath)   
        output = image.copy()
        output =cv2.resize(output, (128, 128))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        features = feature.hog(image, orientations=9,
                               pixels_per_cell=(10, 10), cells_per_block=(2, 2),
                               transform_sqrt=True, block_norm="L1")
        preds = model.predict([features])
        ls = ["../static/assets/not_detected.png","../static/assets/detected.jpg"]
        print(preds[0])
        return render_template("predict.html",image=ls[preds[0]])
   
     
    
    


if __name__ == "__main__":
    app.run(debug=True,port=5555)