from __future__ import print_function, division
import opc, time
import random
import colorsys

class FadeLIB(object):
	LED_ORDER='rgb'
	COLOR_ORDER = []

	NUM_LEDS = 50
	client = opc.Client('localhost:7890')

	BRIGHTNESS = 0.50
	CHANCE_GLITTER = 5
	CHANCE_CONFETTI = 5
	CONFETTI_AMOUNT = 10

	COLOR_BLACK   = (000,000,000)
	COLOR_WHITE   = (255,255,255)
	COLOR_RED     = (255,000,000)
	COLOR_YELLOW  = (255,255,000)
	COLOR_MAGENTA = (255,000,255)
	COLOR_BLUE    = (000,000,255)
	COLOR_GREEN   = (000,255,000)
	COLOR_CYAN    = (000,255,255)
	COLOR_ORANGE  = (255,127,000)

	PREDEFINED_COLORS = []
	PREDEFINED_COLORS.append(COLOR_WHITE)
	PREDEFINED_COLORS.append(COLOR_RED)
	PREDEFINED_COLORS.append(COLOR_YELLOW)
	PREDEFINED_COLORS.append(COLOR_MAGENTA)
	PREDEFINED_COLORS.append(COLOR_BLUE)
	PREDEFINED_COLORS.append(COLOR_GREEN)
	PREDEFINED_COLORS.append(COLOR_CYAN)
	PREDEFINED_COLORS.append(COLOR_ORANGE)

	def __init__(self,**kwargs):
		if 'LED_ORDER' in kwargs:
			self.LED_ORDER = kwargs['LED_ORDER']
			self.COLOR_ORDER.append(self.LED_ORDER.find('r'))
			self.COLOR_ORDER.append(self.LED_ORDER.find('g'))
			self.COLOR_ORDER.append(self.LED_ORDER.find('b'))
		if 'BRIGHTNESS' in kwargs:
			self.BRIGHTNESS = kwargs['BRIGHTNESS']
		self.fill_solid(self.COLOR_BLACK)
		self.update()
		self.update()

	def fill_solid(self,color):
		color = self.fix_colors(color)
		#self.PIXELS = [color] * self.NUM_LEDS
		self.PIXELS = [list(color) for _ in xrange(self.NUM_LEDS)]
		#self.client.put_pixels(pixels)

	def update(self):
		self.client.put_pixels(self.PIXELS)

	def fix_colors(self,incolor):
		outcolor = []
		outcolor.append(int(incolor[self.COLOR_ORDER[0]] * self.BRIGHTNESS))
		outcolor.append(int(incolor[self.COLOR_ORDER[1]] * self.BRIGHTNESS))
		outcolor.append(int(incolor[self.COLOR_ORDER[2]] * self.BRIGHTNESS))
		return(outcolor)

	def addGlitter(self,chance=80):
		if chance < 1:
			chance *= 100

	def blackout(self):
		self.fill_solid(self.COLOR_BLACK)
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
				self.PIXELS[rand_list[x]] = (127,127,127)

	def build_confetti(self):
		fps = 30
		duration = 0.1
		steps = duration * fps
		endcolor = self.COLOR_BLACK
		if self.rand(100) < self.CHANCE_CONFETTI:
			rand_list = self.rand_leds(self.CONFETTI_AMOUNT)
			rand_colors = []
			for x in xrange(len(rand_list)):
				rand_colors.append(self.PREDEFINED_COLORS[random.randrange(len(self.PREDEFINED_COLORS))])
			for step in xrange(int(steps)):
				percentage = step / steps
				for x in xrange(len(rand_list)):
					for color in xrange(3):
						newcolor = int(rand_colors[x][color] + ((endcolor[color] - rand_colors[x][color]) * percentage))

						self.PIXELS[rand_list[x]][color] = newcolor
						#self.PIXELS[23][color] = newcolor
						#print(self.PIXELS[23])
						#print(rand_list[x])
						#print('rand_list[x] = {} - self.PIXELS[rand_list[x]] = {} - color = {}'.format(rand_list[x],self.PIXELS[rand_list[x]],color))
						#time.sleep(2)
				self.update()
				time.sleep(1/fps)

	def hsv2rgb(self,hsv):
		r,g,b = colorsys.hsv_to_rgb(*hsv)
		r = int(r * 255)
		g = int(g * 255)
		b = int(b * 255)
		return (r, g, b)

	def rgb2hsv(self,rgb):
		return colorsys.rgb_to_hsv(*rgb)

	def fill_rainbow(self):
		deltahue=25
		deltahueAdj = deltahue / 360
		saturation = 1
		value = 1
		hue = 0
		starthue = 0
		while True:
			starthueAdj = starthue / 360
			for led in xrange(self.NUM_LEDS):
				hue = starthueAdj
				print(hue, saturation, value)
				print(self.hsv2rgb((hue,saturation,value)))
				self.PIXELS[led] = self.fix_colors(self.hsv2rgb((hue,saturation,value)))
				hue += deltahue / 360
				print(hue)
			starthue += 5
			self.update()
			time.sleep(0.25)


	def transition(self,startcolor,endcolor,duration=5,**kwargs):
		useglitter = False
		useconfetti = False
		if 'GLITTER' in kwargs:
			if kwargs['GLITTER'] == True:
				useglitter = True
		if 'CONFETTI' in kwargs:
			if kwargs['CONFETTI'] == True:
				useconfetti = True
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

def main():
	fc = FadeLIB(LED_ORDER='grb',BRIGHTNESS=0.5)
	fc.fill_rainbow()
	time.sleep(10)
	while True:
		fc.transition(fc.COLOR_RED,fc.COLOR_ORANGE,1,CONFETTI=True)
		fc.transition(fc.COLOR_ORANGE,fc.COLOR_YELLOW,1,CONFETTI=True)
		fc.transition(fc.COLOR_YELLOW,fc.COLOR_GREEN,1,CONFETTI=True)
		fc.transition(fc.COLOR_GREEN,fc.COLOR_BLUE,1,CONFETTI=True)
		fc.transition(fc.COLOR_BLUE,fc.COLOR_MAGENTA,1,CONFETTI=True)
		fc.transition(fc.COLOR_MAGENTA,fc.COLOR_RED,1,CONFETTI=True)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nKeyboardInterrupt caught.')
		fc = FadeLIB(LED_ORDER='grb',BRIGHTNESS=0.5)
		fc.blackout()
