import PySimpleGUI as sg

sg.theme('LightGrey1')

view_frame = [
    [sg.Text("View", justification= 'r', key= '--View--'),sg.Combo(['Month','Week'])]
]

layout = [
    [sg.Frame('Views', view_frame)],
    [sg.Button("OK")]
]

#create window
window = sg.Window("Install Schedule", layout, margins=(300, 200))

#create the event loop
while True:
    event, values = window.read()
    if event == "OK" or event == None:
        break

window.close()