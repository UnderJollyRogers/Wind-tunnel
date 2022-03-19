import math
import tkMessageBox
from Tkinter import *
from serial import *


class Point:
    def __init__(self):
        self.Points = []
        self.Points_small = []
        self.x = []
        self.y = []
        self.Text = []
        self.Regression = []
        self.Equation = []

    def add_point(self):
        speed = E1.get()
        a = 65.77
        b = -7.803*(10**-5)
        c = 3.325
        d = 0.0003156
        e = math.e
        signal = a*(e**(b*float(speed))) + c*(e**(d*float(speed)))
        signal = str(int(signal))
        ser.write(signal.encode())
        y1 = ser.readline()
        const = float(5)/float(1023)
        vs1 = 0.0094*float(y1)*const - 9.375*(10**-5)
        vs = 42.25*vs1 - 0.8120
        pa = (vs - 0.1*5)*(498.16/(0.8*5))     # Sensor Equation
        yo = 644 - pa * (644 - 92) / 100 - 92
        k1 = CheckVar1.get()
        k2 = CheckVar2.get()
        sp = 0
        if k1 == 1:
            sp = int(speed) * (644 - 92) / 12000 + 92
            l.changes()
        if k2 == 1:
            sp1 = 1096.7*((pa/1.205)**0.5)*3.1416*(0.05**2)
            sp = int(sp1) * (644 - 92) / 102 + 92
            print('sp = ', sp, 'sp1 = ', sp1)
            l.changes()
        list.append(self.x, speed)
        list.append(self.y, pa)
        list.append(self.Points, C.create_oval(sp - 3, yo + 3, sp + 3, yo - 3, fill="red"))
        list.append(self.Points_small,
                    C.create_line(sp, yo, sp, yo))

    def erase_points(self):
        for i in range(0, len(self.Points)):
            C.delete(self.Points[i])
            C.delete(self.Points_small[i])
        self.Points = []
        self.Points_small = []
        self.x = []
        self.y = []
        for i in range(0, len(self.Text)):
            C.delete(self.Text[i])

    def changes_coordinates(self):
        k1 = CheckVar1.get()
        k2 = CheckVar2.get()
        for i in range(0, len(self.Points)):
            C.delete(self.Points[i])
            C.delete(self.Points_small[i])
        self.Points = []
        self.Points_small = []
        if k1 == 1:
            cont = 0
            for h in self.y:
                pa = float(h)
                yo = 644 - pa * (644 - 92) / 100 - 92
                sp = int(self.x[cont]) * (644 - 92) / 12000 + 92
                list.append(self.Points, C.create_oval(sp - 3, yo + 3, sp + 3, yo - 3, fill="red"))
                list.append(self.Points_small,
                            C.create_line(sp, yo, sp, yo))
                cont += 1
        if k2 == 1:
            for h in self.y:
                pa = float(h)
                yo = 644 - pa * (644 - 92) / 100 - 92
                speed = 1096.7*((pa/1.205)**0.5)*3.1416*(0.05**2)
                sp = int(speed) * (644 - 92) / 102 + 92
                list.append(self.Points, C.create_oval(sp - 3, yo + 3, sp + 3, yo - 3, fill="red"))
                list.append(self.Points_small,
                            C.create_line(sp, yo, sp, yo))

    def show_coordinates(self, event1):

        def show_point(event):

            def hide_text(event2):
                for j in range(0, len(self.Text)):
                    C.delete(self.Text[j])
                self.Text = []

            pa = float((552 - event.y))*float(100)/float(552)
            pa = float('{0:.2f}'.format(pa))
            k1 = CheckVar1.get()
            k2 = CheckVar2.get()
            if k1 == 1:
                speed = E1.get()
            if k2 == 1:
                speed = 1096.7 * ((pa / 1.205) ** 0.5) * 3.1416 * (0.05**2)
                print('Pos = ', event.x)
                speed = float("{0:.2f}".format(speed))
            if event.x < canvas_width - 100:
                list.append(self.Text, C.create_text(
                    event.x + 38, event.y, text="(" + str(speed) + ", " + str(pa) + ")"))
            else:
                list.append(self.Text, C.create_text(
                    event.x - 38, event.y, text="(" + str(speed) + ", " + str(pa) + ")"))
            for k in range(0, len(self.Points)):
                C.tag_bind(self.Points[k], "<Leave>", hide_text)

        for i in range(0, len(self.Points)):
            C.tag_bind(self.Points_small[i], "<Enter>", show_point)

    def erase_regression(self):
        for i in range(0, len(self.Regression)):
            C.delete(self.Regression[i])
        self.Regression = []
        for j in range(0, len(self.Equation)):
            C.delete(self.Equation[j])
        self.Equation = []

    def linear_regression(self):
        for i in range(0, len(self.Regression)):
            C.delete(self.Regression[i])
        self.Regression = []
        n = float(len(self.x))
        sum_x = 0
        sum_y = 0
        sum_xy = 0
        sum_x2 = 0
        sum_x1 = 0
        sum_x1y = 0
        sum_x12 = 0
        for i in range(len(self.x)):
            sum_xy += float(self.x[i])*float(self.y[i])
            sum_x2 += float(self.x[i])**2
            sum_x += float(self.x[i])
            sum_y += float(self.y[i])
            sp1 = 1096.7 * ((float(self.y[i]) / 1.205) ** 0.5) * 3.1416 * (0.05**2)
            sum_x1 += sp1
            sum_x12 += sp1**2
            sum_x1y += sp1*float(self.y[i])
        if (n*sum_x2-sum_x**2 == 0) | (n*sum_x12-sum_x1**2 == 0):
            tkMessageBox.showinfo("Warning!!!", "The linear regression function needs more points.")
            return
        a1 = (n*sum_xy - sum_x*sum_y)/(n*sum_x2-sum_x**2)
        a0 = (sum_y*sum_x2-sum_xy*sum_x)/(n*sum_x2-sum_x**2)
        a3 = (n*sum_x1y - sum_x1*sum_y)/(n*sum_x12-sum_x1**2)
        a2 = (sum_y*sum_x12-sum_x1y*sum_x1)/(n*sum_x12-sum_x1**2)
        k1 = CheckVar1.get()
        k2 = CheckVar2.get()
        if (k1 == 0 and k2 == 0) or (k1 == 1 and k2 == 1):
            tkMessageBox.showinfo("Warning!!!", "Please, select one pair of variables to make the plot.")
            return
        if k1 == 1:
            sp2 = 644
            sp1 = 92
            pa1 = a0
            pa1 = 644 - pa1 * (644 - 92) / 100 - 92
            pa2 = a0 + a1*12000
            pa2 = 644 - pa2 * (644 - 92) / 100 - 92
            list.append(self.Regression, C.create_line(sp1, pa1, sp2, pa2, fill="red"))
            list.append(self.Equation, C.create_text(220, 30, text='Obtained Equation:'))
            list.append(self.Equation, C.create_text(220, 50, text='F(x) = ' + str(a0) + ' + (' + str(a1) + '*x)'))
        if k2 == 1:
            sp2 = 644
            sp1 = 92
            pa1 = a2
            pa1 = 644 - pa1 * (644 - 92) / 100 - 92
            pa2 = a2 + 102*a3
            pa2 = 644 - pa2 * (644 - 92) / 100 - 92
            list.append(self.Regression, C.create_line(sp1, pa1, sp2, pa2, fill="red"))
            list.append(self.Equation, C.create_text(220, 30, text='Obtained Equation:'))
            list.append(self.Equation, C.create_text(220, 50, text='F(x) = ' + str(a2) + '+' + str(a3) + '*x'))


class LinesOnCanvas:
    def __init__(self):
        t = 0
        t2 = 0
        line_distance = 92
        self.gadgets = []
        self.x1 = "RPM"
        self.y1 = "Pa"
        C.create_line(line_distance, 0, line_distance, canvas_height)
        C.create_line(0, 552, canvas_width, 552)
        list.append(self.gadgets, C.create_text(364, 583, text=self.x1, font=13))
        list.append(self.gadgets, C.create_text(52, 265, text=self.y1, font=13))
        self.incrementY = 100          # Maximum value in the coordinate Y
        self.incrementX = 12000        # Maximum value in the coordinate X
        for x in range(line_distance, canvas_width + 4, line_distance):
            C.create_line(x, 0, x, canvas_height, fill="#b8c2cc", dash=TRUE)
            list.append(self.gadgets, C.create_text(x - 15, 552 + 10, text=str(t)))
            if t != 0:
                list.append(self.gadgets, C.create_text(92 - 15, 650 - (x - 5), text=str(t2)))
            t += int(self.incrementX / 6)
            t2 += int(self.incrementY / 6)
        for y in range(line_distance, canvas_height + 4, line_distance):
            C.create_line(0, y, canvas_width, y, fill="#b8c2cc", dash=TRUE)
        self.parameter = 1

    def changes(self):
        p.erase_regression()
        k1 = CheckVar1.get()
        k2 = CheckVar2.get()
        k3 = 0
        if (k1 == 0 and k2 == 0) or (k1 == 1 and k2 == 1):
            tkMessageBox.showinfo("Warning!!!", "Please, select one pair of variables to make the plot")
            return
        if k1 == 1 and self.parameter == 2:
            for i in range(0, len(self.gadgets)):
                C.delete(self.gadgets[i])
                C.delete(self.gadgets[i])
            self.parameter = 1
            self.x1 = "RPM"
            self.y1 = "Pa"
            self.incrementY = 100
            self.incrementX = 12000
            k3 = 1
        if k2 == 1 and self.parameter == 1:
            for i in range(0, len(self.gadgets)):
                C.delete(self.gadgets[i])
                C.delete(self.gadgets[i])
            self.parameter = 2
            self.x1 = "m^3/min"
            self.y1 = "Pa"
            self.incrementY = 100
            self.incrementX = 102
            k3 = 1
        if k3 == 1:
            t = 0
            t2 = 0
            line_distance = 92
            C.create_line(line_distance, 0, line_distance, canvas_height)
            C.create_line(0, 552, canvas_width, 552)
            list.append(self.gadgets, C.create_text(364, 583, text=self.x1, font=13))
            list.append(self.gadgets, C.create_text(52, 265, text=self.y1, font=13))
            for x in range(line_distance, canvas_width + 4, line_distance):
                C.create_line(x, 0, x, canvas_height, fill="#b8c2cc", dash=TRUE)
                list.append(self.gadgets, C.create_text(x - 15, 552 + 10, text=str(t)))
                if t != 0:
                    list.append(self.gadgets, C.create_text(92 - 15, 650 - (x - 5), text=str(t2)))
                t += int(self.incrementX / 6)
                t2 += int(self.incrementY / 6)
            for y in range(line_distance, canvas_height + 4, line_distance):
                C.create_line(0, y, canvas_width, y, fill="#b8c2cc", dash=TRUE)
        p.changes_coordinates()


def set_speed():
    speed = E1.get()
    if float(speed) > 11700:
        tkMessageBox.showinfo("Warning!!!", "The maximum speed of the motors its 11700RPM please enter a new value.")
        E1.delete(0, len(speed))
        E1.insert(0, "0")
    elif float(speed) >= 6500:
        a = 65.77
        b = -7.803 * (10 ** -5)
        c = 3.325
        d = 0.0003156
        e = math.e
        signal = a * (e ** (b * float(speed))) + c * (e ** (d * float(speed)))
        signal = str(int(signal))
        ser.write(signal.encode())
        ser.readline()
    elif float(speed) == 0:
        speed = "10"
        ser.write(speed.encode())
        ser.readline()
    else:
        tkMessageBox.showinfo("Warning!!!", "The minimum speed of the motors its 6500RPM please enter a new value.")
        E1.delete(0, len(speed))
        E1.insert(0, "0")
        speed = "10"
        ser.write(speed.encode())
        ser.readline()


def get_serial_value():
    serial_port = E2.get()
    ser.baudrate = 9600
    ser.port = serial_port
    ser.open()
    a = ser.readline()
    if "Python" in a:
        root1.destroy()
    else:
        tkMessageBox.showinfo("Warning!!!", "Please enter the Serial Port in which arduino is connected.")


root1 = Tk()
root1.wm_title("Serial Port")
L1 = Label(root1, text="Serial Port: ")
L1.grid(row=0, column=0)
E2 = Entry(root1, bd=4)
E2.grid(row=0, column=2)

ser = Serial()
IntroduceButton = Button(root1, text="Insert", fg="black", command=get_serial_value)
IntroduceButton.grid(row=1, column=2)
root1.mainloop()

p = Point()
# ***** Wind Tunnel *****
root2 = Tk()
root2.wm_title("Axial Fans' Bank")

# ***** Set Right Frame *****
rightFrame = Frame(root2)
rightFrame.pack(side=RIGHT, fill=BOTH)

# ***** Place a canvas on the Right Frame *****
CheckVar1 = IntVar()
canvas_width = 650
canvas_height = 650
C = Canvas(rightFrame, bg="white", relief="sunken", bd=2, height=canvas_height, width=canvas_width)
C.bind("<Enter>", p.show_coordinates)
C.pack(fill=BOTH, expand=TRUE)

# ***** Set Left Frame *****
leftFrame = Frame(root2)
leftFrame.pack(side=LEFT, fill=BOTH)

# ***** Set Labels on Left Frame *****
L1 = Label(leftFrame, text="Motors speed: ")
L1.grid(row=0, column=0, sticky=E)

# ***** Set Entry on Left Frame *****
E1 = Entry(leftFrame, bd=4, width=30, justify=CENTER)
E1.insert(END, '0')
E1.grid(row=0, column=1, sticky=N)

# ***** Set Button on Left Frame *****
Set = Button(leftFrame, text="Set Speed", fg="black", width=26, command=set_speed)
Set.grid(row=1, column=1, sticky=N)

# ***** Set Label on Left Frame *****
L3 = Label(leftFrame, text="Get Pressure Value:")
L3.grid(row=3, column=0, sticky=N)

# ***** Set Button on Left Frame *****
GetPressure = Button(leftFrame, text="Get Pressure", fg="black", width=26, command=p.add_point)
GetPressure.grid(row=3, column=1)

# ***** Erase Button *****
EraseButton = Button(leftFrame, text="Erase Points", fg="black", width=26, command=p.erase_points)
EraseButton.grid(row=5, column=1, sticky=N)

# ***** Check Buttons *****
CheckVar1 = IntVar()
CheckVar2 = IntVar()
ch1 = Checkbutton(leftFrame, text="Dynamic Pressure Vs Speed", variable=CheckVar1, onvalue=1, offvalue=0, width=30)
ch1.select()
ch1.grid(row=7, column=1, sticky=W)
ch2 = Checkbutton(leftFrame, text="Dynamic Pressure Vs Air Flow", variable=CheckVar2, onvalue=1, offvalue=0, width=30)
ch2.grid(row=8, column=1, sticky=W)

# ***** Variable Button *****
l = LinesOnCanvas()
VariableButton = Button(leftFrame, text="Select Variables", fg="black", width=26, command=l.changes)
VariableButton.grid(row=9, column=1, sticky=N)

# ***** Regression Button *****
VariableButton = Button(leftFrame, text="Linear Regression", fg="black", width=26, command=p.linear_regression)
VariableButton.grid(row=10, column=1, sticky=N)

# ***** Erase Regression *****
VariableButton = Button(leftFrame, text="Erase Regression", fg="black", width=26, command=p.erase_regression)
VariableButton.grid(row=11, column=1, sticky=N)

root2.mainloop()
