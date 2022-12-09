import unittest
import Agent

data = {
    "agent": "NAME",
    "description": "DESC",
    "abilities": "ABILITIES",
    "role": {"roleName": "EXAMPLE ROLE"},
    "displayIcon": "example",
}


class TestAgent(unittest.TestCase):
    # Assure printName works
    def test_printname(self):
        a = Agent.Agent(data)
        self.assertEqual(a.printName(), "NAME")

    # Assure printDescription works
    def test_printdescription(self):
        a = Agent.Agent(data)
        self.assertEqual(a.printDescription(), "DESC")

    # Assure printAbilities works
    def test_printabilities(self):
        a = Agent.Agent(data)
        self.assertEqual(a.printAbilities(), "ABILITIES")

    def test_printrole(self):
        a = Agent.Agent(data)
        self.assertEqual(a.printRole(), "EXAMPLE ROLE")

    def test_printimage(self):
        a = Agent.Agent(data)
        self.assertEqual(a.printImage(), "example")
