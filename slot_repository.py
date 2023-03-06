from slot import Slot

class SlotRepository:
	def __init__(self) -> None:
		slotsfile="resources/slots.bin"
		f=open(slotsfile,"rb")
		slots={}
		while True:
			rd=f.read(340)
			if len(rd)==340:
				sl=Slot.from_bytes(rd)
				slots.update({sl.ID:sl})
			else:
				break
		self.slots=dict(sorted(slots.items(),key=lambda t:t[0]))

	def all_indexed(self) -> dict[int, Slot]:
		return self.slots