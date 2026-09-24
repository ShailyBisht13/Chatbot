# ai_engine/build_all_embeddings.py
import os
import json
import torch
from sentence_transformers import SentenceTransformer
from dataset_loader import load_tourism_data, load_temples, load_shlokas

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("Loading SentenceTransformer all-MiniLM-L6-v2...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 1. BUILD TOURISM EMBEDDINGS
print("\n--- Building tourism_embeds.pt ---")
tourism_records = [
    {
        "name": "Taj Mahal",
        "state": "Uttar Pradesh",
        "region": "North",
        "category": "Heritage",
        "attraction": "Taj Mahal, Agra Fort, Mehtab Bagh",
        "accessibility": "Easy (Agra Civil Enclave Airport, Agra Cantt Railway)",
        "details": "Iconic white marble mausoleum built by Shah Jahan in Agra. Best visited October to March. Nearby homestays and heritage hotels available."
    },
    {
        "name": "Jaipur",
        "state": "Rajasthan",
        "region": "West",
        "category": "Heritage & Culture",
        "attraction": "Amber Fort, Hawa Mahal, City Palace, Jantar Mantar",
        "accessibility": "Easy (Jaipur International Airport, Jaipur Junction)",
        "details": "The Pink City of Rajasthan. Popular for palaces, forts, markets, Rajasthani cuisine, and winter travel."
    },
    {
        "name": "Goa",
        "state": "Goa",
        "region": "West",
        "category": "Beach & Nightlife",
        "attraction": "Calangute Beach, Baga Beach, Anjuna, Old Goa Churches",
        "accessibility": "Easy (Dabolim & Mopa Airport, Madgaon Railway)",
        "details": "Premier coastal beach destination in West India. Water sports, Portuguese heritage, seafood, beach shacks, eco-friendly stays."
    },
    {
        "name": "Kerala Backwaters & Hill Stations",
        "state": "Kerala",
        "region": "South",
        "category": "Nature & Backwaters",
        "attraction": "Alleppey Houseboats, Kumarakom, Vembanad Lake, Munnar Tea Gardens, Fort Kochi, Thekkady, Varkala Beach",
        "accessibility": "Easy (Cochin International Airport, Alleppey / Ernakulam Railway)",
        "details": "Top places to visit in Kerala include Alleppey (Alappuzha) backwaters, Munnar tea hills, Kumarakom bird sanctuary, Thekkady Periyar wildlife, Kovalam and Varkala beaches, Fort Kochi heritage, and Athirappilly waterfalls. Homestays available across Kerala."
    },
    {
        "name": "Varanasi",
        "state": "Uttar Pradesh",
        "region": "North",
        "category": "Religious & Heritage",
        "attraction": "Ghats of Varanasi, Kashi Vishwanath Temple, Ganga Aarti, Sarnath",
        "accessibility": "Moderate (Lal Bahadur Shastri Airport, Varanasi Junction)",
        "details": "One of the world's oldest living cities on the banks of the sacred Ganges River. Famous for spiritual immersion, silk weaving, and evening Ganga Aarti."
    },
    {
        "name": "Manali",
        "state": "Himachal Pradesh",
        "region": "North",
        "category": "Adventure & Mountain",
        "attraction": "Solang Valley, Rohtang Pass, Hadimba Temple, Beas Kund Trek, Hampta Pass Trek",
        "accessibility": "Difficult/Mountainous (Bhuntar Airport, Chandigarh Railway)",
        "details": "Popular hill station and trekking hub in Himachal Pradesh. Ideal for adventure, snow sports in winter, and high altitude mountain treks."
    },
    {
        "name": "Sundarbans National Park",
        "state": "West Bengal",
        "region": "East",
        "category": "Nature & Wildlife Reserve",
        "attraction": "Sundarbans Mangrove Forest Boat Safaris, Royal Bengal Tigers, Wildlife Watchtowers",
        "accessibility": "Difficult (Netaji Subhas Chandra Bose Airport Kolkata, Canning Railway)",
        "details": "World's largest mangrove forest delta in East India. Note: Sundarbans is a tidal mangrove forest reserve accessed by boat safaris, NOT a mountain trekking trail."
    },
    {
        "name": "Amritsar",
        "state": "Punjab",
        "region": "North",
        "category": "Religious & Historical",
        "attraction": "Golden Temple (Sri Harmandir Sahib), Wagah Border, Jallianwala Bagh",
        "accessibility": "Easy (Sri Guru Ram Dass Jee Airport, Amritsar Junction)",
        "details": "Spiritual center of Sikhism. Famous for the Golden Temple, community kitchen (Langar), historical sites, and Punjabi hospitality."
    },
    {
        "name": "Mahabalipuram",
        "state": "Tamil Nadu",
        "region": "South",
        "category": "Heritage & Coastal",
        "attraction": "Shore Temple, Pancha Rathas, Arjuna's Penance",
        "accessibility": "Easy (Chennai International Airport, Chengalpattu Railway)",
        "details": "UNESCO World Heritage rock-cut monument site along the Coromandel coast of Tamil Nadu."
    },
    {
        "name": "Andaman & Nicobar Islands",
        "state": "Andaman and Nicobar",
        "region": "East/Island",
        "category": "Beach & Marine",
        "attraction": "Radhanagar Beach (Havelock/Swaraj Dweep), Elephant Beach, Cellular Jail Port Blair",
        "accessibility": "Moderate (Veer Savarkar International Airport Port Blair)",
        "details": "Pristine island archipelago in the Bay of Bengal. Note: Radhanagar Beach is a scenic tropical beach on Havelock Island, famous for white sands and scuba diving, NOT a mountain trek."
    },
    {
        "name": "Kaziranga National Park",
        "state": "Assam",
        "region": "East",
        "category": "Nature & Wildlife",
        "attraction": "One-Horned Rhinoceros Safari, Elephant Safari, Brahmaputra Floodplain",
        "accessibility": "Moderate (Jorhat / Guwahati Airport, Furkating Railway)",
        "details": "UNESCO World Heritage sanctuary in Assam, home to two-thirds of the world's great one-horned rhinoceroses."
    },
    {
        "name": "Mysore (Mysuru)",
        "state": "Karnataka",
        "region": "South",
        "category": "Heritage & Royal City",
        "attraction": "Mysore Palace, Chamundi Hill, Brindavan Gardens",
        "accessibility": "Easy (Mysore Airport, Mysuru Junction)",
        "details": "Royal heritage city of Karnataka famous for Mysore Palace, Dasara festival, and silk."
    },
    {
        "name": "Jaisalmer",
        "state": "Rajasthan",
        "region": "West",
        "category": "Desert & Heritage",
        "attraction": "Jaisalmer Fort (Sonar Qila), Sam Sand Dunes Desert Safari, Patwon Ki Haveli",
        "accessibility": "Moderate (Jaisalmer Airport, Jaisalmer Railway)",
        "details": "The Golden City of Thar Desert, famous for living fort, desert camping, camel safaris, and winter tourism."
    },
    {
        "name": "Rishikesh",
        "state": "Uttarakhand",
        "region": "North",
        "category": "Spiritual & Adventure",
        "attraction": "Laxman Jhula, Ram Jhula, River Rafting, Ganga Aarti, Yoga Ashrams",
        "accessibility": "Easy (Dehradun Jolly Grant Airport, Rishikesh Railway)",
        "details": "Yoga capital of the world located along the holy Ganges river in Uttarakhand. Public restrooms near Laxman Jhula, Ram Jhula, and main bus stand."
    },
    {
        "name": "Shimla",
        "state": "Himachal Pradesh",
        "region": "North",
        "category": "Hill Station & Nature",
        "attraction": "Mall Road, The Ridge, Jakhoo Temple, Kalka-Shimla Toy Train",
        "accessibility": "Easy (Shimla Jubbarhatti Airport, Kalka-Shimla Railway)",
        "details": "Capital of Himachal Pradesh, iconic British summer capital with colonial architecture and scenic mountain views."
    },
    {
        "name": "Udaipur",
        "state": "Rajasthan",
        "region": "West",
        "category": "Heritage & Lakes",
        "attraction": "City Palace, Lake Pichola, Jag Mandir, Saheliyon Ki Bari",
        "accessibility": "Easy (Maharana Pratap Airport, Udaipur City Railway)",
        "details": "The City of Lakes in Rajasthan, renowned for romantic palaces, boat rides, and heritage hospitality."
    },
    {
        "name": "Darjeeling",
        "state": "West Bengal",
        "region": "East",
        "category": "Hill Station & Treks",
        "attraction": "Tiger Hill Sunrise, Tea Gardens, Toy Train, Sandakphu Trek",
        "accessibility": "Moderate (Bagdogra Airport, New Jalpaiguri Railway)",
        "details": "Famous hill station in North Bengal with views of Kanchenjunga, tea plantations, and Sandakphu trekking trail."
    },
    {
        "name": "Munnar",
        "state": "Kerala",
        "region": "South",
        "category": "Nature & Tea Estates",
        "attraction": "Tea Gardens, Eravikulam National Park, Anamudi Peak, Mattupetty Dam",
        "accessibility": "Moderate (Cochin International Airport, Aluva Railway)",
        "details": "Lush hill station in the Western Ghats of Kerala, famous for tea estates, homestays, and cool weather."
    },
    {
        "name": "Ajanta & Ellora Caves",
        "state": "Maharashtra",
        "region": "West",
        "category": "Heritage & Archaeology",
        "attraction": "Ajanta Buddhist Caves, Ellora Kailash Temple Cave 16",
        "accessibility": "Moderate (Aurangabad / Chhatrapati Sambhajinagar Airport & Railway)",
        "details": "UNESCO World Heritage rock-cut cave monuments representing ancient Indian art and architecture."
    },
    {
        "name": "Cherrapunji (Sohra)",
        "state": "Meghalaya",
        "region": "East",
        "category": "Nature & Waterfalls",
        "attraction": "Nohkalikai Falls, Living Root Bridges, Mawsmai Cave, Seven Sisters Falls",
        "accessibility": "Difficult (Shillong Airport, Guwahati Railway)",
        "details": "Famous for heavy rainfall, spectacular waterfalls like Nohkalikai, and bio-engineered living root bridges. Note: Nohkalikai is a dramatic waterfall view, surrounded by rainforest walks."
    },
    {
        "name": "Kedarnath",
        "state": "Uttarakhand",
        "region": "North",
        "category": "Religious Pilgrimage & Trek",
        "attraction": "Kedarnath Shiva Temple, Mandakini River Valley, Bhairavnath Temple",
        "accessibility": "Trek / Helicopter (Dehradun Airport, Haridwar / Rishikesh Railway)",
        "details": "Kedarnath is located in Rudraprayag district, Uttarakhand, high in the Himalayas. Requires a 16 km trek from Gaurikund base camp. Affordable stays include GMVN cottages, pilgrim ashrams, and camps. Note: Hemkund Sahib is in Chamoli district, NOT in Kedarnath."
    },
    {
        "name": "Badrinath",
        "state": "Uttarakhand",
        "region": "North",
        "category": "Religious Pilgrimage",
        "attraction": "Badrinath Temple, Tapt Kund, Mana Village, Vasudhara Falls",
        "accessibility": "Road Accessible (Dehradun Airport, Rishikesh / Haridwar Railway)",
        "details": "Sacred shrine of Lord Vishnu in Chamoli district, Uttarakhand. Part of Char Dham pilgrimage. Accessible May to October."
    },
    {
        "name": "Hemkund Sahib & Valley of Flowers",
        "state": "Uttarakhand",
        "region": "North",
        "category": "Pilgrimage & High Altitude Trek",
        "attraction": "Gurudwara Shri Hemkund Sahib, Valley of Flowers National Park",
        "accessibility": "Trek from Govindghat / Ghangaria (Chamoli district)",
        "details": "Located in Chamoli district near Govindghat in Uttarakhand. Gurudwara Hemkund Sahib sits at 4,329m beside a glacial lake. Valley of Flowers is a nearby UNESCO World Heritage alpine flower valley."
    },
    {
        "name": "Dehradun & Sudhowala",
        "state": "Uttarakhand",
        "region": "North",
        "category": "City & Foothills",
        "attraction": "Clock Tower, Robber's Cave (Guchhupani), Sahastradhara, FRI, Sudhowala Educational Hub",
        "accessibility": "Easy (Jolly Grant Airport, Dehradun Railway Station)",
        "details": "Capital city of Uttarakhand in the Doon Valley. Public restrooms located at Clock Tower Paltan Bazaar entrance, ISBT Dehradun, Prem Nagar Market, and Sudhowala bus stop."
    },
    {
        "name": "Abbott Mount (Abbott Mount Hill Station)",
        "state": "Uttarakhand",
        "region": "Kumaon / North India",
        "category": "Hill Station & Heritage",
        "attraction": "Colonial Bungalows, Himalayan Peak Views, Mukti Koti Sanctuary, Abbott Mount Church, Pine & Deodar Forests",
        "accessibility": "Lohaghat (~7 km), Champawat (~20 km), Tanakpur Railway (~85 km), Pantnagar Airport (~180 km)",
        "details": "Abbott Mount is a tranquil, scenic hill station located in Lohaghat city, Champawat district, Kumaon region of Uttarakhand, India (at an altitude of 6,400 ft). Founded by John Harold Abbott in the early 20th century, it is famous for its European-style heritage cottages, dense pine forests, and sweeping views of the snow-capped Himalayan ranges. Note: Abbott Mount is strictly located in Lohaghat, Champawat district, Uttarakhand, INDIA (NOT in Canada)."
    },
    {
        "name": "Lohaghat & Champawat",
        "state": "Uttarakhand",
        "region": "Kumaon / North India",
        "category": "Heritage & Nature",
        "attraction": "Abbott Mount, Baneswar Temple, Mayawati Ashram (Advaita Ashrama), Shyamla Tal",
        "accessibility": "Tanakpur Railway Station (~85 km), Pantnagar Airport (~180 km)",
        "details": "Lohaghat is a historic town in Champawat district, Kumaon region, Uttarakhand, India, situated along the Lohawati river. gateway to Abbott Mount, Mayawati Ashram, and ancient temples."
    },
    {
        "name": "Almora & Mukteshwar",
        "state": "Uttarakhand",
        "region": "Kumaon / North India",
        "category": "Hill Station & Nature",
        "attraction": "Mukteshwar Dham, Chauli Ki Jali, Bright End Corner, Kasar Devi Temple",
        "accessibility": "Kathgodam Railway Station (~80-90 km), Pantnagar Airport (~130 km)",
        "details": "Cultural capital of Kumaon region in Uttarakhand. Mukteshwar offers spectacular views of Nanda Devi, Trishul, and Panchachuli peaks."
    },
    {
        "name": "Nainital & Ranikhet",
        "state": "Uttarakhand",
        "region": "Kumaon / North India",
        "category": "Hill Station & Lakes",
        "attraction": "Naini Lake, Naina Devi Temple, Jhula Devi Temple, Golf Course Ranikhet",
        "accessibility": "Kathgodam Railway Station (~34 km), Pantnagar Airport (~70 km)",
        "details": "Famous lake district of Kumaon, Uttarakhand. Ranikhet is a serene army cantonment hill station."
    }
]

tourism_texts = []
for t in tourism_records:
    txt = f"Destination: {t['name']} | State: {t['state']} | Region: {t['region']} | Category: {t['category']} | Attractions: {t['attraction']} | Access: {t['accessibility']} | Details: {t['details']}"
    tourism_texts.append(txt)

print(f"Encoding {len(tourism_texts)} tourism records...")
tourism_embeds = model.encode(tourism_texts, convert_to_tensor=True)

torch.save({"texts": tourism_texts, "embeddings": tourism_embeds}, os.path.join(MODELS_DIR, "tourism_embeds.pt"))
print("Saved models/tourism_embeds.pt successfully!")

# 2. BUILD SHLOKAS & TEMPLES EMBEDDINGS
print("\n--- Building shlokas_embeds.pt ---")
shlokas_dict = load_shlokas()
temples_dict = load_temples()

spiritual_texts = []
for key, s in (shlokas_dict or {}).items():
    s_text = f"Shloka ID: {key} | Sanskrit: {s.get('sanskrit', '')} | Hindi: {s.get('hindi', '')} | English: {s.get('english', '')}"
    spiritual_texts.append(s_text)

for name, info in (temples_dict or {}).items():
    t_text = f"Temple: {name} | Location: {info.get('location', '')} | Origin: {info.get('origin_story', '')} | Significance: {info.get('significance', '')} | Best Time: {info.get('best_time_to_visit', '')}"
    spiritual_texts.append(t_text)

print(f"Encoding {len(spiritual_texts)} spiritual records...")
spiritual_embeds = model.encode(spiritual_texts, convert_to_tensor=True)

torch.save({"texts": spiritual_texts, "embeddings": spiritual_embeds}, os.path.join(MODELS_DIR, "shlokas_embeds.pt"))
print("Saved models/shlokas_embeds.pt successfully!")

print("\nAll embeddings rebuilt cleanly!")
