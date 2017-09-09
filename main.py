import api

patients = []
personel = []

p1 = api.Patient("Nemo", "3316255936")
p2 = api.Patient("The Little Mermaid", "4141241255")
m1 = api.MedicalPersonel("Nurse Joy")
m2 = api.MedicalPersonel("Doctor Strange")

patients.append(p1)
patients.append(p2)
personel.append(m1)
personel.append(m2)

p1.logWrite("hello", "Nurse Joy")
m1.logWrite("hi", "Nemo")
p2.logWrite("hullo", "Nurse Joy")
p2.logWrite("bye", "Nurse Joy")
m1.logWrite("bye", "The Little Mermaid")
m1.forwardLog(p2, "Doctor Strange", personel)

p1.updatePain(10)
p2.updatePain(2)

print m2.lookupPatient("Nemo", patients)




