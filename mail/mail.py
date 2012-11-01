from service.grabber import Grabber
from util.configuration import Configuration

config = Configuration()
grabber = Grabber(config)
grabber.run()
