import time
from smashBoardJetson import SmashBoard

smashBoard = SmashBoard(host='10.16.19.2', port=1619)
smashBoard.connect()
smashBoard.startUpdateThread()
print 'Started update thread'

while 1:
	print '-------------------------'
	print 'A - print all'
	print 'G - get value'
	print 'M - monitor value'
	print 'S - set value'
	print 'Z - set up auto'
	print 'Q - quit'
	try:
		command = raw_input(': ')

		if command is 'A':
			print '-------------------------'
			print 'L - longs'
			print 'D - doubles'
			print 'S - strings'
			print 'Q - quit'

			dataType = raw_input(': ')

			if dataType is 'L':
				for key in smashBoard.longMap:
					print key + ' - ' + str(smashBoard.longMap[key])
				time.sleep(1)
			elif dataType is 'D':
				for key in smashBoard.doubleMap:
					print key + ' - ' + str(smashBoard.doubleMap[key])
				time.sleep(1)
			elif dataType is 'S':
				for key in smashBoard.stringMap:
					print key + ' - ' + str(smashBoard.stringMap[key])
				time.sleep(1)
			elif dataType is 'Q':
				continue
		elif command is 'G':
			print '-------------------------'
			print 'L - long'
			print 'D - double'
			print 'S - string'
			print 'Q - quit'

			dataType = raw_input(': ')

			if dataType is 'Q':
				continue

			key = raw_input('Key: ')

			if dataType is 'L':
				print smashBoard.getLong(key)
				time.sleep(1)
			elif dataType is 'D':
				print smashBoard.getDouble(key)
				time.sleep(1)
			elif dataType is 'S':
				print smashBoard.getString(key)
				time.sleep(1)
		elif command is 'M':
			print '-------------------------'
			print 'L - long'
			print 'D - double'
			print 'S - string'
			print 'Q - quit'

			dataType = raw_input(': ')

			if dataType is 'Q':
				continue

			key = raw_input('Key: ')

			if dataType is 'L':
				smashBoardFunction = smashBoard.getLong
			elif dataType is 'D':
				smashBoardFunction = smashBoard.getDouble
			elif dataType is 'S':
				smashBoardFunction = smashBoard.getString

			if not smashBoardFunction(key):
				print 'Value does not exist'
				time.sleep(1)
				continue

			try:
				while 1:
					print smashBoardFunction(key)
					time.sleep(0.25)
			except KeyboardInterrupt:
				time.sleep(1)
				continue
		elif command is 'S':
			print '-------------------------'
			print 'L - long'
			print 'D - double'
			print 'S - string'
			print 'Q - quit'

			dataType = raw_input(': ')

			if dataType is 'Q':
				continue

			key = raw_input('Key: ')

			if not key:
				continue

			value = raw_input('Value: ')

			try:
				if dataType is 'L':
					value = int(value)
				elif dataType is 'D':
					value = float(value)
			except ValueError:
				print 'Invalid input'
				time.sleep(1)
				continue

			if dataType is 'L':
				smashBoard.setLong(key, value)
				print 'Set value'
				time.sleep(1)
			elif dataType is 'D':
				smashBoard.setDouble(key, value)
				print 'Set value'
				time.sleep(1)
			elif dataType is 'S':
				smashBoard.setString(key, value)
				print 'Set value'
				time.sleep(1)
		elif command is 'Z':
			print '-------------------------'
			print '1 - low bar'
			print '2 - chevalle de frise'
			print '3 - portcullis'

			defense = raw_input('Defense: ')

			try:
				defense = int(defense)
			except ValueError:
				print 'Invalid input'
				time.sleep(1)
				continue

			if defense < 1 or defense > 3:
				print 'Invalid input'
				time.sleep(1)
				continue

			if defense is 1:
				lane = 1
			else:
				print '-------------------------'
				print '1-5'

				lane = raw_input('Lane: ')

				try:
					lane = int(lane)
				except ValueError:
					print 'Invalid input'
					time.sleep(1)
					continue

				if lane < 1 or lane > 5:
					print 'Invalid input'
					time.sleep(1)
					continue

			if defense is 1:
				target = 1
			else:
				print '-------------------------'
				print '1 - left'
				print '2 - middle'
				print '3 - right'

				target = raw_input('Target goal: ')

				try:
					target = int(target)
				except ValueError:
					print 'Invalid input'
					time.sleep(1)
					continue

				if target < 1 or target > 3:
					print 'Invalid input'
					time.sleep(1)
					continue

			smashBoard.setLong('autoDefense', defense)
			smashBoard.setLong('autoLane', lane)
			smashBoard.setLong('autoTargetGoal', target)

			print '-------------------------'
			print 'Set auto to cross the ' + ['low bar', 'chevalle de frise', 'portcullis'][defense - 1] + ' from lane ' + str(lane) + ' and shoot in the ' + ['left', 'middle', 'right'][target - 1] + ' high goal'
			time.sleep(1)
		elif command is 'Q':
			smashBoard.cleanUp()
			break
	except KeyboardInterrupt:
		smashBoard.cleanUp()
		break
