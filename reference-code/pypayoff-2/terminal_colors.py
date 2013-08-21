class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m' #yellow
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        
        
        
        
def print_warning(text):
    print bcolors.WARNING + text + bcolors.ENDC
    
def print_okblue(text):
    print bcolors.OKBLUE + text + bcolors.ENDC

def print_okgreen(text):
    print bcolors.OKGREEN + text + bcolors.ENDC
    
def print_fail(text):
    print bcolors.FAIL + text + bcolors.ENDC