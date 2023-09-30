from open_court import GetOpenCourt
from open_court_special import GetOpenCourtSpecial

def start9_11(request):
    GetOpenCourt(9, 11, "人工芝", "Holiday").run()

def start11_13(request):
    GetOpenCourt(11, 13, "人工芝", "Holiday").run()

def start13_15(request):
    GetOpenCourt(13, 15, "人工芝", "Holiday").run()

def start15_17(request):
    GetOpenCourt(15, 17, "人工芝", "Holiday").run()

def start17_19(request):
    GetOpenCourt(17, 19, "人工芝", "MiddleWeek").run()

def start19_21(request):
    GetOpenCourt(19, 21, "人工芝", "Holiday").run()

def f():
    print("Hello, World!!")

def start9_11_special(request):
    GetOpenCourtSpecial(9, 11, "人工芝", "Holiday").run()

def start11_13_special(request):
    GetOpenCourtSpecial(11, 13, "人工芝", "Holiday").run()

def start13_15_special(request):
    GetOpenCourtSpecial(13, 15, "人工芝", "Holiday").run()

def start15_17_special(request):
    GetOpenCourtSpecial(15, 17, "人工芝", "Holiday").run()


# python -c "import main; main.start9_11('dummy')"