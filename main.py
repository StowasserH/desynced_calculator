#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""A small script that calculates the required factories in Desynced and outputs them as a graphviz diagram.
   https://github.com/StowasserH/desynced_calculator
"""
from __future__ import annotations
import math

__author__ = "harald@stowasser.tv"
__copyright__ = "2023 Harald Stowasser"
__license__ = "MIT"
__maintainer__ = "Harald Stowasser"
__email__ = "harald@stowasser.tv"
__status__ = "Production"


class Component:
    """
        Represents a createable item in Desynced.
    """

    def __init__(self, name: string, time_to_build: float, *args):
        """
            Initializes a buildable item with name, build time and required components.

            :param name: The displayed name of the item
            :param time_to_build: The time in seconds to build the item
            :param args: List of components as list[SubCompos]
        """
        self.tree: list = None
        self.factories: dict = None
        self.name = name
        self.subs: list[SubCompos] = list()
        self.time_to_build: float = time_to_build
        for comp in args:
            self.subs.append(comp)

    def append(self, component: Component, nr, pos=1):
        """
            appends a component to the internal lists

            :param component: The component to add
            :param nr: number of the needed factories
            :param pos: level of indentation
        """
        self.tree.append((component, nr, pos))
        if component.name in self.factories:
            self.factories[component.name] = self.factories[component.name] + nr
        else:
            self.factories[component.name] = nr

    def count_factorys(self, nr=1):
        """
            Calculates the required factories for this component and its subcomponents.

            :param nr: How many factories for this component do you want to build?
        """
        self.factories = dict()
        self.tree = list()
        print(self.name + ":  " + str(nr))
        self.append(self, nr)
        self.__count_factorys(self, 1, nr)
        print(self.factories)

    def merge_component(self, component: Component):
        for fac in component.factories.keys():
            nr = math.ceil(component.factories[fac])
            if fac in self.factories:
                if nr > self.factories[fac]:
                    self.factories[fac] = nr
            else:
                self.factories[fac] = nr
        for fac in component.tree:
            self.tree.append(fac)


    def create_dot(self):
        """
            After a successful count_factorys call, a chart for Graphviz can be generated using this method.
        """
        print("digraph {")
        for fac in self.factories.keys():
            nr = math.ceil(self.factories[fac])
            print("  " + fac + " [label=\"" + fac + " " + str(nr) + "\"] ")
        check_double = dict()
        for fac in self.tree:
            component, nr, pos = fac
            for sub in component.subs:
                out = "  " + sub.component.name + " -> " + component.name
                if out in check_double:
                    pass
                else:
                    print(out)
                    check_double[out] = True
        print("}")

    def __count_factorys(self, component: Component, pos=1, nr=1):
        """
            Recursive component for the count_factorys method.

            :param component: The component to add
            :param pos: level of indentation
            :param nr: number of the needed factories
        """
        for sub in component.subs:
            su_time = sub.component.time_to_build * sub.count
            dur_time = nr * su_time / component.time_to_build
            print("  " * pos + sub.component.name + ":  " + str(dur_time))
            self.append(sub.component, dur_time, pos + 1)
            self.__count_factorys(sub.component, pos + 1, dur_time)


class SubCompos:
    """
        Provides a SubComponent and a counter for how many of these are needed to build the parent.
    """

    def __init__(self, component: Component, count: int):
        """
             Initializes a SubComponent.

            :param component: The component
            :param count: how many of these
         """
        self.component = component
        self.count = count


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    iron_ore = Component("iron_ore", 3)
    iron_ingot = Component("iron_ingot", 4, SubCompos(iron_ore, 1))
    iron_plate = Component("iron_plate", 6, SubCompos(iron_ingot, 2))
    iron_hardend_plate = Component("iron_hardend_plate", 8, SubCompos(iron_ingot, 2), SubCompos(iron_plate, 1))
    cristal = Component("cristal", 2.4)
    energy_plate = Component("energy_plate", 30, SubCompos(cristal, 6), SubCompos(iron_hardend_plate, 2))
    silica = Component("silica", 3)

    coil = Component("coil", 16, SubCompos(silica, 1), SubCompos(iron_plate, 1))
    silicium = Component("silicium", 16, SubCompos(silica, 1))
    cable = Component("cable", 20, SubCompos(coil, 2), SubCompos(cristal, 2), SubCompos(silicium, 2))

    circuit = Component("circuit", 12, SubCompos(cristal, 5), SubCompos(iron_plate, 3))
    frame = Component("frame", 40, SubCompos(cable, 3), SubCompos(energy_plate, 2))

    cristal_powder = Component("cristal_powder", 10, SubCompos(silica, 2), SubCompos(cristal, 5))
    datacube = Component("data_core", 20, SubCompos(cristal_powder, 1), SubCompos(frame, 1))
    cristal_core = Component("cristal_core", 20, SubCompos(energy_plate, 2), SubCompos(cristal_powder, 2))

    optic_cable = Component("optic_cable", 10, SubCompos(cristal_core, 2), SubCompos(cable, 2))
    matrix = Component("matrix", 64, SubCompos(optic_cable, 4), SubCompos(frame, 2))
    robotic = Component("robotic", 60, SubCompos(matrix, 1), SubCompos(datacube, 1))

    electrodes = Component("electrodes", 60, SubCompos(matrix, 1), SubCompos(datacube, 1))
    citin= Component("citin", 30)
    infected_circuit = Component("infected_circuit", 24, SubCompos(circuit, 1), SubCompos(citin, 1))
    virus_datacube = Component("virus_datacube", 16, SubCompos(infected_circuit, 1), SubCompos(datacube, 1))
    virus_research = Component("virus_research", 30, SubCompos(virus_datacube, 1), SubCompos(matrix, 1))
    ic_chip = Component("ic_chip", 40, SubCompos(cable,5), SubCompos(silicium, 5), SubCompos(circuit, 5))
    blight_cristal = Component("blight_cristal", 5)
    laterite = Component("laterite", 6)

    aluminium_rod = Component("aluminium_rod", 16,SubCompos(laterite, 5),SubCompos(iron_ore, 1))
    aluminium_sheet = Component("aluminium_sheet", 24, SubCompos(aluminium_rod, 2), SubCompos(silica, 1))
    blight_bar = Component("blight_bar", 22, SubCompos(iron_ingot, 2), SubCompos(blight_cristal, 5))
    transformer = Component("transformer", 10, SubCompos(cristal, 1), SubCompos(iron_hardend_plate,1))
    reaktor = Component("reaktor", 10, SubCompos(blight_bar, 1), SubCompos(transformer, 1))
    human_datacube = Component("human_datacube", 80, SubCompos(laterite, 5), SubCompos(blight_cristal, 1))
    human_research = Component("human_research", 24, SubCompos(human_datacube, 1), SubCompos(matrix, 1))
    engine = Component("engine", 16, SubCompos(aluminium_sheet, 10), SubCompos(reaktor, 1))
    low_frame=Component("low_frame",24, SubCompos(aluminium_sheet,4),   SubCompos(aluminium_rod,4))
    satellites = Component("satellites",2000, SubCompos(engine,80), SubCompos(human_research, 80), SubCompos(low_frame,80))
    obsidian = Component("obsidian", 10)
    blight_extraction = Component("blight_extraction", 22)
    blight_plasma = Component("blight_plasma", 30, SubCompos(blight_cristal, 5), SubCompos(blight_extraction, 20))
    blight_datacube = Component("blight_datacube", 24, SubCompos(blight_plasma, 5), SubCompos(datacube, 1))
    blight_research = Component("blight_research", 24, SubCompos(blight_datacube, 1), SubCompos(matrix, 1))
    ic_chip = Component("ic_chip", 20, SubCompos(cable, 15), SubCompos(silicium, 5), SubCompos(circuit, 5))
    microprocessor = Component("microprocessor", 20, SubCompos(blight_cristal, 10), SubCompos(blight_plasma, 5),
                               SubCompos(ic_chip, 1))

    robotic.count_factorys(4)
    electrodes.count_factorys(4)
    ic_chip.count_factorys(4)
    virus_research.count_factorys(2)
    ic_chip.count_factorys(2)
    human_research.count_factorys(2)
    microprocessor.count_factorys(2)
    blight_research.count_factorys(2)
    satellites.count_factorys(2)
    datacube.count_factorys(6)
    robotic.merge_component(electrodes)
    robotic.merge_component(ic_chip)
    robotic.merge_component(virus_research)
    robotic.merge_component(ic_chip)
    robotic.merge_component(human_research)
    robotic.merge_component(microprocessor)
    robotic.merge_component(blight_research)
    robotic.merge_component(satellites)
    robotic.merge_component(datacube)
    robotic.create_dot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
