# to be used on live data, mlTrain is more to do with training a model on a csv file. 

# for loading the scikit models
mlModel = joblib.load("RF_ddos_model.pkl")


# for loading tensorflow ann model
annModel = keras.models.load_model("ddos_tensorflow_model")


mlPrediction = model.predict(new_features)
annPrediction = annModel.predict(new_features)