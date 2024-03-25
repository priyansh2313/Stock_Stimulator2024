import socket
from threading import Thread
from taipy.gui import Gui, State, invoke_callback, get_state_id
import pandas as pd

HOST = "127.0.0.1"
PORT = 5050


state_id_list = []

def on_init(state: State):
    state_id = get_state_id(state)
    if (state_id := get_state_id(state)) is not None:
        state_id_list.append(state_id)



def client_handler(gui: Gui, state_id_list: list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, _ = s.accept()
    while True:
        if data := conn.recv(1024):
            print(f"Data received: {data.decode()}")
            if hasattr(gui, "_server") and state_id_list:
                invoke_callback(
                    gui, state_id_list[0], update_received_data, (str(data.decode()),)
                )
        else:
            print("Connection closed")
            break


def update_received_data(state: State, val):
    state.received_data = val  
    tempdata=state.data
    tempdata["Price"][0]=tempdata["Price"][1]
    tempdata["Price"][1]=tempdata["Price"][2]
    tempdata["Price"][2]=tempdata["Price"][3]
    tempdata["Price"][3]= state.receiver_data.split(",")[0]
    state.company_name= state.received_data.split(",")[1]
    print(tempdata)   

data = {
    "Date": pd.date_range("20-03-23", periods=4, freq="D"),
    
    "Price": [222,419.7,2.7,323.5]
   
}    


title=" Stock stimulator by Priyanshu "
path= "logo.png"
company_name="Adani"
company_minp=450
company_maxp=1050


def name(state):
    print("Hey hello everyone")
    print(state.path)
    print(state.company_minp)

    with open("data.txt","w") as f:
        f.write(f"{state.company_name},{state.company_minp},{state.company_maxp}")


received_data = "No data"

md = """
<|text-center|
<|{path}|image|>


<|{title}|hover_text={company_name}|>


Name of stock:<|{company_name}|input|>

Max-price:<|{company_maxp}|input|>

Min-price:<|{company_minp}|input|>

<|Run stimulation|button|on_action=name|>





<|{title}|hover_text="Hey,Welcome to stimulation"|>
<|{data}|chart|mode=lines|x=Date|y[1]=Price|line[1]=dash|>
"""
gui = Gui(page=md)

t = Thread(
    target=client_handler,
    args=(
        gui,
        state_id_list,
    ),
)
t.start()

gui.run(title="Receiver Page")