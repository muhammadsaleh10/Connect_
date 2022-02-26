import requests
import json
key = "APIKEY"
def pprint(d):
	print(json.dumps(d,indent=4)) #format dictionary output well


def place_list(query):
	#inp = "GTBank near Abak road uyo"
	query = "%20".join(query.split()) #need to format the address
	url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={key}"
	resp = requests.get(url).json()
	return [Place(res) for res in resp["results"]]


class Place:
	def __init__(self,GooglePlace):

		"""Just parsing Google's results"""
		self.lat, self.long = GooglePlace["geometry"]["location"]["lat"], GooglePlace["geometry"]["location"]["lng"]
		self.name = GooglePlace["name"] if "name" in GooglePlace else None
		self.open_now = GooglePlace["opening_hours"]["open_now"] if "opening_hours" in GooglePlace else None
		self.rating = GooglePlace["rating"] if "rating" in GooglePlace else None
		self.types = tuple(GooglePlace["types"][:2]) if "types" in GooglePlace else None
		self.vicinity = GooglePlace["vicinity"] if "vicinity" in GooglePlace else None
		self.compound_code = GooglePlace["plus_code"]["compound_code"] if "plus_code" in GooglePlace else None
		self.address = GooglePlace["formatted_address"] if "formatted_address" in GooglePlace else self.vicinity
	def __repr__(self):
		return f"Place(name={self.name},address={self.address})"
	def __str__(self):
		return f"Place(name={self.name},address={self.address})"
	def pprint(self):
		print("Name:",p.name, "\nAddress:",p.address, "\nOpen Now:",p.open_now,"\n")


if __name__ == '__main__':

	inp = "GTBank near Abak road uyo"
	places = place_list(inp)
	for p in places:
		p.pprint()
