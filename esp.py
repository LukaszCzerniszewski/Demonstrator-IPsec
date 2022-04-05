import pickle

class Esp:
    def __init__(self, securityParametersIndex, sequenceNumber, data,authenticationData):
        self.securityParametersIndex = securityParametersIndex
        self.sequenceNumber=sequenceNumber
        self.data = data
        self.authenticationData = authenticationData
    
    def __bytes__(self):
        return pickle.dumps(self)
    
    def fromBytesToEsp(self,bytesString):
        return pickle.loads(bytesString)