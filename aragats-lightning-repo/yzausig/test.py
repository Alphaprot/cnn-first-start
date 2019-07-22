

def test():
    print("Please specify input directory as an abs path [or enter skip",
    "to skip this step]:\n")

    imgpath = raw_input()
    if imgpath.lower() == "skip".lower():
        print("Oops")
        return

    if imgpath.endswith("/"):
        imgpath = imgpath[:-1]
        print ("Foo")
    else:
        print("You typed anything else")

test()
