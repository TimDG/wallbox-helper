import requests
from bs4 import BeautifulSoup

def get_meter_reading(ip):
    charger_status = "http://" + ip + "/status"
    response = requests.get(charger_status)
    status = response.json()
    return int(status["total_energy"])

def filter_func(tag):
    return tag.has_attr('data-role') and tag['data-role'] == "meter-value-form"

def get_form_action_url(soup):
    form = soup.find(filter_func)
    return form['action']

def submit_meter_reading(session, get_url, reading):
    response = session.get(get_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "_token"})["value"]
    form = soup.find("form", {"id": "meter_reading_form"})
    post_url = get_form_action_url(soup)
    print(post_url)
    if post_url is None:
        return None

    data = {"value": reading, "_token": csrf_token}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = session.post(post_url, data=data, headers=headers)
    if response.status_code == 200:
        print("Meter reading submitted successfully!")
        save_last_reading(reading)
    else:
        print("Failed to submit meter reading.")

def login(username, password):
    url = "https://counter.ev-point.be/login"
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "_token"})["value"]
    data = {"email": username, "password": password, "_token": csrf_token}
    response = session.post(url, data=data)
    if response.status_code == 200:
        print("Logged in successfully!")
        soup = BeautifulSoup(response.text, "html.parser")
        submit_reading_url = soup.find("a", {"class": "btn-primary"})["href"]
        return session, submit_reading_url
    else:
        print("Failed to log in.")
        return None, None

def save_last_reading(reading):
    with open("last_reading.txt", "w") as file:
        file.write(str(reading))

def load_last_reading():
    try:
        with open("last_reading.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None

if __name__ == '__main__':
    wallbox_ip = '<WALLBOX IP ADDRESS>'
    username = '<EVCOUNTER USERNAME>'
    password = '<EVCOUNTER PASSWORD>'

    reading = get_meter_reading(wallbox_ip)
    last_reading = load_last_reading()

    if last_reading is not None and reading == last_reading:
        print("Meter reading is the same as the last submitted reading.")
        return

    session, new_reading_url = login(username, password)
    if session and new_reading_url:
        submit_meter_reading(session, new_reading_url, reading)
