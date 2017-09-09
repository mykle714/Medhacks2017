import Queue
import os.path

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def changeName(self, name):
        self.name = name
    
    def readLog(self, name):
        if os.path.isfile("%s.%s.log.txt" % (self.name, name)):
            with open("%s.%s.log.txt" % (self.name, name), "a+") as file:
                return file
        elif os.path.isfile("%s.%s.log.txt" % (name, self.name)):
            with open("%s.%s.log.txt" % (name, self.name), "a+") as file:
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

class Patient(User):

    attr = ["name", "email", "password", "phone", "pain", "status"]

    def __init__(self, name, email, password, phone):
        User.__init__(self,name, email, password)
        self.phone = phone

    def requestCall(self):
        self.nurse.calls.put(self)

    def logWrite(self, data, name):
        with open("%s.%s.log.txt" % (self.name, name), "a+") as file:
            file.write("%s: %s\n" % (self.name, data))

    def updatePain(self, pain):
        assert isinstance(pain, int)
        self.pain = pain

    def assignNurse(self, nurse):
        assert isinstance(nurse, MedicalPersonel)
        self.nurse = nurse

class MedicalPersonel(User):

    attr = ["name", "email", "password", "calls", "status"]

    def __init__(self, name):
        User.__init__(self,name)
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

    def logWrite(self, data, name):
        with open("%s.%s.log.txt" % (name, self.name), "a+") as file:
            file.write("%s: %s\n" % (self.name, data))

    def forwardLog(self, patient, name, personel):
        for i in personel:
            if i.name == name:
                with open("%s.%s.log.txt" % (patient.name, i.name), "a+") as file:
                    with open("%s.%s.log.txt" % (patient.name, self.name), "r") as f:
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
        t2.changeStatus()


