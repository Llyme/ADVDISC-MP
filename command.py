import cranberry

vectors = {}

red = (223, 63, 63)
green = (31, 159, 63)
blue = (63, 63, 223)

def tofloat(v):
	try:
		return float(v)
	except ValueError:
		return None

def parse(text, draw):
	if text == "/help":
		draw("Create a vector (separated by spaces).", green)
		draw("/vector `name` `n0 n1 n2 ...`", blue)
		draw("Read the vector.", green)
		draw("/vector `name`", blue)
		draw("Get the vector's magnitude.", green)
		draw("/vector `name` magnitude", blue)
		draw("Get the vector's unit vector.", green)
		draw("/vector `name` unit", blue)
		draw("Delete the existing vector.", green)
		draw("/vector `name` delete", blue)
	elif text[:8] == "/vector ":
		text = text[8:]

		if " " in text:
			i = text.index(" ")
			name = text[:i]
			text = text[i+1:]
			l = []

			if name in vectors:
				if text == "magnitude":
					draw(str(vectors[name].magnitude()), blue)
				elif text == "unit":
					v = vectors[name].unit()

					draw(
						"[" +
						", ".join(
							str(getattr(v, "v" + str(i)))
							for i in range(v.length)
						) +
						"]",
						blue
					)
				elif text == "delete":
					del vectors[name]

					draw("`" + name + "` deleted.", blue)
				else:
					draw("`" + name + "` already exists!", red)

				return

			while (text != None and len(text)):
				n = None

				if " " in text:
					i = text.index(" ")
					n = tofloat(text[:i])
					text = text[i+1:]
				else:
					n = tofloat(text)
					text = None

				if n != None:
					l.append(n)
				else:
					l = None
					break

			if l:
				vectors[name] = cranberry.Vector(*tuple(l))

				draw(
					"Created vector `" + name + "` containing [" +
					", ".join(str(v) for v in l) + "].",
					blue
				)
				return
		else:
			if text not in vectors:
				draw("`" + text + "` doesn't exist!", red)
			else:
				v = vectors[text]

				draw(
					"[" +
					", ".join(
						str(getattr(v, "v" + str(i)))
						for i in range(v.length)
					) +
					"]",
					blue
				)

			return

		draw("Invalid syntax!", red)
		return
	else:
		return text