from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pandas
import numpy as numpy

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
        return cpweAcc


    # extracting Computed Packet Rate Feature (CPRF)

    def getCprf(dataset):
        timeframe = #timeframe used for PPF
        packetPerFlow = #total number of packets in a single flow interval
        monitoringInterval = something

        cprf = packetPerFlow / (timeframe * monitoringInterval)
        return cprf

    
    # extracting Received Flow Packets Standard Deviation (RFPSD)
    def getRfpsd(dataset):
        packetsPerFlow = #column containing packets for each flow from dataset
        noOfFlows = len(packetsPerFlow)

        # formula from the paper
        rfpsd = math.sqrt(sum((n - (sum(packet_counts) / noOfFlows)) ** 2 for n in packetsPerFlow) / f)
        return rfpsd

    # extracting Received Flow Bytes Standard Deviation (RFBSD)

    def getRfbsd(dataset):
        bytesPerFlow = # column containing bytes for each flow from dataset
        noOfFlows = len(bytesPerFlow)

        # formula from the paper
        rfbsd = math.sqrt(sum((n - bytesPerFlow.mean()) ** 2 for n in bytesPerFlow) / noOfFlows)
        return rfbsd

    # extracting Computed Flow Entry Rate (CFER)

    def getCfer(dataset):

        # cfer = total number of flows in a given time / monitoring interval

def trainTest:
    

def main:
    preprocess()