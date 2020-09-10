from tkinter import *
import tkinter.messagebox as tmsg
import requests, json
from PIL import Image, ImageTk
import random
from math import ceil

def get_symbol(file_name):
    global symbol
    symbol = Image.open(file_name)
    symbol = symbol.resize((150, 150), Image.ANTIALIAS)
    symbol = ImageTk.PhotoImage(symbol)
    img_label['image'] = symbol

def get_weather():
    try:
        api_key = "YOUR API KEY HERE"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = city_field.get()
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        x = response.json()
        print(response, x)
        if x["cod"] != "404":
            label2['text'] = city_field.get().capitalize()
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            main_desc = str(z[0]["main"])
            print(main_desc)
            if main_desc == "Clouds":
                get_symbol("images/cloud.png")
            elif main_desc == "Clear":
                get_symbol("images/clear.png")
            elif main_desc == "Rain":
                get_symbol("images/rain.png")
            elif main_desc == "Mist" or main_desc == "Smoke" or main_desc == "Haze":
                get_symbol("images/mist.png")
            else:
                get_symbol("images/default.png")
            label3['text'] = str(ceil(float(current_temperature) - 273.15)) + u"\u2103"
            label4['text'] = str(weather_description).capitalize()
            label5['text'] = "Humidity: "+ str(current_humidiy) + " %"
            label6['text'] = "ATM Pressure: "+ str(current_pressure) + " hPa"

        elif x["cod"] == "401":
            tmsg.showerror("Error", "API Key Error")
        else:
            tmsg.showerror("Error", "City Not Found \n"
                                    "Please enter valid city name")

            city_field.delete(0, END)


    except ConnectionError:
        tmsg.showerror("Error", "Please Check Your Internet Connection")

    except Exception as e:
        tmsg.showerror("Error", f"Some error occured!\n{e}")

def about():
    tmsg.showinfo("About", "Created by Rahul Sharma\nCopyright © 2020")


def clear_all():
    city_field.delete(0, END)
    temp_field.delete(0, END)
    atm_field.delete(0, END)
    humid_field.delete(0, END)
    desc_field.delete(0, END)
    city_field.focus_set()

def city_field_click(event):
    clist = ["orange","indigo","blue","green","blue","purple"]
    city_field['fg'] = random.choice(clist)


if __name__ == "__main__":
    clr_f = "#3838A4"
    root = Tk()
    root.title("ReWeather")
    root.configure(background="#04046C")
    root.geometry("720x480+320+120")
    root.resizable(0, 0)
    logo_img = Image.open("images/logo.png")
    icon = ImageTk.PhotoImage(logo_img)
    logo_img = logo_img.resize((200, 200), Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(logo_img)
    root.iconphoto(False, icon)


    f = Frame(root, bg="#2A2A96", width=1000, height=110)
    f.place(x=0, y=0)

    headlabel = Label(f, image=logo_img, bg="#2A2A96")
    headlabel.place(x=120, y=10)
    Label(f, text="ReWeather", font="candara 35 bold", fg="white", bg="#2A2A96").place(x=250, y=20)

    f1 = Frame(root, bg=clr_f, width=360, height=500, relief="solid", bd=2)
    f1.place(x=0, y=110)

    f2 = Frame(root, bg=clr_f, width=360, height=500, relief="solid", bd=2)
    f2.place(x=360, y=110)

    label1 = Label(f1, text="Enter City Name:",
                   fg='white', bg=clr_f, font="candara 30 bold")
    label1.place(x=30, y=20)

    city_field = Entry(f1, width=18, font="calibri 25", fg="black", justify="center")
    city_field.place(x=20, y=120, height=60)
    city_field.focus()
    temp_field = Entry(root)
    atm_field = Entry(root)
    humid_field = Entry(root)
    desc_field = Entry(root)
    city_field.bind("<KeyRelease>", city_field_click)

    label2 = Label(f2, text="City",
                   fg='white', bg=clr_f, font="candara 30 bold", relief="ridge", padx=135, width=3, justify="left")
    label2.place(x=8, y=20)

    label3 = Label(f2, text="N/A"+u"\u2103",
                   fg='white', bg=clr_f, font="candara 30 bold")
    label3.place(x=90, y=115)

    symbol = Image.open("images/default.png")
    symbol = symbol.resize((100, 100), Image.ANTIALIAS)
    symbol = ImageTk.PhotoImage(symbol)

    img_label = Label(f2, image=symbol, bg=clr_f)
    img_label.place(x=200, y=100)

    label4 = Label(f2, text="Description",
                   fg='white', bg=clr_f, font="candara 20", relief="ridge", padx=138, pady=4, width=4)
    label4.place(x=8, y=220)

    label5 = Label(f2, text="Humidity: N/A",
                   fg='white', bg=clr_f, font="candara 12 bold")
    label5.place(x=20, y=300)

    label6 = Label(f2, text="Atm Pressure: N/A",
                   fg='white', bg=clr_f, font="candara 12 bold")
    label6.place(x=20, y=320)

    button1 = Button(f1, text="Submit", bg="#0068E5",
                     fg="white", command=get_weather, width=10, height=1, relief="solid", bd=1,
                     font="candara 20 bold")
    button1.place(x=100, y=240)

    button2 = Button(f2, text="About", command=about, relief="solid", fg="white", bg="#0068E5",
                     font="candara 12 bold", width=8, height=1)
    button2.place(x=250, y=302)
    root.mainloop()
