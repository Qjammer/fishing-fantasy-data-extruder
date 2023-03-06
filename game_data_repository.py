from fish import Fish
from fish_repository import FishRepository
from item import Item
from lure import Lure
from lure_repository import LureRepository
from item_repository import ItemRepository
from slot import Slot
from slot_repository import SlotRepository

class GameData:
	def __init__(
		self,
		fishes: dict[int, Fish],
		lures: dict[int, Lure],
		items: dict[int, Item],
		slots: dict[int, Slot]
	):
		self.fishes = fishes
		self.lures = lures
		self.items = items
		self.slots = slots

class GameDataRepository:
	def __init__(
		self,
		fish_repository: FishRepository,
		lure_repository: LureRepository,
		item_repository: ItemRepository,
		slot_repository: SlotRepository
	):
		self.fish_repository = fish_repository
		self.lure_repository = lure_repository
		self.item_repository = item_repository
		self.slot_repository = slot_repository

	@staticmethod
	def init():
		return GameDataRepository(
			FishRepository(),
			LureRepository(),
			ItemRepository(),
			SlotRepository()
		)
	def all(self) -> GameData:
		return GameData(
			self.fish_repository.all_indexed(),
			self.lure_repository.all_indexed(),
			self.item_repository.all_indexed(),
			self.slot_repository.all_indexed()
		)