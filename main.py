import math

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

def main():

    power_in = float(input("Enter input power [dBm]: "))
    unit_fiber_attenuation = float(input("Enter unit fiber attenuation [dB/km]: "))
    fiber_length = float(input("Enter the length of fiber[km]: "))
    wave_length = float(input("Enter the wave length[um]: "))
    filter_delta_lambda = float(input("Enter the filter bandwidth[nm]: "))
    apl_in_flag = True
    amp_index = 0
    amps = []
    while apl_in_flag:
        yn = input("Would you like to add an amplifier? y/n: ")
        if yn == 'n':
            apl_in_flag = False
        elif yn == 'y':
            distance = float(input("Enter amplifier distance from the start of the track [km]: "))
            gain = float(input("Enter amplifier gain [dB]: "))
            noises = float(input("Enter amplifier noise [dB]: "))
            amp = [distance, gain, noises]
            amps.append(amp)
            amp_index += 1
        else:
            yn = input("Only 'y' or 'n' answers. Would you like to add an amplifier? y/n: ")

    hfdf = calculate_hfdf(wave_length, filter_delta_lambda)
    # amps = [[1,2,3],[2,2,2],[4,2,4],[90,1,1],[1,1,1], [2,3,3], [4,2,3], [2,31,3]]
    amps = sort_amps(amps, fiber_length)
    Ps = calculate_Ps(power_in, fiber_length,unit_fiber_attenuation, amps )
    Pn_table = amplifiers_noise_calculation(amps, hfdf, fiber_length, unit_fiber_attenuation)
    calculate_OSNR(Ps , Pn_table)



if __name__ == "__main__":
    main()
