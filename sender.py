import paho.mqtt.client as mqtt
import config as cfg
import database as db
import keyboard
from time import sleep
import datetime

client_pub = mqtt.Client()


def scan_card(id_card, id_term):
    client_pub.publish("terminal/" + str(id_term), id_card + "." + str(id_term) + "." +
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)


def connect_to_broker():
    # provide path to certification
    client_pub.tls_set(cfg.CERT)
    # Authenticate
    client_pub.username_pw_set(username=cfg.SENDER_USERNAME, password=cfg.SENDER_PASSWORD)
    # Connect to the broker.
    client_pub.connect(cfg.BROKER, cfg.PORT)
    print("CONNECTED")


def disconnect_from_broker():
    # Disconnet the client.
    client_pub.disconnect()
    print("DISCONNECTED")


def simulate_scan():
    print("PRESS [space] TO SIMULATE SCAN")
    print("PRESS [esc] TO STOP\n")
    while True:
        if keyboard.read_key() == "space":
            sleep(0.01)
            if keyboard.read_key() == "space":
                card_term = db.rfid_scan_random()
                if card_term:
                    scan_card(card_term[0], card_term[1])
                    print("SCAN REGISTERED")
        elif keyboard.read_key() == "esc":
            break


def run_sender():
    connect_to_broker()
    simulate_scan()
    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
