from taipy import Gui
import pandas as pd

data = {
    "Date": pd.date_range("20-03-23", periods=4, freq="D"),
    
    "Min": [222,419.7,2.7,325.5],
    "Max": [28.6,68.2,666,173.5]
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

page = """
<|text-center|
<|{path}|image|>


<|{title}|hover_text="Hey,Welcome to stock screener"|>


Name of stock:<|{company_name}|input|>

Max-price:<|{company_maxp}|input|>

Min-price:<|{company_minp}|input|>

<|Run stimulation|button|on_action=name|>





<|{title}|hover_text="Hey,Welcome to stimulation"|>
<|{data}|chart|mode=lines|x=Date|y[1]=Min|y[2]=Max|line[1]=dash|color[2]=blue|color[3]=red|>
"""


if __name__ =="__main__":
    app=Gui(page)
    app.run(use_reloader= True)