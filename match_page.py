import requests
import json
import base64
import textwrap
import random
import time
import tkinter as tk
from functools import partial
import os

icon = "Trivia/assets/the_icon.ico"
introd = "Trivia/introduction.txt"
path_intro = os.path.abspath(introd)
path_icon = os.path.abspath(icon)

# WINDOWS AND GLOBALS

root = tk.Tk()
root.title("Trivia by @robert_rotaru18")
root.iconbitmap(path_icon)
root.geometry("500x250")
root.resizable = False

mainFrame = tk.Frame(root)
mainFrame.place(relheight = 0.8, relwidth = 0.8, relx = 0.5, rely = 0.1, anchor = "n")

choicesFrame = tk.Frame(mainFrame)

myLabel = tk.Label(mainFrame)

choices = [[
	tk.Button(choicesFrame, font = ('helvetica', '10')),
	tk.Button(choicesFrame, font = ('helvetica', '10')),
	tk.Button(choicesFrame, font = ('helvetica', '10')),
	tk.Button(choicesFrame, font = ('helvetica', '10'))
] for i in range(11)]

for i in range(11):
	choices[i][0].place_forget()
	choices[i][1].place_forget()
	choices[i][2].place_forget()
	choices[i][3].place_forget()

orig_color = choices[0][0]["bg"]

difficulty = ""
counter = -1

correct_ans = []
ans = []
points = 0

selected = 5

score = tk.Label(mainFrame)

# EVALUATE ANSWER

def evaluateAnswer(c, number):
	# GET UNSELECTED AND SELECTED ANSWER
	global selected, points, correct_ans, ans, counter, choices
	if selected < 5:
		choices[counter][selected].configure(bg = orig_color)
		choices[counter][selected].configure(state = "normal")
		if chr(ord("A") + selected) == correct_ans[counter]:
			points -= 1
	choices[counter][number]['bg'] = '#c7ced9'
	choices[counter][number]['fg'] = '#000000'
	choices[counter][number]['state'] = 'disabled'
	selected = number

	# PUT THE ANSWER
	if len(ans) - 1 < counter:
		ans.append(c)
	else:
		ans[counter] = c

	# CHECK WHETHER IS CORRECT OR NOT
	if c == correct_ans[counter]:
		points += 1

# COLOR ANSWERS
def colorAnswers(counter):
	global ans, choices, correct_ans
	index = -1
	if counter >= 0:
		if ans[counter] != correct_ans:
			index = ord(ans[counter]) - ord("A")
		index_of_ca = ord(correct_ans[counter]) - ord("A")
		for i in range(4):
			if i == index_of_ca:
				choices[counter][i].configure(bg = "#00ad23")
			elif i == index:
				choices[counter][i].configure(bg = "#ff4242")
			else:
				choices[counter][i].configure(bg = orig_color)
			choices[counter][i].update()

# MOVE TO PREVIOUS OR NEXT QUESTION
def prevQuestion():
	global counter
	nextButton.place(relx = 0.9, rely = 0.9)
	backButton.place(relx = 0.8, rely = 0.9)
	if counter > 0:
		global _question, choicesFrame, choices, mainFrame
		_question[counter].place_forget()
		for i in range(4):
			choices[counter][i].place_forget()

		counter -= 1
		for i in range(4):
			choices[counter][i]["bg"] = orig_color
			choices[counter][i]["state"] = "normal"
			choices[counter][i].configure(command = lambda : print(1))
		
		colorAnswers(counter)
		_question[counter].place(relx = 0.5, rely = 0.05, anchor = "n")
		choices[counter][0].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0)
		choices[counter][1].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0)
		choices[counter][2].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0.5)
		choices[counter][3].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0.5)

		choicesFrame.config(bd = 5, relief = "sunken")
		choicesFrame.place(relheight = 0.48, relwidth = 0.8, relx = 0.5, rely = 0.42, anchor = "n")

		score.place_forget()
		choicesFrame.update()
		if counter == 0:
			backButton.place_forget()
	else:
		backButton.place_forget()

def nextQuestion():
	global counter
	nextButton.place(relx = 0.9, rely = 0.9)
	backButton.place(relx = 0.8, rely = 0.9)
	if counter < 9:
		global _question, choicesFrame, choices, mainFrame
		_question[counter].place_forget()
		for i in range(4):
			choices[counter][i].place_forget()

		counter += 1
		for i in range(4):
			choices[counter][i]["bg"] = orig_color
			choices[counter][i]["state"] = "normal"
			choices[counter][i].configure(command = lambda : print(1))
		colorAnswers(counter)

		_question[counter].place(relx = 0.5, rely = 0.05, anchor = "n")
		choices[counter][0].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0)
		choices[counter][1].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0)
		choices[counter][2].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0.5)
		choices[counter][3].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0.5)
		
		choicesFrame.config(bd = 5, relief = "sunken")
		choicesFrame.place(relheight = 0.48, relwidth = 0.8, relx = 0.5, rely = 0.42, anchor = "n")

		score.place_forget()
		choicesFrame.update()
		
		if counter == 9:
			nextButton.place_forget()
	else:
		nextButton.place_forget()

# MAKE CHOICES
def getAnswers():
	global selected, correct_ans, choices, counter
	selected = 5
	Wrap = textwrap.TextWrapper(width = 20)
	occur = {
		0 : 0,
		1 : 0,
		2 : 0,
		3 : 0
	}

	c_answer = questions[counter]['correct_answer']
	c_answer = base64.b64decode(c_answer)
	c_answer = c_answer.decode("ascii", errors = "ignore")
	word_list = Wrap.wrap(text = c_answer)
	c_answer = ""
	for w in word_list:
		c_answer = c_answer + w + '\n'

	list_of_ans = questions[counter]['incorrect_answers']

	number = int((random.randint(0, 4) + random.randint(4, 101)) % 4)
	occur[number] = 1

	global correct_ans
	correct_ans.append(chr(ord("A") + number))
	choices[counter][number]["text"] = f"{correct_ans[len(correct_ans) - 1]}. {c_answer}"
	choices[counter][number].configure(command = partial(evaluateAnswer, correct_ans[len(correct_ans) - 1], number))
	choicesFrame.update()

	for ans in list_of_ans:
		ans = base64.b64decode(ans)
		ans = ans.decode("ascii", errors = "ignore")
		word_list = Wrap.wrap(text = ans)
		newAns = ""
		for w in word_list:
			newAns = newAns + w + '\n'

		number = int((random.randint(0, 4) + random.randint(4, 101)) % 4)
		while occur[number] == 1:
			number = int((random.randint(0, 4) + random.randint(4, 101)) % 4)
		occur[number] = 1

		noOrder = chr(ord('A') + number)
		choices[counter][number]["text"] = f"{noOrder}. {newAns}"
		choices[counter][number].configure(command = partial(evaluateAnswer, noOrder, number))
		choicesFrame.update()

# COUNT_DOWN SCREEN
def update_label(txt):
	global myLabel
	myLabel["text"] = txt
	myLabel["font"] = ("helvetica", "40")
	myLabel.update()

def count_down():
	myLabel.place(relx = 0.5, rely = 0.5, anchor = "center")
	update_label("3")
	myLabel.after(1000)
	update_label("2")
	myLabel.after(1000)
	update_label("1")
	myLabel.after(1000)
	update_label("Start!")
	myLabel.after(1000)

	myLabel.destroy()
	createNewQuestion()
	
# CHOOSE DIFFICULTY
def _easy():
	global difficulty, dif, easy, medium, hard
	difficulty = "easy"
	easy.destroy()
	medium.destroy()
	hard.destroy()
	dif.destroy()

	# START THE COUNT-DOWN
	count_down()

def _medium():
	global difficulty, dif, easy, medium, hard
	difficulty = "medium"
	easy.destroy()
	medium.destroy()
	hard.destroy()
	dif.destroy()

	# START THE COUNT-DOWN
	count_down()

def _hard():
	global difficulty, dif, easy, medium, hard
	difficulty = "hard"
	easy.destroy()
	medium.destroy()
	hard.destroy()
	dif.destroy()

	# START THE COUNT-DOWN
	count_down()

# MAKE THE QUESTION

def getQuestion(questions):
	global counter
	question = questions[counter]['question']
	while len(question) % 4 != 0:
		question = question + "="
	question = base64.b64decode(question)
	question = question.decode("ascii", errors = "ignore")
	return question

def createNewQuestion():
	# SAVE DATA
	global counter, choices, choicesFrame, _question, nextButton, backButton

	try:
		choicesFrame.config(bd = 5, relief = "sunken")
		choicesFrame.place(relheight = 0.48, relwidth = 0.8, relx = 0.5, rely = 0.42, anchor = "n")
	except:
		choicesFrame.destroy()

	# MAKE QUESTION
	if counter < 9:
		counter += 1
		if counter > 0:
			_question[counter - 1].place_forget()
			for i in range(4):
				choices[counter - 1][i].place_forget()

		_question[counter].place(relx = 0.5, rely = 0.05, anchor = "n")
		choices[counter][0].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0)
		choices[counter][1].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0)
		choices[counter][2].place(relheight = 0.5, relwidth = 0.5, relx = 0, rely = 0.5)
		choices[counter][3].place(relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0.5)

		_text = getQuestion(questions)
		word_list = wrapper.wrap(text = _text)
		newText = ""
		for row in word_list:
			newText = newText + row + "\n"
		_question[counter].configure(text = newText)
		_question[counter].update()
		nextButton.configure(text = "Next", padx = 0, pady = 0, command = createNewQuestion)
		nextButton.place(relx = 0.9, rely = 0.9)
		nextButton.update()
		getAnswers()
	else:
		counter += 1
		_question[counter - 1].place_forget()
		for i in range(4):
			choices[counter - 1][i].place_forget()
		_question[counter].place(relx = 0.5, rely = 0.05, anchor = "n")
		_question[counter].configure(text = "You have scored:", font = ('helvetica', '18'))
		_question[counter].update()
		choicesFrame.place_forget()
		global points, score
		score.configure(text = "{}/10".format(points), font = ('helvetica', '36'))
		score.place(relx = 0.5, rely = 0.5, anchor = 'center')
		
		#global backButton
		backButton.configure(command = partial(prevQuestion))
		backButton.place(relx = 0.8, rely = 0.9)
		#global nextButton
		nextButton.configure(command = partial(nextQuestion))
		nextButton.place_forget()

# START THE GAME
def startGame():
	global intro, play_button, dif
	intro.destroy()
	play_button.destroy()

	easy.place(relheight = 0.25, relwidth = 0.25, relx = 0.075, rely = 0.5)
	medium.place(relheight = 0.25, relwidth = 0.25, relx = 0.375, rely = 0.5)
	hard.place(relheight = 0.25, relwidth = 0.25, relx = 0.675, rely = 0.5)

	dif.place(relx = 0.5, rely = 0.1, anchor = "n")


# WELCOME PAGE
f = open(path_intro, "r")
text = f.read()
intro = tk.Label(mainFrame, text = text, justify = "center", font = ("times", "12"))
intro.place(relx = 0.5, rely = 0.05, anchor = "n")

play_button = tk.Button(mainFrame, text = "Play!", command = startGame)
play_button.place(relheight = 0.18, relwidth = 0.18, relx = 0.5, rely = 0.7, anchor = "center")

# WRAPPER

wrapper = textwrap.TextWrapper(width = 50)

# API

response = requests.get("https://opentdb.com/api.php?amount=10&difficulty={}&type=multiple&encode=base64".format(difficulty))
questions = response.json()['results']

# DESIGN

_question = [tk.Label(mainFrame) for _ in range(11)]
for i in range(11):
	_question[i].place_forget()

nextButton = tk.Button(mainFrame)
backButton = tk.Button(mainFrame, text = "Back", padx = 0, pady = 0, command = lambda : print(1))
backButton.place(relx = 0.85, rely = 0.9)
backButton.place_forget()

easy = tk.Button(mainFrame, text = "Easy", command = _easy)
medium = tk.Button(mainFrame, text = "Medium", command = _medium)
hard = tk.Button(mainFrame, text = "Hard", command = _hard)

dif = tk.Label(mainFrame, text = "Choose your difficulty!", justify = "center", font = ("helvetica", "18", "bold"))

root.mainloop()