
import sys, re

try:
    import gzip
    have_gzip = True
except ImportError:
    have_gzip = False
try:
    import bz2
    have_bz2 = True
except ImportError:
    have_bz2 = False

from PySTDF.IO import Parser
from PySTDF.Writers import AtdfWriter
import PySTDF.V4

gzPattern = re.compile('\.g?z', re.I)
bz2Pattern = re.compile('\.bz2', re.I)

def process_file(fn):
    filename, = sys.argv[1:]
    
    reopen_fn = None
    if filename is None:
        f = sys.stdin
    elif gzPattern.search(filename):
        if not have_gzip:
            print >>sys.stderr, "gzip is not supported on this system"
            sys.exit(1)
        reopen_fn = lambda: gzip.open(filename, 'rb')
        f = reopen_fn()
    elif bz2Pattern.search(filename):
        if not have_bz2:
            print >>sys.stderr, "bz2 is not supported on this system"
            sys.exit(1)
        reopen_fn = lambda: bz2.BZ2File(filename, 'rb')
        f = reopen_fn()
    else:
        f = open(filename, 'rb')
    p=Parser(inp=f, reopen_fn=reopen_fn)
    p.addSink(AtdfWriter())
    p.parse()
    f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <stdf file>" % (sys.argv[0])
    else:
        process_file(sys.argv[1])