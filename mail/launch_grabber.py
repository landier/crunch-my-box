from grabber.dao import DAO
from grabber.grabber import Grabber
from util.configuration import Configuration


def launchGrabber():
    config = Configuration()

    dao = DAO(config)

    grabber = Grabber(config, dao)
    grabber.run()


launchGrabber()