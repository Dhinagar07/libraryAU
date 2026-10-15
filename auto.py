class automobile:
    def accelerate(self):
        print(" accelerating.")
    def brake(self):
        print(" braking.")

class car(automobile):
    
    def open_trunk(self):
        print("The car's trunk is open.")


z=car()
z.accelerate()
z.brake()
z.open_trunk()