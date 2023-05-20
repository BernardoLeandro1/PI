#Simula as luzes enquanto não temos acesso às reais

import turtle

class lightssss:
    def __init__(self):
        
        wn = turtle.Screen()
        wn.title("Simulating Home Lights")
        wn.bgcolor("white")

        pen = turtle.Turtle()
        pen.penup()
        availableLights = {"quarto": "0", "quarto de banho" : "1", "casa de banho" : "1", "sala" : "2", "cozinha": "3", "dispensa": "4", "entrada" : "5", "espelho": "6"}

        self.quarto_light = turtle.Turtle()
        self.quarto_light.shape("circle")
        self.quarto_light.color("grey")
        self.quarto_light.penup()
        self.quarto_light.goto(-200, -200)
        pen.goto(-230, -180)
        pen.write("Quarto", font=("Arial", 15, "bold"))
        pen.penup()

        self.wc_light = turtle.Turtle()
        self.wc_light.shape("circle")
        self.wc_light.color("grey")
        self.wc_light.penup()
        self.wc_light.goto(-200, 0)
        pen.goto(-260, 20)
        pen.write("Casa de Banho", font=("Arial", 15, "bold"))
        pen.penup()

        self.sala_light = turtle.Turtle()
        self.sala_light.shape("circle")
        self.sala_light.color("grey")
        self.sala_light.penup()
        self.sala_light.goto(-200, 200)
        pen.goto(-220, 220)
        pen.write("Sala", font=("Arial", 15, "bold"))
        pen.penup()

        self.cozinha_light = turtle.Turtle()
        self.cozinha_light.shape("circle")
        self.cozinha_light.color("grey")
        self.cozinha_light.penup()
        self.cozinha_light.goto(0, 200)
        pen.goto(-30, 220)
        pen.write("Cozinha", font=("Arial", 15, "bold"))
        pen.penup()

        self.dispensa_light = turtle.Turtle()
        self.dispensa_light.shape("circle")
        self.dispensa_light.color("grey")
        self.dispensa_light.penup()
        self.dispensa_light.goto(0, 0)
        pen.goto(-30, 20)
        pen.write("Dispensa", font=("Arial", 15, "bold"))
        pen.penup()

        self.entrada_light = turtle.Turtle()
        self.entrada_light.shape("circle")
        self.entrada_light.color("grey")
        self.entrada_light.penup()
        self.entrada_light.goto(0, -200)
        pen.goto(-30, -180)
        pen.write("Entrada", font=("Arial", 15, "bold"))
        pen.penup()

        self.espelho_light = turtle.Turtle()
        self.espelho_light.shape("circle")
        self.espelho_light.color("grey")
        self.espelho_light.penup()
        self.espelho_light.goto(200, 200)
        pen.goto(170, 220)
        pen.write("Espelho", font=("Arial", 15, "bold"))
        pen.penup()



    def turn_on(self, light):
        light = str(light)
        if light.__contains__("sala"):
            if self.sala_light.pencolor() != "yellow":
                self.sala_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("quarto"):
            if self.quarto_light.pencolor() != "yellow":
                self.quarto_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("casa de banho") or light.__contains__("quarto de banho"):
            if self.wc_light.pencolor() != "yellow":
                self.wc_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("cozinha"):
            if self.cozinha_light.pencolor() != "yellow":
                self.cozinha_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("dispensa"):
            if self.dispensa_light.pencolor() != "yellow":
                self.dispensa_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("entrada"):
            if self.entrada_light.pencolor() != "yellow":
                self.entrada_light.color("yellow")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("espelho"):
            if self.espelho_light.pencolor() != "yellow":
                self.espelho_light.color("yellow")
                return "OK"
            else: 
                return "Done" 

    def turn_off(self, light):
        light = str(light)
        if light.__contains__("sala"):
            if self.sala_light.pencolor() != "grey":
                self.sala_light.color("grey")
                return "OK"
            else:
                return "Done"
        elif light.__contains__("quarto"):
            if self.quarto_light.pencolor() != "grey":
                self.quarto_light.color("grey")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("casa de banho") or light.__contains__("quarto de banho"):
            if self.wc_light.pencolor() != "grey":
                self.wc_light.color("grey")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("cozinha"):
            if self.cozinha_light.pencolor() != "grey":
                self.cozinha_light.color("grey")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("dispensa"):
            if self.dispensa_light.pencolor() != "grey":
                self.dispensa_light.color("grey")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("entrada"):
            if self.entrada_light.pencolor() != "grey":
                self.entrada_light.color("grey")
                return "OK"
            else: 
                return "Done"
        elif light.__contains__("espelho"):
            if self.espelho_light.pencolor() != "grey":
                self.espelho_light.color("grey")
                return "OK"
            else: 
                return "Done" 