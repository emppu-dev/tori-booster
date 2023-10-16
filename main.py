import requests
import random
import time
import datetime
import concurrent.futures
import os
import threading

lahetetty = 0
start_time = time.time()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

clear()

ilmoitus = str(input("Ilmoituksen linkki: "))
threadit = int(input("Threadit: "))

clear()

def boost(session):
    global lahetetty
    response = session.get(ilmoitus)
    if response.status_code == 200:
        lahetetty += 1

with open("useragents.txt", "r") as file:
    useragents = file.read().splitlines()

def worker():
    with requests.Session() as session:
        while True:
            useragent = random.choice(useragents)
            session.headers.update({"User-Agent": useragent})
            boost(session)

def display_lahetetty():
    while True:
        time_elapsed = time.time() - start_time
        lahetetty_rate = lahetetty / time_elapsed if time_elapsed > 0 else 0
        print(f"[Näyttökertoja lähetetty > {lahetetty}] - [Näyttökertoja / Sekuntti > {lahetetty_rate:.2f}]", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    num_threads = threadit
    thread = threading.Thread(target=display_lahetetty)
    thread.daemon = True
    thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(worker)
    
    thread.join()
