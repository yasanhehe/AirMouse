import PySimpleGUI as sg


layout = [[sg.Text('１行目です')],
          [sg.Text('２行目です')],
          [sg.Text('３行目です'), sg.Text('これも３行目です')]]

window = sg.Window('sample', layout)

event, values = window.read()
window.close()
