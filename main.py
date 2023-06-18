import math
import tkinter as tk
import tkinter.font as tkFont
from functools import partial


#POLECENIE
# Napisać program pozwalający na określenie wartości OSNR na wyjściu toru wzmacnianego
# optycznie. Parametrami zadawanymi przez użytkownika są:
# -moc sygnału na wejściu światłowodu,
# -tłumienność jednostkowa światłowodu (w dB/km),
# -całkowita długość toru (w km),
# -położenie wzmacniaczy optycznych (ich odległość od początku światłowodu wyrażona w
# kilometrach),
# -wartości wzmocnienia i współczynnika szumów dla poszczególnych wzmacniaczy optycznych
# (mogą być różne dla różnych wzmacniaczy).
# Uwaga: ze względu na różne parametry wzmacniaczy i możliwe nierównomierne odstępy
# między nimi nie można skorzystać z wzoru na OSNR podanego na wykładzie.


def calculate_hfdf(wave_length, filter_delta_lambda):
    PLANCK_CONSTANT = 6.62607015e-34
    SPEED_OF_LIGHT = 299792458.0
    # SPEED_OF_LIGHT = 300000000

    f = SPEED_OF_LIGHT / (wave_length * 0.000001)
    df = (SPEED_OF_LIGHT * filter_delta_lambda * 0.000000001) / ((wave_length * 0.000001)**2)
    hfdf = PLANCK_CONSTANT * f * df
    hfdf = 10.0 * math.log10(hfdf)
    hfdf = hfdf + 30.0
    return hfdf

def calculate_Ps(power_in, fiber_length,unit_fiber_attenuation, amps ):
    amps_power = 0.0
    for amp in amps:
        amps_power += amp[1]
    Ps = power_in - fiber_length*unit_fiber_attenuation + amps_power
    return Ps

def sort_amps(amps,fiber_length):

    to_far=[]
    for x in range(len(amps) - 1):
        if amps[x][0] > fiber_length:
            to_far.append(x)
    to_far.reverse()
    for x in to_far:
        amps.remove(amps[x])
    print(amps)

    amps = sorted(amps, key=lambda x: x[0])
    delete_list = []
    for x in range(len(amps)-1):
        if amps[x][0] == amps[x+1][0]:
            delete_list.append(x)
    delete_list.reverse()
    for x in delete_list:
        amps.remove(amps[x])
    return amps

def amplifiers_noise_calculation(amps,hfdf, fiber_length, unit_fiber_attenuation):
    amplifiers_noises=[]
    for x in range(len(amps)):
        next_amps_gain = 0
        for y in range(len(amps)):
            if amps[x][0] < amps[y][0]:
                next_amps_gain = next_amps_gain+amps[y][1]
        noise = amps[x][1] + amps[x][2] + hfdf - (fiber_length - amps[x][0])*unit_fiber_attenuation + next_amps_gain
        amplifiers_noises.append(noise)

    return amplifiers_noises

def calculate_OSNR(Ps,Pn_table):
    noise_sum = 0
    for noise in Pn_table:
        noise_sum += 10.0**(noise/10.0)
    Psignal = 10.0**(Ps/10.0)
    osnr_mw = Psignal/noise_sum
    OSNR = 10*math.log10(osnr_mw)
    print("OSNR = {:.1f} dB".format(OSNR))
    return(OSNR)


def calculations(power_in, fiber_length, unit_fiber_attenuation, wave_length,filter_delta_lambda, amps):
    hfdf = calculate_hfdf(wave_length, filter_delta_lambda)
    amps = sort_amps(amps, fiber_length)
    Ps = calculate_Ps(power_in, fiber_length,unit_fiber_attenuation, amps )
    Pn_table = amplifiers_noise_calculation(amps, hfdf, fiber_length, unit_fiber_attenuation)
    res = calculate_OSNR(Ps , Pn_table)
    return res

class App:



    def __init__(self, root):
        #setting title
        root.title("OSNR Calculator")
        #setting window size
        width=1000
        height=400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


        GLabel_883=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_883["font"] = ft
        GLabel_883["fg"] = "#333333"
        GLabel_883["justify"] = "center"
        GLabel_883["text"] = "Sender Power [dBm]"
        GLabel_883.place(x=40,y=30,width=194,height=34)

        GLineEdit_635=tk.Entry(root)
        GLineEdit_635["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_635["font"] = ft
        GLineEdit_635["fg"] = "#333333"
        GLineEdit_635["justify"] = "center"
        GLineEdit_635.insert(0, "")
        GLineEdit_635.place(x=290,y=30,width=112,height=30)

        GLabel_624=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_624["font"] = ft
        GLabel_624["fg"] = "#333333"
        GLabel_624["justify"] = "center"
        GLabel_624["text"] = "Unit fiber attenuation [db/km]"
        GLabel_624.place(x=20,y=140,width=255,height=52)

        GLabel_481=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_481["font"] = ft
        GLabel_481["fg"] = "#333333"
        GLabel_481["justify"] = "center"
        GLabel_481["text"] = "Filter bandwidth[nm]"
        GLabel_481.place(x=40,y=260,width=195,height=39)

        GLabel_23=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_23["font"] = ft
        GLabel_23["fg"] = "#333333"
        GLabel_23["justify"] = "center"
        GLabel_23["text"] = "Fiber length[km]"
        GLabel_23.place(x=30,y=90,width=215,height=30)

        GLabel_604=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_604["font"] = ft
        GLabel_604["fg"] = "#333333"
        GLabel_604["justify"] = "center"
        GLabel_604["text"] = "Wave length [um]"
        GLabel_604.place(x=50,y=200,width=179,height=50)

        GLineEdit_775=tk.Entry(root)
        GLineEdit_775["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_775["font"] = ft
        GLineEdit_775["fg"] = "#333333"
        GLineEdit_775["justify"] = "center"
        GLineEdit_775.insert(0, "")
        GLineEdit_775.place(x=290,y=210,width=110,height=32)

        GLineEdit_506=tk.Entry(root)
        GLineEdit_506["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_506["font"] = ft
        GLineEdit_506["fg"] = "#333333"
        GLineEdit_506["justify"] = "center"
        GLineEdit_506.insert(0, "")
        GLineEdit_506.place(x=290,y=150,width=111,height=31)

        GLineEdit_72=tk.Entry(root)
        GLineEdit_72["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_72["font"] = ft
        GLineEdit_72["fg"] = "#333333"
        GLineEdit_72["justify"] = "center"
        GLineEdit_72.insert(0, "")
        GLineEdit_72.place(x=290,y=90,width=110,height=31)

        GLineEdit_567=tk.Entry(root)
        GLineEdit_567["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_567["font"] = ft
        GLineEdit_567["fg"] = "#333333"
        GLineEdit_567["justify"] = "center"
        GLineEdit_567.insert(0, "")
        GLineEdit_567.place(x=290,y=270,width=112,height=30)

        GLabel_653=tk.Label(root)
        ft = tkFont.Font(family='Times',size=21)
        GLabel_653["font"] = ft
        GLabel_653["fg"] = "#333333"
        GLabel_653["justify"] = "center"
        GLabel_653["text"] = "OSNR[dB] = "
        GLabel_653.place(x=330,y=340,width=155,height=31)

        GLabel_185=tk.Label(root)
        ft = tkFont.Font(family='Times',size=21)
        GLabel_185["font"] = ft
        GLabel_185["fg"] = "#333333"
        GLabel_185["justify"] = "center"
        GLabel_185["text"] = ""
        GLabel_185.place(x=500,y=330,width=90,height=48)

        GLabel_954=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_954["font"] = ft
        GLabel_954["fg"] = "#333333"
        GLabel_954["justify"] = "center"
        GLabel_954["text"] = "Amp distance \n from sender"
        GLabel_954.place(x=560,y=30,width=139,height=53)

        GLineEdit_138=tk.Entry(root)
        GLineEdit_138["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_138["font"] = ft
        GLineEdit_138["fg"] = "#333333"
        GLineEdit_138["justify"] = "center"
        GLineEdit_138.insert(0, "")
        GLineEdit_138.place(x=580,y=100,width=70,height=25)

        GLineEdit_628=tk.Entry(root)
        GLineEdit_628["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_628["font"] = ft
        GLineEdit_628["fg"] = "#333333"
        GLineEdit_628["justify"] = "center"
        GLineEdit_628.insert(0, "")
        GLineEdit_628.place(x=580,y=140,width=70,height=25)

        GLineEdit_725=tk.Entry(root)
        GLineEdit_725["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_725["font"] = ft
        GLineEdit_725["fg"] = "#333333"
        GLineEdit_725["justify"] = "center"
        GLineEdit_725.insert(0, "")
        GLineEdit_725.place(x=580,y=180,width=70,height=25)

        GLineEdit_807=tk.Entry(root)
        GLineEdit_807["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_807["font"] = ft
        GLineEdit_807["fg"] = "#333333"
        GLineEdit_807["justify"] = "center"
        GLineEdit_807.insert(0, "")
        GLineEdit_807.place(x=580,y=220,width=70,height=25)

        GLineEdit_856=tk.Entry(root)
        GLineEdit_856["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_856["font"] = ft
        GLineEdit_856["fg"] = "#333333"
        GLineEdit_856["justify"] = "center"
        GLineEdit_856.insert(0, "")
        GLineEdit_856.place(x=720,y=180,width=70,height=25)

        GLineEdit_589=tk.Entry(root)
        GLineEdit_589["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_589["font"] = ft
        GLineEdit_589["fg"] = "#333333"
        GLineEdit_589["justify"] = "center"
        GLineEdit_589.insert(0, "")
        GLineEdit_589.place(x=720,y=140,width=70,height=25)

        GLineEdit_431=tk.Entry(root)
        GLineEdit_431["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_431["font"] = ft
        GLineEdit_431["fg"] = "#333333"
        GLineEdit_431["justify"] = "center"
        GLineEdit_431.insert(0, "")
        GLineEdit_431.place(x=720,y=100,width=70,height=25)

        GLineEdit_981=tk.Entry(root)
        GLineEdit_981["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_981["font"] = ft
        GLineEdit_981["fg"] = "#333333"
        GLineEdit_981["justify"] = "center"
        GLineEdit_981.insert(0, "")
        GLineEdit_981.place(x=580,y=260,width=70,height=25)

        GLineEdit_835=tk.Entry(root)
        GLineEdit_835["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_835["font"] = ft
        GLineEdit_835["fg"] = "#333333"
        GLineEdit_835["justify"] = "center"
        GLineEdit_835.insert(0, "")
        GLineEdit_835.place(x=720,y=220,width=70,height=25)

        GLineEdit_251=tk.Entry(root)
        GLineEdit_251["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_251["font"] = ft
        GLineEdit_251["fg"] = "#333333"
        GLineEdit_251["justify"] = "center"
        GLineEdit_251.insert(0, "")
        GLineEdit_251.place(x=720,y=260,width=70,height=25)

        GLineEdit_541=tk.Entry(root)
        GLineEdit_541["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_541["font"] = ft
        GLineEdit_541["fg"] = "#333333"
        GLineEdit_541["justify"] = "center"
        GLineEdit_541.insert(0, "")
        GLineEdit_541.place(x=860,y=100,width=70,height=25)

        GLineEdit_744=tk.Entry(root)
        GLineEdit_744["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_744["font"] = ft
        GLineEdit_744["fg"] = "#333333"
        GLineEdit_744["justify"] = "center"
        GLineEdit_744.insert(0, "")
        GLineEdit_744.place(x=860,y=140,width=70,height=25)

        GLineEdit_261=tk.Entry(root)
        GLineEdit_261["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_261["font"] = ft
        GLineEdit_261["fg"] = "#333333"
        GLineEdit_261["justify"] = "center"
        GLineEdit_261.insert(0, "")
        GLineEdit_261.place(x=860,y=260,width=70,height=25)

        GLineEdit_918=tk.Entry(root)
        GLineEdit_918["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_918["font"] = ft
        GLineEdit_918["fg"] = "#333333"
        GLineEdit_918["justify"] = "center"
        GLineEdit_918.insert(0, "")
        GLineEdit_918.place(x=860,y=220,width=70,height=25)

        GLineEdit_782=tk.Entry(root)
        GLineEdit_782["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=14)
        GLineEdit_782["font"] = ft
        GLineEdit_782["fg"] = "#333333"
        GLineEdit_782["justify"] = "center"
        GLineEdit_782.insert(0, "")
        GLineEdit_782.place(x=860,y=180,width=70,height=25)

        GLabel_879=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_879["font"] = ft
        GLabel_879["fg"] = "#333333"
        GLabel_879["justify"] = "center"
        GLabel_879["text"] = "Amp Gain"
        GLabel_879.place(x=710,y=40,width=94,height=30)

        GLabel_783=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_783["font"] = ft
        GLabel_783["fg"] = "#333333"
        GLabel_783["justify"] = "center"
        GLabel_783["text"] = "Amp Noise"
        GLabel_783.place(x=840,y=40,width=99,height=30)

        GLabel_794=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_794["font"] = ft
        GLabel_794["fg"] = "#333333"
        GLabel_794["justify"] = "center"
        GLabel_794["text"] = "Amp  1"
        GLabel_794.place(x=480,y=100,width=70,height=25)

        GLabel_266=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_266["font"] = ft
        GLabel_266["fg"] = "#333333"
        GLabel_266["justify"] = "center"
        GLabel_266["text"] = "Amp 2"
        GLabel_266.place(x=480,y=140,width=70,height=25)

        GLabel_558=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_558["font"] = ft
        GLabel_558["fg"] = "#333333"
        GLabel_558["justify"] = "center"
        GLabel_558["text"] = "Amp 3"
        GLabel_558.place(x=480,y=180,width=70,height=25)

        GLabel_600=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_600["font"] = ft
        GLabel_600["fg"] = "#333333"
        GLabel_600["justify"] = "center"
        GLabel_600["text"] = "Amp 4"
        GLabel_600.place(x=480,y=220,width=70,height=25)

        GLabel_866=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        GLabel_866["font"] = ft
        GLabel_866["fg"] = "#333333"
        GLabel_866["justify"] = "center"
        GLabel_866["text"] = "Amp 5"
        GLabel_866.place(x=480,y=260,width=70,height=25)

        def GButton_65_command():
            power_in = GLineEdit_635.get()
            fiber_length = GLineEdit_72.get()
            unit_fiber_attenuation = GLineEdit_506.get()
            wave_length = GLineEdit_775.get()
            filter_delta_lambda = GLineEdit_567.get()

            amps = []
            a1=[]
            a2=[]
            a3=[]
            a4=[]
            a5=[]
            a1.append(GLineEdit_138.get())
            a1.append(GLineEdit_431.get())
            a1.append(GLineEdit_541.get())
            a2.append(GLineEdit_628.get())
            a2.append(GLineEdit_589.get())
            a2.append(GLineEdit_744.get())
            a3.append(GLineEdit_725.get())
            a3.append(GLineEdit_856.get())
            a3.append(GLineEdit_782.get())
            a4.append(GLineEdit_807.get())
            a4.append(GLineEdit_835.get())
            a4.append(GLineEdit_918.get())
            a5.append(GLineEdit_981.get())
            a5.append(GLineEdit_251.get())
            a5.append(GLineEdit_261.get())
            amps.append(a1)
            amps.append(a2)
            amps.append(a3)
            amps.append(a4)
            amps.append(a5)

            def is_float(value):
                try:
                    float_value = float(value)
                    return True
                except ValueError:
                    return False

            to_remove = []
            for x in range(len(amps)):
                for i in range(len(amps[x])):
                    if is_float(amps[x][i])==False:
                        to_remove.append(x)
            to_remove = list( dict.fromkeys(to_remove))

            amps_valid=[]
            goods = [0,1,2,3,4]
            for x in to_remove:
                goods.remove(x)

            for x in goods:
                if x == 0: amps_valid.append(a1)
                if x == 1: amps_valid.append(a2)
                if x == 2: amps_valid.append(a3)
                if x == 3: amps_valid.append(a4)
                if x == 4: amps_valid.append(a5)
            GLabel_185.config(text=str(power_in))
            # print(power_in, fiber_length, unit_fiber_attenuation, wave_length, filter_delta_lambda)
            # print(amps_valid)

            for x in range(len(amps_valid)):
                for y in range(len(amps_valid[x])):
                    amps_valid[x][y] = float(amps_valid[x][y])
            print(amps_valid)

            power_in = float(power_in) if is_float(power_in) else GLabel_185.config(text="ERROR")
            fiber_length = float(fiber_length) if is_float(fiber_length) else GLabel_185.config(text="ERROR")
            unit_fiber_attenuation = float(unit_fiber_attenuation) if is_float(unit_fiber_attenuation) else GLabel_185.config(text="ERROR")
            wave_length = float(wave_length) if is_float(wave_length) else GLabel_185.config(text="ERROR")
            filter_delta_lambda = float(filter_delta_lambda) if is_float(filter_delta_lambda) else GLabel_185.config(text="ERROR")

            res = calculations(power_in, fiber_length, unit_fiber_attenuation, wave_length,filter_delta_lambda, amps_valid)
            res = round(res,2)
            GLabel_185.config(text=str(res))

        GButton_65 = tk.Button(root)
        GButton_65["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=21)
        GButton_65["font"] = ft
        GButton_65["fg"] = "#000000"
        GButton_65["justify"] = "center"
        GButton_65["text"] = "Calculate OSNR"
        GButton_65.place(x=90, y=340, width=207, height=30)
        GButton_65["command"] = GButton_65_command




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
