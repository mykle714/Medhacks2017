import requests
import api

class Logic:
    def __init__(self):
        self.patients = []
        self.personnel = []
        self.user = None
        self.load("loads/saved.txt")

    def setUser(self, user):
        self.user = user

    def clearUser(self):
        self.user = None

    def saveUser(self, user):
        with open("loads/saved.txt", "a+") as file:
            if isinstance(user, api.Patient):
                str = "%s %s %s %s %s %s %s %s %s %s %s %s" % ("patient",
                                                               user.name,
                                                               user.birthday,
                                                               user.address,
                                                               user.phone,
                                                               user.email,
                                                               user.password,
                                                               user.insurance,
                                                               user.group,
                                                               user.policy,
                                                               user.type,
                                                               user.customer)
            elif isinstance(user, api.MedicalPersonel):
                str = "%s %s %s %s" % ("personnel", user.name, user.email, user.password)
            file.write(str)

    def load(self, filename):
        with open(filename, "r") as file:
            for i in file:
                t1 = i.split(" ")

                if t1[0] == "patient":
                    self.addPatient(t1[1], t1[2], t1[3], t1[4], t1[5], t1[6], t1[7], t1[8], t1[9], t1[10], t1[11])
                elif t1[0] == "personnel":
                    self.addPersonel(t1[1], t1[2], t1[3])

    def addPatient2(self, p):
        self.patients.append(p)

    def addPatient(self, name, birthday, address, phone, email, password, insurance, group, policy, type, customer):
        p = api.Patient(name, birthday, address, phone, email, password)
        p.updateInsurance(insurance, group, policy, type, customer)
        p.setStatus(False)

        self.patients.append(p)

    def addPersonel(self, name, email, password):
        p = api.MedicalPersonel(name, email, password)
        p.setStatus(False)

        self.personnel.append(p)

    def findPatient(self, criteria):
        for i in self.patients:
            if criteria == i.name or criteria == i.email or criteria == i.birthday or criteria == i.address or criteria == i.phone:
                   return i

        return None

    def findPersonel(self, criteria):
        for i in self.patients:
            if criteria == i.name or criteria == i.email:
                return i

        return None

    def login(self, email, password):
        if email == "" or password == "":
            return None
        login = False

        p = self.findPatient(email)
        if p is not None and password == p.password:
            login = True
        else:
            p = self.findPersonel(email)
            if p is not None and password == p.password:
                login = True

        if login:
            return p
        else:
            return None

    def startChat(self, patient, title, message, pain, symptoms):
        with open("%s.%s.txt" % (title, patient.nurse.name), "w+") as file:
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
