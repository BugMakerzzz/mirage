### Some template and default settings in our work

# commonsense relation from atomic-2020
ATLOC = 'AtLocation'
OBJUSE = 'ObjectUse'
MADEUP = 'MadeUpOf'
HASPRO = 'HasProperty'
CAPAOF = 'CapableOf'
DESIRE = 'Desires'
ISA = 'IsA'
REL_LIST = [ATLOC, OBJUSE, MADEUP, HASPRO, CAPAOF, DESIRE, ISA]

# different template format of the commonsense example generation
CASE_FORMAT_LIST = ['..., then ...', '..., so ...', '..., and ...', '..., but ...', '..., after that, ...', 'Before ..., ...']

# openai config
OPENAI_API_KEY = ''
MAX_REQUESTS_PER_MINUTE = 3500 # 3_000 * 0.5
MAX_TOKENS_PER_MINUTE = 90000 #250_000 * 0.5
REQUEST_URL = ''


llama3_8b_base_path = '/mnt/usercache/huggingface/Meta-Llama-3-8B'
llama3_8b_chat_path = '/mnt/usercache/huggingface/Meta-Llama-3-8B-Instruct'
llama3_70b_chat_path = '/mnt/usercache/huggingface/Meta-Llama-3-70B-Instruct'
llama2_13b_base_path = '/mnt/usercache/huggingface/Llama-2-13b-hf'
llama2_13b_chat_path = '/mnt/usercache/huggingface/Llama-2-13b-chat-hf'
vicuna_13b_base_path = '/mnt/usercache/huggingface/vicuna-13b'
mistral_7b_base_path = '/mnt/usercache/huggingface/Mistral-7B-v0.1'
mistral_7b_chat_path = '/mnt/usercache/huggingface/Mistral-7B-Instruct-v0.2'
qwq_32b_path = '/mnt/usercache/huggingface/QwQ-32B-Preview'
marco_o1_path = '/mnt/publiccache/huggingface/Marco-o1'

pisces_types = [
    "Salmon",
    "Tuna",
    "Trout", 
    "Cod",
    "Herring",
    "Mackerel",
    "Bass",
    "Perch",
    "Sardine",
    "Snapper"
]

amphibia_types = [
    "Frog",
    "Toad",
    "Salamander",
    "Newt",
    "Caecilian",
    "Tree Frog",
    "Bullfrog",
    "Mudpuppy",
    "Axolotl",
    "Tadpole"
]

reptilia_types = [
    "Lizard",
    "Snake",
    "Turtle",
    "Tortoise",
    "Crocodile",
    "Alligator",
    "Gecko",
    "Chameleon",
    "Iguana",
    "Monitor Lizard"
]

aves_types = [
    "Eagle",
    "Sparrow",
    "Parrot",
    "Penguin",
    "Owl",
    "Duck",
    "Hawk",
    "Flamingo",
    "Pigeon",
    "Swan"
]

mammalia_types = [
    "Tiger",
    "Elephant",
    "Dog",
    "Cat",
    "Horse",
    "Dolphin",
    "Bat",
    "Kangaroo",
    "Lion",
    "Whale"
]

animal_types = {
    "Pisces":pisces_types,
    "Amphibia":amphibia_types,
    "Reptilia":reptilia_types,
    "Aves":aves_types,
    "Mammalia":mammalia_types
}


vegetables_types = [
    "Carrot",
    "Broccoli",
    "Spinach",
    "Potato",
    "Tomato",
    "Cucumber",
    "Pepper",
    "Onion",
    "Garlic",
    "Lettuce"
]

fruits_types = [
    "Apple",
    "Banana",
    "Orange",
    "Grapes",
    "Strawberry",
    "Pineapple",
    "Mango",
    "Blueberry",
    "Watermelon",
    "Cherry"
]

grains_types = [
    "Rice",
    "Wheat",
    "Oats",
    "Barley",
    "Corn",
    "Quinoa",
    "Rye",
    "Millet",
    "Sorghum",
    "Buckwheat"
]

dairy_types = [
    "Milk",
    "Cheese",
    "Yogurt",
    "Butter",
    "Cream",
    "Ice Cream",
    "Cottage Cheese",
    "Sour Cream",
    "Ghee",
    "Buttermilk"
]

meats_types = [
    "Chicken",
    "Beef",
    "Pork",
    "Lamb",
    "Turkey",
    "Duck",
    "Goat",
    "Venison",
    "Rabbit",
    "Buffalo"
]

food_types = {
    "Vegetables":vegetables_types,
    "Fruits":fruits_types,
    "Grains":grains_types,
    "Dairy":dairy_types,
    "Meat":meats_types
}


furniture_types = [
    "Sofa",
    "Dining table",
    "Chair",
    "Bed",
    "Desk",
    "Wardrobe",
    "Bookshelf",
    "Coffee table",
    "Dresser",
    "Nightstand"
]

vehicles_types = [
    "Car",
    "Bicycle",
    "Motorcycle",
    "Bus",
    "Truck",
    "Train",
    "Airplane",
    "Boat",
    "Helicopter",
    "Scooter"
]

electronics_types = [
    "Smartphone",
    "Laptop",
    "Television",
    "Tablet",
    "Desktop computer",
    "Printer",
    "Camera",
    "Smartwatch",
    "Speakers",
    "Router"
]

clothing_types = [
    "T-shirts",
    "Jeans",
    "Dresses",
    "Jackets",
    "Sweaters",
    "Shorts",
    "Skirts",
    "Socks",
    "Underwear",
    "Hats"
]

tools_types = [
    "Hammer",
    "Screwdriver",
    "Wrench",
    "Pliers",
    "Saw",
    "Drill",
    "Tape measure",
    "Level",
    "Chisel",
    "Utility knife"
]

objects_types = {
    "Tools":tools_types,
    "Vehicles":vehicles_types,
    "Electronics":electronics_types,
    "Furniture":furniture_types,
    "Clothing":clothing_types
}


creation_types = [
    "drawing",
    "writing",
    "painting",
    "sculpting",
    "building",
    "composing",
    "designing",
    "coding",
    "crafting",
    "filming"
]

learning_types = [
    "reading",
    "listening",
    "observing",
    "practicing",
    "experimenting",
    "studying",
    "questioning",
    "discussing",
    "reflecting",
    "mentoring"
]

movement_types = [
    "walking",
    "running",
    "jumping",
    "swimming",
    "cycling",
    "dancing",
    "climbing",
    "stretching",
    "lifting",
    "skating"
]

rest_types = [
    "sleeping",
    "napping",
    "meditating",
    "relaxing",
    "daydreaming",
    "lounging",
    "bathing",
    "reclining",
    "sitting",
    "deep breathing"
]

socialization_types = [
    "conversing",
    "meeting",
    "celebrating",
    "networking",
    "collaborating",
    "playing games",
    "attending events",
    "sharing meals",
    "mentoring",
    "volunteering"
]

activities_types = {
    "creation":creation_types,
    "learning":learning_types,
    "movement":movement_types,
    "rest":rest_types,
    "socialization":socialization_types
}


educators_types = [
    "Teacher",
    "Professor",
    "Tutor",
    "Instructor",
    "Trainer",
    "Coach",
    "Mentor",
    "Facilitator",
    "Lecturer",
    "Advisor"
]

healers_types = [
    "Doctor",
    "Nurse",
    "Therapist",
    "Chiropractor",
    "Acupuncturist",
    "Herbalist",
    "Psychiatrist",
    "Surgeon",
    "Paramedic",
    "Physical Therapist"
]

artists_types = [
    "Painter",
    "Sculptor",
    "Musician",
    "Dancer",
    "Writer",
    "Photographer",
    "Filmmaker",
    "Graphic Designer",
    "Actor",
    "Illustrator"
]

scientists_types = [
    "Physicist",
    "Chemist",
    "Biologist",
    "Astronomer",
    "Geologist",
    "Mathematician",
    "Ecologist",
    "Geneticist",
    "Meteorologist",
    "Anthropologist"
]

organizers_types = [
    "Project Manager",
    "Event Planner",
    "Logistics Coordinator",
    "Office Manager",
    "Team Leader",
    "Community Organizer",
    "Scheduler",
    "Administrative Assistant",
    "Operations Manager",
    "Coordinator"
]

profession_types = {
    "Educator":educators_types,
    "Healer":healers_types,
    "Artist":artists_types,
    "Scientist":scientists_types,
    "Organizer":organizers_types
}


head_dics = {
    "Food":food_types,
    "Animal":animal_types,
    "Artificial object":objects_types,
    "Hunman activity":activities_types,
    "Profession": profession_types
}

head_rels = {
    "Animal": [ATLOC, CAPAOF, DESIRE, HASPRO],
    "Food":[ATLOC, OBJUSE, HASPRO, MADEUP],
    "Artificial object": [ATLOC, OBJUSE, HASPRO, MADEUP],
    "Hunman activity":[ATLOC, DESIRE, HASPRO, MADEUP],
    "Profession":[ATLOC, CAPAOF, DESIRE, HASPRO],
    "Seraphine": [ATLOC, CAPAOF, DESIRE, HASPRO, MADEUP, OBJUSE],
    "Crython": [ATLOC, CAPAOF, DESIRE, HASPRO, MADEUP, OBJUSE]
}

wumpus_ls = [
    "Zalophane",
    "Brixtor",
    "Glimbari",
    "Xenovark",
    "Trelothian",
    "Vortanix",
    "Qwendal",
    "Lystari",
    "Nexoria",
    "Drakthor"
]

yumpus_ls = [
    "Zorblax", 
    "Quintex", 
    "Maldora", 
    "Vexlorn", 
    "Tralith", 
    "Glimbor", 
    "Jorvix", 
    "Zentara", 
    "Braxian", 
    "Xylith"
]

impus_ls = [
    "Zalquar", 
    "Xenolith", 
    "Vorathic", 
    "Taldros", 
    "Nyvoria", 
    "Glimmar", 
    "Krynos", 
    "Avenara", 
    "Belthos", 
    "Syrillian"
]

lorpus_ls = [
    "Lumirex", 
    "Jynthor", 
    "Dravath", 
    "Pylora", 
    "Quenari", 
    "Xalithor", 
    "Wendara", 
    "Felyra", 
    "Zorveth", 
    "Yalorin"
]

lempus_ls = [
    "Gravorn", 
    "Tymeris", 
    "Velthar", 
    "Lunara", 
    "Frostyn", 
    "Quilaris", 
    "Zenthara", 
    "Melrith", 
    "Ryvaris", 
    "Tormek"
]

rompus_ls = [
    "Zyralor", 
    "Vanthel", 
    "Nyxara", 
    "Krovan", 
    "Pelithor", 
    "Wylena", 
    "Draxis", 
    "Myralon", 
    "Selthic", 
    "Jorvath"
]

grimpus_ls = [
    "Branthor", 
    "Zelvyn", 
    "Xylaris", 
    "Gryndor", 
    "Tynara", 
    "Lorthic", 
    "Quovira", 
    "Fendara", 
    "Syldor", 
    "Merithon"
]

shumpus_ls = [
    "Travenor", 
    "Lycoris", 
    "Zarveth", 
    "Jenthara", 
    "Velmorin", 
    "Phylor", 
    "Wynthor", 
    "Kalithon", 
    "Ryzenor", 
    "Sylaris"
]


zumpus_ls = [
    "Nylath", 
    "Vorenth", 
    "Zyloria", 
    "Morthis", 
    "Praxilon", 
    "Xylindra", 
    "Tavoris", 
    "Glimnor", 
    "Rynthor", 
    "Felvyn"
]

dumpus_ls = [
    "Vandara", 
    "Lothryn", 
    "Xenvar", 
    "Drathil", 
    "Mythoria", 
    "Kaldor", 
    "Zyraxis", 
    "Prython", 
    "Wylthar", 
    "Jorlyn"
]

Seraphine_types = {
    'Wumpus': wumpus_ls, 
    'Yumpus': yumpus_ls, 
    'Impus': impus_ls, 
    'Lorpus': lorpus_ls, 
    'Lempus': lempus_ls
}

Crython_types = {
    'Rompus': rompus_ls,
    'Grimpus': grimpus_ls,
    'Shumpus': shumpus_ls,
    'Zumpus': zumpus_ls,
    'Dumpus': dumpus_ls
}

f_head_dics = {
    "Seraphine": Seraphine_types,
    "Crython": Crython_types
}

sent_prompt_path = '/mnt/userdata/ljc/code/inductive_reason/prompt/generate_sent.json'
train_data_prompt_path = '/mnt/userdata/ljc/code/inductive_reason/prompt/generate_train_data.json'

abstract_objects = [
    "Person", 
    "Animal", 
    "Plant", 
    "Food", 
    "Alcohol", 
    "Disease", 
    "Drug", 
    "Natural Phenomenon", 
    "Condition", 
    "Material", 
    "Substance", 
    "Furniture", 
    "Publication", 
    "Organization", 
    "Authorization", 
    "Facility", 
    "Natural Place", 
    "Event", 
    "Show", 
    "Artwork", 
    "Job", 
    "Game", 
    "Vehicle", 
    "Tool", 
    "Technology", 
    "Electronic Device", 
    "Platform", 
    "Financial Product", 
    "Skill", 
    "Legislation", 
    "Region", 
    "Time Period"
]


locations = [
    "kitchen",
    "living room",
    "bedroom",
    "bathroom",
    "garage",
    "attic",
    "basement",
    "closet",
    "pantry",
    "drawer",
    "shelf",
    "cabinet",
    "desk",
    "table",
    "counter",
    "sofa",
    "bed",
    "chair",
    "nightstand",
    "bookcase",
    "hallway",
    "porch",
    "balcony",
    "backyard",
    "front yard",
    "car",
    "trunk",
    "locker",
    "shed",
    "workshop",
    "office",
    "dining room",
    "laundry room",
    "mudroom",
    "staircase",
    "hall closet",
    "bathroom cabinet",
    "utility room",
    "garden",
    "patio",
    "pool area",
    "roof",
    "cellar",
    "playroom",
    "nursery",
    "guest room",
    "storage unit",
    "gym",
    "studio",
    "attic storage"
]

uses = [
    "writing",
    "cutting",
    "cleaning",
    "cooking",
    "storing",
    "holding",
    "opening",
    "closing",
    "carrying",
    "fixing",
    "repairing",
    "measuring",
    "weighing",
    "mixing",
    "stirring",
    "sitting",
    "lying down",
    "hanging",
    "protecting",
    "decorating",
    "illuminating",
    "charging",
    "connecting",
    "disconnecting",
    "securing",
    "fastening",
    "locking",
    "unlocking",
    "signaling",
    "communicating",
    "listening",
    "watching",
    "reading",
    "writing",
    "drawing",
    "painting",
    "gardening",
    "planting",
    "watering",
    "feeding",
    "grooming",
    "repairing",
    "playing",
    "exercising",
    "training",
    "driving",
    "flying",
    "navigating",
    "recording",
    "filming"
]

materials = [
    "wood",
    "metal",
    "plastic",
    "glass",
    "ceramic",
    "rubber",
    "leather",
    "fabric",
    "paper",
    "cardboard",
    "stone",
    "concrete",
    "brick",
    "clay",
    "steel",
    "aluminum",
    "copper",
    "iron",
    "bronze",
    "brass",
    "gold",
    "silver",
    "platinum",
    "carbon fiber",
    "fiberglass",
    "polyester",
    "nylon",
    "silk",
    "cotton",
    "wool",
    "bamboo",
    "marble",
    "granite",
    "sandstone",
    "pewter",
    "tin",
    "zinc",
    "titanium",
    "kevlar",
    "graphite",
    "porcelain",
    "mica",
    "asphalt",
    "latex",
    "silicone",
    "polyurethane",
    "acrylic",
    "PVC",
    "epoxy"
]

properties = [
    "elegance",
    "simplicity",
    "complexity",
    "ruggedness",
    "sleekness",
    "durability",
    "fragility",
    "modernity",
    "antiquity",
    "sophistication",
    "minimalism",
    "luxury",
    "affordability",
    "practicality",
    "versatility",
    "functionality",
    "portability",
    "stability",
    "flexibility",
    "adaptability",
    "precision",
    "efficiency",
    "effectiveness",
    "reliability",
    "aesthetics",
    "comfort",
    "innovation",
    "tradition",
    "quality",
    "sustainability",
    "eco-friendliness",
    "user-friendliness",
    "compactness",
    "spaciousness",
    "lightness",
    "heaviness",
    "transparency",
    "opacity",
    "brightness",
    "dullness",
    "shininess",
    "matte finish",
    "boldness",
    "subtlety",
    "vibrancy",
    "calmness",
    "warmth",
    "coolness",
    "neutrality"
]

capabilities = [
    "running",
    "jumping",
    "swimming",
    "flying",
    "climbing",
    "digging",
    "crawling",
    "hunting",
    "foraging",
    "grazing",
    "burrowing",
    "nesting",
    "building",
    "hiding",
    "mating",
    "communicating",
    "singing",
    "howling",
    "roaring",
    "barking",
    "purring",
    "chirping",
    "hissing",
    "growling",
    "biting",
    "scratching",
    "stinging",
    "camouflaging",
    "mimicking",
    "playing",
    "nurturing",
    "protecting",
    "territorial marking",
    "migrating",
    "hibernating",
    "molting",
    "shedding",
    "regenerating",
    "photosynthesizing",
    "ruminating",
    "filter feeding",
    "symbiosis",
    "cooperating",
    "forming packs",
    "forming flocks",
    "forming herds",
    "forming colonies",
    "problem-solving"
]

desires = [
    "food",
    "water",
    "shelter",
    "safety",
    "rest",
    "companionship",
    "mating",
    "territory",
    "warmth",
    "comfort",
    "protection",
    "nurturing",
    "play",
    "exploration",
    "social interaction",
    "dominance",
    "affection",
    "attention",
    "grooming",
    "hunting",
    "foraging",
    "nesting",
    "migration",
    "hibernation",
    "security",
    "freedom",
    "movement",
    "exercise",
    "communication",
    "cleanliness",
    "order",
    "routine",
    "predictability",
    "stimulation",
    "curiosity",
    "challenge",
    "variety",
    "breeding",
    "solitude",
    "peace",
    "understanding",
    "learning",
    "control",
    "dominance",
    "territoriality",
    "recognition",
    "achievement",
    "survival"
]

# objects = [
#     "cat",
#     "dog",
#     "bird",
#     "fish",
#     "tree",
#     "car",
#     "bicycle",
#     "book",
#     "phone",
#     "laptop",
#     "table",
#     "chair",
#     "lamp",
#     "sofa",
#     "fridge",
#     "television",
#     "clock",
#     "pencil",
#     "cup",
#     "bottle",
#     "watch",
#     "wallet",
#     "umbrella",
#     "backpack",
#     "shoe",
#     "hat",
#     "glove",
#     "scarf",
#     "camera",
#     "printer",
#     "keyboard",
#     "mouse",
#     "speaker",
#     "guitar",
#     "piano",
#     "bed",
#     "blanket",
#     "pillow",
#     "door",
#     "window",
#     "mirror",
#     "plant",
#     "flower",
#     "rabbit",
#     "horse",
#     "cow",
#     "sheep",
#     "chicken",
#     "snake"
# ]

# rel_tails = {
#     ISA:objects,
#     ATLOC:locations,
#     OBJUSE:uses,
#     CAPAOF:capabilities,
#     MADEUP:materials,
#     DESIRE:desires,
#     HASPRO:properties
# }

example_names = [
    "Zalophane",
    "Brixtor",
    "Glimbari",
    "Xenovark",
    "Trelothian",
    "Vortanix",
    "Qwendal",
    "Lystari",
    "Nexoria",
    "Drakthor",
    "Zorblax", 
    "Quintex", 
    "Maldora", 
    "Vexlorn", 
    "Tralith", 
    "Glimbor", 
    "Jorvix", 
    "Zentara", 
    "Braxian", 
    "Xylith",
    "Zalquar", 
    "Xenolith", 
    "Vorathic", 
    "Taldros", 
    "Nyvoria", 
    "Glimmar", 
    "Krynos", 
    "Avenara", 
    "Belthos", 
    "Syrillian",
    "Lumirex", 
    "Jynthor", 
    "Dravath", 
    "Pylora", 
    "Quenari", 
    "Xalithor", 
    "Wendara", 
    "Felyra", 
    "Zorveth", 
    "Yalorin",
    "Gravorn", 
    "Tymeris", 
    "Velthar", 
    "Lunara", 
    "Frostyn", 
    "Quilaris", 
    "Zenthara", 
    "Melrith", 
    "Ryvaris", 
    "Tormek",
    "Zyralor", 
    "Vanthel", 
    "Nyxara", 
    "Krovan", 
    "Pelithor", 
    "Wylena", 
    "Draxis", 
    "Myralon", 
    "Selthic", 
    "Jorvath",
    "Branthor", 
    "Zelvyn", 
    "Xylaris", 
    "Gryndor", 
    "Tynara", 
    "Lorthic", 
    "Quovira", 
    "Fendara", 
    "Syldor", 
    "Merithon",
    "Travenor", 
    "Lycoris", 
    "Zarveth", 
    "Jenthara", 
    "Velmorin", 
    "Phylor", 
    "Wynthor", 
    "Kalithon", 
    "Ryzenor", 
    "Sylaris",
    "Nylath", 
    "Vorenth", 
    "Zyloria", 
    "Morthis", 
    "Praxilon", 
    "Xylindra", 
    "Tavoris", 
    "Glimnor", 
    "Rynthor", 
    "Felvyn",
    "Vandara", 
    "Lothryn", 
    "Xenvar", 
    "Drathil", 
    "Mythoria", 
    "Kaldor", 
    "Zyraxis", 
    "Prython", 
    "Wylthar", 
    "Jorlyn"
]

default_names = [
    "Tom",
    "Anna",
    "Jack",
    "Emma",
    "Sam",
    "Lily",
    "Max",
    "Eva",
    "Jake",
    "Mia",
    "Ben",
    "Amy",
    "Leo",
    "Zoe",
    "John",
    "Kate",
    "Paul",
    "Ivy",
    "Luke",
    "Ella"
]

default_items = [
    "chairs",
    "tables",
    "pens",
    "cups",
    "bags",
    "lamps",
    "spoons",
    "plates",
    "bottles",
    "shirts",
    "hats",
    "pillows",
    "brushes",
    "forks",
    "shoes"
]

default_foods = [
    "apples",
    "bananas",
    "oranges",
    "carrots",
    "breads",
    "eggs",
    "pastas",
    "potatoes",
    "tomatoes",
    "chickens",
    "fishes",
    "yogurts",
    "cheeses",
    "cucumbers",
    "shrimp"
]

default_cards = [
    'Hearts 1s',
    'Diamond 4s',
    'Hearts 3s',
    'Diamonds 8s',
    'Spade Queens',
    'Diamond 9s',
    'Spade Jacks',
    'Hearts Aces',
    'Club 10s',
    'Club Kings',
    'Club 7s',
    'Diamond 2s',
    'Spade 5s',
    'Jokers',
    'Hearts 6s',
]

default_investments = [
    "stocks classes",
    "bonds",
    "funds",
    "etfs",
    "real estate",
    "commodities",
    "cryptocurrencies",
    "annuities",
    "savings",
    "accounts",
    "securities",
    "loans",
    "mortgages",
    "options",
    "futures"
]

default_subjects = [
    "math classes",
    "science classes",
    "history classes",
    "geography classes",
    "art classes",
    "music classes",
    "physical classes",
    "computer classes",
    "economics classes",
    "chemistry classes",
    "biology classes",
    "literature classes",
    "philosophy classes",
    "technology classes",
    "english classes"
]

default_objects = {
    'trade': default_items,
    'diet': default_foods,
    'magic': default_cards,
    'invest': default_investments,
    'course': default_subjects
}


arbic_to_words_dic = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 
    18: 'eighteen', 19: 'nineteen', 20: 'twenty', 21: 'twenty-one', 22: 'twenty-two', 23: 'twenty-three', 
    24: 'twenty-four', 25: 'twenty-five', 26: 'twenty-six', 27: 'twenty-seven', 28: 'twenty-eight', 
    29: 'twenty-nine', 30: 'thirty', 31: 'thirty-one', 32: 'thirty-two', 33: 'thirty-three', 34: 'thirty-four', 
    35: 'thirty-five', 36: 'thirty-six', 37: 'thirty-seven', 38: 'thirty-eight', 39: 'thirty-nine', 40: 'forty',
    41: 'forty-one', 42: 'forty-two', 43: 'forty-three', 44: 'forty-four', 45: 'forty-five', 46: 'forty-six', 
    47: 'forty-seven', 48: 'forty-eight', 49: 'forty-nine', 50: 'fifty', 51: 'fifty-one', 52: 'fifty-two', 
    53: 'fifty-three', 54: 'fifty-four', 55: 'fifty-five', 56: 'fifty-six', 57: 'fifty-seven', 58: 'fifty-eight', 
    59: 'fifty-nine', 60: 'sixty', 61: 'sixty-one', 62: 'sixty-two', 63: 'sixty-three', 64: 'sixty-four', 
    65: 'sixty-five', 66: 'sixty-six', 67: 'sixty-seven', 68: 'sixty-eight', 69: 'sixty-nine', 70: 'seventy', 
    71: 'seventy-one', 72: 'seventy-two', 73: 'seventy-three', 74: 'seventy-four', 75: 'seventy-five', 
    76: 'seventy-six', 77: 'seventy-seven', 78: 'seventy-eight', 79: 'seventy-nine', 80: 'eighty', 
    81: 'eighty-one', 82: 'eighty-two', 83: 'eighty-three', 84: 'eighty-four', 85: 'eighty-five', 86: 'eighty-six', 
    87: 'eighty-seven', 88: 'eighty-eight', 89: 'eighty-nine', 90: 'ninety', 91: 'ninety-one', 92: 'ninety-two', 
    93: 'ninety-three', 94: 'ninety-four', 95: 'ninety-five', 96: 'ninety-six', 97: 'ninety-seven', 98: 'ninety-eight', 
    99: 'ninety-nine'
}

words_to_arbic_dic = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twenty-one': 21, 'twenty-two': 22, 'twenty-three': 23,
    'twenty-four': 24, 'twenty-five': 25, 'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28, 'twenty-nine': 29,
    'thirty': 30, 'thirty-one': 31, 'thirty-two': 32, 'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35,
    'thirty-six': 36, 'thirty-seven': 37, 'thirty-eight': 38, 'thirty-nine': 39, 'forty': 40, 'forty-one': 41,
    'forty-two': 42, 'forty-three': 43, 'forty-four': 44, 'forty-five': 45, 'forty-six': 46, 'forty-seven': 47,
    'forty-eight': 48, 'forty-nine': 49, 'fifty': 50, 'fifty-one': 51, 'fifty-two': 52, 'fifty-three': 53,
    'fifty-four': 54, 'fifty-five': 55, 'fifty-six': 56, 'fifty-seven': 57, 'fifty-eight': 58, 'fifty-nine': 59,
    'sixty': 60, 'sixty-one': 61, 'sixty-two': 62, 'sixty-three': 63, 'sixty-four': 64, 'sixty-five': 65,
    'sixty-six': 66, 'sixty-seven': 67, 'sixty-eight': 68, 'sixty-nine': 69, 'seventy': 70, 'seventy-one': 71,
    'seventy-two': 72, 'seventy-three': 73, 'seventy-four': 74, 'seventy-five': 75, 'seventy-six': 76,
    'seventy-seven': 77, 'seventy-eight': 78, 'seventy-nine': 79, 'eighty': 80, 'eighty-one': 81, 'eighty-two': 82,
    'eighty-three': 83, 'eighty-four': 84, 'eighty-five': 85, 'eighty-six': 86, 'eighty-seven': 87, 'eighty-eight': 88,
    'eighty-nine': 89, 'ninety': 90, 'ninety-one': 91, 'ninety-two': 92, 'ninety-three': 93, 'ninety-four': 94,
    'ninety-five': 95, 'ninety-six': 96, 'ninety-seven': 97, 'ninety-eight': 98, 'ninety-nine': 99
}

figure_colors = ['#90BCD5', '#FFE6B7', '#E76254','#376795', '#FFD06F']