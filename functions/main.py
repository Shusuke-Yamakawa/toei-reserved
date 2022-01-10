from open_court import GetOpenCourt

def start9_11(request):
    GetOpenCourt(9, 11, "人工芝", "Holiday").run()

def start11_13(request):
    GetOpenCourt(11, 13, "人工芝", "Holiday").run()

def start13_15(request):
    GetOpenCourt(13, 15, "人工芝", "Holiday").run()

def start15_17(request):
    GetOpenCourt(15, 17, "人工芝", "Holiday").run()

def start17_19(request):
    GetOpenCourt(17, 19, "人工芝", "Holiday").run()

def start19_21(request):
    GetOpenCourt(19, 21, "人工芝", "Holiday").run()

def f():
    print("Hello, World!!")

# python -c "import main; main.start9_11('dummy')"