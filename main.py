from elections import *

import gspread
import time

def run(url):
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url) 
    sheet1 = spreadsheet.get_worksheet(0)
    document = sheet1.get_all_records()
    
    ListOfParties = []
    ListOfCombinedParties = set()
    votes = 0
    for party in document:
        ListOfParties.append(Party(party['name'][::-1], party['votes'], 0))
        votes += party['votes']
    
    smallParties = []
    smallPartiesObjects = []
    newListOfParties = []
    for index, party in enumerate(ListOfParties):
        if party.votes/votes * 100 <= 3.25:
            print(party.name, "is out")
            smallParties.append(index)
            smallPartiesObjects.append(party)
        else:
            newListOfParties.append(party)
    ListOfParties = newListOfParties

    print([party.name for party in ListOfParties])
    for index, party in enumerate(document):
        if party['with']:
            for innerIndex, innerParty in enumerate(ListOfParties):
                if innerIndex in smallParties or index in smallParties: 
                    continue
                if innerParty.name == party['with'] or innerParty.name == party['with'][::-1]:
                    if (index, innerIndex) not in ListOfCombinedParties and (innerIndex, index) not in ListOfCombinedParties:
                        ListOfCombinedParties.add((index, innerIndex))
                    break
    print(ListOfCombinedParties)
    parties = elections(jeffersonsF, ListOfParties, outtype=out.fullPrintedOutput, combinedTuples=ListOfCombinedParties)
    sheet2 = spreadsheet.get_worksheet(1)

    sheet2.batch_clear(["A1:C111"])
    sheet2.update('A1', "name")
    sheet2.update('B1', "votes")
    sheet2.update('C1', "seats")
    for i in range(len(parties)):
            sheet2.update('A'+str(i+2), parties[i].name[::-1])
            sheet2.update('B'+str(i+2), parties[i].votes)
            sheet2.update('C'+str(i+2), parties[i].newSeats)

    for i in range(len(smallPartiesObjects)):
        sheet2.update('A'+str(len(parties)+i+2), smallPartiesObjects[i].name[::-1])
        sheet2.update('B'+str(len(parties)+i+2), smallPartiesObjects[i].votes)
        sheet2.update('C'+str(len(parties)+i+2), smallPartiesObjects[i].newSeats)