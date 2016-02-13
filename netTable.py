from networktables import NetworkTable


class ConnectionListener:

    def __init__(self, path):
        self.path = path

    def connected(self, table):
        with open(self.path, 'a') as f:
            f.write("Connected" + str(table))

    def disconnected(self, table):
        with open(self.path, 'a') as f:
            f.write("Disconnected" + str(table))

def makeNetworkTable(ip='10.16.19.2', tableKey='SmartDashboard'):
    '''Return NetworkTable with specified ip address and tableKey'''
    NetworkTable.setIPAddress(ip)
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    return NetworkTable.getTable(tableKey)
