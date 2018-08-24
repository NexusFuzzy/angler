from winappdbg import Debug, EventHandler
import sys
import os

class MyEventHandler ( EventHandler):
	apiHooks = {
		'kernel32.dll' : [
						( 'InternetOpenUrlW', 6),
						],
	}

# The pre functions are called upon entering the API

def pre_InternetOpenUrlW (self, event, ra, hInternet, lpszUrl, lpszHeaders, dwHeadersLength, dwFlags, dwContext):
	url = event.get_process().peek_string(lpszUrl, fUnicode=True)
	print "URL: %s" % (lpszUrl) 

if __name__ == "__main__":
	if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
		print "\nUsage: %s <File to monitor> [arg1 arg2 ...]\n" % sys.argv[0]
		sys.exit()

debug = Debug ( MyEventHandler() )

try:
	# Start a new process for debugging
	p = debug.execv(sys.argv[1:], bFollow=True)
	# Wait for the debugged process to finish
	debug.loop()
# Stop the debugger
finally:
	debug.stop()
