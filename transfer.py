# encoding=utf8

class transfer:
    content = None
    style  = None
    finish_callback = None

    def __init__(self,args,finish_callback):
        self.content = args.get("content")
        self.style = args.get("style")
        self.finish_callback = finish_callback
        pass

    def process(self):
        pass