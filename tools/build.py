"""One command: bundle assets, then generate the HTML pages.   python tools/build.py
Add --dev to point the pages at the readable sources instead of the minified files.
"""
import subprocess, sys, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
dev = '--dev' in sys.argv
subprocess.check_call([sys.executable, '-I', os.path.join(here, 'bundle.py'), root])
subprocess.check_call([sys.executable, '-I', os.path.join(here, 'build_pages.py'), root] + (['--dev'] if dev else []))
