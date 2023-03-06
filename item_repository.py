from item import Item

class ItemRepository:
	def __init__(self) -> None:
		itemfile="resources/items.bin"
		f=open(itemfile,"rb")
		items={}
		while True:
			rd=f.read(328)
			if len(rd)==328:
				it=Item.from_bytes(rd)
				items.update({it.ID:it})
			else:
				break
		self.items=dict(sorted(items.items(),key=lambda t:t[0]))

	def all_indexed(self) -> dict[int, Item]:
		return self.items