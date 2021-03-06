import time
import curses
import curses.textpad
import threading
import sys
import random
from operator import itemgetter
import pickle
#simple men


def appendHighscore(player = 'DaVe', score = 1238):
	high_scores = [
	('Liz', 100),
    ]
	
	with open('highscores.txt', 'rb') as f:
		high_scores = pickle.load(f)
		for playerf, scoref in high_scores:
			if playerf == player and scoref == score:
				return
	high_scores.append((player, score))
	high_scores = sorted(high_scores,key=itemgetter(1), reverse=True)[:10]

	with open('highscores.txt', 'wb') as f:
		pickle.dump(high_scores, f)
		
def readHighscore():
	global screen2
	# unpickle
	high_scores = []
	
	with open('highscores.txt', 'rb') as f:
		high_scores = pickle.load(f)
		screen2.erase()
		i = 1
		for player, score in high_scores:
			screen2.addstr(5 + i,4, f'{i}: {player}: {score}')
			i += 1
		screen2.refresh()

def thread_function(screen):
    global bstop
    global ch
    global bgameover
    global screen2
    chOld = ch
    while bstop:
    	chOld = ch
    	ch = screen2.getch()
    	if((chOld == ord('a') and ch == ord('d')) or (chOld == ord('d') and ch == ord('a')) or (chOld == ord('w') and ch == ord('s')) or (chOld == ord('s') and ch == ord('w'))):
    		ch = chOld

    	if ch == ord('q'):
    		 break
    	elif ch == ord('g'):
    		ch = chOld
    		genGoodyPos(screen2)
    	elif bgameover:
    		break

bstop = True

def genGoodyPos(screen):
    global gX
    global gY
    rows, cols = screen.getmaxyx()
    gX = random.randint(1, cols-1)#20
    gY = random.randint(1, rows-1)#19
	
def moveSuake(dir, expand=False):
    global suakePos
    global rows
    global cols
    if expand:
    	suakePos.append([suakePos[0][0], suakePos[0][1]])
    
    if len(suakePos) > 1:
    	idx = 0
    	for i, pos in suakePos:
    		if idx < len(suakePos) - 1:
    			suakePos[len(suakePos) - idx - 1][0] = suakePos[len(suakePos) - 2- idx][0]
    			suakePos[len(suakePos) - idx - 1][1] = suakePos[len(suakePos) - 2- idx][1]
    			idx += 1
    			
    if dir == ord('d'):
    	suakePos[0][1] += 1
    elif dir == ord('s'):
    	suakePos[0][0] += 1
    elif dir == ord('w'):
    	suakePos[0][0] -= 1
    elif dir == ord('a'):
    	suakePos[0][1] -= 1
    	
    if suakePos[0][1] <= 0 or suakePos[0][0] <= 0 or suakePos[0][1] >= cols or suakePos[0][0] >= rows:
    	return False
    else:
    	return True
	
def gameboard(window):
    global ch
    global gX
    global gY
    global suakePos
    global rows
    global cols
    global bstop
    global bgameover
    global screen2
    bgameover = False
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    curses.nonl()
    curses.resizeterm(61,65)
    screen2 = screen
    rows, cols = screen.getmaxyx()
    ch = ord('d')
    timeout = 0.25
    goodyChar = '???'#'G' #'???'#'@'
    suakeChar = '???'#''X' #'???'#' '???'
    score = 0
    x = 10
    y = 10
    suakePos = [[10, 10]]
    gX = random.randint(1, cols-1)#20
    gY = random.randint(1, rows-1)#19
    genGoodyPos(screen)
    t = threading.Thread(target=thread_function, args=(screen,))
    t.start()
    starttime = time.time()
    bshowinghs = False
    while True:
    	try:
    		if bshowinghs and ch != ord('q'):
    			continue
    		bexpand = False
    		rows, cols = screen.getmaxyx()
    		if suakePos[0][1] == gX and suakePos[0][0] == gY:
    			score += 100
    			print('\a')
    			genGoodyPos(screen)
    			bexpand = True
    		screen.erase()
    		screen.border(0,0,0,0)
    		screen.addstr(0,4, f'{score}')
    		screen.addstr(0,14, f'{rows}/{cols}')
    		screen.addstr(0,20,f'{len(suakePos)}')
    		timedifOrig = int(time.time() - starttime)
    		timedifsecs = timedifOrig % 60
    		timestr = f'{timedifsecs}'
    		if len(timestr) == 1:
    			timestr = f'0{timestr}'
    			
    		if timedifOrig >= 60:
    			timedifmin = int(timedifOrig / 60)
    			if timedifmin < 10:
    				timestr = f'0{timedifmin}:{timestr}'
    			else:
    				timestr = f'{timedifmin}:{timestr}'
    		else:
    			timestr = f'00:{timestr}'
    			
    		screen.addstr(0,38, f'{timestr}')
    		if not bgameover:
    			for pos in suakePos:
    				screen.addstr(pos[0],pos[1], suakeChar)
    		else:
    			screen.addstr(int(rows / 2), int((cols / 2) - 5), 'GAME OVER!')
    			
    		screen.addstr(gY,gX, goodyChar)
    		time.sleep(timeout)
    		
    		if ch == ord('q'):
    			break
    		elif ch == ord('h') and not bshowinghs:
    			bshowinghs = True
    			readHighscore()
    			time.sleep(5.0)
    		elif ch == curses.KEY_RESIZE:
    			screen.border(0,0,0,0)
    			genGoodyPos(screen)
    		else:
    			if len(suakePos) > 0:
    				x = suakePos[0][1]
    				y = suakePos[0][0]
    			if not moveSuake(ch, bexpand):
    				bgameover = True
    				break
    	finally:
    		screen.refresh()
    appendHighscore('Kim', score)
    readHighscore()


curses.wrapper(gameboard)