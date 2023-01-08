import csv
import math as m

import outputtypes as out
from typing import Callable
class Party:
    def __init__(self, name="", votesNum=0, originalSeat=0, newSeats = 0, originalPartiesTuple: tuple=None) -> None:
        self.name = name#[::-1] # reverse hebrew string
        if isinstance(votesNum, str):
            self.votes = int(votesNum.replace(',', ''))
        else:
            self.votes = votesNum
        self.seats = int(originalSeat)
        self.newSeats = newSeats
        self.originalParties = originalPartiesTuple
    
    def __add__(self, other):
        resultParty = Party(self.name+"+"+other.name, self.votes+other.votes, 0, self.newSeats+other.newSeats, (self, other))
        return resultParty

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

def hanington_hil(s, y=None):
    return m.sqrt(s*(s+1))

def jeffersonsF(s, none):
    return s+1

def webstersF(s, none):
    return s+0.5

def generalF(s, y):
    return s+1-y

def initializePartiesFromFile(filename) -> list:
    """creates a list of Party according to a csv file"""
    parties = list()
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            parties.append(Party(row[0], row[1], row[2]))
    return parties

def sumGoodVotes(parties: list) -> int:
    """returns a sum of good votes in this election (Gets a party list)
    >>> sumGoodVotes([Party(votesNum=50),Party(votesNum=70)])
    120"""
    sum = 0
    for party in parties:
        sum += party.votes
    return sum

def apportionmentAlgorithm(start:int, end:int, methodFunction: callable, parties:list, y=None):
    """
    uses hamiltons method: (party votes)/f(party current seats)
    for each iteration gives one seat to the party the maximizes (party votes)/f(party current seats)
    f is parameter 'methodFunction'
    """
    quotient = list()
    for party in parties:
        quotient.append(0)

    for i in range(start, end):
        for index, party in enumerate(parties):
            quotient[index] = party.votes/methodFunction(party.newSeats,y)
        max_index = quotient.index(max(quotient))
        parties[max_index].newSeats += 1

def electionsAlgorithm(parties: list, seats: int = 120) -> int:
    """
    allocate seats to each party according to [(the amount of good votes) divided by (the amount of seats) (rounded down)]
    returns the amount of unalloccated seats (were not allocated due to rounding)
    >>> electionsAlgorithm([Party(votesNum=50),Party(votesNum=70)])
    120
    >>> electionsAlgorithm([Party("ot1", 200, 0), Party("ot2", 400, 0), Party("ot3", 150, 0), Party("ot4", 1000, 0)])
    118
    """
    seatCostInVotes = sumGoodVotes(parties=parties)/seats
    allocatedSeats = 0
    for party in parties:
        party.newSeats = int(party.votes/seatCostInVotes)
        allocatedSeats += party.newSeats
    return allocatedSeats

def elections(algorithm: Callable, input,  outtype: out.OutputType ,combinedTuples=None):
    """
    Gets an algrithm (callable), input(str or list(Party)), combinedTuples(list(tuple)) and outtype
    1.Handles the different kinds of inputs, 
    2.Performs the algorithm according to the requested algorithm
    3.Handles the output according to the requested output

    usage examples:
    >>> elections(webstersF, [Party("ot1", 200, 0), Party("ot2", 400, 0), Party("ot3", 50, 0), Party("ot4", 1000, 0)], outtype=out.oneLineOutput)
    1to, 15 | 2to, 29 | 3to, 4 | 4to, 72 | 
    >>> elections(jeffersonsF, [Party("ot1", 200, 0), Party("ot2", 400, 0), Party("ot3", 50, 0), Party("ot4", 1000, 0)], outtype=out.oneLineOutput)
    1to, 14 | 2to, 29 | 3to, 3 | 4to, 74 | 
    """

    """1. Handles the input:"""
    if isinstance(input, str):
        parties = initializePartiesFromFile(input)
    else:
        parties = input
    # create combinedParties for agreed upon deals according to a list of tuples (combinedTuples)
    if combinedTuples:
        usedIndex = list()
        combinedParties = list()
        for tuple in combinedTuples:
            party = parties[tuple[0]]
            usedIndex.append(tuple[0])
            for i in tuple[1:]:
                party += parties[i]
                usedIndex.append(i)
            combinedParties.append(party)
        for index, party in enumerate(parties):
            if index not in usedIndex:
                combinedParties.append(party)
    else:
        combinedParties = parties

    """2. Performs the algorithm:"""
    # allocate seats and return the amount of allocated seats    
    allocatedSeats = electionsAlgorithm(parties=combinedParties)
    # For each unallocated seats, run an algorithm to allocate the seats according to a method functuin
    apportionmentAlgorithm(start=allocatedSeats, end=120, methodFunction=algorithm, parties=combinedParties)
    # for each combined party, divide the seats according to the same algorithm we used for all the parties together
    for party in combinedParties:
        if party.originalParties is not None:
            newPartyList = list(party.originalParties)
            a = electionsAlgorithm(parties=newPartyList, seats=party.newSeats)
            apportionmentAlgorithm(start=a, end=party.newSeats, methodFunction=algorithm, parties=newPartyList)
    
    """3. Handle the output according to request"""
    return outtype.extract_output_from_calculated_list(parties)

if __name__ == "__main__":
    import doctest
    doctest.testmod()