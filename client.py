import xmlrpc.client
import datetime

def main():
    s = xmlrpc.client.ServerProxy('http://localhost:8000', allow_none=True)
    userInput = 0
    
    while True:
        print("1) Send msg")
        print("2) Get topic msgs")
        print("3) Search wikipedia")
        print("0) Quit")
        try:
            userInput = int(input("Choice: "))

            if userInput == 0:
                break

            elif userInput == 1:
                #SEND MSG
                msgTopic = input("Give msg topic: ")
                msgHeader = input("Give msg header: ")
                msgText = input("Give msg text: ")
                msgTime = datetime.datetime.now().strftime("%c")
                print("\nMessage topic:", msgTopic, "\nMessage text:", msgText, "\nMessage time:", msgTime, "\n")
                res = s.sendMsg(msgTopic, msgHeader, msgText, msgTime)
                print(res)

            elif userInput == 2:
                #GET MSG
                topic = input("Give topic to fetch: ")
                res = s.getMsg(topic)
                for i in res:
                    print(i)

            elif userInput == 3:
                #SEARCH WIKIPEDIA
                topic = input("Give topic: ")
                searchTerms = input("Give search terms to search with: ")
                time = datetime.datetime.now().strftime("%c")
                res = s.searchWiki(topic, searchTerms, time)
                print(res)

            else:
                print("Unknown input")
        except Exception as e:
            print("Error:", e)

        


main()