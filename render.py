import cranberry, command, pygame

import assets.api.SenPy as senpai
ahoge = senpai.remote["ahoge"]
kouhai = senpai.remote["kouhai"]
imouto = senpai.remote["imouto"]
kuudere = senpai.remote["kuudere"]


# Assets
segoe = kuudere.get("segoe ui", 16, False)
calibri = kuudere.get("calibri", 18, False)
calibri_linesize = calibri.get_linesize()


# Configuration
scroll_delta = 0 # The scroll that's trying to reach 'scroll'.
scroll = 0 # The real scroll.
screen_min = 440 # Minimum size.
screen_y = 0 # The text collection's current height.
screen = pygame.Surface((310, screen_min)) # The text collection.
screen.fill((255, 255, 255)) # Make it white.

imouto.screen.fill((255, 255, 255))


# Textbox
textbox = kouhai.TextBox({
	"rect": (0, 450, 320, 30)
})
textbox.set_focus(1)

def textbox_unfocused():
	textbox.set_focus(1)

textbox.on("unfocused", textbox_unfocused)

def textbox_keyinput(event):
	imouto.screen.fill((255, 255, 255), (5, 450, 315, 30))

	text = textbox.properties["text"]

	if event and event.key == 13:
		text = command.parse(text, draw)

		if text:
			draw(text)

		textbox.properties["text"] = ""
		text = ""

	d = len(text) > 0

	imouto.screen.blit(
		segoe.render(
			d and text or "Type here.",
			1,
			d and (0, 0, 0) or (127, 127, 127)
		),
		(10, 450)
	)

textbox.on("keyinput", textbox_keyinput)
textbox_keyinput(None)


# Draw function.
def draw(txt, color=(0, 0, 0)):
	global screen_min, screen_y, screen, calibri_linesize, scroll

	l, y, txt = kuudere.wrap(
		calibri,
		(310, 0),
		calibri_linesize,
		txt,
		1,
		color
	)

	if max(screen_min, screen_y + y) > screen_y:
		temp = pygame.Surface((310, screen_y + y))
		temp.fill((255, 255, 255))
		temp.blit(screen, (0, 0))
		screen = temp

	i = 0
	for image in l:
		screen.blit(
			image,
			(0, screen_y + calibri_linesize*i)
		)

		i += 1

	if scroll >= screen_y - screen_min:
		scroll = max(0, screen_y - screen_min + y)

	screen_y += y

	#imouto.screen.fill((255, 255, 255), (5, 5, 310, 440))
	imouto.screen.blit(
		screen,
		(5, 5),
		(0, scroll_delta, 310, screen_min)
	)


# Mouse Wheel
def mousebuttondown(event):
	global scroll, scroll_delta

	if event.button == 4: # Scroll Up
		scroll = max(0, scroll - calibri_linesize)
	elif event.button == 5: # Scroll Down
		scroll = min(
			scroll + calibri_linesize,
			max(0, screen_y - screen_min)
		)

imouto.on("mousebuttondown", mousebuttondown)

draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")
draw("The big brown fox jumps over the lazy dog.")


# Render Stepping (Fired before it renders.)
def update(dt):
	global scroll, scroll_delta, screen_min

	if scroll_delta != scroll:
		dt = min(1, dt*30)
		scroll_delta = cranberry.floor(
			(scroll_delta*dt + scroll*(1-dt))*100
		)/100

		imouto.screen.blit(
			screen,
			(5, 5),
			(0, scroll_delta, 310, screen_min)
		)

imouto.on("update", update)