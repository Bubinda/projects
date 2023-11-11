from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests
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

#to run this endpoint we can use a docker image of tf-serving:
#docker run -t --rm - p 8501:8501 -v /Users/philipbuchbender/Desktop/projects/deep_learning/potato_disease_classification:/potato_models tensorflow/serving --rest_api_port=8501 --model_config_file=/potato_disease_classification/models.config
#for this the newermodel need to be changed to only number in the folder names

endpoint = "http://localhost:8501/v1/models/potato_model:predict" # this way the server will always use the latest version of the model
# if the versatile .config is used the endpoint would be:
# production_endpoint = "http://localhost:8501/v1/models/potato_model/lables/production:predict"
# beta_endpoint = "http://localhost:8501/v1/models/potato_model/lables/beta:predict"


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
    img_batch = np.expand_dims(image, 0)

    json_data = {
        "instances": img_batch.tolist()
    }

    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()["predictions"][0])

    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction)

    return {
        "class": predicted_class,
        'confidence': round(float((confidence*100)),2) # convert the convidence into a percentage value and round it
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)

