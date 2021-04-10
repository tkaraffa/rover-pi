from gpiozero import Button
class Distance(Button):
    distance = 0
    def add_distance(self):
        distance += 1
        if distance % 10 == 0:
            print(distance)
