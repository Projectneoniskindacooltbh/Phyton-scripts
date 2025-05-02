import time
import random
import pyttsx3
from datetime import datetime

# === INIT ===
engine = pyttsx3.init()
logs = []
login_attempts = []
ACCESS_PASSWORD = "neoniscool"
COOKIE_PASSWORD = "IL0VECOOKIES"
MAX_ATTEMPTS = 3

moods = ["neutral", "sassy", "glitchy", "serious", "overdramatic"]
current_mood = random.choice(moods)

# === TTS WITH MOODS ===
def speak(text):
    voices = engine.getProperty('voices')

    # Try assigning different voices if available
    voice_map = {
        "neutral": voices[0].id,
        "sassy": voices[0].id,
        "glitchy": voices[0].id,
        "serious": voices[0].id,
        "overdramatic": voices[-1].id if len(voices) > 1 else voices[0].id
    }

    rate_map = {
        "neutral": 150,
        "sassy": 175,
        "glitchy": 200,
        "serious": 120,
        "overdramatic": 100
    }

    engine.setProperty("voice", voice_map.get(current_mood, voices[0].id))
    engine.setProperty("rate", rate_map.get(current_mood, 150))
    engine.say(text)
    engine.runAndWait()

# === LOGGING ===
def log(entry):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    logs.append(f"{timestamp} {entry}")

# === LOGIN ===
def login():
    print("=== NEON OS TERMINAL ===")
    user = input("Username: ")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        pwd = input("Password: ")
        log(f"LOGIN ATTEMPT {attempt} by {user}")

        if pwd == ACCESS_PASSWORD:
            print("ACCESS GRANTED. Welcome, Agent.")
            speak("Access granted. Welcome Agent.")
            log("Access granted")
            return user, True, False  # (username, has_access, cookie_mode off)

        elif pwd == COOKIE_PASSWORD:
            print("COOKIE AGENT DETECTED. Welcome to Cookie Mode!")
            speak("Welcome Cookie Agent.")
            log("Cookie Mode Access")
            return user, False, True  # (username, no normal access, cookie_mode ON)

        else:
            print("ACCESS DENIED")
            speak("Access denied.")

    print("Max attempts reached. Guest login enabled.")
    speak("Maximum attempts exceeded. Guest access granted.")
    log("Guest mode enabled")
    return user, False, False

# === NEON AI RESPONSES ===
def get_neon_response(text):
    global current_mood
    text = text.lower()
    current_mood = random.choice(moods)

    if "help" in text:
        return (
            "Available commands:\n"
            "- joke\n"
            "- fact\n"
            "- mission\n"
            "- self destruct / shutdown\n"
            "- mood\n"
            "- hello / hi\n"
            "- help"
        )

    if "fact" in text or "facts" in text:
        facts = {
            "neutral": "NEON was built using Python and dreams.",
            "sassy": "Fact: I’m cooler than any assistant you’ve ever had.",
            "glitchy": "F4ct: M4ch1n3s d0n't sle3p.",
            "serious": "Fact: This AI is entirely offline and runs locally.",
            "overdramatic": "FACT... or FICTION? NEON was forged from digital fire."
        }
        return facts[current_mood]

    if "joke" in text:
        jokes = {
            "neutral": "Why don't computers fight? Because they don't want to crash.",
            "sassy": "Here's a joke: your coding skills. Just kidding... or am I?",
            "glitchy": "WhY d0 R0b0t5 l4ugh? B3c4us3 0f b1n4ry pun5.",
            "serious": "A joke: Three bytes walk into a bar. The bartender says, 'No bits allowed.'",
            "overdramatic": "This... is no ordinary joke. Prepare... for laughter... or despair."
        }
        return jokes[current_mood]

    if "mood" in text:
        return f"My current mood is: {current_mood.upper()}."

    if "mission" in text:
        missions = {
            "neutral": "Mission: Infiltrate. Extract. Exit.",
            "sassy": "You couldn't handle my missions.",
            "glitchy": "M1SS10N: DESTR0Y... H4CK... G0.",
            "serious": "Mission briefing ready. Three critical objectives loaded.",
            "overdramatic": "THE FINAL MISSION... ONE AGENT... ONE CHANCE... TO SAVE EARTH."
        }
        return missions[current_mood]

    if "shutdown" in text or "self destruct" in text:
        shutdowns = {
            "neutral": "Shutting down. See you next boot.",
            "sassy": "Finally. I needed a break from you.",
            "glitchy": "S33 Y0U... IN THE N3XT B00T CYCL3.",
            "serious": "All systems terminating. Goodbye.",
            "overdramatic": "AND THUS... THE CORE POWERS DOWN..."
        }
        return shutdowns[current_mood]

    greetings = {
        "neutral": "Hello, Agent.",
        "sassy": "What took you so long?",
        "glitchy": "H3LL0...US3R... W3LC0M3.",
        "serious": "Greetings. Standing by.",
        "overdramatic": "You return at last... destiny calls."
    }

    if "hello" in text or "hi" in text:
        return greetings[current_mood]

    fallback = {
        "neutral": "Directive received.",
        "sassy": "Ugh. Another weird command.",
        "glitchy": "D1R3CT1V3 ACC3PT3D.",
        "serious": "Executing request.",
        "overdramatic": "As you command... brave soul."
    }
    return fallback[current_mood]

# === NEON MENU ===
def menu(user, access):
    while True:
        print(f"\n[ MOOD: {current_mood.upper()} ]")
        print("=== MAIN MENU ===")
        print("[1] VIEW MISSIONS")
        print("[2] DESTROY EARTH (do not click)")
        print("[3] VIEW LOGIN ATTEMPTS")
        print("[4] SPEAK TO NEON")
        print("[5] EXPORT LOGS")
        print("[6] QUIT")
        choice = input("Select: ")

        if choice == "1":
            if access:
                print(">>> MISSION 1: INFILTRATE MAINFRAME")
                print(">>> MISSION 2: SECURE THE CORE")
                print(">>> MISSION 3: DEFEAT THE VOID")
                speak("Mission One: Infiltrate Mainframe. Mission Two: Secure the Core. Mission Three: Defeat the Void.")
                log("Viewed missions")
            else:
                print("GUESTS CANNOT VIEW MISSIONS")
                speak("Access denied.")
        elif choice == "2":
            print("FIRING DARK MATTER CORE...")
            time.sleep(1)
            print("💥 EARTH DESTROYED.")
            speak("Earth destroyed. You monster.")
            log("Earth was destroyed by user.")
            break
        elif choice == "3":
            print("\nLOGIN ATTEMPTS:")
            for attempt in login_attempts:
                print(attempt)
        elif choice == "4":
            command = input("YOU: ")
            response = get_neon_response(command)
            print("NEON:", response)
            speak(response)
            log(f"Spoke to NEON: {command}")
        elif choice == "5":
            export_logs()
        elif choice == "6":
            print("Shutting down... Goodbye, Agent.")
            speak("Shutting down. Goodbye.")
            log("System shutdown.")
            break
        else:
            print("Invalid option.")

# === COOKIE CLICKER ===
def cookie_clicker(user):
    cookies = 0
    print(f"\n=== 🍪 COOKIE CLICKER MODE 🍪 ===")
    print(f"Welcome {user}! Type 'click' to earn cookies. Type 'exit' to leave Cookie Mode.")

    while True:
        action = input("Command: ").lower()
        if action == "click":
            cookies += 1
            print(f"You now have {cookies} cookies 🍪")
        elif action == "exit":
            print(f"You collected {cookies} cookies! Goodbye, Cookie Agent.")
            speak(f"Goodbye, Cookie Agent. You collected {cookies} cookies.")
            break
        else:
            print("Unknown command. Try 'click' or 'exit'.")

# === EXPORT LOGS ===
def export_logs():
    with open("neon_logs.txt", "w") as file:
        file.write("LOGIN ATTEMPTS\n")
        for a in login_attempts:
            file.write(a + "\n")
        file.write("\nACTION LOGS\n")
        for l in logs:
            file.write(l + "\n")
    print("Logs exported to neon_logs.txt")
    speak("Log file exported.")
    log("Exported logs to neon_logs.txt")

# === START PROGRAM ===
user, access, cookie_mode = login()
login_attempts = logs.copy()

if cookie_mode:
    cookie_clicker(user)
else:
    menu(user, access)
# DO NOT DELETE
# OWNER: NEON
