from controller import *

if __name__ == "__main__":
    controller = Controller()
    create_clients(controller)
    controller.run()
