import json


class Agent:
    def __init__(self, data):
        self.agent = data["agent"]
        self.description = data["description"]
        self.abilities = data["abilities"]
        self.role = data["role"]["roleName"]
        self.image = data["displayIcon"]

    def printName(self):
        return self.agent

    def printDescription(self):
        return self.description

    def printAbilities(self):
        return self.abilities

    def printRole(self):
        return self.role

    def printImage(self):
        return self.image
