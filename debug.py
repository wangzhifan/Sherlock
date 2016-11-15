import Sherlock
import otherfile
import sys

sys.settrace(Sherlock.traceit)
otherfile.main()
sys.settrace(None)