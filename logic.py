import requests
import api
import os

class Logic:
    def __init__(self):
        self.patients = []
        self.personnel = []
        self.user = None
        for root, dirs, files in os.walk("."):
            for i in files:
                if i[-5:] == ".load":
                    self.load(i)

    def setUser(self, user):
        self.user = user

    def clearUser(self):
        self.user = None

    def getUser(self):
        return self.user.get()

    def saveUser(self, user):
        with open("loads/%s.load" % user.attr["name"], "a+") as file:
            if isinstance(user, api.Patient):
                str = "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" % ("patient",
                user.attr["name"],
                user.attr["birthday"],
                user.attr["address"],
                user.attr["phone"],
                user.attr["email"],
                user.attr["password"],
                user.attr["insurance"],
                user.attr["group"],
                user.attr["policy"],
                user.attr["type"],
                user.attr["customer"],
                user.attr["nurse"])
            elif isinstance(user, api.MedicalPersonnel):
                str = "%s\n%s\n%s\n%s\n" % ("personnel", user.attr["name"], user.attr["email"], user.attr["password"])
            file.write(str)

    def load(self, filename):
        with open("loads/" + filename, "r") as file:
            data = file.readlines()

            if len(data) > 0 and data[0] == "patient\n":
                self.addPatient(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12])
            elif len(data) > 0 and data[0] == "personnel\n":
                self.addPersonnel(data[1], data[2], data[3])

    def addPatient2(self, p):
        self.patients.append(p)

    def addPatient(self, name, birthday, address, phone, email, password, insurance, group, policy, type, customer, nurse):
        p = api.Patient(name, birthday, address, phone, email, password)
        p.updateInsurance(insurance, group, policy, type, customer)
        p.setStatus(False)
        p.assignNurse(nurse)

        self.patients.append(p)

    def addPersonnel(self, name, email, password):
        p = api.MedicalPersonnel(name, email, password)
        p.setStatus(False)

        self.personnel.append(p)

    def findPatient(self, criteria):
        for i in self.patients:
            if criteria == i.attr["name"].rstrip()  or criteria == i.attr["email"].rstrip()  or criteria == i.attr["birthday"].rstrip()  or criteria == i.attr["address"].rstrip()  or criteria == i.attr["phone"].rstrip() :
                return i

        return None

    def findPersonnel(self, criteria):
        for i in self.personnel:
            if criteria == i.attr["name"].rstrip() or criteria == i.attr["email"].rstrip():
                return i

        return None

    def assignNurse(self, user):
        min = -1
        nurse = None
        for i in self.personnel:
            if min == -1 or len(i.list()) < min:
                min = len(i.list())
                nurse = i

        if nurse is not None:
            user.assignNurse(nurse.attr["name"])
            return nurse.attr["name"]
        else:
            return None

    def login(self, email, password):
        if email == "" or password == "":
            return None
        login = False

        p = self.findPatient(email)
        if p is not None and password == p.attr["password"].rstrip():
            login = True
        else:
            p = self.findPersonnel(email)
            if p is not None and password == p.attr["password"].rstrip():
                login = True

        if login:
            return p
        else:
            return None

    def startChat(self, patient, title, message, pain, symptoms):
        with open("%s.%s.txt" % (title, patient.attr["nurse"].attr["name"]), "w+") as file:
            file.write("""message: %s\n
                          pain: %d\n
                          symptoms:\n
                          fever: %s\n
                          headache: %s\n
                          nausia: %s\n
                          swelling: %s\n
                          drainage: %s
                          """ % (message,
                                 pain,
                                 symptoms[0],
                                 symptoms[1],
                                 symptoms[2],
                                 symptoms[3],
                                 symptoms[4]))
