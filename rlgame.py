import pygame, sys, random
from pygame.locals import *

g=open('replay.txt','w')

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((1200,700),0,32)
pygame.display.set_caption('OpenCollege AI Class')

# set up the colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
GRAY = (180,180,180)


FPS = 40 # frames per second setting
fpsClock = pygame.time.Clock()

BASICFONTSIZE = 16
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

player=[]
archieve=[] # history archieve, all player state and action saving
message=[] # display message(ex:kill)

# user character
class user:
	# character status
	name=''
	alive=False
	sit=False
	hp=100
	mhp=100
	sp=100
	msp=100
	atk=5
	kill=0

	killercandidate=[] # if player dead, use to give bonus
	killer=-1 # killer`s name. it got kill bonus
	x=0
	y=0
	direction=0 # ini=0, up=1, down=2, left=3, right=4
	action=0 # no action=0, move up=1, move down=2, move left=3, move right=4
	# attack=5, sit=6, stand=7, heal=8
	color=(0,0,0)
	def generate(self,chaname):
		self.name=chaname
		self.alive=True
		self.hp = 100
		self.mhp = 100
		self.sp = 100
		self.msp = 100
		self.atk = 5
		self.kill = 0
		self.direction=random.randrange(1,5)

		while True:
			self.x=random.randrange(0,30)
			self.y=random.randrange(0,30)
			if collision()==0: break

		while True:
			self.color=(random.randrange(0,256),random.randrange(0,256),random.randrange(0,256))
			print(self.color)
			if colorcollision()==0: break


	def killbonus(self):
		self.hp+=10
		self.mhp+=20
		self.sp+=10
		self.msp+=20
		self.atk+=1


def colorcollision():
	distance=0
	distance1=0
	# use to determine chracter color collision
	for i in range(len(player)):
		distance1=abs(player[i].color[0]-GRAY[0])+abs(player[i].color[1]-GRAY[1])+abs(player[i].color[2]-GRAY[2])
		if distance1<=100:
			return 1
	for i in range(len(player)):
		for j in range(i):
			distance=abs(player[i].color[0]-player[j].color[0])+abs(player[i].color[1]-player[j].color[1])+abs(player[i].color[2]-player[j].color[2])
			if distance<=100:
				return 1
	return 0

def collision():
	#determine collision to wall
	for i in range(len(player)):
		if player[i].x<0: return 1
		if player[i].x>=30: return 1
		if player[i].y<0: return 1
		if player[i].y>=30: return 1

	# use to determine character collision to other character
	for i in range(len(player)):
		for j in range(i):
			if player[i].alive == True and player[j].alive == True and player[i].x == player[j].x and player[i].y == player[j].y:
				return 1
	return 0

def generatecharacter():

	for i in range(25):
		temp=user()
		player.append(temp)
		player[i].generate('player'+str(i))
		print('number: ',i)
		print(player[i].name)
		print(player[i].hp)
		print(player[i].mhp)
		print(player[i].sp)
		print(player[i].msp)
		print(player[i].atk)
		print(player[i].x)
		print(player[i].y)

generatecharacter()


def drawmap():
	for i in range(30):
		for j in range(30):
			pygame.draw.rect(DISPLAYSURF, GRAY, (i*20+50,j*20+50,16,16))

	# must be refine : from rec to tri, use unique color
	for i in range(25):
		if player[i].alive==True:
			#pygame.draw.rect(DISPLAYSURF,player[i].color,(player[i].x*20+50,player[i].y*20+50,16,16))
			if player[i].direction==1: # UP
				pygame.draw.polygon(DISPLAYSURF,player[i].color,((player[i].x*20+50,player[i].y*20+66),(player[i].x*20+66,player[i].y*20+66),(player[i].x*20+58,player[i].y*20+50)))
			elif player[i].direction==2: # DOWN
				pygame.draw.polygon(DISPLAYSURF,player[i].color,((player[i].x*20+50,player[i].y*20+50),(player[i].x*20+66,player[i].y*20+50),(player[i].x*20+58,player[i].y*20+66)))
			elif player[i].direction==3: # LEFT
				pygame.draw.polygon(DISPLAYSURF,player[i].color,((player[i].x*20+50,player[i].y*20+58),(player[i].x*20+66,player[i].y*20+50),(player[i].x*20+66,player[i].y*20+66)))
			elif player[i].direction==4: # RIGHT
				pygame.draw.polygon(DISPLAYSURF,player[i].color,((player[i].x*20+50,player[i].y*20+50),(player[i].x*20+50,player[i].y*20+66),(player[i].x*20+66,player[i].y*20+58)))



	textSurf = BASICFONT.render('NAME', True, (255,255,255))
	textRect = textSurf.get_rect()
	textRect.center = 780, 40
	DISPLAYSURF.blit(textSurf,textRect)

	textSurf = BASICFONT.render('     HP       SP         ATK    KILL', True, (255,255,255))
	textRect = textSurf.get_rect()
	textRect.center = 980, 40
	DISPLAYSURF.blit(textSurf,textRect)

	
	for i in range(25):
		if player[i].alive==True:
			pygame.draw.rect(DISPLAYSURF,player[i].color,(700,i*20+60,16,16))

			# display character status
			text = str(player[i].hp).rjust(3)+'/'+str(player[i].mhp).rjust(3)+'  '+str(player[i].sp).rjust(3)+'/'+str(player[i].msp).rjust(3)+'        '+str(player[i].atk).rjust(2)+'        '+str(player[i].kill).rjust(2)
			textSurf = BASICFONT.render(text, True, (255,255,255))
			textRect = textSurf.get_rect()
			textRect.center = 970, i*20+68
			DISPLAYSURF.blit(textSurf,textRect)


	for i in range(25):
		if player[i].alive==True:
			# display player name
			text=player[i].name
			textSurf = BASICFONT.render(text, True, (255,255,255))
			textRect = textSurf.get_rect()
			textRect.center = 780, i*20+68
			DISPLAYSURF.blit(textSurf,textRect)


# this is space for player`s function
def player0():
	near=[]
	target=0
	for i in range(len(player)):
		dis=abs(player[i].x-player[0].x)+abs(player[i].y-player[0].y)
		near.append(dis)

	shortest=100
	for i in range(len(player)):
		if i==0: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[0].x==player[target].x and player[0].y-1==player[target].y:
			if player[0].direction==1 and player[0].sp>=5:
				return 5
			elif player[0].direction==1:
				return 0
			else:
				return 1				
		elif player[0].x==player[target].x and player[0].y+1==player[target].y:
			if player[0].direction==2 and player[0].sp>=5:
				return 5
			elif player[0].direction==2:
				return 0
			else:
				return 2
		elif player[0].x-1==player[target].x and player[0].y==player[target].y:
			if player[0].direction==3 and player[0].sp>=5:
				return 5
			elif player[0].direction==3:
				return 0
			else:
				return 3
		elif player[0].x+1==player[target].x and player[0].y==player[target].y:
			if player[0].direction==4 and player[0].sp>=5:
				return 5
			elif player[0].direction==4:
				return 0
			else:
				return 4
	elif player[0].sp<=30:
		return 0
	else:
		dis1=abs(player[0].x-player[target].x)
		dis2=abs(player[0].y-player[target].y)

		if dis1>dis2:
			if player[0].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[0].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1

def player1():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[1].x)+abs(player[i].y-player[1].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==1: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[1].x==player[target].x and player[1].y-1==player[target].y:
			if player[1].direction==1 and player[1].sp>=5:
				return 5
			elif player[1].direction==1:
				return 0
			else:
				return 1				
		elif player[1].x==player[target].x and player[1].y+1==player[target].y:
			if player[1].direction==2 and player[1].sp>=5:
				return 5
			elif player[1].direction==2:
				return 0
			else:
				return 2
		elif player[1].x-1==player[target].x and player[1].y==player[target].y:
			if player[1].direction==3 and player[1].sp>=5:
				return 5
			elif player[1].direction==3:
				return 0
			else:
				return 3
		elif player[1].x+1==player[target].x and player[1].y==player[target].y:
			if player[1].direction==4 and player[1].sp>=5:
				return 5
			elif player[1].direction==4:
				return 0
			else:
				return 4
	elif player[1].sp<=30:
		return 0
	else:
		dis1=abs(player[1].x-player[target].x)
		dis2=abs(player[1].y-player[target].y)


		if dis1>dis2:
			if player[1].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[1].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player2():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[2].x)+abs(player[i].y-player[2].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==2: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[2].x==player[target].x and player[2].y-1==player[target].y:
			if player[2].direction==1 and player[2].sp>=5:
				return 5
			elif player[2].direction==1:
				return 0
			else:
				return 1				
		elif player[2].x==player[target].x and player[2].y+1==player[target].y:
			if player[2].direction==2 and player[2].sp>=5:
				return 5
			elif player[2].direction==2:
				return 0
			else:
				return 2
		elif player[2].x-1==player[target].x and player[2].y==player[target].y:
			if player[2].direction==3 and player[2].sp>=5:
				return 5
			elif player[2].direction==3:
				return 0
			else:
				return 3
		elif player[2].x+1==player[target].x and player[2].y==player[target].y:
			if player[2].direction==4 and player[2].sp>=5:
				return 5
			elif player[2].direction==4:
				return 0
			else:
				return 4
	elif player[2].sp<=30:
		return 0
	else:
		dis1=abs(player[2].x-player[target].x)
		dis2=abs(player[2].y-player[target].y)

		if dis1>dis2:
			if player[2].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[2].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player3():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[3].x)+abs(player[i].y-player[3].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==3: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[3].x==player[target].x and player[3].y-1==player[target].y:
			if player[3].direction==1 and player[3].sp>=5:
				return 5
			elif player[3].direction==1:
				return 0
			else:
				return 1				
		elif player[3].x==player[target].x and player[3].y+1==player[target].y:
			if player[3].direction==2 and player[3].sp>=5:
				return 5
			elif player[3].direction==2:
				return 0
			else:
				return 2
		elif player[3].x-1==player[target].x and player[3].y==player[target].y:
			if player[3].direction==3 and player[3].sp>=5:
				return 5
			elif player[3].direction==3:
				return 0
			else:
				return 3
		elif player[3].x+1==player[target].x and player[3].y==player[target].y:
			if player[3].direction==4 and player[3].sp>=5:
				return 5
			elif player[3].direction==4:
				return 0
			else:
				return 4
	elif player[3].sp<=30:
		return 0
	else:
		dis1=abs(player[3].x-player[target].x)
		dis2=abs(player[3].y-player[target].y)

		if dis1>dis2:
			if player[3].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[3].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1


def player4():
	near=[]
	target=0
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[4].x)+abs(player[i].y-player[4].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==4: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[4].x==player[target].x and player[4].y-1==player[target].y:
			if player[4].direction==1 and player[4].sp>=5:
				return 5
			elif player[4].direction==1:
				return 0
			else:
				return 1				
		elif player[4].x==player[target].x and player[4].y+1==player[target].y:
			if player[4].direction==2 and player[4].sp>=5:
				return 5
			elif player[4].direction==2:
				return 0
			else:
				return 2
		elif player[4].x-1==player[target].x and player[4].y==player[target].y:
			if player[4].direction==3 and player[4].sp>=5:
				return 5
			elif player[4].direction==3:
				return 0
			else:
				return 3
		elif player[4].x+1==player[target].x and player[4].y==player[target].y:
			if player[4].direction==4 and player[4].sp>=5:
				return 5
			elif player[4].direction==4:
				return 0
			else:
				return 4
	elif player[4].sp<=30:
		return 0
	else:
		dis1=abs(player[4].x-player[target].x)
		dis2=abs(player[4].y-player[target].y)

		if dis1>dis2:
			if player[4].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[4].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1




	return 1


def player5():
	near=[]
	target=0
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[5].x)+abs(player[i].y-player[5].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==5: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[5].x==player[target].x and player[5].y-1==player[target].y:
			if player[5].direction==1 and player[5].sp>=5:
				return 5
			elif player[5].direction==1:
				return 0
			else:
				return 1				
		elif player[5].x==player[target].x and player[5].y+1==player[target].y:
			if player[5].direction==2 and player[5].sp>=5:
				return 5
			elif player[5].direction==2:
				return 0
			else:
				return 2
		elif player[5].x-1==player[target].x and player[5].y==player[target].y:
			if player[5].direction==3 and player[5].sp>=5:
				return 5
			elif player[5].direction==3:
				return 0
			else:
				return 3
		elif player[5].x+1==player[target].x and player[5].y==player[target].y:
			if player[5].direction==4 and player[5].sp>=5:
				return 5
			elif player[5].direction==4:
				return 0
			else:
				return 4
	elif player[5].sp<=30:
		return 0
	else:
		dis1=abs(player[5].x-player[target].x)
		dis2=abs(player[5].y-player[target].y)

		if dis1>dis2:
			if player[5].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[5].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player6():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[6].x)+abs(player[i].y-player[6].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==6: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[6].x==player[target].x and player[6].y-1==player[target].y:
			if player[6].direction==1 and player[6].sp>=5:
				return 5
			elif player[6].direction==1:
				return 0
			else:
				return 1				
		elif player[6].x==player[target].x and player[6].y+1==player[target].y:
			if player[6].direction==2 and player[6].sp>=5:
				return 5
			elif player[6].direction==2:
				return 0
			else:
				return 2
		elif player[6].x-1==player[target].x and player[6].y==player[target].y:
			if player[6].direction==3 and player[6].sp>=5:
				return 5
			elif player[6].direction==3:
				return 0
			else:
				return 3
		elif player[6].x+1==player[target].x and player[6].y==player[target].y:
			if player[6].direction==4 and player[6].sp>=5:
				return 5
			elif player[6].direction==4:
				return 0
			else:
				return 4
	elif player[6].sp<=30:
		return 0
	else:
		dis1=abs(player[6].x-player[target].x)
		dis2=abs(player[6].y-player[target].y)

		if dis1>dis2:
			if player[6].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[6].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player7():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[7].x)+abs(player[i].y-player[7].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==7: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[7].x==player[target].x and player[7].y-1==player[target].y:
			if player[7].direction==1 and player[7].sp>=5:
				return 5
			elif player[7].direction==1:
				return 0
			else:
				return 1				
		elif player[7].x==player[target].x and player[7].y+1==player[target].y:
			if player[7].direction==2 and player[7].sp>=5:
				return 5
			elif player[7].direction==2:
				return 0
			else:
				return 2
		elif player[7].x-1==player[target].x and player[7].y==player[target].y:
			if player[7].direction==3 and player[7].sp>=5:
				return 5
			elif player[7].direction==3:
				return 0
			else:
				return 3
		elif player[7].x+1==player[target].x and player[7].y==player[target].y:
			if player[7].direction==4 and player[7].sp>=5:
				return 5
			elif player[7].direction==4:
				return 0
			else:
				return 4
	elif player[7].sp<=30:
		return 0
	else:
		dis1=abs(player[7].x-player[target].x)
		dis2=abs(player[7].y-player[target].y)

		if dis1>dis2:
			if player[7].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[7].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player8():
	near=[]
	target=1
	for i in list(range(len(player))):
		dis=abs(player[i].x-player[8].x)+abs(player[i].y-player[8].y)
		near.append(dis)

	shortest=100
	for i in list(range(len(player))):
		if i==8: continue
		if player[i].alive==False:continue
		if shortest>int(near[i]):
			shortest=int(near[i])
			target=i

	if near[target]==1:
		if player[8].x==player[target].x and player[8].y-1==player[target].y:
			if player[8].direction==1 and player[8].sp>=5:
				return 5
			elif player[8].direction==1:
				return 0
			else:
				return 1				
		elif player[8].x==player[target].x and player[8].y+1==player[target].y:
			if player[8].direction==2 and player[8].sp>=5:
				return 5
			elif player[8].direction==2:
				return 0
			else:
				return 2
		elif player[8].x-1==player[target].x and player[8].y==player[target].y:
			if player[8].direction==3 and player[8].sp>=5:
				return 5
			elif player[8].direction==3:
				return 0
			else:
				return 3
		elif player[8].x+1==player[target].x and player[8].y==player[target].y:
			if player[8].direction==4 and player[8].sp>=5:
				return 5
			elif player[8].direction==4:
				return 0
			else:
				return 4
	elif player[8].sp<=30:
		return 0
	else:
		dis1=abs(player[8].x-player[target].x)
		dis2=abs(player[8].y-player[target].y)

		if dis1>dis2:
			if player[8].x<=player[target].x:
				if dis1+dis2==1 and direction==4: return 0
				else:
					return 4
			else:
				if dis1+dis2==1 and direction==3: return 0
				else:
					return 3
		else:
			if player[8].y<=player[target].y:
				if dis1+dis2==1 and direction==2: return 0
				else:
					return 2
			else:
				if dis1+dis2==1 and direction==1: return 0
				else:
					return 1
def player9():
	return 0
def player10():
	return 0
def player11():
	return 0
def player12():
	return 0
def player13():
	return 0
def player14():
	return 0
def player15():
	return 0
def player16():
	return 0
def player17():
	return 0
def player18():
	return 0
def player19():
	return 0
def player20():
	return 0
def player21():
	return 0
def player22():
	return 0
def player23():
	return 0
def player24():
	return 0


# space end

def action():
	# receive AI`s choice
	if player[0].alive==True:
		player[0].action=player0()
	if player[1].alive==True:
		player[1].action=player1()
	if player[2].alive==True:
		player[2].action=player2()
	if player[3].alive==True:
		player[3].action=player3()
	if player[4].alive==True:
		player[4].action=player4()
	if player[5].alive==True:
		player[5].action=player5()
	if player[6].alive==True:
		player[6].action=player6()
	if player[7].alive==True:
		player[7].action=player7()
	if player[8].alive==True:
		player[8].action=player8()
	if player[9].alive==True:
		player[9].action=player9()
	if player[10].alive==True:
		player[10].action=player10()
	if player[11].alive==True:
		player[11].action=player11()
	if player[12].alive==True:
		player[12].action=player12()
	if player[13].alive==True:
		player[13].action=player13()
	if player[14].alive==True:
		player[14].action=player14()
	if player[15].alive==True:
		player[15].action=player15()
	if player[16].alive==True:
		player[16].action=player16()
	if player[17].alive==True:
		player[17].action=player17()
	if player[18].alive==True:
		player[18].action=player18()
	if player[19].alive==True:
		player[19].action=player19()
	if player[20].alive==True:
		player[20].action=player20()
	if player[21].alive==True:
		player[21].action=player21()
	if player[22].alive==True:
		player[22].action=player22()
	if player[23].alive==True:
		player[23].action=player23()
	if player[24].alive==True:
		player[24].action=player24()

	# process action if valid. no action if invalid
	for i in range(len(player)):
		if player[i].alive==False: continue

		if player[i].action==1:
			# move up
			if player[i].sit==True: player[i].action=0
			if player[i].sp<2: player[i].action=0
			if player[i].y==0: player[i].action=0

		if player[i].action==2:
			# move down
			if player[i].sit==True: player[i].action=0
			if player[i].sp<2: player[i].action=0
			if player[i].y==29: player[i].action=0

		elif player[i].action==3:
			# move left
			if player[i].sit==True: player[i].action=0
			if player[i].sp<2: player[i].action=0
			if player[i].x==0: player[i].action=0

		elif player[i].action==4:
			# move right
			if player[i].sit==True: player[i].action=0
			if player[i].sp<2: player[i].action=0
			if player[i].x==29: player[i].action=0
		
		elif player[i].action==5:
			# attack
			if player[i].sit==True: player[i].action=0
			if player[i].sp<5: player[i].action=0
		
		elif player[i].action==6:
			# sit
			if player[i].sit==True: player[i].action=0

		elif player[i].action==7:
			# stand
			if player[i].sit==False: player[i].action=0
			if player[i].sp<3: player[i].action=0

		elif player[i].action==8:
			# heal
			if player[i].hp==player[i].mhp: player[i].action=0
			if player[i].sp<20: player[i].action=0


def hit():
	# heal
	for i in range(len(player)):
		if player[i].alive==False: continue
		if player[i].action==8:
			player[i].hp+=5
			player[i].sp-=20
			if player[i].hp>player[i].mhp:
				player[i].hp=player[i].mhp

	# i hit j
	for i in range(len(player)):
		if player[i].alive==False or player[i].action!=5: continue
		player[i].sp-=5 # sp will decrease Regardless hit or not
		for j in range(len(player)): # target 
			if player[j].alive==False: continue
			if i==j: continue
			if (player[i].x==player[j].x and player[i].y-1==player[j].y and player[i].direction==1) or (player[i].x==player[j].x and player[i].y+1==player[j].y and player[i].direction==2) or (player[i].x-1==player[j].x and player[i].y==player[j].y and player[i].direction==3) or (player[i].x+1==player[j].x and player[i].y==player[j].y and player[i].direction==4):

				player[j].hp-=player[i].atk
				if player[j].hp<=0: player[j].killercandidate.append(i)

	# kill check and get bonus
	for i in range(len(player)):
		# death check
		if player[i].hp<=0 and player[i].alive==True:
			luck=random.randrange(0,len(player[i].killercandidate)) # it will got bonus
			player[i].killer=player[i].killercandidate[luck]
			temp=player[i].killer
			if player[temp].hp>0:
				player[temp].killbonus()
			message.append('player'+str(player[i].killer)+' kill player'+str(i))
			player[i].alive=False




def move():
	playerlist=list(range(len(player)))
	random.shuffle(playerlist)
	for i in playerlist:
		if player[i].action>=1 and player[i].action<=4 and player[i].sp>=2 and player[i].sit==False:

			player[i].sp-=2

			if player[i].action==1:
				player[i].y-=1
				player[i].direction=1
				if collision()==1:
					player[i].y+=1

			if player[i].action==2:
				player[i].y+=1
				player[i].direction=2
				if collision()==1:
					player[i].y-=1

			if player[i].action==3:
				player[i].x-=1
				player[i].direction=3
				if collision()==1:
					player[i].x+=1

			if player[i].action==4:
				player[i].x+=1
				player[i].direction=4
				if collision()==1:
					player[i].x-=1

	return 0

def residue():
	for i in range(len(player)):
		if player[i].action==6:
			player[i].sit=True
		elif player[i].action==7 and player[i].sp>=3:
			player[i].sit=False
			player[i].sp-=3
		elif player[i].action==0:
			if player[i].sit==True:
				player[i].sp+=2
				if player[i].sp>player[i].msp:
					player[i].sp=player[i].msp
			else:
				player[i].sp+=1
				if player[i].sp>player[i].msp:
					player[i].sp=player[i].msp


	return 0

def lastsurvive():
	cnt=0
	for i in range(len(player)):
		if player[i].alive==True:
			cnt+=1
	if cnt==1:
		return 1
	return 0



time=0
while True: # the main game loop
	currentstate=[]
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


	DISPLAYSURF.fill(BLACK)
	drawmap()

	# game loop
	if lastsurvive()==1:
		#for i in range(time):
		#	for j in range(len(player)):
		#		g.write(str(archieve[i][j].action)+' ')
		#	g.write('\n')
		#g.write('\n\n')
		#print(archieve)
		pygame.quit()
		sys.exit()

	action()
	hit()
	move()
	residue()

	# make currentstate (all player`s states and action)
	for i in range(len(player)):
		currentstate.append(player[i])
		if time>=1:
			g.write(str(archieve[time-1][i].action)+' ')
	g.write('\n')


	# construct archieve_time t, so player can read until t-1

	archieve.append(currentstate)


	#if player[0].x>0:
	#	player[0].x-=1
	#	player[0].hp-=1
	pygame.display.update()
	fpsClock.tick(FPS)

	time+=1