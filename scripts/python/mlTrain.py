from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pandas
import numpy as numpy
import tensorflow as tensorFlow
from tensorflow import keras
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from sklearn.model_selection import train_test_split

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
    # dataset = scaler.fit_transform(dataset)
    dataset = pandas.DataFrame(scaler.fit_transform(dataset), columns=dataset.columns)
    return dataset

def featureExtraction():
    monitoringInterval = something  #this should be a constant once derived
    noOfFlows = len(dataset)

    # ALL ASSUMING STATIC DATASETS

    # extracting computed particular window entropy (CPWE)
    def getCpwe(dataset):
        cpweWindow = []
        cpweAcc = []  #accumulated values of CPWE
        windowSize = 32

        def calculateEntropy(window):
            counts = {ip: window.count(ip) for ip in set(window)}
            entropy = 0

            for count in counts.values():
                p = count / len(window)
                entropy -= p * math.log2(p)

            return entropy

        for dstip in dataset['dstip']:

            cpweWindow.append(str(dstip))

            if len(cpweWindow) == windowSize:
                cpwe = calculateEntropy(cpweWindow)
                cpweAcc.append(cpwe)
                cpweWindow.pop(0)   # slide the window forward

        # calculate and return the mean entropy value across all windows
        cpweMean = sum(cpweAcc) / len(cpweAcc)
        return cpweMean


    # extracting Computed Packet Rate Feature (CPRF)

    def getCprf(dataset):
        timeframe = #timeframe used for PPF
        packetsPerFlow = dataset['packets'].sum()

        cprf = packetsPerFlow / (timeframe * monitoringInterval)
        return cprf

    
    # extracting Received Flow Packets Standard Deviation (RfalsePositivesSD)
    def getRfalsePositivessd():
        # formula from the paper
        rfalsePositivessd = math.sqrt(sum((n - (sum(packet_counts) / noOfFlows)) ** 2 for n in packetsPerFlow) / f)
        return rfalsePositivessd

    # extracting Received Flow Bytes Standard Deviation (RFBSD)

    def getRfbsd():
        # formula from the paper
        rfbsd = math.sqrt(sum((n - bytesPerFlow.mean()) ** 2 for n in bytesPerFlow) / noOfFlows)
        return rfbsd

    # extracting Computed Flow Entry Rate (CFER)

    def getCfer():
        cfer = noOfFlows / monitoringInterval
        return cfer
        
        # cfer = total number of flows in a given time / monitoring interval






    # add the features to the database, assuming they already exist
    dataset['cpwe'] = getCpwe(dataset)
    dataset['cprf'] = getCprf(dataset)
    dataset['rfalsePositivessd'] = getRfalsePositivessd()
    dataset['rfbsd'] = getRfbsd()
    dataset['cfer'] = getCfer()

# for training scikit learn stuff
def trainTest():

    # features = dataset[['cpwe', 'cprf', 'rfalsePositivessd', 'rfbsd', 'cfer']]  #add any other features necessary here (these are only the 5 new ones)
    # decisionClass = dataset['trafficType']  #can be normal or ddos (boolean)
    features = dataset[['SSIP','Stdevpack','Stdevbyte','NbFlow','NbIntFlow']]   #using this since the example dataset is using this
    decisionClass = dataset['isAttackTraffic']


    featuresTrain, featuresTest, decisionClassTrain, decisionClassTest = train_test_split(
        features,
        decisionClass,
        test_size=0.3,
        random_state=42
    )

    featuresTrain = featuresTrain.to_numpy()
    featuresTest = featuresTest.to_numpy()
    decisionClassTrain = decisionClassTrain.to_numpy()
    decisionClassTest = decisionClassTest.to_numpy()


    # instantiate models
    svm = SVC()
    gnb = GaussianNB()
    knn = KNeighborsClassifier()
    rf = RandomForestClassifier()
    dt = DecisionTreeClassifier()
    blr = LogisticRegression(max_iter=1000)

    # train models
    svm.fit(featuresTrain, decisionClassTrain)
    gnb.fit(featuresTrain, decisionClassTrain)
    knn.fit(featuresTrain, decisionClassTrain)
    rf.fit(featuresTrain, decisionClassTrain)
    dt.fit(featuresTrain, decisionClassTrain)
    blr.fit(featuresTrain, decisionClassTrain)

    # apply to test data
    svmResults = svm.predict(featuresTest)
    gnbResults = gnb.predict(featuresTest)
    knnResults = knn.predict(featuresTest)
    rfResults = rf.predict(featuresTest)
    dtResults = dt.predict(featuresTest)
    blrResults = blr.predict(featuresTest)

    # outruePositivesut results 
    print("\nTraining: SVM")
    print("accuracy:", accuracy_score(decisionClassTest, svmResults))
    print("Classification report:", classification_report(decisionClassTest, svmResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, svmResults))

    print("\nTraining: GNB")
    print("accuracy:", accuracy_score(decisionClassTest, gnbResults))
    print("Classification report:", classification_report(decisionClassTest, gnbResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, gnbResults))

    print("\nTraining: kNN")
    print("accuracy:", accuracy_score(decisionClassTest, knnResults))
    print("Classification report:", classification_report(decisionClassTest, knnResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, knnResults))

    print("\nTraining: Random Forest")
    print("accuracy:", accuracy_score(decisionClassTest, rfResults))
    print("Classification report:", classification_report(decisionClassTest, rfResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, rfResults))

    print("\nTraining: Decision Tree")
    print("accuracy:", accuracy_score(decisionClassTest, dtResults))
    print("Classification report:", classification_report(decisionClassTest, dtResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, dtResults))

    print("\nTraining: Binomial Logistic Regression")
    print("accuracy:", accuracy_score(decisionClassTest, blrResults))
    print("Classification report:", classification_report(decisionClassTest, blrResults))
    print("Confusion matrix:", confusion_matrix(decisionClassTest, blrResults))

    # save using joblib
    joblib.dump(svm, "SVM_ddos_model.pkl")
    joblib.dump(gnb, "GNB_ddos_model.pkl")
    joblib.dump(knn, "kNN_ddos_model.pkl")
    joblib.dump(rf, "RF_ddos_model.pkl")
    joblib.dump(dt, "DT_ddos_model.pkl")
    joblib.dump(blr, "BLR_ddos_model.pkl")

    # create a ANN called model
    model = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(features.shape[1],)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')  #reduces it down to a value between 0 and 1
    ])  

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.TruePositives(name='True positives'),
            keras.metrics.TrueNegatives(name='True negatives'),
            keras.metrics.FalsePositives(name='False positives'),
            keras.metrics.FalseNegatives(name='False negatives')
        ]
    )

    model.fit(
        featuresTrain,
        decisionClassTrain,
        epochs=30,   #Doesnt need many since the adam optimizer 
        batch_size=32,
        validation_split=0.2
    )

    loss, accuracy, precision, recall, truePositives, trueNegatives, falsePositives, falseNegatives = model.evaluate(featuresTest, decisionClassTest)
    print("Loss:", loss)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("True Positives:", truePositives)
    print("True Negatives:", trueNegatives)
    print("False Positives:", falsePositives)
    print("False Negatives:", falseNegatives)


def main():
    dataset = preprocess(dataset)
    trainTest()

