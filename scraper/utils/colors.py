class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    FAIL = RED
    WARNING = YELLOW

    @staticmethod
    def print(text: str, color: str = RESET) -> None:
        print(f"{color}{text}{Colors.RESET}")

