#V1     first usage of the NEF Em 
#V1.1   Request for localisation and QoS
#V2.0   With SDK and .env file
#V3.0   Onboard capif, for vApp to retrieve localization, QoS and connection status
version = "3.1" 

#run main app with 'uvicorn main:app --port 8000 --reload'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#https://patorjk.com/software/taag/

def print_initmess():
    mess =  "  _______  ___  ___   __       __   __   _______  ___________     ___       ______    ______   " + '\n'
    mess += " /  _____||   \/   | |  |     |  \ |  | |   ____||           |   /   \     |   _  \  |   _  \  " + '\n'
    mess += "|  |  __  |  \  /  | |  |     |   \|  | |  |__   `---|  |----`  /  ^  \    |  |_)  | |  |_)  | " + '\n'
    mess += "|  | |_ | |  |\/|  | |  |     |  . `  | |   __|      |  |      /  /_\  \   |   ___/  |   ___/  " + '\n'
    mess += "|  |__| | |  |  |  | |  |     |  |\   | |  |____     |  |     /  _____  \  |  |      |  |      " + '\n'
    mess += " \______| |__|  |__| |__|     |__| \__| |_______|    |__|    /__/     \__\ | _|      | _|      " + '\n'
    print(mess)
    print(bcolors.BOLD + bcolors.OKBLUE + " => VERSION OF THE NETAPP : " + bcolors.OKGREEN + version)
