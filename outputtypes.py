from abc import ABC
from typing import Callable
import csv 
from elections import *

class OutputType(ABC):
    @classmethod
    def extract_output_from_calculated_list(cls, list: list) -> list:
        """
        return the desired output
        """
        raise NotImplementedError("Choose a specific output type")

class fullPrintedOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        print("\t"+"          ", "\t| S E A T S |")
        print("\t"+"party name", "\t","new","\t", "IRL")
        for party in parties:
            print("\t"+party.name, "\t",party.newSeats,"\t", party.seats)
        return parties

class shortPrintedOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        print("\t"+"     ", "\t| S E A T S |")
        print("\t"+"party name", "\t","new","\t")
        for party in parties:
            print("\t"+party.name, "\t",party.newSeats,"\t")
        return parties

class fullCsvOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        with open('newresults.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['votes', 'seats', 'name'])
            for party in parties:
                csvwriter.writerow([party.name[::-1], party.votes,party.newSeats])
        return parties

class shortCsvOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        with open('newresults.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['seats', 'name'])
            for party in parties:
                csvwriter.writerow([party.name[::-1], party.newSeats])
        return parties

class biggestPartyOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        max = 0
        name = ""
        for party in parties:
            if party.newSeats > max:
                max = party.newSeats
                name = party.name
        print("\t"+name, "\t",max,"\t")
        return parties

class oneLineOutput(OutputType):
    @classmethod
    def extract_output_from_calculated_list(cls, parties: list) -> list:
        for party in parties:
            print(party.name+", "+str(party.newSeats)+" | ", end="")
        return parties