import struct
from fish import Fish


class FishRepository:
    def __init__(self):
        fishfile = "resources/fishes.bin"
        f = open(fishfile, "rb")
        fishes = {}
        offset = 0
        while True:
            rd = f.read(1244)
            if len(rd) == 1244:
                fsh = Fish.from_bytes(rd)
                fishes[fsh.ID] = fsh
            else:
                break
            offset +=1244
        self.fishes = dict(sorted(fishes.items(), key=lambda t: t[0]))
        self.__verify_constants()

    def __verify_constants(self):
        f0 = self.fishes[0]
        for fish in self.fishes.values():
            if f0.constants != fish.constants:
                print("Constant values are not constant!")
                return False
        return True

    def all_indexed(self) -> dict[int, Fish]:
        return self.fishes
