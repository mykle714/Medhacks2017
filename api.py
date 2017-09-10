import Queue
import os.path
import os

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def changeName(self, name):
        self.name = name
    
    def readLog(self, name):
        if os.path.isfile(logs % (self.name, name)):
            with open(logs % (self.name, name), "a+") as file:
                return file
        elif os.path.isfile(logs % (name, self.name)):
            with open(logs % (name, self.name), "a+") as file:
                return file

    def findUser(name, list):
        for i in list:
            if i.name == name:
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
        with open("logs/%s.%s.txt" % (title, self.name if isinstance(self, MedicalPersonel) else self.nurse), "a") as file:
            file.write("%s: %s" % (self.name, data))

class Patient(User):

    attr = ["name", "birthday", "address", "phone", "email", "password", "insurance", "group", "policy", "type", "medication", "allergies", "history", "pain", "status"]

    def __init__(self, name, birthday, address, phone, email, password):
        User.__init__(self,name, email, password)
        self.birthday = birthday
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        
    def updateInsurance(self, insurance, group, policy, type, customer):
        self.insurance = insurance
        self.group = group
        self.policy = policy
        self.type = type
        self.customer = customer

    def requestCall(self):
        self.nurse.calls.put(self)

    def updatePain(self, pain):
        assert isinstance(pain, int)
        self.pain = pain

    def assignNurse(self, nurse):
        assert isinstance(nurse, MedicalPersonel)
        self.nurse = nurse

    def get(self, name):
        if name is not None:
            return getattr(self, name)
        else:
            ret = []
            for i in Patient.attr:
                ret.append(getattr(self,i))

            return ret

class MedicalPersonel(User):

    attr = ["name", "email", "password", "calls", "status"]

    def __init__(self, name, email, password):
        User.__init__(self,name, email, password)
        self.calls = Queue.Queue()
        self.status = False

    def lookupPatient(self, name, patients):
        ret = []
        t1 = findUser(name, patients)
        if t1 is None:
            return None
        for i in Patient.attr:
            ret.append(getattr(t1, i))
        return ret

    def forwardLog(self, patient, name, personel):
        for i in personel:
            if i.name == name:
                with open(logs % (patient.name, i.name), "a+") as file:
                    with open(logs % (patient.name, self.name), "r") as f:
                        for i in f:
                            file.write(i)
                return True
        return False

    def changeNurse(self, name, patients, nurse, personel):
        t1 = findUser(name, patients)
        t2 = findUser(nurse, personel)
        if t1 is None or t2 is None:
            return None

        t1.assignNurse(t2)
        t1.changeStatus()
        t2.changeStatus()

    def takeCall(self):
        if not self.calls.empty():
            patient = self.calls.get()
        #start call with patient

    def list(self):
        ret = []

        for root, dir, files in os.walk("./logs"):
            for i in files:
                t1 = i.split(".")
                if t1[1] == self.name:
                    ret.append(t1[0])

        return ret
