import PySimpleGUI as sg

class WarningWindow:

	def __init__(self):
		layout = [
				[sg.Text('Warning, this tool should not be used as a sole decider on whether to trade an asset or not. By clicking OK, you agree that any party involved in the making of this program is not liable for any losses or impacts that occur due to the use of the product',size=(45,5))],
				[sg.Checkbox('Do you agree with the statement above?',key='check')],
				[sg.Button('Begin',key='agree')],
				[sg.Button('Quit',key='quit')]
		]
		sg.theme('Reddit')
		window = sg.Window("The Price of Free Speech Conditions",layout)
		while True:
			event,values = window.read()
			print(values['check'])
			if event == sg.WIN_CLOSED or event == 'quit': exit()
			elif event == 'agree' and values['check'] == True: 
				if values['check']:
					window.close()
					break


