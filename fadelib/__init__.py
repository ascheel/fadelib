# -*- coding: utf-8 -*-
from __future__ import print_function, division
import opc, time
import random
import colorsys
import copy
import sys
import datetime
import math

"""
fill_rainbow()

"""


class FadeLIB(object):
	CHANNEL=0
	LED_ORDER='rgb'
	PIXELS = None

	NUM_LEDS = 50
	client = opc.Client('localhost:7890')

	BRIGHTNESS = 1.0
	CHANCE_GLITTER = 5
	CHANCE_CONFETTI = 5
	CONFETTI_AMOUNT = 3

	COLOR = {}
	COLOR['BLACK']   = (000,000,000)
	COLOR['GREY']    = (127,127,127)
	COLOR['GRAY']    = (127,127,127)
	COLOR['WHITE']   = (255,255,255)
	COLOR['RED']     = (255,000,000)
	COLOR['YELLOW']  = (255,255,000)
	COLOR['MAGENTA'] = (255,000,255)
	COLOR['BLUE']    = (000,000,255)
	COLOR['GREEN']   = (000,255,000)
	COLOR['CYAN']    = (000,255,255)
	COLOR['ORANGE']  = (255,127,000)
	COLOR['GOLD']    = '#FFFF00'
	COLOR['DARK_GREEN'] = '#006600'
	COLOR['BROWN']   = '#803000'
	COLOR['PURPLE']  = '#C038FF'
	COLOR['SILVER']  = '#C0C0C0'
	COLOR['ANTIQUE_WHITE'] = '#FAEBD7'
	COLOR['AMETHYST'] = '#9966CC'
	COLOR['AQUA'] = COLOR['CYAN']
	COLOR['AQUAMARINE'] = '#7FFFD4'
	COLOR['AZURE'] = '#F0FFFF'
	COLOR['BEIGE'] = '#F5F5DC'
	COLOR['BISQUE'] = '#FF34C4'
	COLOR['BLANCHED_ALMOND'] = '#FFEBCD'
	COLOR['BLUE_VIOLET'] = '#8A2BE2'
	COLOR['BROWN'] = '#A52A2A'
	COLOR['BURLY_WOOD'] = '#DEB887'
	COLOR['CADET_BLUE'] = '#5F9EA0'
	COLOR['CHARTREUSE'] = '#7FFF00'
	COLOR['CHOCOLATE'] = '#D2691E'

	THEME = {}
	THEME['christmas'] = ('RED','GREEN','RED','GREEN','WHITE')
	THEME['independence'] = ('RED','WHITE','BLUE')
	THEME['halloween'] = ('ORANGE','ORANGE','GREEN','DARK_GREEN')
	THEME['usmc'] = ('RED','GOLD')

	def __init__(self,**kwargs):
		if 'BRIGHTNESS' in kwargs:
			self.BRIGHTNESS = kwargs['BRIGHTNESS']
			if self.BRIGHTNESS > 1:
				self.BRIGHTNESS = 1
			elif self.BRIGHTNESS < 0:
				self.BRIGHTNESS = 0
		if 'NUM_LEDS' in kwargs:
			self.NUM_LEDS = kwargs['NUM_LEDS']
		if 'CHANNEL' in kwargs:
			self.CHANNEL = kwargs['CHANNEL']
		self.PIXELS = self.fill_solid('BLACK')
		self.update()
		self.update()

	def roll(self,matrix):
		height = len(matrix)
		width = max(len(row) for row in matrix)

		#for col in xrange(width):
		#	for row in xrange(center[0]+1):
		#		y = float(row) / float(center[1])
		#		x = float(col) / float(center[0])
		#	time.sleep(sleepTime)
		col = len(matrix[0])-1
		for row in xrange(height):
			self.blackout(False)
			self.drawLine(matrix,row,col)

		row = len(matrix)-1
		for col in xrange(width-1,-1,-1):
			self.blackout(False)
			self.drawLine(matrix,row,col)

		col = 0
		for row in xrange(height-1,-1,-1):
			self.blackout(False)
			self.drawLine(matrix,row,col)

		row = 0
		for col in xrange(width):
			self.blackout(False)
			self.drawLine(matrix,row,col)

	def drawLine(self,matrix,row,col):
		height = len(matrix)
		width = max(len(row) for row in matrix)
		center = (int(width/2), int(height/2))
		points = self.get_line((row, col), center)
		self.draw_points(matrix,points,'WHITE')
		self.update()
		time.sleep(0.25)

	def draw_points(self, matrix, points, color):
		for point in points:
			if matrix[point[0]][point[1]] > -1:
				self.PIXELS[matrix[point[0]][point[1]]] = 'WHITE'

	def get_line(self, start, end):
		"""Bresenham's Line Algorithm
		Produces a list of tuples from start and end
	 
		>>> points1 = get_line((0, 0), (3, 4))
		>>> points2 = get_line((3, 4), (0, 0))
		>>> assert(set(points1) == set(points2))
		>>> print points1
		[(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
		>>> print points2
		[(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
		"""
		# Setup initial conditions
		x1, y1 = start
		x2, y2 = end
		dx = x2 - x1
		dy = y2 - y1
	 
		# Determine how steep the line is
		is_steep = abs(dy) > abs(dx)
	 
		# Rotate line
		if is_steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
	 
		# Swap start and end points if necessary and store swap state
		swapped = False
		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
			swapped = True
	 
		# Recalculate differentials
		dx = x2 - x1
		dy = y2 - y1
	 
		# Calculate error
		error = int(dx / 2.0)
		ystep = 1 if y1 < y2 else -1
	 
		# Iterate over bounding box generating points between start and end
		y = y1
		points = []
		for x in range(x1, x2 + 1):
			coord = (y, x) if is_steep else (x, y)
			points.append(coord)
			error -= abs(dy)
			if error < 0:
				y += ystep
				error += dx
	 
		# Reverse the list if the coordinates were swapped
		if swapped:
			points.reverse()
		return points

	def wipe(self,matrix,direction=None):
		"""
		directions:
			0 = top down
			1 = right
			2 = bottom
			3 = left
		"""
		pauseTime = 0.25
		if not direction:
			direction = random.randrange(4)
		print('direction ' + str(direction))
		height = len(matrix)
		width = max(len(row) for row in matrix)
		if direction == 0:
			for row in xrange(height):
				for col in xrange(width):
					if matrix[row][col] != -1:
						self.PIXELS[matrix[row][col]] = 'WHITE'
				self.update(True)
				time.sleep(pauseTime)
		if direction == 1:
			for col in xrange(width-1,-1,-1):
				for row in xrange(height):
					if matrix[row][col] != -1:
						self.PIXELS[matrix[row][col]] = 'WHITE'
				self.update(True)
				time.sleep(pauseTime)
		if direction == 2:
			for row in xrange(height-1,-1,-1):
				for col in xrange(width):
					if matrix[row][col] != -1:
						self.PIXELS[matrix[row][col]] = 'WHITE'
				self.update(True)
				time.sleep(pauseTime)
		if direction == 3:
			for col in xrange(width):
				for row in xrange(height):
					if matrix[row][col] != -1:
						self.PIXELS[matrix[row][col]] = 'WHITE'
				self.update(True)
				time.sleep(pauseTime)

	def fill_solid(self,color):
		"""Provide a tuple and get a list of values filled with that color"""
		if not isinstance(color,basestring):
			color = [list(color) for _ in xrange(self.NUM_LEDS)]
		else:
			color = [color for _ in xrange(self.NUM_LEDS)]
		return color

	#def update(self,hardupdate=False):
	#	tmp_pixel = copy.deepcopy(self.PIXELS)
	#	for pixel in xrange(len(self.PIXELS)):
	#		tmp_pixel[pixel] = self.fix_colors(self.PIXELS[pixel])
	#	if hardupdate:
	#		#self.client.put_pixels(self.fill_solid(self.COLOR['BLACK']))
	#		self.client.put_pixels(tmp_pixel)
	#	self.client.put_pixels(tmp_pixel,self.CHANNEL)
	def update(self,hardupdate=False):
		self.PIXELS = self.fix_pixels()
		if hardupdate:
			self.client.put_pixels(self.PIXELS)
		self.client.put_pixels(self.PIXELS,self.CHANNEL)

	def fix_pixels(self,tmp_pixel=None):
		if tmp_pixel == None:
			tmp_pixel = copy.deepcopy(self.PIXELS)
		for pixel in xrange(len(tmp_pixel)):
			tmp_pixel[pixel] = self.fix_colors(tmp_pixel[pixel])
		return tmp_pixel

	def hexToDec(self,color):
		if len(color) == 3:
			# Convert 3 digit hex to 3 tuples
			color = tuple(((int(val,16) + 1) * 16)-1 for val in color)
		elif len(color) == 6:
			color = (color[0:2],color[2:4],color[4:6])
			color = tuple(int(val,16) for val in color)
		else:
			raise ValueError('Invalid input color value')
		return color

	def fix_colors(self,incolor):
		if incolor in self.COLOR:
			incolor = self.COLOR[incolor]
		if isinstance(incolor,basestring):
			if incolor[0] == '#':
				incolor = self.hexToDec(incolor[1:])
			else:
				raise ValueError('Invalid input color value ({})'.format(repr(incolor)))
		outcolor = tuple(int(incolor[val] * self.BRIGHTNESS) for val in xrange(3))
	
		return(outcolor)

	def addGlitter(self,chance=80):
		if chance < 1:
			chance *= 100

	def blackout(self,draw=None):
		if draw == None:
			draw = True
		self.PIXELS = self.fill_solid('BLACK')
		if draw == True:
			self.update()
			self.update()

	def rand(self,*args):
		minrange=0
		if len(args) == 1:
			maxrange=args[0]
		elif len(args) == 2:
			minrange,maxrange=args
		return random.randrange(minrange,maxrange)

	def rand_leds(self,number,maxnum=NUM_LEDS):
		"""
		Chooses <number> of random LEDs maxing out at <maxnum>.
		<maxnum> defaults to self.NUM_LEDS.
		"""
		if maxnum == -1:
			maxnum = self.NUM_LEDS
		rand_list = []
		number += 1
		for x in xrange(number):
			rand_number = random.randrange(maxnum)
			if rand_number in rand_list:
				x -= 1
			else:
				rand_list.append(rand_number)
		return rand_list

	def add_glitter(self):
		if self.rand(100) < self.CHANCE_GLITTER:
			rand_list = self.rand_leds(10)
			for x in xrange(len(rand_list)):
				whitevalue = 127
				self.PIXELS[rand_list[x]] = [whitevalue * self.BRIGHTNESS,whitevalue * self.BRIGHTNESS,whitevalue * self.BRIGHTNESS]

	def build_confetti(self):
		fps = 30
		duration = 0.1
		steps = duration * fps
		endcolor = 'BLACK'
		if self.rand(100) < self.CHANCE_CONFETTI:
			rand_list = self.rand_leds(self.CONFETTI_AMOUNT)
			rand_colors = []
			for x in xrange(len(rand_list)):
				rand_colors.append(self.PREDEFINED_COLORS[random.randrange(len(self.PREDEFINED_COLORS))])
			for step in xrange(int(steps)):
				percentage = step / steps
				for x in xrange(len(rand_list)):
					for color in xrange(3):
						newcolor = int(rand_colors[x][color] + ((endcolor[color] - rand_colors[x][color]) * percentage)) * self.BRIGHTNESS

						#print(repr(self.PIXELS))
						self.PIXELS[rand_list[x]][color] = newcolor
						#self.PIXELS[23][color] = newcolor
						#print(self.PIXELS[23])
						#print(rand_list[x])
						#print('rand_list[x] = {} - self.PIXELS[rand_list[x]] = {} - color = {}'.format(rand_list[x],self.PIXELS[rand_list[x]],color))
						#time.sleep(2)
				self.update()
				time.sleep(1/fps)

	def hsv(self,hsv):
		""" Takes triple of H, S, V format where H = 0-359, S = 0-99, V = 0-99 """
		hsv = [val for val in hsv]
		if hsv[2] == 0:
			# 0 value is black.  Processing is pointless
			return (0,0,0)
		if hsv[0] > 359:
			# hue has 359 max
			hsv[0] = 359
		if hsv[1] > 99:
			# saturation has 99 max
			hsv[1] = 99
		if hsv[2] > 99:
			# Value has 99 max
			hsv[2] = 99
		for x in xrange(3):
			if hsv[x] < 0:
				hsv[x] = 0
		hsv = (float(hsv[0] / 360),float(hsv[1] / 100),float(hsv[2] / 100))
		return tuple(int(val * 255) for val in colorsys.hsv_to_rgb(*hsv))

	def fill_rainbow(self):
		#tmp_pixel = copy.deepcopy(self.PIXELS)
		deltahue=10
		deltahueAdj = deltahue
		saturation = 100
		value = 100 * self.BRIGHTNESS
		hue = 0
		starthue = 0
		runVar = 0
		while runVar < 5:
			hue = starthue
			for led in xrange(self.NUM_LEDS):
				#print(hue, saturation, value)
				#print(self.hsv2rgb((hue,saturation,value)))
				self.PIXELS[led] = self.hsv((hue,saturation,value))
				hue += deltahue
				while hue >= 360:
					hue -= 360
					if led == 0:
						runVar += 1
			starthue += 5
			while starthue > 360:
				starthue -= 360
			self.update()
			time.sleep(0.1)
		#return tmp_pixel

	#def roll(self, season):
	#	if season not in self.THEME:
	#		return None
	#	template = []
	#	count = 0
	#	try:
	#		for a in xrange(self.NUM_LEDS):
	#			for color in self.THEME[season]:
	#				template.append(color)
	#				count += 1
	#				if count >= NUM_LEDS:
	#					raise BreakIt
	#	except BreakIt:
	#		pass
	#	#start roll
	#	while True:
	#		currentColors = []
	#		offset += 1
	#		if offset >= len(self.THEME[season]):
	#			offset -= len(self.THEME[season])
	#		for a in xrange(len(self.THEME[season])):
				

	def transition2(self, pixels2, **kwargs):
		duration = 2
		if 'duration' in kwargs:
			duration = kwargs['duration']
		fps = 30
		sleeptime = float(1/fps)
		useglitter = False
		useconfetti = False
		pixels1 = copy.deepcopy(self.PIXELS)
		pixels1 = self.fix_pixels(pixels1)
		pixels2 = self.fix_pixels(pixels2)
		pixels3 = []
		if 'GLITTER' in kwargs:
			if kwargs['GLITTER'] == True:
				useglitter = True
		if 'CONFETTI' in kwargs:
			if kwargs['CONFETTI'] == True:
				useconfetti = True
		steps = int(math.ceil(duration * fps))
		for step in xrange(steps):
			percentage = step / steps
			for dot in xrange(self.NUM_LEDS):
				for color in xrange(3):
					self.PIXELS[dot] = tuple(int(pixels1[dot][color] + ((pixels2[dot][color] - pixels1[dot][color]) * percentage)) for color in xrange(3))
			if useglitter:
				self.add_glitter()
			if useconfetti:
				self.add_confetti()
			self.update()
			time.sleep(sleeptime)

	def transition(self,startcolor,endcolor,**kwargs):
		useglitter = False
		useconfetti = False
		duration = 5
		if 'GLITTER' in kwargs:
			if kwargs['GLITTER'] == True:
				useglitter = True
		if 'CONFETTI' in kwargs:
			if kwargs['CONFETTI'] == True:
				useconfetti = True
		if 'DURATION' in kwargs:
			duration = kwargs['DURATION']
		fps = 30
		steps = duration * fps
		trancolor = [0,0,0]
		for step in xrange(steps):
			percentage = step / steps
			for color in xrange(3):
				trancolor[color] = int(startcolor[color] + ((endcolor[color] - startcolor[color]) * percentage))
			self.fill_solid(trancolor)
			if useglitter:
				self.add_glitter()
			if useconfetti:
				self.build_confetti()
			self.update()
			time.sleep(1/fps)
		return endcolor

	def fill_random_maxhsv(self):
		pixels = []
		for dot in xrange(self.NUM_LEDS):
			pixels.append(self.hsv((random.randrange(360),100,100)))
		return pixels

	def theme(self,season):
		outcolor = []
		if season not in self.THEME:
			return None
		for color in xrange(self.NUM_LEDS):
			outcolor.append(self.THEME[season][random.randrange(len(self.THEME[season]))])
		return outcolor


def main():
	fc1 = FadeLIB(LED_ORDER='grb',BRIGHTNESS=0.3)
	fc.PIXELS = fc.fill_rainbow()
	#time.sleep(10)
	fc.PIXELS = fc.fill_random_maxhsv()
	pixels = fc.fill_solid(fc.hsv((random.randrange(360),100,100)))
	while True:
		fc.transition2(pixels,DURATION=1)
		pixels = fc.fill_random_maxhsv()
		fc.transition2(pixels,DURATION=1)
		pixels = fc.fill_solid((fc.hsv((random.randrange(360),100,100))))

	"""for var in xrange(1):
		print('Transition2 ' + str(var))
		pixels = fc.fill_random_maxhsv()
		fc.transition2(pixels, DURATION=1)"""
	"""while True:
		glitterValue=False
		confettiValue=False
		fc.transition(fc.COLOR['RED'],fc.COLOR['ORANGE'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)
		fc.transition(fc.COLOR['ORANGE'],fc.COLOR['YELLOW'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)
		fc.transition(fc.COLOR['YELLOW'],fc.COLOR['GREEN'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)
		fc.transition(fc.COLOR['GREEN'],fc.COLOR['BLUE'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)
		fc.transition(fc.COLOR['BLUE'],fc.COLOR['MAGENTA'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)
		fc.transition(fc.COLOR['MAGENTA'],fc.COLOR['RED'],CONFETTI=confettiValue,GLITTER=glitterValue,DURATION=1)"""
	fc.blackout()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		#e = sys.exc_info()
		#print(repr(e))
		print('\nKeyboardInterrupt caught.')
		fc = FadeLIB()
		fc.blackout()
