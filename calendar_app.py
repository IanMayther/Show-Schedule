import PySimpleGUI as sg

layout = [
    [sg.Text("Hello Moose!")],
    [sg.Button("OK")]
]

#create window
window = sg.Window("Demo", layout, margins=(200, 300))

#create the event loop
while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED():
        break

window.close()