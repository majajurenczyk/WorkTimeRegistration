import paho.mqtt.client as mqtt
import config as cfg
import database as db
import keyboard

client_sub = mqtt.Client()


def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    # Print message to console.
    print(message_decoded[2] + ", " + "RFID CARD: " +
            message_decoded[0] + " WAS USED ON TERMINAL: " + message_decoded[1])
    # Add to database
    db.add_log(message_decoded[1], message_decoded[0], message_decoded[2])


def connect_to_broker():
    # provide path to certification
    client_sub.tls_set(cfg.CERT)
    # Authenticate
    client_sub.username_pw_set(username=cfg.RECEIVER_USERNAME, password=cfg.RECEIVER_PASSWORD)
    # Connect to the broker.
    client_sub.connect(cfg.BROKER, cfg.PORT)
    # Send message about conenction.
    client_sub.on_message = process_message
    # Starts client and subscribe.
    client_sub.loop_start()
    # Subscribe all clients terminals
    client_sub.subscribe("terminal/#")


def disconnect_from_broker():
    # Disconnet the client.
    client_sub.loop_stop()
    client_sub.disconnect()


def run_receiver():
    print("LISTENING, PRESS [q] TO STOP\n")
    connect_to_broker()
    while True:
        if keyboard.read_key() == "q":
            break
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
