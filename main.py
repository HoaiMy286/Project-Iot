# from controller import *
from SCH_Controller import * 

if __name__ == "__main__":
    # controller = Controller()
    SCH_Controller = SCH_Controller(scheduler=Scheduler())
    create_clients(SCH_Controller)
    SCH_Controller.run()         