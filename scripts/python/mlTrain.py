from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pandas

# replace with actual dataset name
# do i need to convert live traffic into 
dataset = pandas.read_csv("dataset.csv")

def preprocess():
    encoder = LabelEncoder()
    scaler = StandardScaler()

    # missing values replacement (mean) 
    dataset = dataset.fillna(dataset.mean())

    # encoding categorical data
    categoricalCols = dataset.select_dtypes(include=["object"]).columns
    for col in categoricalCols:
        dataset[col] = encoder.fit_transform(dataset[col])

    # feature scaling
    dataset = scaler.fit_transform(dataset)

def featureExtraction():



def trainTest:


def main:
    preprocess()