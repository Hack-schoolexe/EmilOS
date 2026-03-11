# dette her er ikke med i vurderingen, dette er bare meg tester noe

import os

import sys

import random

import datetime

import msvcrt  # Windows: for å fange taster én og én til ****-passord

import time



# ===================== FARGER / TEMA =====================



FARGETEMAER = [

    ("Standard (grå på svart)", "07"),

    ("Hacker (grønn på svart)", "0A"),

    ("Blå (hvit på blå)", "1F"),

    ("Gul (gul på svart)", "0E"),

    ("Rød (rød på svart)", "0C"),

    ("Lilla (hvit på lilla)", "5F"),

    ("Aqua (aqua på svart)", "0B"),

    ("Grå (mørk grå på svart)", "08"),

]



CURRENT_COLOR = "07"  # standard





def sett_farge(kode: str):

    global CURRENT_COLOR

    CURRENT_COLOR = kode

    os.system(f"color {kode}")





def farge_meny():

    os.system("cls")

    print("===== VELG FARGE/TEMA =====\n")

    for i, (navn, kode) in enumerate(FARGETEMAER, start=1):

        print(f"{i}. {navn}  (color {kode})")

    print("\n0. Tilbake")



    while True:

        valg = input("\nVelg tema (0-" + str(len(FARGETEMAER)) + "): ").strip()

        if valg == "0":

            return

        if valg.isdigit():

            idx = int(valg)

            if 1 <= idx <= len(FARGETEMAER):

                sett_farge(FARGETEMAER[idx - 1][1])

                os.system("cls")

                print(f"✅ Tema satt til: {FARGETEMAER[idx - 1][0]}")

                time.sleep(0.8)

                return

        print("Ugyldig valg, prøv igjen.")





# ===================== BAT-START (FIX) =====================



BAT_PATH = r"C:\Users\27emsa01\OneDrive - Lillestrøm kommune\Dokumenter\Valgfag\KI-opplegg\echo off1.bat"





def start_bat_kun_en_gang():

    """

    Starter .bat-fila kun én gang per programkjøring (og overlever reboot med os.execv).

    Hindrer vindu-spam.

    """

    if os.environ.get("EMILOS_BAT_STARTED") == "1":

        return

    os.environ["EMILOS_BAT_STARTED"] = "1"

    os.system(fr'start "" "{BAT_PATH}"')





# ===================== BOOT / SHUTDOWN / REBOOT =====================



def vent_på_start():

    os.system("cls")

    print("Trykk MELLOMROM for å starte EmilOS...  (S = Skru av, F = Farger)")

    while True:

        if msvcrt.kbhit():

            t = msvcrt.getch()

            if t == b" ":

                return "start"

            if t in (b"s", b"S"):

                return "shutdown"

            if t in (b"f", b"F"):

                return "colors"





def bios_animation():

    os.system("cls")

    print("EMILWARE BIOS v1.20\n")

    time.sleep(0.4)



    linjer = [

        "CPU: Multi-Core Processor @ 3.40GHz",

        "Memory Testing: 8192MB OK",

        "SATA Port 1: WDC WD10EZEX-00...  OK",

        "SATA Port 2: ST1000DM010-2EP...  OK",

        "USB Devices total: 2 Drives, 1 Keyboard, 1 Mouse",

        "Press DEL to run Setup, F11 for Boot Menu",

        "Detecting boot device...",

        "Boot device found: EmilOS Loader"

    ]

    for l in linjer:

        print(l)

        time.sleep(0.25)



    # 5 sek. nedtelling før loader

    for i in range(5, 0, -1):

        print(f"\nStarter systemloader om {i} sek...", end="\r", flush=True)

        time.sleep(1)

    print()





def boot_animation():

    frames = [

        "Booting .",

        "Booting ..",

        "Booting ...",

        "System Starting.",

        "System Starting..",

        "System Starting...",

        "Loading EmilOS █▒▒▒▒▒▒▒ 10%",

        "Loading EmilOS ██▒▒▒▒▒▒ 20%",

        "Loading EmilOS ███▒▒▒▒▒ 30%",

        "Loading EmilOS ████▒▒▒▒ 40%",

        "Loading EmilOS █████▒▒▒ 50%",

        "Loading EmilOS ██████▒▒ 60%",

        "Loading EmilOS ███████▒ 80%",

        "Loading EmilOS ████████ 100%",

        "System Ready!"

    ]



    for frame in frames:

        os.system("cls")

        print(frame)

        time.sleep(0.15)

    time.sleep(0.5)

    os.system("cls")





def shutdown_animation():

    gammel = CURRENT_COLOR

    os.system("color 0C")



    os.system("cls")

    sekvenser = [

        "[●] Lukker programmer...",

        "[●] Lagrer tilstand...",

        "[●] Slår av tjenester...",

        "[✓] Systemet er klart til å slå av."

    ]

    for s in sekvenser:

        print(s)

        time.sleep(0.6)



    for i in range(3, 0, -1):

        print(f"\nSkru av om {i}...", end="\r", flush=True)

        time.sleep(1)



    os.system("cls")

    print("Power off.")

    time.sleep(0.8)



    os.system(f"color {gammel}")





def reboot_program():

    """

    Rebooter programmet (starter fra toppen) uten å spamme .bat-vinduer,

    fordi start_bat_kun_en_gang() bruker miljøvariabel.

    """

    shutdown_animation()

    try:

        sys.stdout.flush()

    except Exception:

        pass

    os.execv(sys.executable, [sys.executable] + sys.argv)





# ===================== HJELPEFUNKSJONER =====================



def skriv_passord(prompt="Passord: "):

    """

    Leser passord tast-for-tast og skriver ● i stedet for tegn.

    Fungerer i CMD/PowerShell/.bat, ikke i VS Code-terminal.

    """

    print(prompt, end="", flush=True)

    passord = ""

    while True:

        t = msvcrt.getch()

        # Enter

        if t in (b"\r", b"\n"):

            print()

            return passord

        # Backspace

        elif t == b"\x08":

            if len(passord) > 0:

                passord = passord[:-1]

                print("\b \b", end="", flush=True)

        # Ignorer spesialtaster (pil, etc.)

        elif t in (b"\x00", b"\xe0"):

            msvcrt.getch()

            continue

        else:

            try:

                ch = t.decode("utf-8")

            except Exception:

                continue

            passord += ch

            print("●", end="", flush=True)





def rydd_skjerm():

    os.system("cls")





def les_int(prompt, feilmelding="Ugyldig tall, prøv igjen."):

    while True:

        s = input(prompt)

        try:

            return int(s)

        except ValueError:

            print(feilmelding)





# ===================== "DATABASE" I MINNET =====================



brukere = {"admin": "1234"}

notater = {}

saldo = {}





def sørg_for_brukerdata(brukernavn):

    if brukernavn not in notater:

        notater[brukernavn] = []

    if brukernavn not in saldo:

        saldo[brukernavn] = 0





# ===================== INNLOGGING =====================



def login():

    while True:

        brukernavn = input("Tast inn brukernavn: ").strip()



        if brukernavn not in brukere:

            print("Feil brukernavn, prøv igjen.")

            continue



        riktig = brukere[brukernavn]

        passord = ""

        while passord != riktig:

            passord = skriv_passord("Tast inn passord: ")

            if passord != riktig:

                print("Feil passord, prøv igjen!")



        print("Innlogging vellykket. Velkommen,", brukernavn)

        sørg_for_brukerdata(brukernavn)

        return brukernavn





# ===================== FUNKSJONER I MENYEN =====================



def spill_gjett_tallet():

    hemmelig = random.randint(1, 20)

    forsøk = 0

    print("Jeg tenker på et tall mellom 1 og 20. (skriv q for å avslutte)")

    while True:

        g = input("Gjett: ").strip().lower()

        if g == "q":

            print("Avslutter spillet.")

            return

        try:

            tall = int(g)

        except ValueError:

            print("Skriv et tall (eller q for å avslutte).")

            continue



        forsøk += 1

        if tall < hemmelig:

            print("For lavt!")

        elif tall > hemmelig:

            print("For høyt!")

        else:

            print(f"Riktig! Du brukte {forsøk} forsøk.")

            return





def ikke_tomt_og_match(a, b):

    return (a is not None) and (b is not None) and (a.strip() != "") and (a == b)





def endre_passord(brukernavn):

    nåværende = skriv_passord("Skriv nåværende passord: ")

    if nåværende != brukere[brukernavn]:

        print("Feil nåværende passord.")

        return

    nytt1 = skriv_passord("Nytt passord: ")

    nytt2 = skriv_passord("Gjenta nytt passord: ")

    if ikke_tomt_og_match(nytt1, nytt2):

        brukere[brukernavn] = nytt1

        print("Passord oppdatert!")

    else:

        print("Passordene var tomme eller matchet ikke.")





def meny(brukernavn):

    while True:

        print("\n===== MENY =====")

        print("1. Si hei")

        print("2. Si navnet mitt")

        print("3. Logg ut")

        print("4. Lag notat")

        print("5. Se notater")

        print("6. Vis dato og tid")

        print("7. Sett inn penger")

        print("8. Se saldo")

        print("9. Spill: Gjett tallet")

        print("10. Endre passord")

        print("11. Rydd skjermen")

        print("12. Avslutt programmet (shutdown)")

        print("13. Bytt farge/tema")

        print("14. Slå av (reboot / start på nytt)")

        valg = input("Velg (1-14): ").strip()



        if valg == "1":

            print("Hei!")



        elif valg == "2":

            print("Du er logget inn som", brukernavn)



        elif valg == "3":

            print("Du har logget ut.")

            return



        elif valg == "4":

            nytt = input("Skriv notat: ").strip()

            if nytt:

                notater[brukernavn].append(nytt)

                print("Notat lagret!")

            else:

                print("Tomt notat ble ikke lagret.")



        elif valg == "5":

            bruker_notater = notater.get(brukernavn, [])

            if not bruker_notater:

                print("Du har ingen notater enda.")

            else:

                print("Dine notater:")

                for i, n in enumerate(bruker_notater, start=1):

                    print(f"{i}. {n}")



        elif valg == "6":

            nå = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Dato og tid:", nå)



        elif valg == "7":

            beløp = les_int("Hvor mye vil du sette inn? ")

            if beløp <= 0:

                print("Beløpet må være større enn 0.")

            else:

                saldo[brukernavn] += beløp

                print("Innskudd OK. Ny saldo:", saldo[brukernavn])



        elif valg == "8":

            print("Saldo:", saldo.get(brukernavn, 0))



        elif valg == "9":

            spill_gjett_tallet()



        elif valg == "10":

            endre_passord(brukernavn)



        elif valg == "11":

            rydd_skjerm()



        elif valg == "12":

            print("Avslutter programmet...")

            shutdown_animation()

            sys.exit(0)



        elif valg == "13":

            farge_meny()

            rydd_skjerm()



        elif valg == "14":

            print("Rebooter EmilOS...")

            reboot_program()



        else:

            print("Ugyldig valg, prøv igjen.")





# ===================== HOVEDLØKKE =====================



if __name__ == "__main__":

    # FIX: starter .bat kun én gang (hindrer vindus-spam ved reboot)

    start_bat_kun_en_gang()



    # Sett standard farge ved start (kan endres)

    sett_farge(CURRENT_COLOR)



    # Oppstartsskjerm

    while True:

        valg = vent_på_start()

        if valg == "shutdown":

            shutdown_animation()

            sys.exit(0)

        if valg == "colors":

            farge_meny()

            continue

        if valg == "start":

            break



    # Boot-sekvens

    bios_animation()

    boot_animation()



    rydd_skjerm()

    print("Velkommen til Emil sitt mini-OS 👋")



    while True:

        bruker = login()

        meny(bruker)