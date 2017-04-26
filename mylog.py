import logging
import os,sys
import ConfigParser

config_file = os.path.join(sys.path[0],'config.ini')
cp = ConfigParser.SafeConfigParser()
cp.read(config_file)

logfile = cp.get('log','logfile')

if os.path.exists(logfile):
    pass
else:
    os.mknod(logfile)

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logfile,
                    filemode='a+')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
