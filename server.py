from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def main():
    with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()

        def sendMsg(msgTopic, msgHeader, msgText, msgTime):
            try:
                tree = ET.parse('db.xml')
                root = tree.getroot()

                print("\nRequest for new msg\nMsg topic:", msgTopic, "\nMsg header:", msgHeader, "\nMsg text:", msgText, "\nMsg time:", msgTime)
                for elem in root:
                    if elem.attrib['name'] == msgTopic:
                        print("Found existing topic", msgTopic)
                        newNote = ET.SubElement(elem, 'note')
                        newNote.set('name', msgHeader)
                        newNoteText = ET.SubElement(newNote, 'text')
                        newNoteText.text = msgText
                        newNoteTimestamp = ET.SubElement(newNote, 'timestamp')
                        newNoteTimestamp.text = msgTime
                        tree.write('db.xml')
                        return "Added new message to existing topic\n"

                print("Creating new topic", msgTopic)
                newTopic = ET.SubElement(root, 'topic')
                newTopic.set('name', msgTopic)
                newNote = ET.SubElement(newTopic, 'note')
                newNote.set('name', msgHeader)
                newNoteText = ET.SubElement(newNote, 'text')
                newNoteText.text = msgText
                newNoteTimestamp = ET.SubElement(newNote, 'timestamp')
                newNoteTimestamp.text = msgTime
                tree.write('db.xml')
                return "Created new topic and message\n"
            except Exception as e:
                print("Error:", e)

        def getMsg(topic):
            try:
                tree = ET.parse('db.xml')
                root = tree.getroot()

                print("\nRequest for topic:", topic)
                res = []
                for elem in root:
                    if elem.attrib["name"] == topic:
                        res.append(elem.attrib["name"])
                        res.append("\n")
                        for subelem in elem:
                            res.append(subelem.attrib["name"])
                            for msgelem in subelem:
                                res.append(msgelem.text)
                            res.append("\n")
                        return res
                return ["No such topic"]
            except Exception as e:
                print("Error:", e)

        def searchWiki(topic, searchTerms, time):
            try:
                tree = ET.parse('db.xml')
                root = tree.getroot()

                print("\nRequest for wikisearch with search terms:", searchTerms)
                S = requests.Session()
                URL = "https://en.wikipedia.org/w/api.php"
                PARAMS = {
                    "action": "opensearch",
                    "namespace": "0",
                    "search": searchTerms,
                    "limit": "5",
                    "format": "json"
                }

                R = S.get(url=URL, params=PARAMS)
                DATA = R.json()
                
                for elem in root:
                    if elem.attrib['name'] == topic:
                        print("Found existing topic", topic)
                        newNote = ET.SubElement(elem, 'note')
                        newNote.set('name', searchTerms)
                        newNoteText = ET.SubElement(newNote, 'text')
                        newNoteText.text = str(DATA)
                        newNoteTimestamp = ET.SubElement(newNote, 'timestamp')
                        newNoteTimestamp.text = time
                        tree.write('db.xml')
                        return DATA

                print("Creating new topic", topic)
                newTopic = ET.SubElement(root, 'topic')
                newTopic.set('name', topic)
                newNote = ET.SubElement(newTopic, 'note')
                newNote.set('name', searchTerms)
                newNoteText = ET.SubElement(newNote, 'text')
                newNoteText.text = str(DATA)
                newNoteTimestamp = ET.SubElement(newNote, 'timestamp')
                newNoteTimestamp.text = time
                tree.write('db.xml')
                
                return DATA
            except Exception as e:
                print("Error:", e)

        server.register_function(sendMsg, 'sendMsg')
        server.register_function(getMsg, 'getMsg')
        server.register_function(searchWiki, 'searchWiki')

        server.serve_forever()

main()