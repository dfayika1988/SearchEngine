

import PySimpleGUI as sg
import os

def search(values, window):
    """Perform a search based on term and type"""
    global results

    results.clear()
    window['-RESULTS-'].update(values=results)
    window['-INFO-'].update(value='Searching for matches...')
    

    for root, _, files in os.walk(values['-PATH-']):
        for file in files:
            if values['-ENDSWITH-'] and file.lower().endswith(values['-TERM-'].lower()):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
            if values['-STARTSWITH-'] and file.lower().startswith(values['-TERM-'].lower()):
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
            if values['-CONTAINS-'] and values['-TERM-'].lower() in file.lower():
                results.append(f'{root}\\{file}'.replace('\\', '/'))
                window['-RESULTS-'].update(results)
    window['-INFO-'].update('Enter a search term and press `Search`')
    sg.PopupOK('Finished!')

def open_file(file_name):

    os.system(file_name)

results = []
sg.change_look_and_feel('Black')
layout = [
    [sg.Text('Search Term', size=(11, 1)), sg.Input('', size=(40, 1), key='-TERM-'), 
     sg.Radio('Contains', group_id='search_type', size=(10, 1), default=True, key='-CONTAINS-'),
     sg.Radio('StartsWith', group_id='search_type', size=(10, 1), key='-STARTSWITH-'),
     sg.Radio('EndsWith', group_id='search_type', size=(10, 1), key='-ENDSWITH-')],
    [sg.Text('Search Path', size=(11, 1)), sg.Input('/..', size=(40, 1), key='-PATH-'),
     sg.FolderBrowse(size=(10, 1), key='-BROWSE-'), 
     sg.Button('Search', size=(10, 1), key='-SEARCH-')],
    [sg.Text('Enter a search term and press `Search`', key='-INFO-')],
    [sg.Listbox(values=results, size=(100, 28), enable_events=True, key='-RESULTS-')]]

window = sg.Window('File Search Engine', layout=layout, finalize=True, return_keyboard_events=True)
window['-RESULTS-'].expand(expand_x=True, expand_y=True)


while True:
    event, values = window.read()
    if event is None:
        break
    if event == '-SEARCH-':
        search(values, window)
    if event == '-RESULTS-':
        file_name = values['-RESULTS-']
        if file_name:
            open_file(file_name[0])
