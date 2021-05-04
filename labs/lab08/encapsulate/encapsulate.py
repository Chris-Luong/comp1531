import datetime 

class Student:
    def __init__(self, firstName, lastName, birth_year):
        self.name = firstName + " " + lastName
        self.birth_year = birth_year
    
    def getAge(self):
        present = datetime.datetime.now()
        return present.year - self.birth_year
    
    def getName(self):
        return self.name
    
    def print_age(self):
        print(f"{self.getName} is {self.getAge} years old")

if __name__ == '__main__':
    s = Student("Rob", "Everest", 1961)
    s.print_age
