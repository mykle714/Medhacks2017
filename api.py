import Queue
import os.path
import os

class User:
    def __init__(self, name, email, password):
        self.attr = {"name":name, "email":email, "password":password}
    
    def changeName(self, name):
        self.attr["name"] = name
    
    def readLog(self, name):
        if os.path.isfile(logs % (self.attr["name"], name)):
            with open(logs % (self.attr["name"], name), "a+") as file:
                return file
        elif os.path.isfile(logs % (name, self.attr["name"])):
            with open(logs % (name, self.attr["name"]), "a+") as file:
                return file

    def findUser(name, list):
        for i in list:
            if i.attr["name"] == name:
                return i
        return None
    
    def changeStatus(self):
        if self.status:
            self.status = False
        else:
            self.status = True

    def setStatus(self, status):
        assert isinstance(status, bool)
        self.status = status

    def logWrite(self, title, data):
        with open("logs/%s.%s.txt" % (title, self.attr["name"] if isinstance(self, MedicalPersonnel) else self.nurse), "a") as file:
            file.write("%s: %s" % (self.attr["name"], data))

    def get(self, name=None):
        if name is not None:
            return getattr(self, name)
        elif isinstance(self, Patient):
            ret = []
            for i in self.attr:
                ret.append(self.attr[i])

            return ret
        elif isinstance(self, MedicalPersonnel):
            ret = []
            for i in self.attr:
                ret.append(self.attr[i])

            return ret

class Patient(User):

    def __init__(self, name, birthday, address, phone, email, password):
        User.__init__(self, name, email, password)
        self.attr["birthday"] = birthday
        self.attr["address"] = address
        self.attr["phone"] = phone
        self.attr["insurance"] = None
        self.attr["group"] = None
        self.attr["policy"] = None
        self.attr["type"] = None
        self.attr["customer"] = None

    def updateInsurance(self, insurance, group, policy, type, customer):
        self.attr["insurance"] = insurance
        self.attr["group"] = group
        self.attr["policy"] = policy
        self.attr["type"] = type
        self.attr["customer"] = customer

    def requestCall(self):
        self.attr["nurse"].calls.put(self)

    def updatePain(self, pain):
        assert isinstance(pain, int)
        self.attr["pain"] = pain

    def assignNurse(self, nurse):
        self.attr["nurse"] = nurse



class MedicalPersonnel(User):

    def __init__(self, name, email, password):
        User.__init__(self, name, email, password)
        self.attr["calls"] = Queue.Queue()
        self.attr["status"] = False

    def lookupPatient(self, name, patients):
        ret = []
        t1 = findUser(name, patients)
        if t1 is None:
            return None
        for i in Patient.attr:
            ret.append(getattr(t1, i))
        return ret

    def forwardLog(self, patient, name, personnel):
        for i in personnel:
            if i.attr["name"] == name:
                with open(logs % (patient.name, i.attr["name"]), "a+") as file:
                    with open(logs % (patient.name, self.attr["name"]), "r") as f:
                        for i in f:
                            file.write(i)
                return True
        return False

    def changeNurse(self, name, patients, nurse, personnel):
        t1 = findUser(name, patients)
        t2 = findUser(nurse, personnel)
        if t1 is None or t2 is None:
            return None

        t1.assignNurse(t2)
        t1.changeStatus()
        t2.changeStatus()

    def takeCall(self):
        if not self.attr["calls"].empty():
            patient = self.attr["calls"].get()
        #start call with patient

    def list(self):
        ret = []

        for root, dir, files in os.walk("./logs"):
            for i in files:
                t1 = i.split(".")
                if t1[1] == self.attr["name"]:
                    ret.append(t1[0])

        return ret
