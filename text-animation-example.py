# (c) 2022 Niels Provos
#
# A simple script to generate a typewriter like type-on animation effect in Nuke
#
# The basic idea is to add each character typed as a new text node. This gets
# doubled up with a separate set of text nodes that contain the blinking cursor.
# Automation on the switch node provides the type-on animation effect over time.
#
# Font and 2k canvas are currently baked into the script. The only changable 
# parameter is the global font scale that gets propagated into the group node.
#
def createText(content, ref):
	txt = nuke.createNode("Text", inpanel=False)
	txt["selected"].setValue(False)
	txt.setInput(0, ref)
	txt["message"].setValue(content)
	txt["yjustify"].setValue('top')
	txt['box'].setX(0)
	txt['box'].setY(0)
	txt['box'].setT(2048)
	txt['box'].setR(2048)
	txt["font"].setValue('C:/Program Files/Nuke13.2v2/plugins/fonts/Courier.pfa')
	txt['size'].setExpression('100*parent.scale')

	return txt

def createTypeOn(name, text, speed=3):
	# which text objects
	texts = []
	# text objects with a blinky on it
	blink = []
	# when to activate them
	when = []

	# let's put everything into a group
	with nuke.root():
		group_node = nuke.createNode('Group')

	group_node['name'].setValue(name)
	group_node.begin()

	knob = nuke.Double_Knob('scale', 'scale')
	knob.setValue(1.0)
	group_node.addKnob(knob)

	ref = nuke.nodes.Reformat()
	ref['format'].setValue("square_2K")

	current = ""
	minframe = 0
	for frame, text in text:
		if frame < minframe:
			frame = minframe + 1
		for i in range(len(text)):
			if text != '<':
				current += text[i]
			texts.append(createText(current, ref))
			blink.append(createText(current + '_', ref))
			when.append(frame + i * speed)
			minframe = frame + i * speed
		if text != '<':
			current += "\n"


	# not that anyone will ever open the group but lets
	# improve the layout
	spacing = 80
	columns = 5
	count = 0
	for node in texts:
		node.setXpos((count % columns) * spacing)
		node.setYpos(int(count / columns) * spacing)
		count += 1

	count = 0
	for node in blink:
		node.setXpos((columns + 1 + (count % columns)) * spacing)
		node.setYpos(int(count / columns) * spacing)
		count += 1

	# main text
	sw = nuke.nodes.Switch(inputs=texts)
	kn = sw['which']
	kn.setAnimated()
	for i in range(len(when)):
		kn.setValueAt(i, when[i])

	# blinky text
	swBlink = nuke.nodes.Switch(inputs=blink)
	kn = swBlink['which']
	kn.setAnimated()
	for i in range(len(when)):
		kn.setValueAt(i, when[i])

	fsw = nuke.nodes.Switch()
	fsw.setInput(1, swBlink)
	fsw.setInput(0, sw)
	fsw["which"].setExpression('frame % 24 > 12 ? 1 : 0')

	out = nuke.createNode('Output', inpanel=False)
	out.setInput(0, fsw)

	group_node.end()

	print("created")
	return group_node

hookone = [
[0, "<"],
[30, "Better Patch Your Network"],
[130, "Better Patch Your Network"],
[200, "Eh Eh Better Patch Your Network"],
[320, "Better Patch Your Network"],
[385, "Eh Eh Eh Better Patch Your"]
]

createTypeOn('HOOK1fxd2', hookone, speed=1)