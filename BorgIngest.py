"""Script to read from BorgConnect."""
import requests

class BorgConnectIngestor:
    """Class provides to read latest values of BorgConnect attributes listed in a file.
    The file is to be available in the executing directory.
    """
    def __init__(self, addr="localhost"):
        self.borgconnect_addr = addr

    def ingest(self):
        """ Function to read list of attributes from map file.
        Returns a list of value, timestamp."""
        with  open("BC_SMIP_map.csv", "r") as file:
            lines = file.readlines()

        output = []
        for line in lines:
            # each line in the mapping file is in the format [name, borgconnect_id, SMIP_id]
            values = line.split(",")
            try:
                response_value = self.read_value(values[1])
                # Adding to list in the sequence -> SMIP_id, Value, Epochtime
                output.append([values[3].replace("\r\n",""), values[0], values[1], response_value[1], response_value[0]])
            except Exception as exception:
                print("error reading for the id - {0} : {1}".format(values[1], exception))
        return output

    def read_value(self, attribute_id):
        """ Function to consume BorgConnect REST endpoint to read data.
        The BorgConnect demo instance does not take security token, so just doing a GET. """
        url = "http://{0}:8005/resource/data/?device_id={1}".\
            format(self.borgconnect_addr, attribute_id)
        response = requests.get(url)
        obj = response.json()
        #print(obj)
        return obj

if __name__ == "__main__":
    # initialise by providing the IP Address of the BorgConnect Hub from which data is to be read
    ing = BorgConnectIngestor("127.0.0.1")
    output = ing.ingest()
    for line in output:
        print(line)
