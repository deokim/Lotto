class Student:
    def __init__(self, name, korean, math, english, science):
        self.name=name
        self.korean=korean
        self.math=math
        self.english=english
        self.science=science

    def get_sum(self):
        return self.korean+self.math+self.english+self.science
    
    def get_average(self):
        return self.get_sum()/4
    
    def __str__(self):
        return "{}\t{}\t{}".format(self.name, self.get_sum(), self.get_average())
    
    def __eq__(self, value):
        return self.get_average()==value
    
    def __gt__(self, value):
        return self.get_average() > value
    

students=[
    Student("윤인성", 87, 98, 88, 95),
    Student("연하진", 92, 98, 96, 98),
    Student("구지연", 76, 96, 94, 90),
    Student("나선주", 92, 92, 96, 92),
    Student("윤아린", 95, 98, 88, 98),
    Student("윤명월", 64, 88, 92, 92),
]

studens_a=students[0]
studens_b=students[1]

test=Student("A", 90, 90, 90, 90)

print("test==90", test>89.1)
