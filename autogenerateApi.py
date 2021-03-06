# -*- encoding: utf-8 -*-

import os
import shutil
import errno


class AnalyzedClass():
    def __init__(self):
        self.className = ""
        self.modulePath = ""
        self.relativePath = ""
        self.fullTargetPath = ""
        self.rstFileContent = ""



class AnalyzedFolder():
    def __init__(self):
        self.folderName = ""
        self.relativePath = ""
        self.fullTargetPath = ""
        self.rstFileContent = ""



class ApiMaker():
    def __init__(self):

        self.thisDir = os.path.dirname(os.path.realpath(__file__))

        self.relativeTargetFolder = "autoGeneratedApi"

        self.targetFolder = os.path.join(self.thisDir, "sphinx", self.relativeTargetFolder)

        self.excludedFolders = [
            ".\\.git",
            ".\\.idea",
            ".\\build",
            ".\\core\includeFileTemplates",
            ".\\officialWebsite",
            ".\\dist",
            ".\\documentation",
            ".\\gui\designerfiles",
            ".\\inkScapeLogos",
            ".\\pyqtgraph",
            ".\\sphinx",
            ".\\testSnippets",
            ".\\tests"
        ]

        self.excludedFiles = [
            ".\\autogenerateApi.py",
            ".\\countLines.py"
        ]

        self.fileContentsForClassesCurrentFolder = list()
        self.fileContentsForCurrentFolder = list()

        self.allClasses = list()
        self.allFolders = list()


    def generateRstFiles(self):

        self.removeTargetFolder()

        self.scanCodeFiles()


        for aFolder in self.allFolders:
            # print aFolder.rstFileContent
            print aFolder.fullTargetPath

        for aClass in self.allClasses:
            # print aClass.rstFileContent
            print aClass.fullTargetPath

        self.writeRstFiles()


    def removeTargetFolder(self):
        try:
            shutil.rmtree(self.targetFolder)
            # print "targetFolder {} deleted".format(self.targetFolder)
        except WindowsError as er:
            if er.args[0] == errno.WSAEADDRNOTAVAIL:
                pass


    def scanCodeFiles(self):
        for root, dirs, files in os.walk("."):

            dirsNotExcluded = list()
            for aDir in dirs:
                relativeDirPath = os.path.join(root, aDir)
                if relativeDirPath not in self.excludedFolders:
                    dirsNotExcluded.append(aDir)
            dirs[:] = dirsNotExcluded

            filesNotExcluded = list()
            for aFile in files:
                relativeFilePath = os.path.join(root, aFile)
                if relativeFilePath not in self.excludedFiles:
                    filesNotExcluded.append(aFile)
            files[:] = filesNotExcluded



            for fileName in files:
                if not fileName.endswith(".py"):
                    continue
                # print root, fileName
                self.generateRstForClasses(root, fileName)


            self.generateRstForFolder(root, dirs)

            for generatedFolder in self.fileContentsForCurrentFolder:
                self.allFolders.append(generatedFolder)
            self.fileContentsForCurrentFolder = list()

            for generatedClass in self.fileContentsForClassesCurrentFolder:
                self.allClasses.append(generatedClass)
            self.fileContentsForClassesCurrentFolder = list()


    def writeRstFiles(self):
        for analyzedClass in self.allClasses:
            targetFolder = os.path.split(analyzedClass.fullTargetPath)[0]
            if not os.path.isdir(targetFolder):
                os.makedirs(targetFolder)
            with open(analyzedClass.fullTargetPath, "w") as f:
                f.write(analyzedClass.rstFileContent)

        for analyzedFolder in self.allFolders:
            targetFolder = os.path.split(analyzedFolder.fullTargetPath)[0]
            if not os.path.isdir(targetFolder):
                os.makedirs(targetFolder)
            with open(analyzedFolder.fullTargetPath, "w") as f:
                f.write(analyzedFolder.rstFileContent)


    def generateRstForClasses(self, root, fileName):
        filePath = os.path.join(root, fileName)

        filePathSphinxFormat = filePath[ : filePath.find(".py")]

        filePathSphinxFormat = filePathSphinxFormat.lstrip(".\\").replace("\\", ".").lstrip(".")


        # print filePathSphinxFormat

        for className in self.findClassesOfModuleFile(filePath):
            className = className.lstrip(".")
            headLineMark = "=" * len(className)
            modulePath = filePathSphinxFormat
            modulePath = modulePath + "." + className
            modulePath = modulePath.lstrip(".")

            templateString = \
                "{className}\n" \
                "{headLineMark}\n\n" \
                ".. autoclass:: {pathToClass}\n" \
                "    :members:\n" \
                "    :undoc-members:\n" \
                "    :show-inheritance:\n\n"

            templateString = templateString.format(className=className,
                                                   headLineMark=headLineMark,
                                                   pathToClass=modulePath)

            analyzedClass = AnalyzedClass()
            analyzedClass.className = className
            analyzedClass.modulePath = modulePath
            analyzedClass.relativePath = filePath.lstrip(".\\")

            fileFolder, fileName = os.path.split(analyzedClass.relativePath)

            targetFileName = className + ".rst"

            analyzedClass.fullTargetPath = os.path.join(self.targetFolder, fileFolder, targetFileName)


            analyzedClass.rstFileContent = templateString

            self.fileContentsForClassesCurrentFolder.append(analyzedClass)


    def generateRstForFolder(self, folder, subDirs):

        folderName = os.path.split(folder)[-1]

        folderDisplayName = folder.lstrip(".\\")
        folderDisplayName = folderDisplayName.replace("\\", ".")

        if len(folderDisplayName) == 0:
            folderDisplayName = "microRay API reference"


        headLineMark = "=" * len(folderDisplayName)
        templateString = \
            "{folderName}\n" \
            "{headLineMark}\n\n" \
            ".. toctree::\n\n"

        templateString = templateString.format(folderName=folderDisplayName,
                                               headLineMark=headLineMark)

        if len(subDirs) > 0:

            for subDir in subDirs:
                relativeSubDirRstFilePath = subDir + "/" + subDir + ".rst"
                templateString += "    {relativeSubDirRstFilePath}\n".format(relativeSubDirRstFilePath=relativeSubDirRstFilePath)


        # if len(self.fileContentsForClassesCurrentFolder) > 0:
        for aClass in self.fileContentsForClassesCurrentFolder:
            templateString += "    {className}\n".format(className=aClass.className)

        analyzedFolder = AnalyzedFolder()
        analyzedFolder.rstFileContent = templateString
        analyzedFolder.relativePath = folder.lstrip(".\\")
        analyzedFolder.folderName = folderName

        relativeFolderPath = folder.lstrip(".\\")
        fullFolderPath = os.path.join(self.targetFolder, relativeFolderPath)

        targetFileName = folderName + ".rst"

        if folderDisplayName == "microRay API reference":
            targetFileName = "microRayAPI" + ".rst"

        fullTargetPath = os.path.join(fullFolderPath, targetFileName)

        analyzedFolder.fullTargetPath = fullTargetPath


        self.fileContentsForCurrentFolder.append(analyzedFolder)


    def findClassesOfModuleFile(self, path):
        foundClasses = list()
        with open(path, "r") as f:
            for line in f:
                if line.startswith("class"):
                    extract = self.extractClassName(line)
                    foundClasses.append(extract)
        return foundClasses


    def extractClassName(self, classInitializationLine):
        modLine = classInitializationLine.lstrip("class ")
        modLine = modLine[ : modLine.find("(")]
        return modLine






def run():
    apiMaker = ApiMaker()
    apiMaker.generateRstFiles()

if __name__ == "__main__":
    run()
    print "sphinx rst-files generated successfully"