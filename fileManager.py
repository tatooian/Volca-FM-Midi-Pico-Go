import sdcard
import machine
import uos

class FileManager:
    def __init__(self, spiChannel, sckPin, mosiPin, misoPin, csPin):
        self.sd_spi = machine.SPI(spiChannel, sck = machine.Pin(sckPin, machine.Pin.OUT), mosi = machine.Pin(mosiPin, machine.Pin.OUT), miso = machine.Pin(misoPin, machine.Pin.OUT))
        self.sd = sdcard.SDCard(self.sd_spi, machine.Pin(csPin))
        self.path = ["sd"]
        self.folderCount = 0

    def __pathToString(self):
        strPath = ""
        for x in self.path:
            strPath = strPath + "/" + x
        return strPath

    def CurrentFolderName(self):
        return self.path[len(self.path)-1]

    def CurrentFolder(self):
        return uos.getcwd()

    def ChangeFolder(self, newPath):
        self.path.append(newPath)
        print(self.__pathToString())
        uos.chdir(self.__pathToString())

    def ParentFolder(self):
        if len(self.path) > 2:
            self.path.pop()
            uos.chdir(self.__pathToString())

    def Mount(self):
        uos.mount(self.sd, "/sd", readonly=True)

    def Unmount(self):
        uos.umount("/sd")

    def CardSize(self):
        return "Size: {} MB".format(self.sd.sectors/2048)

    def FolderList(self):
        mylist = uos.ilistdir()
        folders = []
        for x in mylist:
            if x[1] == 0x4000:
                folders.append(x[0])


        self.folderCount = len(folders)
        folders.sort()
        return folders

    def FolderCount(self):
        return self.folderCount

    def FileList(self):
        mylist = uos.ilistdir()
        files = []
        for x in mylist:
            if x[1] == 0x8000:
                files.append(x[0])
        print("got files from folder: " + self.CurrentFolder())
        return files

    def GetByteArrayFromFile(self, fileName):
        file = self.__pathToString() + "/" + fileName
        with open(file, "rb") as f:
            blob_data = bytearray(f.read())

        f.close()
        return blob_data
