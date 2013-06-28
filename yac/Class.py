

class Class:
    def __init__(self, className, classFile, parentClassName, parentClassFile=None):
        self.className = className
        self.classFile = classFile
        self.parentClassName = parentClassName
        self.parentClassFile = parentClassFile

    def classExists(self):
        return len(self.className) > 0

    def getClassName(self):
        return self.className

    def getParentClassName(self):
        return self.parentClassName

    def getClassFile(self):
        return self.classFile
