import os
import sys
import time
import random
import tty
import termios
import datetime

# ===================== MAC HELPERS =====================

def clear():
    os.system("clear")

def get_key():
    """
    macOS alternativ til msvcrt.getch()
    Leser EN tast uten enter.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# ===================== COLORS (ANSI FOR MAC) =====================

THEMES = [
    ("Standard (hvit/svart)", "\033[97;40m"),
    ("Hacker (grønn/svart)", "\033[92;40m"),
    ("Mac Aqua (cyan/svart)", "\033[96;40m"),
    ("Gul (gul/svart)", "\033[93;40m"),
    ("Rød (rød/svart)", "\033[91;40m"),
    ("Lilla (magenta/svart)", "\033[95;40m"),
]

CURRENT_THEME = "\033[97;40m"
RESET = "\033[0m"

def colorize(text):
    return CURRENT_THEME + text + RESET

def choose_theme():
    global CURRENT_THEME
    clear()
    print(colorize("===== VELG TEMA =====\n"))
    for i,(name,code) in enumerate(THEMES,1):
        print(colorize(f"{i}. {name}"))
    print(colorize("\n0. Tilbake"))

    while True:
        choice = input(colorize("Velg tema (0-6): ")).strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(THEMES):
            CURRENT_THEME = THEMES[int(choice)-1][1]
            clear()
            print(colorize("Tema endret!"))
            time.sleep(0.7)
            return
        print(colorize("Ugyldig valg."))

# ===================== APPLE BOOT SEQUENCE =====================

APPLE = """
          
"""

def boot_wait_screen():
    clear()
    print(colorize("Trykk MELLOMROM for å starte EmilOS..."))
    print(colorize("(S = Skru av   |   F = Farger)"))
    while True:
        k = get_key()
        if k == " ":
            return "start"
        if k.lower() == "s":
            return "shutdown"
        if k.lower() == "f":
            return "colors"

def apple_boot_logo():
    clear()
    print(colorize(APPLE))
    time.sleep(0.6)

def apple_progress_bar():
    clear()
    print(colorize(APPLE))
    bar = ""
    for i in range(20):
        bar += "█"
        clear()
        print(colorize(APPLE))
        print(colorize(bar))
        time.sleep(0.10)

def shutdown_animation():
    clear()
    print(colorize("[●] Lukker programmer...")); time.sleep(0.5)
    print(colorize("[●] Lagrer tilstand...")); time.sleep(0.5)
    print(colorize("[✓] Systemet er klart til å slå av.")); time.sleep(0.5)
    print(colorize("\nSlår av...")); time.sleep(1)
    clear()
    sys.exit()

def reboot_emilos():
    clear()
    print(colorize("Starter EmilOS på nytt..."))
    time.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv) 

# ===================== LOGIN SYSTEM =====================

users = {"admin": "1234"}
notes = {}
saldo = {}

def ensure_user_data(u):
    notes.setdefault(u, [])
    saldo.setdefault(u, 0)

def get_password(prompt="Passord: "):
    print(colorize(prompt), end="", flush=True)
    pw = ""
    while True:
        k = get_key()
        if k == "\n" or k == "\r":
            print()
            return pw
        elif k == "\x7f":  # backspace
            if pw:
                pw = pw[:-1]
                print("\b \b", end="", flush=True)
        else:
            pw += k
            print("●", end="", flush=True)

def login():
    while True:
        u = input(colorize("Brukernavn: ")).strip()
        if u not in users:
            print(colorize("Feil brukernavn!"))
            continue

        pw = get_password(colorize("Passord: "))
        if pw == users[u]:
            print(colorize(f"Velkommen {u}!"))
            ensure_user_data(u)
            return u
        else:
            print(colorize("Feil passord!"))

# ===================== FUNKSJONER =====================

def menu(user):
    while True:
        print(colorize("\n===== MENY ====="))
        print(colorize("1. Si hei"))
        print(colorize("2. Vis brukernavn"))
        print(colorize("3. Logg ut"))
        print(colorize("4. Lag notat"))
        print(colorize("5. Se notater"))
        print(colorize("6. Vis dato/tid"))
        print(colorize("7. Sett inn penger"))
        print(colorize("8. Vis saldo"))
        print(colorize("9. Spill: Gjett tallet"))
        print(colorize("10. Endre passord"))
        print(colorize("11. Rydd skjermen"))
        print(colorize("12. Slå av"))
        print(colorize("13. Bytt tema"))
        print(colorize("14. Restart EmilOS"))
        choice = input(colorize("Velg (1-14): ")).strip()

        if choice == "1":
            print(colorize("Hei!"))

        elif choice == "2":
            print(colorize(f"Du er logget inn som {user}"))

        elif choice == "3":
            return

        elif choice == "4":
            note = input(colorize("Skriv notat: "))
            notes[user].append(note)
            print(colorize("Notat lagret!"))

        elif choice == "5":
            if not notes[user]:
                print(colorize("Ingen notater."))
            else:
                for i,n in enumerate(notes[user],1):
                    print(colorize(f"{i}. {n}"))

        elif choice == "6":
            print(colorize(str(datetime.datetime.now())))

        elif choice == "7":
            try:
                amount = int(input(colorize("Beløp: ")))
                if amount > 0:
                    saldo[user] += amount
                print(colorize(f"Ny saldo: {saldo[user]}"))
            except:
                print(colorize("Ugyldig tall."))

        elif choice == "8":
            print(colorize(f"Saldo: {saldo[user]}"))

        elif choice == "9":
            guess_game()

        elif choice == "10":
            change_pw(user)

        elif choice == "11":
            clear()

        elif choice == "12":
            shutdown_animation()

        elif choice == "13":
            choose_theme()

        elif choice == "14":
            reboot_emilos()

        else:
            print(colorize("Ugyldig valg."))

def guess_game():
    number = random.randint(1,20)
    print(colorize("Gjett tallet 1–20. (q for å avslutte)"))
    while True:
        guess = input(colorize("Gjett: ")).strip().lower()
        if guess == "q":
            return
        try:
            g = int(guess)
            if g < number:
                print(colorize("For lavt!"))
            elif g > number:
                print(colorize("For høyt!"))
            else:
                print(colorize("Riktig!"))
                return
        except:
            print(colorize("Skriv et tall."))

def change_pw(user):
    old = get_password("Nåværende passord: ")
    if old != users[user]:
        print(colorize("Feil passord."))
        return
    new1 = get_password("Nytt passord: ")
    new2 = get_password("Gjenta nytt passord: ")
    if new1 == new2 and new1.strip():
        users[user] = new1
        print(colorize("Passord endret!"))
    else:
        print(colorize("Feil – prøv igjen."))

# ===================== MAIN =====================

if __name__ == "__main__":
    clear()

    while True:
        action = boot_wait_screen()

        if action == "shutdown":
            shutdown_animation()

        if action == "colors":
            choose_theme()
            continue

        if action == "start":
            break

    apple_boot_logo()
    apple_progress_bar()

    clear()
    print(colorize("Velkommen til EmilOS "))
    print()

    while True:
        user = login()
        menu(user)
