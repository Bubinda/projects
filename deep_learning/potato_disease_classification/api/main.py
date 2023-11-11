

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# the part obove is added for the requests comming from the react website so those calls are allowed

# load the model

max_model_version = max([int(i.split('_')[1]) if len(i) > 1 else int(i) for i in os.listdir('../saved_models')]) 

MODEL = tf.keras.models.load_model(f"../saved_models/model_{max_model_version}") # always load the newest model

CLASS_NAMES = [i.split('___')[1] for i in os.listdir('../training/data')] # dynamic assignnemt of the lass names, if there are added more to the project data or if the model is changed to other data
# if the data is change to another source the split operator might have to be changed
#CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Server up and running!"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0) #expand the image so the batch_size dimension is added for the models prediction (in this case this would be an empty dimnesion)
    
    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': round(float((confidence*100)),2) # convert the convidence into a percentage value and round it
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)

