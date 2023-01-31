# coding: utf-8

class QOSINFO:

    def __init__(self):
        self._status = "QOSUNKNOWN"

    def _getStatus(self):
        #print("get status")
        return self._status

    def _setStatus(self, s):
        #print("s = " + s)
        if(s == "QOS_GUARANTEED"):
            self._status = "QOSOK"
        elif(s == "QOS_NOT_GUARANTEED"):
            self._status = "QOSNOK"
        else:
            self.status = "QOSUNKNOWN"

    status=property(_getStatus, _setStatus)