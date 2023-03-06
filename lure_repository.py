from lure import Lure

class LureRepository:
	def __init__(self) -> None:
		lurefile="resources/lures.bin"
		f=open(lurefile,"rb")
		lures={}
		while True:
			rd=f.read(364)
			if len(rd)==364:
				lr=Lure.from_bytes(rd)
				lures.update({lr.ID:lr})
			else:
				break
		self.lures=dict(sorted(lures.items(),key=lambda t:t[0]))

	def all_indexed(self) -> dict[int, Lure]:
		return self.lures