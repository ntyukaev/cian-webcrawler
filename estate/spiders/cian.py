import json
import scrapy
import subprocess
from decimal import Decimal
import urllib.parse
import dateutil.parser
from geopy.geocoders import Nominatim
from scrapy.utils.project import get_project_settings
from ..models import Cian
from ..utils import send_mail


class CianSpider(scrapy.Spider):
    name = "cian"
    domain = "cian.ru"
    allowed_domains = [domain]

    def __init__(
        self,
        location,
        minprice,
        maxprice,
        zoom=0.001,
        step=0.001,
        room1=1,
        room2=0,
        room3=0,
        room4=0,
        engine_version=2,
        deal_type="sale",
        offer_type="flat",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.zoom = float(zoom)
        self.step = float(step)
        self.room1 = int(room1)
        self.room2 = int(room2)
        self.room3 = int(room3)
        self.room4 = int(room4)
        self.location = str(location)
        self.minprice = int(minprice)
        self.maxprice = int(maxprice)
        self.deal_type = str(deal_type)
        self.offer_type = str(offer_type)
        self.engine_version = int(engine_version)
        project_settings = get_project_settings()
        geolocator = Nominatim(user_agent=project_settings.get("USER_AGENT"))
        parsed_location = geolocator.geocode(self.location)
        self.latitude = float(parsed_location.latitude)
        self.longitude = float(parsed_location.longitude)
        self.updates = []

    def get_coord_polygon(self, latitude: Decimal, longitude: Decimal):
        return [
            (
                Decimal(latitude) - Decimal(self.step),
                Decimal(longitude) - Decimal(self.step),
            ),
            (
                Decimal(latitude) + Decimal(self.step),
                Decimal(longitude) - Decimal(self.step),
            ),
            (
                Decimal(latitude) + Decimal(self.step),
                Decimal(longitude) + Decimal(self.step),
            ),
            (
                Decimal(latitude) - Decimal(self.step),
                Decimal(longitude) + Decimal(self.step),
            ),
        ]

    def start_requests(self):
        yield scrapy.Request(url="https://cian.ru/map", callback=self.get_map)

    def get_map(self, _):
        left_latitude = Decimal(self.latitude) - Decimal(self.zoom)
        right_latitude = Decimal(self.latitude) + Decimal(self.zoom)
        right_longitude = Decimal(self.longitude) + Decimal(self.zoom)
        count = 0
        while left_latitude < right_latitude:
            left_longitude = Decimal(self.longitude) - Decimal(self.zoom)
            while left_longitude < right_longitude:
                coord_polygon = self.get_coord_polygon(
                    latitude=left_latitude, longitude=left_longitude
                )
                left_longitude += Decimal(self.step)
                params = {
                    "engine_version": self.engine_version,
                    "deal_type": self.deal_type,
                    "minprice": self.minprice,
                    "maxprice": self.maxprice,
                    "offer_type": self.offer_type,
                    "room1": self.room1,
                    "room2": self.room2,
                    "room3": self.room3,
                    "room4": self.room4,
                    "in_polygon[0]": ",".join(
                        [
                            "_".join([str(coord) for coord in angle])
                            for angle in coord_polygon
                        ]
                    ),
                }
                count += 1
                url = f"https://cian.ru/ajax/map/roundabout/?{urllib.parse.urlencode(params)}"
                yield scrapy.Request(url, callback=self.get_roundabout)
            left_latitude += Decimal(self.step)

    def get_roundabout(self, response):
        json_response = json.loads(response.body)
        link_template = json_response["data"]["link_template"]
        for point in json_response["data"]["points"].values():
            for offer in point["offers"]:
                _id = offer["id"]
                yield scrapy.Request(
                    url=link_template.format().format(id=_id), callback=self.get_offer
                )

    def close(self):
        if self.updates:
            send_mail("\n".join(self.updates))

    def get_offer(self, response):
        script = (
            response.selector.xpath(
                "//script[@type='text/javascript' and contains(text(), 'frontend-offer-card') and contains(text(), 'window._cianConfig')]/text()"
            )
            .get()
            .replace("\n", "")
            .replace("'", '"')
        )
        data = json.loads(
            subprocess.check_output(
                [
                    "node",
                    "-e",
                    f"let window={{}};{script};console.log(JSON.stringify(window._cianConfig['frontend-offer-card'].find((item) => item.key === 'defaultState')?.value?.offerData))",
                ]
            )
        )

        cian = Cian(
            id=int(data.get("offer").get("id")),
            category=data.get("offer").get("category"),
            status=data.get("offer").get("status"),
            deal_type=data.get("offer").get("dealType"),
            offer_type=data.get("offer").get("offerType"),
            address=", ".join(
                [
                    part.get("fullName")
                    for part in data.get("offer").get("geo", {}).get("address", [])
                ]
            ),
            photos=json.dumps(
                {
                    "photos": [
                        photo.get("fullUrl")
                        for photo in data.get("offer").get("photos", [])
                    ]
                }
            ),
            lat=data.get("offer").get("geo", {}).get("coordinates", {}).get("lat"),
            lng=data.get("offer").get("geo", {}).get("coordinates", {}).get("lng"),
            description=data.get("offer").get("description"),
            phones=json.dumps(data.get("offer").get("phones", {})),
            flat_type=data.get("offer").get("flatType"),
            total_area=data.get("offer").get("totalArea"),
            living_area=data.get("offer").get("livingArea"),
            kitchen_area=data.get("offer").get("kitchenArea"),
            balcony_count=data.get("offer").get("balconiesCount"),
            separate_wc_count=data.get("offer").get("separateWcsCount"),
            combined_wc_count=data.get("offer").get("combinedWcsCount"),
            repair_type=data.get("offer").get("repairType"),
            room_count=data.get("offer").get("roomsCount"),
            floor_number=data.get("offer").get("floorNumber"),
            mortgage_allowed=data.get("offer")
            .get("bargainTerms", {})
            .get("mortgageAllowed"),
            sale_type=data.get("offer").get("bargainTerms", {}).get("saleType"),
            edit_date=int(dateutil.parser.parse(edit_date).timestamp())
            if (edit_date := data.get("offer").get("editDate"))
            else None,
            publication_date=data.get("offer").get("publicationDate"),
            price=data.get("offer").get("priceTotal"),
            price_per_square=data.get("priceInfo", {}).get("pricePerSquareValue"),
            pdf_url=data.get("offer").get("exportLinks", {}).get("pdfUrl"),
            docx_url=data.get("offer").get("exportLinks").get("docxUrl"),
            year_built=data.get("bti", {}).get("houseData", {}).get("yearRelease"),
            house_material_type=data.get("offer")
            .get("building", {})
            .get("materialType"),
            floor_count=data.get("offer").get("building", {}).get("floorsCount"),
            entrance_count=data.get("bti", {}).get("houseData", {}).get("entrances"),
            total_visitors=data.get("stats", {}).get("total"),
            url=response.url,
        )
        yield {"data": cian}
