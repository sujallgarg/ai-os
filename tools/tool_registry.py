class ToolRegistry:
    def __init_(self):
        self.tool={}
    def register(self,name,func):
        self.tool[name]=func

    def get(self,name):
        return self.tool.get(name)