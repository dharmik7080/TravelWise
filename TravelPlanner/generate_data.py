import csv

destinations_data = [
    # Kashmir & Ladakh
    {
        "name": "Srinagar", "city": "Srinagar", "state": "Jammu & Kashmir", "region": "North", "category": "Hill Station",
        "desc": "The summer capital of Jammu & Kashmir, famous for houseboats, iconic lakes, and beautiful Mughal gardens.",
        "season": "Summer", "days": 3, "budget": "Moderate", "cost": 3500.0, "rating": 4.8,
        "attractions": [
            ("Dal Lake", "Nature", "Scenic lake famous for shikaras and wooden houseboats.", 0.0, "06:00:00", "21:00:00", 120),
            ("Shalimar Bagh Mughal Garden", "Heritage", "Beautiful garden built by Mughal Emperor Jahangir.", 25.0, "09:00:00", "18:00:00", 90),
            ("Nishat Bagh", "Heritage", "Terraced Mughal garden offering panoramic views of Dal Lake.", 25.0, "09:00:00", "18:00:00", 90),
            ("Shankaracharya Temple", "Spiritual", "Ancient temple dedicated to Lord Shiva on a hilltop.", 0.0, "07:00:00", "20:00:00", 60),
            ("Indira Gandhi Memorial Tulip Garden", "Nature", "The largest tulip garden in Asia, showcasing vibrant blooms.", 50.0, "09:00:00", "19:00:00", 120),
            ("Hazratbal Shrine", "Spiritual", "White marble Islamic shrine housing a holy relic.", 0.0, "05:00:00", "21:00:00", 60)
        ],
        "season_detail": ("Summer", "April to October", "15°C - 30°C", "Low", "Book shikara rides and houseboats well in advance.")
    },
    {
        "name": "Gulmarg", "city": "Gulmarg", "state": "Jammu & Kashmir", "region": "North", "category": "Adventure",
        "desc": "A legendary ski destination and hill station, renowned for the world's second-highest cable car.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 6000.0, "rating": 4.9,
        "attractions": [
            ("Gulmarg Gondola", "Adventure", "One of the highest cable cars in Asia offering snow views.", 900.0, "10:00:00", "17:00:00", 180),
            ("Khilanmarg", "Nature", "A small valley offering spectacular views of the Himalayas.", 0.0, "08:00:00", "16:00:00", 120),
            ("Gulmarg Golf Course", "Adventure", "A beautiful 18-hole golf course located at a high altitude.", 100.0, "09:00:00", "18:00:00", 90),
            ("St. Mary's Church Gulmarg", "Heritage", "A historic Victorian style church built during the British era.", 0.0, "10:00:00", "17:00:00", 45),
            ("Alpathar Lake", "Nature", "A high altitude lake that remains frozen until mid-June.", 0.0, "08:00:00", "15:00:00", 150)
        ],
        "season_detail": ("Winter", "December to March", "-5°C - 10°C", "Heavy Snowfall", "Perfect for skiing. Carry heavy woolen garments.")
    },
    {
        "name": "Pahalgam", "city": "Pahalgam", "state": "Jammu & Kashmir", "region": "North", "category": "Nature",
        "desc": "A pristine hill station at the confluence of the Lidder River and Sheshnag Lake, famous for lush meadows.",
        "season": "Summer", "days": 3, "budget": "Moderate", "cost": 3000.0, "rating": 4.7,
        "attractions": [
            ("Baisaran Valley", "Nature", "Known as Mini Switzerland, featuring pine forests and meadows.", 50.0, "08:00:00", "18:00:00", 120),
            ("Aru Valley", "Nature", "A scenic village known for its tranquil meadows and activities.", 0.0, "08:00:00", "18:00:00", 180),
            ("Betaab Valley", "Nature", "Named after a famous Bollywood movie, featuring crystal streams.", 100.0, "08:00:00", "18:00:00", 120),
            ("Lidder Amusement Park", "Adventure", "A small amusement park next to the rushing Lidder river.", 150.0, "10:00:00", "19:00:00", 90),
            ("Sheshnag Lake", "Nature", "A high-altitude oligotrophic lake reachable by trekking.", 0.0, "07:00:00", "17:00:00", 240)
        ],
        "season_detail": ("Summer", "April to June", "10°C - 25°C", "Moderate", "Great base for the Amarnath Yatra. Enjoy horse riding.")
    },
    {
        "name": "Leh", "city": "Leh", "state": "Ladakh", "region": "North", "category": "Adventure",
        "desc": "A high-altitude desert city in the Himalayas, famous for rugged mountain passes, monasteries, and lakes.",
        "season": "Summer", "days": 5, "budget": "Luxury", "cost": 5500.0, "rating": 4.9,
        "attractions": [
            ("Leh Palace", "Heritage", "A 17th-century former royal palace overlooking the town.", 200.0, "08:00:00", "17:00:00", 90),
            ("Shanti Stupa", "Spiritual", "A white-domed Buddhist stupa offering panoramic views.", 0.0, "05:00:00", "21:00:00", 60),
            ("Magnetic Hill", "Adventure", "A cyclops hill where gravity-defying phenomena occur.", 0.0, "00:00:00", "23:59:59", 45),
            ("Thiksey Monastery", "Spiritual", "A twelve-story Tibetan Buddhist monastery resembling Lhasa.", 50.0, "07:00:00", "19:00:00", 120),
            ("Pangong Tso Lake", "Nature", "A breathtaking endorheic lake extending from India to China.", 0.0, "00:00:00", "23:59:59", 240),
            ("Hall of Fame Museum", "Heritage", "A museum built by the Indian Army in memory of martyrs.", 100.0, "09:00:00", "19:00:00", 90)
        ],
        "season_detail": ("Summer", "June to September", "15°C - 30°C", "Very Low", "Acclimatize for 24-48 hours to prevent altitude sickness.")
    },

    # Himachal Pradesh
    {
        "name": "Manali", "city": "Manali", "state": "Himachal Pradesh", "region": "North", "category": "Hill Station",
        "desc": "A popular resort town nestled in the mountains near the northern end of the Kullu Valley.",
        "season": "Summer", "days": 3, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Hadimba Temple", "Spiritual", "An ancient wooden temple built around a natural cave.", 0.0, "08:00:00", "18:00:00", 60),
            ("Solang Valley", "Adventure", "Famous for adventure sports like paragliding and zorbing.", 0.0, "09:00:00", "18:00:00", 180),
            ("Jogini Waterfalls", "Nature", "A scenic waterfall reachable by a short hillside trek.", 0.0, "08:00:00", "17:00:00", 120),
            ("Vashisht Hot Water Springs", "Spiritual", "Natural sulfur hot water springs known for healing properties.", 0.0, "07:00:00", "21:00:00", 45),
            ("Mall Road Manali", "City", "A bustling street full of shops, eateries, and local markets.", 0.0, "10:00:00", "22:00:00", 90),
            ("Atal Tunnel", "Adventure", "The longest highway single-tube tunnel above 10,000 feet.", 0.0, "00:00:00", "23:59:59", 60)
        ],
        "season_detail": ("Summer", "March to June", "10°C - 25°C", "Low", "Ideal for paragliding and river rafting. Carry light woolens.")
    },
    {
        "name": "Shimla", "city": "Shimla", "state": "Himachal Pradesh", "region": "North", "category": "Hill Station",
        "desc": "The colonial-era summer capital of British India, known for the toy train, Ridge, and colonial heritage.",
        "season": "Summer", "days": 3, "budget": "Moderate", "cost": 3000.0, "rating": 4.6,
        "attractions": [
            ("The Ridge Shimla", "City", "A large open space in the heart of Shimla, offering mountain views.", 0.0, "00:00:00", "23:59:59", 90),
            ("Jakhoo Temple", "Spiritual", "An ancient temple dedicated to Hanuman with a giant statue.", 0.0, "07:00:00", "20:00:00", 90),
            ("Kalka Shimla Toy Train", "Heritage", "A UNESCO World Heritage narrow-gauge railway journey.", 300.0, "06:00:00", "18:00:00", 300),
            ("Mall Road Shimla", "City", "Pedestrian-only avenue packed with heritage buildings and shops.", 0.0, "09:00:00", "22:00:00", 120),
            ("Viceregal Lodge", "Heritage", "Historical British imperial residence with gardens.", 100.0, "09:00:00", "17:00:00", 90),
            ("Christ Church Shimla", "Heritage", "The second oldest church in North India, displaying neo-Gothic style.", 0.0, "08:00:00", "18:00:00", 45)
        ],
        "season_detail": ("Summer", "March to June", "15°C - 30°C", "Moderate", "Avoid walking on Mall Road during peak afternoon heat.")
    },
    {
        "name": "Dharamshala", "city": "Dharamshala", "state": "Himachal Pradesh", "region": "North", "category": "Spiritual",
        "desc": "Home to the Dalai Lama and the Tibetan government-in-exile, surrounded by dense cedar forests.",
        "season": "Spring", "days": 3, "budget": "Budget", "cost": 1800.0, "rating": 4.6,
        "attractions": [
            ("Tsuglagkhang Complex", "Spiritual", "The official residence and temple complex of the Dalai Lama.", 0.0, "06:00:00", "19:00:00", 120),
            ("Bhagsunag Waterfall", "Nature", "A scenic fresh waterfall located near Bhagsunath Temple.", 0.0, "07:00:00", "18:00:00", 90),
            ("HPCA Stadium Dharamshala", "Adventure", "A picturesque international cricket stadium with snow mountains background.", 30.0, "09:00:00", "18:00:00", 60),
            ("Namgyal Monastery", "Spiritual", "The personal monastery of the Dalai Lama, founded in the 16th century.", 0.0, "06:00:00", "20:00:00", 90),
            ("St. John in the Wilderness Church", "Heritage", "An old Anglican church built in 1852 amidst deodar trees.", 0.0, "09:00:00", "18:00:00", 45),
            ("Triund Hill", "Adventure", "A popular trekking spot offering panoramic views of the Dhauladhars.", 0.0, "00:00:00", "23:59:59", 240)
        ],
        "season_detail": ("Spring", "September to November", "15°C - 25°C", "Low", "Perfect for trekking to Triund. Respect temple customs.")
    },
    {
        "name": "Dalhousie", "city": "Dalhousie", "state": "Himachal Pradesh", "region": "North", "category": "Hill Station",
        "desc": "A quiet hill station built on five hills, boasting colonial-era churches and dense pine forest slopes.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2500.0, "rating": 4.5,
        "attractions": [
            ("Khajjiar Lake", "Nature", "Often called the Switzerland of India, surrounded by cedar forests.", 0.0, "08:00:00", "18:00:00", 120),
            ("Panchpula", "Nature", "A scenic picnic spot featuring waterfalls and streams.", 0.0, "09:00:00", "19:00:00", 90),
            ("Dainkund Peak", "Nature", "The highest peak in Dalhousie, offering panoramic valley views.", 0.0, "08:00:00", "17:00:00", 120),
            ("St. John's Church Dalhousie", "Heritage", "The oldest church in the town, embodying Protestant structure.", 0.0, "07:00:00", "19:00:00", 45),
            ("Satdhara Falls", "Nature", "Mica-rich mineral springs known for medicinal virtues.", 0.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Summer", "March to May", "15°C - 25°C", "Low", "Enjoy boating at Chamera lake and zorbing at Khajjiar.")
    },

    # Uttarakhand
    {
        "name": "Mussoorie", "city": "Mussoorie", "state": "Uttarakhand", "region": "North", "category": "Hill Station",
        "desc": "Known as the Queen of the Hills, offering breathtaking views of the Doon Valley and Shivalik ranges.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.6,
        "attractions": [
            ("Kempty Falls", "Nature", "A popular giant waterfall where tourists enjoy bathing.", 50.0, "08:00:00", "17:00:00", 120),
            ("Gun Hill", "Nature", "The second highest point in Mussoorie, accessible by ropeway.", 150.0, "09:00:00", "19:00:00", 90),
            ("Lal Tibba Scenic Point", "Nature", "The highest peak in Mussoorie offering telescope views of snow peaks.", 50.0, "08:00:00", "19:00:00", 60),
            ("Company Garden Mussoorie", "Nature", "A colorful municipal garden with a mini lake and amusement rides.", 25.0, "09:00:00", "18:00:00", 90),
            ("Cloud's End", "Nature", "A quiet resort forest marker marking the geographical end of Mussoorie.", 50.0, "08:00:00", "18:00:00", 120)
        ],
        "season_detail": ("Summer", "April to June", "15°C - 25°C", "Moderate", "Expect heavy weekend traffic. Travel early to waterfalls.")
    },
    {
        "name": "Nainital", "city": "Nainital", "state": "Uttarakhand", "region": "North", "category": "Hill Station",
        "desc": "A beautiful Himalayan resort town set around Nainital Lake, a popular destination for families and couples.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2900.0, "rating": 4.6,
        "attractions": [
            ("Naini Lake", "Nature", "A crescent-shaped natural freshwater body famous for boating.", 120.0, "06:00:00", "18:00:00", 90),
            ("Naina Devi Temple", "Spiritual", "A sacred Hindu temple situated on the northern shore of the lake.", 0.0, "06:00:00", "22:00:00", 60),
            ("Naini Peak", "Nature", "Also known as China Peak, the highest mountain peak in Nainital.", 0.0, "08:00:00", "17:00:00", 180),
            ("Tiffin Top", "Nature", "A terraced hilltop offering scenic mountain scenery views.", 0.0, "08:00:00", "18:00:00", 90),
            ("G.B. Pant High Altitude Zoo", "Wildlife", "One of the few high-altitude zoos in India.", 100.0, "10:00:00", "16:30:00", 120)
        ],
        "season_detail": ("Summer", "March to June", "10°C - 25°C", "Low", "Book boat rides in the morning for calm lake views.")
    },
    {
        "name": "Rishikesh", "city": "Rishikesh", "state": "Uttarakhand", "region": "North", "category": "Spiritual",
        "desc": "Known as the Yoga Capital of the World, a major hub for spiritual study and adventure sports.",
        "season": "Autumn", "days": 3, "budget": "Budget", "cost": 1500.0, "rating": 4.8,
        "attractions": [
            ("Laxman Jhula", "Heritage", "A famous suspension bridge across the holy Ganges River.", 0.0, "00:00:00", "23:59:59", 45),
            ("Triveni Ghat", "Spiritual", "A sacred bathing ghat known for the evening Ganga Aarti.", 0.0, "05:00:00", "22:00:00", 90),
            ("Neer Garh Waterfall", "Nature", "A natural hiking trail leading to double fresh waterfalls.", 30.0, "08:00:00", "18:00:00", 120),
            ("Parmarth Niketan Ashram", "Spiritual", "The largest ashram in Rishikesh, holding spiritual lectures.", 0.0, "06:00:00", "21:00:00", 90),
            ("Jumpin Heights", "Adventure", "India's highest bungee jumping zone run by experts.", 3500.0, "09:30:00", "16:00:00", 180),
            ("The Beatles Ashram", "Heritage", "The ruins of Maharishi Mahesh Yogi ashram visited by The Beatles.", 150.0, "09:00:00", "17:00:00", 90)
        ],
        "season_detail": ("Autumn", "October to March", "15°C - 28°C", "Low", "Attend the evening Ganga Aarti. Try white water rafting.")
    },
    {
        "name": "Haridwar", "city": "Haridwar", "state": "Uttarakhand", "region": "North", "category": "Spiritual",
        "desc": "An ancient city where the Ganges emerges from the Himalayas, one of the seven holiest Hindu sites.",
        "season": "Spring", "days": 2, "budget": "Budget", "cost": 1200.0, "rating": 4.7,
        "attractions": [
            ("Har Ki Pauri", "Spiritual", "The most famous ghat on the banks of the Ganges, holding Aarti.", 0.0, "00:00:00", "23:59:59", 90),
            ("Mansa Devi Temple", "Spiritual", "A temple dedicated to Mansa Devi on Bilwa Parvat hill.", 0.0, "05:00:00", "21:00:00", 120),
            ("Chandi Devi Temple", "Spiritual", "A hilltop temple accessible by a steep trek or ropeway.", 0.0, "06:00:00", "20:00:00", 120),
            ("Bharat Mata Mandir", "Spiritual", "A unique multi-story temple dedicated to Mother India.", 0.0, "09:00:00", "18:00:00", 60),
            ("Daksh Mahadev Temple", "Spiritual", "An ancient temple of Shiva located in Kankhal district.", 0.0, "06:00:00", "21:00:00", 60)
        ],
        "season_detail": ("Spring", "October to April", "10°C - 25°C", "Low", "Rent lockers for shoes at Har Ki Pauri to avoid theft.")
    },
    {
        "name": "Auli", "city": "Auli", "state": "Uttarakhand", "region": "North", "category": "Adventure",
        "desc": "A premier ski resort destination surrounded by coniferous oak forests and majestic peaks.",
        "season": "Winter", "days": 3, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Auli Ropeway", "Adventure", "A long cable car ride linking Joshimath and Auli skiing slopes.", 1000.0, "09:00:00", "17:00:00", 120),
            ("Auli Artificial Lake", "Nature", "A pristine artificial lake providing snowmaking system water.", 0.0, "08:00:00", "18:00:00", 60),
            ("Gorson Bugyal Trek", "Adventure", "A scenic meadow trek offering massive views of Nanda Devi.", 0.0, "07:00:00", "16:00:00", 180),
            ("Kwani Bugyal", "Nature", "A beautiful high altitude meadow situated at 3384 meters.", 0.0, "08:00:00", "16:00:00", 240),
            ("Joshimath Temple Complex", "Spiritual", "A historic religious gateway town situated near Auli.", 0.0, "06:00:00", "20:00:00", 90)
        ],
        "season_detail": ("Winter", "December to March", "-4°C - 12°C", "Heavy Snowfall", "Rent quality ski equipment locally from certified stores.")
    },

    # Rajasthan
    {
        "name": "Jaipur", "city": "Jaipur", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The Pink City, capital of Rajasthan, famous for royal palaces, imposing forts, and rich heritage crafts.",
        "season": "Winter", "days": 3, "budget": "Moderate", "cost": 3200.0, "rating": 4.8,
        "attractions": [
            ("Amer Fort", "Heritage", "A majestic hilltop fortress featuring Mughal and Rajput style elements.", 200.0, "08:00:00", "17:30:00", 120),
            ("Hawa Mahal", "Heritage", "The Palace of Winds, a five-story pink sandstone structure.", 50.0, "09:00:00", "17:00:00", 60),
            ("City Palace Jaipur", "Heritage", "A royal palace complex hosting museums and royal courtyards.", 300.0, "09:30:00", "17:00:00", 120),
            ("Jantar Mantar Jaipur", "Heritage", "An astronomical observatory featuring the world's largest stone sundial.", 50.0, "09:00:00", "16:30:00", 90),
            ("Nahargarh Fort", "Heritage", "Fort offering sweeping panoramic views of the city.", 200.0, "10:00:00", "22:00:00", 90),
            ("Chokhi Dhani", "Heritage", "An ethnic mock village offering traditional Rajasthani food and dances.", 900.0, "17:00:00", "23:00:00", 180)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Very Low", "Purchase a Composite Entry Ticket to save money on entry fees.")
    },
    {
        "name": "Udaipur", "city": "Udaipur", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The City of Lakes, known for its romantic settings, floating palaces, and gorgeous lakefront ghats.",
        "season": "Winter", "days": 3, "budget": "Luxury", "cost": 4800.0, "rating": 4.9,
        "attractions": [
            ("City Palace Udaipur", "Heritage", "The largest palace complex in Rajasthan, situated on Lake Pichola.", 250.0, "09:00:00", "17:30:00", 120),
            ("Lake Pichola Boating", "Nature", "A scenic boat ride around the floating Jag Mandir and Lake Palace.", 400.0, "09:00:00", "18:00:00", 60),
            ("Sajjangarh Monsoon Palace", "Heritage", "A hilltop palace offering spectacular sunset views of Udaipur.", 150.0, "09:00:00", "18:00:00", 90),
            ("Jagdish Temple", "Spiritual", "A large Indo-Aryan temple built in the middle of Udaipur town.", 0.0, "05:00:00", "22:00:00", 45),
            ("Saheliyon-ki-Bari", "Heritage", "A historic garden featuring marble fountains, kiosks, and pools.", 50.0, "09:00:00", "19:00:00", 60),
            ("Bagore Ki Haveli", "Heritage", "An old mansion hosting an evening Rajasthani folk dance show.", 100.0, "09:00:00", "20:00:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "12°C - 28°C", "Low", "Enjoy a sunset boat cruise at Lake Pichola.")
    },
    {
        "name": "Jodhpur", "city": "Jodhpur", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The Blue City, dominated by the massive Mehrangarh Fort towering over blue-painted houses.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Mehrangarh Fort", "Heritage", "One of the largest forts in India, containing royal treasures.", 200.0, "09:00:00", "17:00:00", 120),
            ("Jaswant Thada", "Heritage", "A beautiful white marble cenotaph built by the royal family.", 50.0, "09:00:00", "17:00:00", 45),
            ("Umaid Bhawan Palace Museum", "Heritage", "Part museum, part luxury hotel, one of the largest private residences.", 100.0, "09:00:00", "17:00:00", 90),
            ("Mandore Gardens", "Heritage", "Historical town gardens featuring Cenotaphs and temples.", 0.0, "08:00:00", "20:00:00", 90),
            ("Ghanta Ghar Clock Tower", "City", "A historic marketplace clock tower surrounding Sardar Market.", 0.0, "09:00:00", "21:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 27°C", "Low", "Visit Mehrangarh Fort in the morning to avoid heat.")
    },
    {
        "name": "Jaisalmer", "city": "Jaisalmer", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The Golden City, situated in the heart of the Thar Desert, featuring a living fort and sand dunes.",
        "season": "Winter", "days": 3, "budget": "Moderate", "cost": 3000.0, "rating": 4.8,
        "attractions": [
            ("Jaisalmer Fort", "Heritage", "A living fort where a quarter of the city's population resides.", 100.0, "09:00:00", "18:00:00", 120),
            ("Patwon Ki Haveli", "Heritage", "A cluster of five historic Havelis showing intricate carvings.", 100.0, "09:00:00", "18:00:00", 90),
            ("Sam Sand Dunes", "Adventure", "Sand dunes offering camel safaris and overnight desert camping.", 500.0, "15:00:00", "23:00:00", 240),
            ("Gadisar Lake", "Nature", "A rainwater conservation reservoir surrounded by temples.", 0.0, "08:00:00", "20:00:00", 60),
            ("Kuldhara Abandoned Village", "Heritage", "An old abandoned ghost village known for its mystery.", 50.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "5°C - 24°C", "Negligible", "Carry warm clothes as desert temperatures drop at night.")
    },
    {
        "name": "Pushkar", "city": "Pushkar", "state": "Rajasthan", "region": "West", "category": "Spiritual",
        "desc": "A holy town surrounding Pushkar Lake, home to the rare Brahma Temple and the famous annual Camel Fair.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1500.0, "rating": 4.5,
        "attractions": [
            ("Brahma Temple", "Spiritual", "One of the very few temples in the world dedicated to Lord Brahma.", 0.0, "06:00:00", "21:00:00", 45),
            ("Pushkar Lake Ghats", "Spiritual", "Dozens of bathing ghats where pilgrims take holy dips.", 0.0, "00:00:00", "23:59:59", 60),
            ("Savitri Temple", "Spiritual", "A hilltop temple offering sunrise views over Pushkar.", 0.0, "05:00:00", "19:00:00", 90),
            ("Varaha Temple", "Spiritual", "The oldest temple in Pushkar, dedicated to Lord Vishnu.", 0.0, "06:00:00", "20:00:00", 45),
            ("Pushkar Camel Fair Grounds", "Heritage", "The venue of the world-famous Pushkar camel festival.", 0.0, "09:00:00", "21:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 28°C", "Low", "Respect local culture by removing shoes near holy lake.")
    },
    {
        "name": "Ranthambore", "city": "Sawai Madhopur", "state": "Rajasthan", "region": "West", "category": "Wildlife",
        "desc": "Famous for its national park and tiger reserves, offering tourists a chance to spot royal Bengal tigers.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Ranthambore National Park Safari", "Wildlife", "A jeep safari inside zones to spot Bengal tigers.", 1200.0, "06:00:00", "18:00:00", 210),
            ("Ranthambore Fort", "Heritage", "A UNESCO-listed fort located inside the national park territory.", 0.0, "06:00:00", "18:00:00", 120),
            ("Trinetra Ganesha Temple", "Spiritual", "A historic three-eyed Ganesha temple situated in the fort.", 0.0, "06:00:00", "18:00:00", 60),
            ("Padam Talao Lake", "Nature", "The largest lake in the park, famous for water lily blooms.", 0.0, "06:00:00", "18:00:00", 45),
            ("Kachida Valley", "Nature", "A rocky outpost valley known for panther sightings.", 0.0, "06:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Winter", "October to April", "10°C - 30°C", "Low", "Book safaris several months in advance for top zones.")
    },
    {
        "name": "Mount Abu", "city": "Mount Abu", "state": "Rajasthan", "region": "West", "category": "Hill Station",
        "desc": "The only hill station in Rajasthan, featuring Dilwara temples and refreshing mountain air.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.5,
        "attractions": [
            ("Dilwara Temples", "Spiritual", "Famous Jain temples known for spectacular marble carvings.", 0.0, "12:00:00", "17:00:00", 90),
            ("Nakki Lake", "Nature", "A sacred lake situated in the hills, offering boating activities.", 100.0, "08:00:00", "18:00:00", 60),
            ("Toad Rock", "Nature", "A large rock formation resembling a toad, offering views.", 0.0, "06:00:00", "18:00:00", 45),
            ("Guru Shikhar", "Nature", "The highest peak in the Aravali Range.", 0.0, "08:00:00", "18:00:00", 90),
            ("Sunset Point Mount Abu", "Nature", "Scenic sunset point overlooking green hills.", 0.0, "16:00:00", "19:00:00", 60)
        ],
        "season_detail": ("Summer", "March to June", "20°C - 32°C", "Moderate", "Dress modestly for the Dilwara Jain Temples.")
    },

    # Uttar Pradesh
    {
        "name": "Agra", "city": "Agra", "state": "Uttar Pradesh", "region": "North", "category": "Heritage",
        "desc": "Home to the Taj Mahal, one of the New Seven Wonders of the World, and former capital of the Mughal Empire.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.9,
        "attractions": [
            ("Taj Mahal", "Heritage", "The world-famous white marble mausoleum built by Shah Jahan.", 50.0, "06:00:00", "18:30:00", 180),
            ("Agra Fort", "Heritage", "A massive red sandstone Mughal fort overlooking the Yamuna River.", 50.0, "06:00:00", "18:00:00", 120),
            ("Itimad-ud-Daulah Tomb", "Heritage", "Often called the Baby Taj, an exquisite Mughal marble tomb.", 30.0, "06:00:00", "18:00:00", 60),
            ("Mehtab Bagh", "Heritage", "A garden complex located opposite the Taj Mahal across the river.", 30.0, "06:00:00", "18:00:00", 90),
            ("Fatehpur Sikri Palace", "Heritage", "The majestic ghost city built by Emperor Akbar.", 50.0, "06:00:00", "18:00:00", 150)
        ],
        "season_detail": ("Winter", "October to March", "8°C - 25°C", "Low", "Taj Mahal is closed on Fridays. Arrive at sunrise to avoid crowd.")
    },
    {
        "name": "Varanasi", "city": "Varanasi", "state": "Uttar Pradesh", "region": "North", "category": "Spiritual",
        "desc": "One of the oldest continuously inhabited cities in the world, the spiritual center of Hinduism.",
        "season": "Winter", "days": 3, "budget": "Budget", "cost": 1600.0, "rating": 4.9,
        "attractions": [
            ("Kashi Vishwanath Temple", "Spiritual", "A sacred temple dedicated to Lord Shiva with golden spires.", 0.0, "03:00:00", "23:00:00", 120),
            ("Dashashwamedh Ghat", "Spiritual", "The main ghat in Varanasi, hosting the iconic evening Ganga Aarti.", 0.0, "00:00:00", "23:59:59", 90),
            ("Assi Ghat", "Spiritual", "Ghat located at the confluence of Ganges and Assi rivers.", 0.0, "00:00:00", "23:59:59", 60),
            ("Sarnath Archaeological Site", "Spiritual", "The historical park where Lord Buddha first taught the Dharma.", 50.0, "08:00:00", "18:00:00", 120),
            ("Banaras Hindu University", "Heritage", "A massive green university campus hosting temples.", 0.0, "09:00:00", "19:00:00", 90),
            ("Ramnagar Fort", "Heritage", "A 18th-century sand-stone fort with museum near the river.", 50.0, "10:00:00", "17:00:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Book river boat rides in early morning for sunrise views.")
    },
    {
        "name": "Lucknow", "city": "Lucknow", "state": "Uttar Pradesh", "region": "North", "category": "Heritage",
        "desc": "The City of Nawabs, famous for its architecture, rich Awadhi cuisine, and classical culture.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2500.0, "rating": 4.7,
        "attractions": [
            ("Bara Imambara", "Heritage", "A monumental shrine housing a spectacular architectural labyrinth.", 50.0, "06:00:00", "17:00:00", 120),
            ("Chhota Imambara", "Heritage", "An ornate congregation hall with chandeliers and gardens.", 50.0, "06:00:00", "17:00:00", 60),
            ("Rumi Darwaza", "Heritage", "An imposing historic gateway built by Nawab Asaf-ud-Daula.", 0.0, "00:00:00", "23:59:59", 30),
            ("British Residency Lucknow", "Heritage", "Ruins of colonial buildings, key in the 1857 Uprising.", 25.0, "07:00:00", "18:00:00", 90),
            ("Hazratganj Market", "City", "The central shopping street of Lucknow, famous for Chikankari clothes.", 0.0, "10:00:00", "22:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Sample local Tunday Kababi and buy authentic Chikankari.")
    },

    # Madhya Pradesh
    {
        "name": "Khajuraho", "city": "Khajuraho", "state": "Madhya Pradesh", "region": "Central", "category": "Heritage",
        "desc": "A UNESCO World Heritage site famous for its magnificent Nagara-style Hindu and Jain temples.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.8,
        "attractions": [
            ("Kandariya Mahadeva Temple", "Heritage", "The largest and most ornate temple in the western group.", 40.0, "06:00:00", "18:00:00", 90),
            ("Lakshmana Temple", "Heritage", "A well-preserved temple dedicated to Vaikuntha Vishnu.", 40.0, "06:00:00", "18:00:00", 60),
            ("Duladeo Temple", "Heritage", "A late temple in the southern group, dedicated to Shiva.", 0.0, "06:00:00", "18:00:00", 45),
            ("Archaeological Museum Khajuraho", "Heritage", "A museum housing sculptures recovered from site digs.", 10.0, "09:00:00", "17:00:00", 60),
            ("Raneh Falls", "Nature", "A natural waterfall forming a deep canyon in crystalline rocks.", 100.0, "08:00:00", "17:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "12°C - 26°C", "Low", "Attend the light and sound show at Western Group of Temples.")
    },
    {
        "name": "Pachmarhi", "city": "Pachmarhi", "state": "Madhya Pradesh", "region": "Central", "category": "Nature",
        "desc": "Known as the Queen of Satpura, a green hill station with waterfalls, caves, and scenic viewpoints.",
        "season": "Summer", "days": 2, "budget": "Budget", "cost": 2000.0, "rating": 4.6,
        "attractions": [
            ("Bee Falls", "Nature", "A popular waterfall supplying drinking water to the town.", 15.0, "09:00:00", "17:00:00", 90),
            ("Dhoopgarh Peak", "Nature", "The highest point in Madhya Pradesh, offering sunsets.", 0.0, "06:00:00", "19:00:00", 120),
            ("Pandav Caves", "Heritage", "Five rock-cut Buddhist temples where Pandavas allegedly stayed.", 0.0, "08:00:00", "18:00:00", 60),
            ("Jata Shankar Caves", "Spiritual", "A natural cave shrine of Lord Shiva located in a ravine.", 0.0, "07:00:00", "19:00:00", 90),
            ("Handi Khoh", "Nature", "A deep, forest-covered ravine with a 300-foot cliff.", 0.0, "09:00:00", "17:00:00", 45)
        ],
        "season_detail": ("Summer", "October to June", "18°C - 35°C", "Moderate", "Hire a local gypsy to navigate Satpura Biosphere Reserve.")
    },
    {
        "name": "Orchha", "city": "Orchha", "state": "Madhya Pradesh", "region": "Central", "category": "Heritage",
        "desc": "A medieval town frozen in time, displaying spectacular forts and chhatris along the Betwa River.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.7,
        "attractions": [
            ("Orchha Fort Complex", "Heritage", "A huge fort compound containing Raja Mahal and Jahangir Mahal.", 50.0, "09:00:00", "17:00:00", 120),
            ("Chaturbhuj Temple", "Spiritual", "A colossal temple constructed on a massive stone platform.", 0.0, "06:00:00", "20:00:00", 90),
            ("Orchha Chhatris", "Heritage", "Fourteen majestic stone cenotaphs on the banks of Betwa River.", 0.0, "08:00:00", "18:00:00", 90),
            ("Ram Raja Temple", "Spiritual", "The only temple where Lord Ram is worshipped as a reigning King.", 0.0, "08:00:00", "22:00:00", 60),
            ("Laxminarayan Temple Orchha", "Spiritual", "A grand temple displaying a unique mix of fort and temple design.", 0.0, "09:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Enjoy river rafting on Betwa River near the Chhatris.")
    },
    {
        "name": "Gwalior", "city": "Gwalior", "state": "Madhya Pradesh", "region": "Central", "category": "Heritage",
        "desc": "Famous for its imposing Gwalior Fort, ancient temples, palaces, and musical legacy.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2200.0, "rating": 4.6,
        "attractions": [
            ("Gwalior Fort", "Heritage", "An ancient fort complex described as the pearl in the necklace.", 75.0, "06:00:00", "17:30:00", 150),
            ("Jai Vilas Palace Museum", "Heritage", "The majestic Italianate palace of Scindias containing museums.", 150.0, "10:00:00", "17:00:00", 120),
            ("Sas Bahu Temples", "Spiritual", "Two twin 11th-century temples displaying beautiful carvings.", 0.0, "08:00:00", "18:00:00", 60),
            ("Tomb of Tansen", "Heritage", "The final resting place of Akbar's legendary musician.", 0.0, "08:00:00", "20:00:00", 45),
            ("Sun Temple Gwalior", "Spiritual", "A red sandstone temple built replicating Konark design.", 0.0, "06:00:00", "20:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Observe the impressive sound and light show at the fort.")
    },

    # Maharashtra
    {
        "name": "Mumbai", "city": "Mumbai", "state": "Maharashtra", "region": "West", "category": "City",
        "desc": "The financial capital of India, a bustling metropolis known as the City of Dreams.",
        "season": "Winter", "days": 3, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Gateway of India", "Heritage", "An iconic arch monument built during the British Raj.", 0.0, "00:00:00", "23:59:59", 45),
            ("Marine Drive", "City", "A scenic 3km promenade overlooking the Arabian Sea.", 0.0, "00:00:00", "23:59:59", 90),
            ("Chhatrapati Shivaji Maharaj Terminus", "Heritage", "A UNESCO-listed Victorian Gothic railway terminal.", 0.0, "00:00:00", "23:59:59", 45),
            ("Elephanta Caves", "Spiritual", "A network of cave temples carved on Elephanta Island.", 250.0, "09:00:00", "17:00:00", 240),
            ("Siddhivinayak Temple", "Spiritual", "A highly revered temple dedicated to Lord Ganesha.", 0.0, "05:30:00", "22:00:00", 90),
            ("Haji Ali Dargah", "Spiritual", "A mosque and tomb located on an islet off the coast.", 0.0, "06:00:00", "22:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "18°C - 30°C", "Low", "Travel in local trains during non-peak hours to avoid massive crowds.")
    },
    {
        "name": "Pune", "city": "Pune", "state": "Maharashtra", "region": "West", "category": "City",
        "desc": "The cultural capital of Maharashtra, known as the Oxford of the East.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2400.0, "rating": 4.5,
        "attractions": [
            ("Shaniwar Wada", "Heritage", "A historic fortification seat of Peshwas of Maratha Empire.", 25.0, "08:00:00", "18:30:00", 90),
            ("Aga Khan Palace", "Heritage", "A majestic palace which served as a prison for Mahatma Gandhi.", 50.0, "09:00:00", "17:30:00", 90),
            ("Dagadusheth Halwai Ganapathi Temple", "Spiritual", "A famous temple housing a massive golden Ganesha idol.", 0.0, "06:00:00", "23:00:00", 60),
            ("Sinhagad Fort", "Adventure", "A hillside fortress offering trekking and panoramic views.", 50.0, "06:00:00", "18:00:00", 180),
            ("Osho Ashram", "Spiritual", "A tranquil meditation resort campus in Koregaon Park.", 970.0, "09:00:00", "18:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 28°C", "Low", "Try regional street food like Misal Pav and Vada Pav.")
    },
    {
        "name": "Mahabaleshwar", "city": "Mahabaleshwar", "state": "Maharashtra", "region": "West", "category": "Hill Station",
        "desc": "A popular Western Ghats hill station, famous for strawberry farms, viewpoints, and lakes.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.6,
        "attractions": [
            ("Venna Lake", "Nature", "A scenic lake offering boating and horse riding on banks.", 150.0, "08:00:00", "20:00:00", 90),
            ("Arthur's Seat Mahabaleshwar", "Nature", "A popular viewpoint overlooking the deep Savitri valley.", 0.0, "09:00:00", "18:00:00", 60),
            ("Mapro Garden", "Nature", "A strawberry processing park offering cafes and retail shops.", 0.0, "08:00:00", "23:00:00", 90),
            ("Pratapgad Fort", "Heritage", "A historic hill fort built by Chhatrapati Shivaji Maharaj.", 0.0, "08:00:00", "18:00:00", 120),
            ("Mahabaleshwar Mandir", "Spiritual", "An old temple containing natural water springs.", 0.0, "06:00:00", "21:00:00", 45)
        ],
        "season_detail": ("Winter", "November to February", "12°C - 25°C", "Low", "Visit strawberry farms in winter to taste fresh berries.")
    },
    {
        "name": "Lonavala", "city": "Lonavala", "state": "Maharashtra", "region": "West", "category": "Hill Station",
        "desc": "A green getaway in the Sahyadri mountains, famous for lush valleys, chikki, and ancient caves.",
        "season": "Monsoon", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Karla Caves", "Spiritual", "Ancient Buddhist rock-cut caves dating back to 2nd century BC.", 25.0, "09:00:00", "18:00:00", 90),
            ("Bhushi Dam", "Nature", "A popular masonry dam where people enjoy water cascading over steps.", 0.0, "09:00:00", "17:00:00", 120),
            ("Lohagad Fort", "Adventure", "A grand hill fort built on a long mountain spur.", 0.0, "09:00:00", "18:00:00", 150),
            ("Tiger's Point Lonavala", "Nature", "A cliff viewpoint offering views of waterfalls and clouds.", 0.0, "06:00:00", "19:00:00", 60),
            ("Lonavala Wax Museum", "City", "An entertainment wax museum featuring life-like statues.", 200.0, "09:00:00", "21:30:00", 90)
        ],
        "season_detail": ("Monsoon", "June to September", "18°C - 26°C", "Heavy Rainfall", "Monsoon is best to experience waterfalls and misty hills.")
    },

    # Goa
    {
        "name": "North Goa", "city": "Panaji", "state": "Goa", "region": "West", "category": "Beach",
        "desc": "Famous for its golden beaches, night bazaars, parties, and water adventure activities.",
        "season": "Winter", "days": 3, "budget": "Moderate", "cost": 3500.0, "rating": 4.8,
        "attractions": [
            ("Calangute Beach", "Beach", "The Queen of Beaches, famous for seafood and water sports.", 0.0, "06:00:00", "23:00:00", 120),
            ("Baga Beach", "Beach", "A happening beach known for nightlife, shacks, and water sports.", 0.0, "06:00:00", "23:59:59", 120),
            ("Aguada Fort", "Heritage", "A 17th-century Portuguese fortress and lighthouse.", 25.0, "09:00:00", "18:00:00", 90),
            ("Anjuna Flea Market", "City", "A bustling Wednesday market offering clothing, jewelry, and spices.", 0.0, "09:00:00", "18:00:00", 150),
            ("Basilica of Bom Jesus", "Spiritual", "UNESCO world heritage site containing mortal remains of St. Francis Xavier.", 0.0, "09:00:00", "18:30:00", 90),
            ("Chapora Fort", "Heritage", "Hilltop fort famous for Dil Chahta Hai movie views.", 0.0, "09:00:00", "17:30:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Very Low", "Rent a scooter locally to explore beaches comfortably.")
    },
    {
        "name": "South Goa", "city": "Margao", "state": "Goa", "region": "West", "category": "Beach",
        "desc": "Best known for quiet beaches, Portuguese architecture mansions, and peaceful resorts.",
        "season": "Winter", "days": 3, "budget": "Luxury", "cost": 4500.0, "rating": 4.7,
        "attractions": [
            ("Colva Beach", "Beach", "A quiet white-sand beach lined with palms and shacks.", 0.0, "06:00:00", "23:00:00", 90),
            ("Palolem Beach", "Beach", "A beautiful crescent-shaped beach offering dolphin cruises.", 0.0, "06:00:00", "22:00:00", 120),
            ("Cabo de Rama Fort", "Heritage", "A historic fort overlooking the blue ocean waters.", 0.0, "09:00:00", "17:30:00", 90),
            ("Dudhsagar Waterfalls", "Nature", "A four-tiered waterfall falling down steep mountains.", 400.0, "09:00:00", "16:00:00", 240),
            ("Margao Municipal Market", "City", "A traditional Goan market selling spices and fresh fish.", 0.0, "08:00:00", "20:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Very Low", "Choose South Goa for a quiet, relaxing holiday.")
    },

    # Karnataka
    {
        "name": "Hampi", "city": "Hampi", "state": "Karnataka", "region": "South", "category": "Heritage",
        "desc": "A UNESCO World Heritage site featuring ruins of the Vijayanagara Empire situated amidst boulder hills.",
        "season": "Winter", "days": 3, "budget": "Budget", "cost": 1800.0, "rating": 4.9,
        "attractions": [
            ("Virupaksha Temple", "Spiritual", "An active 7th-century Hindu temple dedicated to Shiva.", 25.0, "06:00:00", "18:00:00", 90),
            ("Vijaya Vittala Temple", "Heritage", "Famous temple housing the iconic stone chariot.", 40.0, "08:30:00", "17:30:00", 120),
            ("Hampi Stone Chariot", "Heritage", "A monumental shrine carved in the shape of a stone chariot.", 0.0, "08:30:00", "17:30:00", 30),
            ("Lotus Mahal Hampi", "Heritage", "A beautiful secular palace showcasing Indo-Islamic design.", 0.0, "08:30:00", "17:30:00", 60),
            ("Matanga Hill", "Nature", "A hill offering gorgeous sunrise and sunset views over Hampi.", 0.0, "05:00:00", "19:00:00", 90),
            ("Elephant Stables Hampi", "Heritage", "Eleven large domed chambers designed for royal elephants.", 0.0, "08:30:00", "17:30:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 33°C", "Low", "Rent a bicycle to explore the vast ruins easily.")
    },
    {
        "name": "Coorg", "city": "Madikeri", "state": "Karnataka", "region": "South", "category": "Hill Station",
        "desc": "Often called the Scotland of India, famous for coffee plantations and mist-covered hills.",
        "season": "Autumn", "days": 3, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Abbey Falls", "Nature", "A scenic waterfall surrounded by cardamom plantations.", 15.0, "09:00:00", "17:00:00", 90),
            ("Raja's Seat", "Nature", "A seasonal flower garden providing spectacular valley views.", 5.0, "06:00:00", "20:00:00", 60),
            ("Dubare Elephant Camp", "Wildlife", "An elephant training camp next to the Cauvery River.", 100.0, "09:00:00", "17:00:00", 150),
            ("Namdroling Golden Temple", "Spiritual", "A gorgeous Tibetan Buddhist monastery housing large statues.", 0.0, "09:00:00", "18:00:00", 120),
            ("Talakaveri", "Spiritual", "The source birthplace of the sacred Cauvery River.", 0.0, "06:00:00", "20:30:00", 90)
        ],
        "season_detail": ("Autumn", "October to April", "15°C - 28°C", "Moderate", "Buy local spices, honey, and fresh coffee beans.")
    },
    {
        "name": "Mysore", "city": "Mysore", "state": "Karnataka", "region": "South", "category": "Heritage",
        "desc": "The cultural capital of Karnataka, famous for its grand palaces, temples, and sandalwood.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2400.0, "rating": 4.8,
        "attractions": [
            ("Mysore Palace", "Heritage", "The majestic royal palace seat of Wodeyar dynasty.", 100.0, "10:00:00", "17:30:00", 120),
            ("Chamundeshwari Temple", "Spiritual", "A hilltop temple dedicated to Chamundeshwari deity.", 0.0, "07:30:00", "21:00:00", 90),
            ("Brindavan Gardens", "Nature", "Beautiful terrace gardens famous for musical fountain shows.", 50.0, "09:00:00", "21:00:00", 120),
            ("Mysore Zoo", "Wildlife", "One of the oldest and most famous zoos in India.", 100.0, "08:30:00", "17:30:00", 150),
            ("St. Philomena's Church Mysore", "Heritage", "A tall Gothic style cathedral containing relics.", 0.0, "05:00:00", "18:00:00", 45)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 30°C", "Low", "Visit Mysore Palace illuminated on Sunday nights.")
    },
    {
        "name": "Bengaluru", "city": "Bengaluru", "state": "Karnataka", "region": "South", "category": "City",
        "desc": "The Silicon Valley of India, known for parks, tech hubs, microbreweries, and museums.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 4000.0, "rating": 4.6,
        "attractions": [
            ("Lalbagh Botanical Garden", "Nature", "A historic 240-acre greenhouse garden built by Hyder Ali.", 25.0, "06:00:00", "19:00:00", 90),
            ("Bangalore Palace", "Heritage", "A majestic Tudor style palace resembling Windsor Castle.", 230.0, "10:00:00", "17:30:00", 120),
            ("Cubbon Park", "Nature", "A huge green park located in the central administrative area.", 0.0, "06:00:00", "18:00:00", 90),
            ("Visvesvaraya Museum", "City", "An interactive science and technology museum.", 85.0, "10:00:00", "18:00:00", 150),
            ("Bull Temple", "Spiritual", "An old temple hosting a massive monolithic Nandi bull.", 0.0, "06:00:00", "20:00:00", 45)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 30°C", "Low", "Take a stroll in Cubbon Park on Sunday mornings.")
    },
    {
        "name": "Gokarna", "city": "Gokarna", "state": "Karnataka", "region": "South", "category": "Beach",
        "desc": "A pilgrimage town turned beach paradise, offering rocky coastline cliffs and temples.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1600.0, "rating": 4.6,
        "attractions": [
            ("Mahabaleshwar Temple Gokarna", "Spiritual", "A sacred Shiva temple housing the Atma Linga.", 0.0, "06:00:00", "20:00:00", 90),
            ("Om Beach", "Beach", "A naturally shaped Om symbol beach offering boat rides.", 0.0, "00:00:00", "23:59:59", 120),
            ("Kudle Beach", "Beach", "A wide sandy beach famous for sunsets and beach volleyball.", 0.0, "00:00:00", "23:59:59", 90),
            ("Half Moon Beach", "Beach", "A small secluded cove reachable by trekking over cliffs.", 0.0, "00:00:00", "23:59:59", 120),
            ("Paradise Beach Gokarna", "Beach", "A remote rocky beach popular with campers.", 0.0, "00:00:00", "23:59:59", 120)
        ],
        "season_detail": ("Winter", "October to March", "18°C - 32°C", "Low", "Trek between the five major beaches during sunset.")
    },

    # Tamil Nadu
    {
        "name": "Ooty", "city": "Ooty", "state": "Tamil Nadu", "region": "South", "category": "Hill Station",
        "desc": "The Queen of Hill Stations, located in the blue Nilgiri Hills, famous for tea gardens.",
        "season": "Summer", "days": 3, "budget": "Moderate", "cost": 2800.0, "rating": 4.6,
        "attractions": [
            ("Ooty Botanical Gardens", "Nature", "A terraced garden featuring fossilized tree trunks.", 30.0, "07:00:00", "18:30:00", 120),
            ("Ooty Lake", "Nature", "An artificial lake offering boating and a mini train.", 100.0, "09:00:00", "18:00:00", 90),
            ("Doddabetta Peak", "Nature", "The highest point in South India, offering telescopic views.", 10.0, "09:00:00", "18:00:00", 90),
            ("Nilgiri Mountain Railway", "Heritage", "A historic steam engine toy train journey.", 200.0, "07:00:00", "15:00:00", 300),
            ("Ooty Rose Garden", "Nature", "An extensive rose garden showing thousands of varieties.", 30.0, "09:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Summer", "April to June", "15°C - 25°C", "Moderate", "Book Nilgiri Toy Train tickets in advance on IRCTC.")
    },
    {
        "name": "Kodaikanal", "city": "Kodaikanal", "state": "Tamil Nadu", "region": "South", "category": "Hill Station",
        "desc": "The Princess of Hill Stations, featuring high forests, waterfalls, and Kodai Lake.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Kodaikanal Lake", "Nature", "A star-shaped lake offering rowing boats.", 100.0, "09:00:00", "18:00:00", 90),
            ("Coaker's Walk", "Nature", "A scenic paved pathway along steep mountain cliffs.", 10.0, "07:00:00", "19:00:00", 60),
            ("Bryant Park", "Nature", "A botanical garden showing structural roses and dahlias.", 30.0, "09:00:00", "18:00:00", 90),
            ("Silver Cascade Falls", "Nature", "A roadside waterfall coming down from cliffs.", 0.0, "00:00:00", "23:59:59", 30),
            ("Pillar Rocks", "Nature", "Three granite boulders standing vertically in cliffs.", 5.0, "09:00:00", "16:30:00", 60)
        ],
        "season_detail": ("Summer", "April to June", "15°C - 25°C", "Moderate", "Rent a bicycle to ride around Kodaikanal Lake path.")
    },
    {
        "name": "Chennai", "city": "Chennai", "state": "Tamil Nadu", "region": "South", "category": "City",
        "desc": "The gateway to South India, blending rich temples, beaches, and automotive industries.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2400.0, "rating": 4.5,
        "attractions": [
            ("Marina Beach", "Beach", "The longest natural urban beach in the country.", 0.0, "00:00:00", "23:59:59", 90),
            ("Kapaleeshwarar Temple", "Spiritual", "A Dravidian temple showcasing towering Gopurams.", 0.0, "05:00:00", "21:00:00", 90),
            ("Fort St. George Museum", "Heritage", "A British fort enclosing assembly structures.", 100.0, "09:00:00", "17:00:00", 90),
            ("Government Museum Chennai", "Heritage", "A large museum containing Bronze artifacts.", 15.0, "09:30:00", "17:00:00", 120),
            ("San Thome Basilica", "Spiritual", "A neo-Gothic cathedral built over the tomb of St. Thomas.", 0.0, "06:00:00", "21:00:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 30°C", "Moderate", "Visit Marina Beach during early mornings or evenings.")
    },
    {
        "name": "Mahabalipuram", "city": "Mahabalipuram", "state": "Tamil Nadu", "region": "South", "category": "Heritage",
        "desc": "Famous for its rock-cut cave temples and monolithic structures from the Pallava dynasty.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2200.0, "rating": 4.7,
        "attractions": [
            ("Shore Temple", "Heritage", "An old temple built overlooking the Bay of Bengal.", 40.0, "06:00:00", "18:00:00", 90),
            ("Pancha Rathas", "Heritage", "Five monolithic rock-cut chariot structures.", 40.0, "06:00:00", "18:00:00", 90),
            ("Krishna's Butterball", "Nature", "A giant balancing granite boulder resting on a slope.", 0.0, "06:00:00", "18:00:00", 45),
            ("Arjuna's Penance", "Heritage", "A colossal bas-relief carving detailing mythical tales.", 0.0, "06:00:00", "18:00:00", 45),
            ("Mahabalipuram Beach", "Beach", "A sandy beach situated adjacent to Shore Temple.", 0.0, "00:00:00", "23:59:59", 90)
        ],
        "season_detail": ("Winter", "October to March", "18°C - 30°C", "Low", "Observe the magnificent relief carvings using a local guide.")
    },
    {
        "name": "Madurai", "city": "Madurai", "state": "Tamil Nadu", "region": "South", "category": "Spiritual",
        "desc": "One of the oldest continuously inhabited cities in India, centered around Meenakshi Temple.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1600.0, "rating": 4.8,
        "attractions": [
            ("Meenakshi Amman Temple", "Spiritual", "A massive temple displaying 14 colorful Gopurams.", 0.0, "05:00:00", "22:00:00", 150),
            ("Thirumalai Nayakkar Mahal", "Heritage", "A 17th-century palace showing grand pillars.", 10.0, "09:00:00", "17:00:00", 90),
            ("Gandhi Memorial Museum Madurai", "Heritage", "A museum housing the blood-stained garment of Gandhi.", 0.0, "10:00:00", "17:45:00", 90),
            ("Alagar Koyil", "Spiritual", "A temple of Lord Vishnu situated on hills.", 0.0, "06:00:00", "18:00:00", 90),
            ("Vandiyur Mariamman Teppakulam", "Spiritual", "A massive temple tank reservoir with an island temple.", 0.0, "06:00:00", "21:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "20°C - 32°C", "Low", "Dress conservatively when entering Meenakshi Temple.")
    },
    {
        "name": "Rameswaram", "city": "Rameswaram", "state": "Tamil Nadu", "region": "South", "category": "Spiritual",
        "desc": "A holy island city, containing one of the Char Dham pilgrimage sites, linked by Pamban Bridge.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1500.0, "rating": 4.8,
        "attractions": [
            ("Ramanathaswamy Temple", "Spiritual", "Famous for its massive pillared corridors.", 0.0, "05:00:00", "21:00:00", 120),
            ("Pamban Bridge", "Heritage", "A historic cantilever railway bridge crossing sea waters.", 0.0, "00:00:00", "23:59:59", 45),
            ("Dhanushkodi Beach", "Beach", "A ghost town beach at the tip of India's border.", 0.0, "06:00:00", "18:00:00", 120),
            ("Agnitheertham", "Spiritual", "The sacred beach where pilgrims bathe before entering temples.", 0.0, "05:00:00", "18:00:00", 60),
            ("Dr. A.P.J. Abdul Kalam Memorial", "Heritage", "A memorial built honoring India's Missile Man.", 0.0, "09:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "20°C - 30°C", "Low", "Take a holy dip in the 22 temple wells.")
    },
    {
        "name": "Kanyakumari", "city": "Kanyakumari", "state": "Tamil Nadu", "region": "South", "category": "Nature",
        "desc": "The southernmost tip of mainland India, famous for sunrise/sunset over three oceans.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.7,
        "attractions": [
            ("Vivekananda Rock Memorial", "Spiritual", "A memorial built on a rock offshore.", 50.0, "08:00:00", "16:00:00", 120),
            ("Thiruvalluvar Statue", "Heritage", "A 133-foot tall stone statue of Tamil poet.", 0.0, "08:00:00", "16:00:00", 60),
            ("Kanyakumari Temple", "Spiritual", "A 3000-year-old temple overlooking the ocean.", 0.0, "04:30:00", "20:30:00", 60),
            ("Sunset View Point", "Nature", "A popular beach view point showing spectacular sunsets.", 0.0, "16:00:00", "19:00:00", 60),
            ("Triveni Sangam", "Nature", "The confluence of Bay of Bengal, Arabian Sea, and Indian Ocean.", 0.0, "00:00:00", "23:59:59", 45)
        ],
        "season_detail": ("Winter", "October to March", "22°C - 33°C", "Low", "Arrive early at the ferry to Vivekananda Rock to beat queues.")
    },

    # Kerala
    {
        "name": "Munnar", "city": "Munnar", "state": "Kerala", "region": "South", "category": "Hill Station",
        "desc": "A scenic hill station famous for rolling hills, tea museums, and rare Nilgiri tahr wildlife.",
        "season": "Autumn", "days": 3, "budget": "Moderate", "cost": 3000.0, "rating": 4.8,
        "attractions": [
            ("Eravikulam National Park", "Wildlife", "Home of the endangered Nilgiri Tahr mountain goat.", 200.0, "07:30:00", "16:00:00", 180),
            ("Mattupetty Dam", "Nature", "A scenic masonry dam offering speed boat rides.", 30.0, "09:00:00", "17:00:00", 90),
            ("Anamudi Peak", "Nature", "The highest mountain peak in South India.", 0.0, "08:00:00", "16:00:00", 120),
            ("Tea Museum Munnar", "Heritage", "A museum tracking history of local tea estates.", 75.0, "09:00:00", "17:00:00", 90),
            ("Echo Point Munnar", "Nature", "A scenic lake point famous for natural acoustics.", 0.0, "06:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Autumn", "September to May", "15°C - 25°C", "Moderate", "Avoid trekking in national park during monsoon landslide season.")
    },
    {
        "name": "Alleppey", "city": "Alappuzha", "state": "Kerala", "region": "South", "category": "Nature",
        "desc": "The Venice of the East, famous for houseboat cruises in the peaceful palm-fringed backwaters.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3200.0, "rating": 4.8,
        "attractions": [
            ("Alleppey Backwaters", "Nature", "A network of canals, lagoons, and rivers with houseboats.", 0.0, "00:00:00", "23:59:59", 240),
            ("Alappuzha Beach", "Beach", "A sandy beach featuring a 150-year-old historic pier.", 0.0, "06:00:00", "22:00:00", 90),
            ("Pathiramanal Island", "Nature", "A small island haven for rare migratory birds.", 0.0, "06:00:00", "18:00:00", 120),
            ("Krishnapuram Palace", "Heritage", "A palace displaying fine murals and antiquities.", 20.0, "09:00:00", "16:30:00", 90),
            ("Alleppey Lighthouse", "Heritage", "An old red-white lighthouse offering panoramic views.", 20.0, "15:00:00", "17:00:00", 45)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Low", "Opt for an overnight houseboat stay for backwater views.")
    },
    {
        "name": "Wayanad", "city": "Kalpetta", "state": "Kerala", "region": "South", "category": "Nature",
        "desc": "A green mountainous district offering ancient caves, spice plantations, and waterfalls.",
        "season": "Autumn", "days": 3, "budget": "Moderate", "cost": 2500.0, "rating": 4.6,
        "attractions": [
            ("Banasura Sagar Dam", "Nature", "The largest earth dam in India, offering boating.", 40.0, "09:00:00", "17:00:00", 120),
            ("Edakkal Caves", "Heritage", "Caves displaying Neolithic rock carvings.", 20.0, "09:00:00", "16:00:00", 120),
            ("Chembra Peak", "Adventure", "A popular trekking peak hosting a heart-shaped lake.", 20.0, "07:00:00", "14:00:00", 240),
            ("Soochipara Waterfalls", "Nature", "A three-tiered waterfall surrounded by forests.", 50.0, "09:00:00", "17:00:00", 90),
            ("Pookode Lake", "Nature", "A natural freshwater lake offering paddle boats.", 30.0, "09:00:00", "17:00:00", 90)
        ],
        "season_detail": ("Autumn", "October to May", "18°C - 28°C", "Moderate", "Edakkal Caves are closed on Mondays. Wear sturdy shoes.")
    },
    {
        "name": "Kovalam", "city": "Kovalam", "state": "Kerala", "region": "South", "category": "Beach",
        "desc": "Famous for its three crescent beaches and a historic red-striped lighthouse.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 4000.0, "rating": 4.7,
        "attractions": [
            ("Lighthouse Beach", "Beach", "The most popular beach, dominated by a tall lighthouse.", 0.0, "06:00:00", "22:00:00", 120),
            ("Hawa Beach", "Beach", "Also known as Eve's beach, popular for catamaran rides.", 0.0, "06:00:00", "22:00:00", 90),
            ("Samudra Beach", "Beach", "A quiet sandy beach located in northern Kovalam.", 0.0, "06:00:00", "22:00:00", 90),
            ("Halcyon Castle", "Heritage", "A palace built by the Royal Family of Travancore.", 0.0, "09:00:00", "18:00:00", 45),
            ("Vellayani Lake", "Nature", "A scenic freshwater lake located in Kovalam suburbs.", 0.0, "08:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "22°C - 33°C", "Low", "Climb the lighthouse at Lighthouse Beach for views.")
    },
    {
        "name": "Thekkady", "city": "Kumily", "state": "Kerala", "region": "South", "category": "Wildlife",
        "desc": "Home to the Periyar National Park, offering boat safaris, elephants, and spices.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.7,
        "attractions": [
            ("Periyar National Park Boat Cruise", "Wildlife", "A lake boat cruise to spot wild elephants.", 250.0, "07:00:00", "15:00:00", 120),
            ("Periyar Tiger Trail", "Wildlife", "A guided trekking trail inside tiger habitats.", 3000.0, "07:00:00", "16:00:00", 300),
            ("Abraham's Spice Garden", "Nature", "An organic farm explaining spice crops.", 100.0, "08:00:00", "18:00:00", 90),
            ("Anakkara", "Nature", "A spice cultivation hub offering local shopping.", 0.0, "09:00:00", "19:00:00", 90),
            ("Mangala Devi Temple", "Spiritual", "A ancient temple situated deep in reserve forests.", 0.0, "06:00:00", "17:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 28°C", "Moderate", "Book Periyar boat cruise tickets early in morning.")
    },
    {
        "name": "Kochi", "city": "Kochi", "state": "Kerala", "region": "South", "category": "Heritage",
        "desc": "The Queen of the Arabian Sea, blending Chinese, Portuguese, Dutch, and British history.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.8,
        "attractions": [
            ("Fort Kochi Beach", "Beach", "A beach famous for giant Chinese Fishing Nets.", 0.0, "06:00:00", "22:00:00", 90),
            ("Mattancherry Palace", "Heritage", "Also known as the Dutch Palace, hosting historic murals.", 5.0, "09:00:00", "17:00:00", 90),
            ("Paradesi Synagogue", "Spiritual", "The oldest active synagogue in the Commonwealth.", 5.0, "10:00:00", "17:00:00", 60),
            ("Santa Cruz Cathedral Basilica", "Spiritual", "A grand Gothic style basilica built by Portuguese.", 0.0, "09:00:00", "18:00:00", 60),
            ("St. Francis Church Kochi", "Heritage", "The oldest European church in India, where Vasco da Gama lay buried.", 0.0, "09:00:00", "17:00:00", 45)
        ],
        "season_detail": ("Winter", "November to February", "22°C - 32°C", "Moderate", "Observe Chinese fishing nets action in evening.")
    },
    {
        "name": "Varkala", "city": "Varkala", "state": "Kerala", "region": "South", "category": "Beach",
        "desc": "Famous for its unique red cliffs adjacent to the Arabian Sea, offering cafes and beaches.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.7,
        "attractions": [
            ("Varkala Cliff Beach", "Beach", "A sandy beach framed by unique towering red cliffs.", 0.0, "06:00:00", "22:00:00", 120),
            ("Janardhana Swamy Temple", "Spiritual", "A 2000-year-old temple dedicated to Lord Vishnu.", 0.0, "06:00:00", "20:00:00", 90),
            ("Kappil Beach", "Beach", "A quiet estuary beach where lakes merge with the sea.", 0.0, "00:00:00", "23:59:59", 90),
            ("Anjengo Fort", "Heritage", "An old British fort constructed in the late 17th century.", 0.0, "09:00:00", "18:00:00", 60),
            ("Sivagiri Mutt", "Spiritual", "A sacred ashram pilgrimage founded by Sree Narayana Guru.", 0.0, "06:00:00", "19:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "22°C - 32°C", "Low", "Enjoy dinner at Varkala Cliff cliffside cafes.")
    },
    {
        "name": "Kumarakom", "city": "Kumarakom", "state": "Kerala", "region": "South", "category": "Nature",
        "desc": "A quiet backwater town on Vembanad Lake, famous for luxury resorts and bird sanctuaries.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Kumarakom Bird Sanctuary", "Wildlife", "A sanctuary hosting rare migratory birds.", 50.0, "06:30:00", "17:00:00", 120),
            ("Vembanad Lake Boating", "Nature", "A boat cruise on the largest lake in Kerala.", 300.0, "09:00:00", "18:00:00", 90),
            ("Aravukad Temple", "Spiritual", "A historic local temple showing fine architecture.", 0.0, "06:00:00", "19:00:00", 45),
            ("Bay Island Driftwood Museum", "Heritage", "A museum housing unique driftwood sculptures.", 50.0, "10:00:00", "17:00:00", 60),
            ("Kumarakom Beach", "Beach", "A small sandy beach area next to local resorts.", 0.0, "06:00:00", "19:00:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Low", "Great base for luxury Ayurvedic spa resorts.")
    },

    # West Bengal & Sikkim
    {
        "name": "Darjeeling", "city": "Darjeeling", "state": "West Bengal", "region": "East", "category": "Hill Station",
        "desc": "Famous for tea estates, views of Kanchenjunga, and the UNESCO Toy Train.",
        "season": "Spring", "days": 3, "budget": "Moderate", "cost": 3000.0, "rating": 4.8,
        "attractions": [
            ("Tiger Hill Darjeeling", "Nature", "A peak offering spectacular sunrise views over Mount Kanchenjunga.", 50.0, "04:00:00", "16:00:00", 90),
            ("Darjeeling Toy Train", "Heritage", "A historic Himalayan railway steam train ride.", 1400.0, "08:00:00", "16:00:00", 120),
            ("Batasia Loop", "Heritage", "A spiral railway loop surrounding a war memorial.", 20.0, "06:00:00", "17:00:00", 60),
            ("Padmaja Naidu Himalayan Zoo", "Wildlife", "A zoo conserving snow leopards and red pandas.", 100.0, "08:30:00", "16:30:00", 120),
            ("Himalayan Mountaineering Institute", "Heritage", "A mountaineering museum set up by Tenzing Norgay.", 100.0, "09:00:00", "17:00:00", 90),
            ("Ghoom Monastery", "Spiritual", "An old Tibetan Buddhist monastery housing Maitreya Buddha.", 0.0, "06:00:00", "18:00:00", 45)
        ],
        "season_detail": ("Spring", "October to May", "8°C - 20°C", "Moderate", "Wake up at 3:30 AM to catch the Tiger Hill sunrise.")
    },
    {
        "name": "Kalimpong", "city": "Kalimpong", "state": "West Bengal", "region": "East", "category": "Hill Station",
        "desc": "A quiet hill station known for nurseries, colonial buildings, and views of Teesta valley.",
        "season": "Spring", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.5,
        "attractions": [
            ("Durpin Monastery", "Spiritual", "A Buddhist monastery offering views of Kalimpong.", 0.0, "09:00:00", "17:00:00", 90),
            ("Pine View Nursery", "Nature", "A nursery showing hundreds of species of cacti.", 20.0, "08:30:00", "17:30:00", 60),
            ("Graham's Homes", "Heritage", "A sprawling school campus built in the British era.", 0.0, "09:00:00", "17:00:00", 90),
            ("Deolo Hill", "Nature", "A high park offering panoramic mountain views.", 20.0, "08:00:00", "18:00:00", 120),
            ("Morgan House", "Heritage", "A colonial British cottage now used as a tourist lodge.", 0.0, "09:00:00", "17:00:00", 45)
        ],
        "season_detail": ("Spring", "March to May", "15°C - 25°C", "Moderate", "Enjoy river rafting on Teesta River nearby.")
    },
    {
        "name": "Gangtok", "city": "Gangtok", "state": "Sikkim", "region": "East", "category": "Hill Station",
        "desc": "The capital of Sikkim, showcasing modern streets, monasteries, and cable cars.",
        "season": "Spring", "days": 3, "budget": "Moderate", "cost": 3200.0, "rating": 4.8,
        "attractions": [
            ("Rumtek Monastery", "Spiritual", "A highly sacred Tibetan Buddhist monastery complex.", 50.0, "08:00:00", "17:00:00", 120),
            ("Nathu La Pass", "Adventure", "A high mountain pass connecting India and Tibet.", 200.0, "08:00:00", "14:00:00", 240),
            ("Tsomgo Lake", "Nature", "A high altitude glacial lake situated at 3753 meters.", 0.0, "08:00:00", "15:00:00", 180),
            ("Gangtok Ropeway", "Adventure", "A cable car offering aerial views of Gangtok city.", 150.0, "09:30:00", "16:30:00", 60),
            ("MG Marg Gangtok", "City", "A clean pedestrian avenue with shops and cafes.", 0.0, "10:00:00", "21:30:00", 90),
            ("Hanuman Tok", "Spiritual", "A temple dedicated to Hanuman situated on high peaks.", 0.0, "07:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Spring", "October to June", "10°C - 22°C", "Low", "Nathu La requires a special inner line permit.")
    },
    {
        "name": "Pelling", "city": "Pelling", "state": "Sikkim", "region": "East", "category": "Hill Station",
        "desc": "Renowned for scenic monasteries, waterfalls, and India's first glass skywalk.",
        "season": "Spring", "days": 2, "budget": "Moderate", "cost": 2500.0, "rating": 4.6,
        "attractions": [
            ("Pemayangtse Monastery", "Spiritual", "An old premier Buddhist monastery in Sikkim.", 50.0, "09:00:00", "18:00:00", 90),
            ("Pelling Skywalk", "Adventure", "India's first glass skywalk offering views of Chenrezig statue.", 100.0, "09:00:00", "18:00:00", 120),
            ("Rabdentse Ruins", "Heritage", "The ancient ruins of the second capital of Sikkim.", 0.0, "09:00:00", "17:00:00", 90),
            ("Kanchenjunga Falls", "Nature", "A giant high waterfall crashing down rocky cliffs.", 20.0, "08:00:00", "17:00:00", 60),
            ("Khecheopalri Lake", "Spiritual", "A sacred wishing lake hidden in dense forests.", 20.0, "08:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Spring", "October to May", "10°C - 20°C", "Moderate", "Walk carefully on the Pelling Glass Skywalk.")
    },

    # Northeast
    {
        "name": "Shillong", "city": "Shillong", "state": "Meghalaya", "region": "Northeast", "category": "Hill Station",
        "desc": "The Scotland of the East, showcasing pine trees, waterfalls, and rock music culture.",
        "season": "Spring", "days": 3, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Shillong Peak", "Nature", "The highest point in Shillong offering city views.", 50.0, "09:00:00", "17:00:00", 90),
            ("Elephant Falls", "Nature", "A three-tiered waterfall with stepping walkways.", 20.0, "09:00:00", "17:00:00", 60),
            ("Umiam Lake", "Nature", "A massive reservoir lake offering water sports.", 50.0, "09:00:00", "18:00:00", 120),
            ("Don Bosco Museum", "Heritage", "A major museum of indigenous cultures of Northeast.", 100.0, "09:00:00", "17:30:00", 150),
            ("Ward's Lake", "Nature", "A horseshoe-shaped lake situated in city center.", 25.0, "09:00:00", "17:30:00", 90)
        ],
        "season_detail": ("Spring", "October to April", "15°C - 25°C", "Low", "Visit local cafes in Shillong for live rock performances.")
    },
    {
        "name": "Cherrapunji", "city": "Sohra", "state": "Meghalaya", "region": "Northeast", "category": "Nature",
        "desc": "Renowned for double decker living root bridges and being one of the wettest spots on earth.",
        "season": "Monsoon", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.8,
        "attractions": [
            ("Nohkalikai Falls", "Nature", "The tallest plunge waterfall in India, dropping 340 meters.", 20.0, "09:00:00", "17:00:00", 90),
            ("Double Decker Living Root Bridge", "Adventure", "A unique bio-engineered tree bridge at Nongriat.", 50.0, "06:00:00", "17:00:00", 240),
            ("Mawsmai Cave", "Adventure", "A lit limestone cave system showing stalactites.", 20.0, "09:00:00", "17:00:00", 90),
            ("Seven Sisters Falls Cherra", "Nature", "A seven-segmented plunge waterfall coming off cliffs.", 0.0, "09:00:00", "17:00:00", 60),
            ("Eco Park Cherrapunji", "Nature", "A park on cliffs offering views of Bangladesh plains.", 20.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Monsoon", "June to September", "15°C - 23°C", "Very Heavy", "Carry raincoats. Treks to root bridges are physically demanding.")
    },
    {
        "name": "Kaziranga", "city": "Kohora", "state": "Assam", "region": "Northeast", "category": "Wildlife",
        "desc": "A UNESCO site, hosting two-thirds of the world's great one-horned rhinoceroses.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 4500.0, "rating": 4.9,
        "attractions": [
            ("Elephant Safari Kaziranga", "Wildlife", "An early morning elephant safari to spot rhinos.", 800.0, "05:00:00", "07:30:00", 120),
            ("Jeep Safari Kaziranga", "Wildlife", "A safari exploring core zones like Kohora and Bagori.", 2000.0, "07:30:00", "16:00:00", 180),
            ("Kaziranga National Orchid Park", "Nature", "A large conservatory showcasing rare orchids.", 100.0, "08:00:00", "18:00:00", 90),
            ("Hollongapar Gibbon Sanctuary", "Wildlife", "Home of India's only gibbons, the Hoolock Gibbon.", 250.0, "06:00:00", "17:00:00", 150),
            ("Kakochang Waterfalls", "Nature", "A scenic waterfall located close to rubber estates.", 0.0, "08:00:00", "17:00:00", 120)
        ],
        "season_detail": ("Winter", "November to April", "10°C - 25°C", "Low", "National Park remains closed during the monsoon season.")
    },
    {
        "name": "Majuli", "city": "Majuli", "state": "Assam", "region": "Northeast", "category": "Nature",
        "desc": "The largest river island in the world, situated on the Brahmaputra River, famous for Satras.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1500.0, "rating": 4.6,
        "attractions": [
            ("Kamalabari Satra", "Spiritual", "A famous Vaishnavite monastery center for arts.", 0.0, "09:00:00", "17:00:00", 90),
            ("Dakhinpat Satra", "Spiritual", "A royal satra showing ancient manuscripts.", 0.0, "09:00:00", "17:00:00", 90),
            ("Garmur Satra", "Spiritual", "A prominent Satra housing old armaments.", 0.0, "09:00:00", "17:00:00", 60),
            ("Tengapania", "Nature", "A picnic spot situated next to Brahmaputra riverbanks.", 0.0, "08:00:00", "18:00:00", 60),
            ("Samaguri Satra", "Heritage", "Famed Satra known for masks craftsmanship.", 0.0, "09:00:00", "17:00:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "12°C - 25°C", "Low", "Ferry services from Jorhat are suspended in high currents.")
    },
    {
        "name": "Tawang", "city": "Tawang", "state": "Arunachal Pradesh", "region": "Northeast", "category": "Hill Station",
        "desc": "A mountain town known for Tawang Monastery and gorgeous high passes.",
        "season": "Spring", "days": 4, "budget": "Moderate", "cost": 3000.0, "rating": 4.8,
        "attractions": [
            ("Tawang Monastery", "Spiritual", "The second largest Buddhist monastery in the world.", 0.0, "07:00:00", "19:00:00", 120),
            ("Sela Pass", "Adventure", "A high mountain pass situated at 4170 meters.", 0.0, "08:00:00", "16:00:00", 120),
            ("Nuranang Falls", "Nature", "Also known as Jang Falls, a stunning 100-meter waterfall.", 0.0, "08:00:00", "17:00:00", 90),
            ("Maduri Lake", "Nature", "Originally called Sangestar Tso, formed by an earthquake.", 0.0, "08:00:00", "16:00:00", 120),
            ("Tawang War Memorial", "Heritage", "A stupa built honoring soldiers of 1962 Sino-Indian War.", 0.0, "09:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Spring", "March to June", "10°C - 22°C", "Moderate", "Inner Line Permit (ILP) is required to enter Arunachal.")
    },
    {
        "name": "Ziro", "city": "Ziro", "state": "Arunachal Pradesh", "region": "Northeast", "category": "Nature",
        "desc": "A scenic valley famous for Apatani culture and pine tree hills.",
        "season": "Autumn", "days": 2, "budget": "Budget", "cost": 1600.0, "rating": 4.5,
        "attractions": [
            ("Talle Valley Wildlife Sanctuary", "Wildlife", "A biodiversity reserve containing rare flora.", 50.0, "08:00:00", "16:30:00", 180),
            ("Meghna Cave Temple", "Spiritual", "A historic cave temple dedicated to Lord Shiva.", 0.0, "07:00:00", "18:00:00", 60),
            ("Tarin Fish Farm", "Nature", "A unique high altitude paddy-cum-fish culture farm.", 20.0, "09:00:00", "17:00:00", 60),
            ("Kile Pakho", "Nature", "A ridge offering panoramic valley views.", 0.0, "08:00:00", "17:00:00", 90),
            ("Ziro Putu", "Nature", "A small hillock offering panoramic Ziro valley views.", 0.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Autumn", "September to November", "15°C - 25°C", "Low", "Ziro Music Festival is held in late September.")
    },

    # Odisha & East India
    {
        "name": "Puri", "city": "Puri", "state": "Odisha", "region": "East", "category": "Spiritual",
        "desc": "A holy coastal city, famous for the Jagannath Temple and Puri golden beach.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.7,
        "attractions": [
            ("Jagannath Temple Puri", "Spiritual", "An ancient grand temple dedicated to Lord Jagannath.", 0.0, "05:00:00", "23:00:00", 120),
            ("Golden Beach Puri", "Beach", "A blue flag beach famous for sand art displays.", 20.0, "06:00:00", "22:00:00", 120),
            ("Chilika Lake at Satapada", "Nature", "A brackish lagoon offering dolphin watching cruises.", 200.0, "08:00:00", "17:00:00", 180),
            ("Gundicha Temple", "Spiritual", "A garden temple where deities stay during Ratha Yatra.", 0.0, "06:00:00", "21:00:00", 90),
            ("Raghurajpur Artist Village", "Heritage", "A heritage crafts village famous for Pattachitra art.", 0.0, "09:00:00", "18:00:00", 120)
        ],
        "season_detail": ("Winter", "October to March", "18°C - 30°C", "Low", "Only Hindus are permitted inside Jagannath Temple.")
    },
    {
        "name": "Konark", "city": "Konark", "state": "Odisha", "region": "East", "category": "Heritage",
        "desc": "Famous for the 13th-century Konark Sun Temple, a UNESCO world heritage site.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2200.0, "rating": 4.8,
        "attractions": [
            ("Konark Sun Temple", "Heritage", "A massive 13th-century chariot-shaped Sun temple.", 40.0, "06:00:00", "20:00:00", 120),
            ("Chandrabhaga Beach", "Beach", "A quiet sandy beach situated next to Sun Temple.", 0.0, "00:00:00", "23:59:59", 90),
            ("Konark Archaeological Museum", "Heritage", "A museum housing original temple carvings.", 10.0, "09:00:00", "17:00:00", 90),
            ("Kuruma Buddhist Site", "Heritage", "An ancient Buddhist monastery site located nearby.", 0.0, "08:00:00", "17:00:00", 60),
            ("Ramachandi Temple", "Spiritual", "A temple situated at the confluence of Kushabhadra river.", 0.0, "06:00:00", "19:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "18°C - 30°C", "Low", "Attend the annual Konark Dance Festival in December.")
    },
    {
        "name": "Bhubaneswar", "city": "Bhubaneswar", "state": "Odisha", "region": "East", "category": "Heritage",
        "desc": "The Temple City of India, showing historical sandstone temples and caves.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2000.0, "rating": 4.6,
        "attractions": [
            ("Lingaraj Temple", "Spiritual", "A grand 11th-century temple dedicated to Harihara.", 0.0, "06:00:00", "21:00:00", 120),
            ("Udayagiri and Khandagiri Caves", "Heritage", "Rock-cut caves containing ancient inscriptions.", 25.0, "09:00:00", "17:00:00", 120),
            ("Dhauli Shanti Stupa", "Spiritual", "A white peace stupa overlooking Kalinga war fields.", 0.0, "06:00:00", "20:00:00", 90),
            ("Nandankanan Zoological Park", "Wildlife", "A zoo famous for white tiger safaris.", 100.0, "08:00:00", "17:00:00", 150),
            ("Mukteshvara Temple", "Spiritual", "An old temple famous for its arched stone gateway.", 0.0, "06:00:00", "19:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 30°C", "Low", "Hire local ASI guides at Udayagiri cave sites.")
    },
    {
        "name": "Kolkata", "city": "Kolkata", "state": "West Bengal", "region": "East", "category": "City",
        "desc": "The City of Joy, famous for colonial architecture, trams, arts, and Durga Puja.",
        "season": "Autumn", "days": 3, "budget": "Moderate", "cost": 2600.0, "rating": 4.8,
        "attractions": [
            ("Victoria Memorial", "Heritage", "A white marble palace museum built for Queen Victoria.", 60.0, "10:00:00", "17:00:00", 120),
            ("Dakshineswar Kali Temple", "Spiritual", "A major temple complex dedicated to Goddess Kali.", 0.0, "06:00:00", "21:00:00", 120),
            ("Howrah Bridge", "Heritage", "An iconic cantilever steel bridge crossing Hooghly river.", 0.0, "00:00:00", "23:59:59", 45),
            ("Indian Museum Kolkata", "Heritage", "The oldest and largest multipurpose museum in Asia.", 50.0, "10:00:00", "17:00:00", 150),
            ("Belur Math", "Spiritual", "Headquarters of Ramakrishna Mission, promoting universal religion.", 0.0, "06:00:00", "20:30:00", 90),
            ("Science City Kolkata", "City", "A major interactive science exhibition park.", 100.0, "09:00:00", "20:00:00", 180)
        ],
        "season_detail": ("Autumn", "October to March", "18°C - 30°C", "Moderate", "Durga Puja in Autumn is the best time to experience Kolkata.")
    },

    # Andhra Pradesh
    {
        "name": "Visakhapatnam", "city": "Visakhapatnam", "state": "Andhra Pradesh", "region": "South", "category": "Beach",
        "desc": "A port city famous for golden beaches, hills, and a unique submarine museum.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2500.0, "rating": 4.6,
        "attractions": [
            ("Rishikonda Beach", "Beach", "A blue flag beach popular for swimming and windsurfing.", 20.0, "06:00:00", "18:00:00", 120),
            ("INS Kursura Submarine Museum", "Heritage", "A decommissioned submarine set up on the beach.", 70.0, "14:00:00", "20:30:00", 90),
            ("Kailasagiri", "Nature", "A hilltop park offering panoramic views of the bay.", 20.0, "08:00:00", "20:00:00", 90),
            ("Yarada Beach", "Beach", "A tranquil beach surrounded by hills on three sides.", 0.0, "06:00:00", "18:00:00", 90),
            ("Simhachalam Temple", "Spiritual", "A historic temple dedicated to Lord Narasimha.", 0.0, "07:00:00", "21:00:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "18°C - 32°C", "Low", "Visit the submarine museum in the evening hours.")
    },
    {
        "name": "Tirupati", "city": "Tirupati", "state": "Andhra Pradesh", "region": "South", "category": "Spiritual",
        "desc": "Home to the Tirumala Venkateswara Temple, one of the most visited holy sites in the world.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.9,
        "attractions": [
            ("Tirumala Venkateswara Temple", "Spiritual", "The world-famous hilltop temple of Lord Venkateswara.", 0.0, "03:00:00", "23:59:59", 240),
            ("Sri Kapileswara Swamy Temple", "Spiritual", "An ancient temple dedicated to Shiva, next to a waterfall.", 0.0, "05:00:00", "21:00:00", 60),
            ("Chandragiri Fort", "Heritage", "A 11th-century fort which served as late Vijayanagara capital.", 25.0, "09:00:00", "17:30:00", 90),
            ("Sri Govindaraja Swamy Temple", "Spiritual", "A prominent temple complex with an imposing tower.", 0.0, "05:00:00", "21:30:00", 90),
            ("Talakona Waterfall", "Nature", "The highest waterfall in Andhra Pradesh, inside reserve forests.", 10.0, "06:00:00", "17:00:00", 120)
        ],
        "season_detail": ("Winter", "September to March", "18°C - 32°C", "Low", "Book Darshan tickets online weeks/months in advance.")
    },
    {
        "name": "Araku Valley", "city": "Araku", "state": "Andhra Pradesh", "region": "South", "category": "Hill Station",
        "desc": "A quiet valley in the Eastern Ghats, famous for coffee gardens, tribes, and caves.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.5,
        "attractions": [
            ("Borra Caves", "Nature", "Deep limestone caves showing stalactites.", 80.0, "10:00:00", "17:00:00", 90),
            ("Katiki Waterfalls", "Nature", "A waterfall reachable by jeep track and trek.", 0.0, "08:00:00", "17:00:00", 120),
            ("Araku Tribal Museum", "Heritage", "A museum explaining tribal lifestyle artifacts.", 40.0, "09:00:00", "18:00:00", 90),
            ("Padmapuram Gardens", "Nature", "A historical botanical garden hosting treehouse stays.", 40.0, "09:00:00", "18:00:00", 60),
            ("Ananthagiri Coffee Plantations", "Nature", "Scenic tea and coffee gardens located on hill slopes.", 0.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 26°C", "Low", "Enjoy local bamboo chicken dish and buy coffee powders.")
    },

    # Puducherry & Island territories
    {
        "name": "Pondicherry", "city": "Puducherry", "state": "Puducherry", "region": "South", "category": "Beach",
        "desc": "A French colonial settlement in India, blending French architecture with spiritual ashrams.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Promenade Beach", "Beach", "A rocky beachfront boulevard lined with heritage monuments.", 0.0, "00:00:00", "23:59:59", 90),
            ("Auroville", "Spiritual", "An experimental township containing the Matrimandir.", 0.0, "09:00:00", "17:00:00", 180),
            ("Sri Aurobindo Ashram", "Spiritual", "A spiritual community ashram founded by Aurobindo.", 0.0, "08:00:00", "18:00:00", 60),
            ("Paradise Beach Pondicherry", "Beach", "A golden sand beach accessible by ferry across backwaters.", 300.0, "09:00:00", "17:00:00", 120),
            ("French Quarter", "Heritage", "Streets filled with mustard yellow colonial buildings and cafes.", 0.0, "00:00:00", "23:59:59", 120)
        ],
        "season_detail": ("Winter", "October to March", "22°C - 32°C", "Low", "Explore the French Quarter by renting a bicycle.")
    },
    {
        "name": "Havelock Island", "city": "Havelock", "state": "Andaman & Nicobar", "region": "South", "category": "Beach",
        "desc": "Renowned for its crystal clear diving waters and Radhanagar Beach, one of Asia's best.",
        "season": "Winter", "days": 3, "budget": "Luxury", "cost": 6500.0, "rating": 4.9,
        "attractions": [
            ("Radhanagar Beach", "Beach", "Award-winning beach famous for turquoise waters and sunsets.", 0.0, "06:00:00", "18:00:00", 180),
            ("Elephant Beach", "Beach", "Famous for coral reefs and water sports like snorkeling.", 0.0, "08:00:00", "15:00:00", 180),
            ("Kalapathar Beach", "Beach", "A quiet sandy beach framed by black rocks and forest tracks.", 0.0, "06:00:00", "18:00:00", 90),
            ("Neil's Cove", "Beach", "A beautiful hidden lagoon cove located next to Radhanagar.", 0.0, "06:00:00", "17:30:00", 60),
            ("Havelock Dive Center", "Adventure", "A diving school offering Scuba courses.", 3500.0, "07:00:00", "16:00:00", 150)
        ],
        "season_detail": ("Winter", "November to April", "22°C - 30°C", "Low", "Book ferry tickets between Port Blair and Havelock in advance.")
    },
    {
        "name": "Port Blair", "city": "Port Blair", "state": "Andaman & Nicobar", "region": "South", "category": "Heritage",
        "desc": "The capital of Andaman islands, famous for the historical Cellular Jail and colonial ruins.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3500.0, "rating": 4.7,
        "attractions": [
            ("Cellular Jail National Memorial", "Heritage", "The historic colonial prison housing freedom fighters.", 30.0, "09:00:00", "17:00:00", 120),
            ("Ross Island", "Heritage", "A colonial ruins island now home to wild deer.", 100.0, "08:30:00", "16:00:00", 150),
            ("Chidiya Tapu", "Nature", "A bird watching beach point famous for sunsets.", 0.0, "06:00:00", "18:00:00", 90),
            ("Samudrika Marine Museum", "Heritage", "A museum run by Indian Navy explaining marine life.", 50.0, "09:00:00", "17:00:00", 90),
            ("Corbyn's Cove Beach", "Beach", "A palm-fringed sandy beach offering jet ski rides.", 0.0, "06:00:00", "21:00:00", 90)
        ],
        "season_detail": ("Winter", "November to April", "22°C - 31°C", "Low", "Attend the light and sound show at Cellular Jail.")
    },

    # Gujarat & Others
    {
        "name": "Gir National Park", "city": "Sasan Gir", "state": "Gujarat", "region": "West", "category": "Wildlife",
        "desc": "The only natural habitat of the Asiatic lions in the world.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 4800.0, "rating": 4.8,
        "attractions": [
            ("Gir Jungle Trail Safari", "Wildlife", "A safari to spot Asiatic lions in natural forest habitats.", 1000.0, "06:00:00", "17:00:00", 180),
            ("Devalia Safari Park", "Wildlife", "An enclosed safari park offering guaranteed lion sightings.", 200.0, "07:30:00", "17:30:00", 90),
            ("Kamleshwar Dam", "Nature", "A scenic dam built inside Gir forest housing crocodiles.", 0.0, "08:00:00", "17:00:00", 45),
            ("Durbar Hall Museum Junagadh", "Heritage", "A museum showing weapons and royal clothing relics.", 20.0, "10:00:00", "17:00:00", 90),
            ("Somnath Temple Gate", "Spiritual", "A nearby holy temple situated on shores of Gujarat.", 0.0, "06:00:00", "21:30:00", 90)
        ],
        "season_detail": ("Winter", "December to March", "10°C - 28°C", "Low", "The park is closed from mid-June to mid-October.")
    },
    {
        "name": "Rann of Kutch", "city": "Bhuj", "state": "Gujarat", "region": "West", "category": "Nature",
        "desc": "A massive white salt desert salt flat, hosting the colorful Rann Utsav festival.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 5500.0, "rating": 4.9,
        "attractions": [
            ("White Desert Salt Flat", "Nature", "A flat salt crust desert shining white under moon.", 100.0, "00:00:00", "23:59:59", 120),
            ("Kalo Dungar Black Hill", "Nature", "The highest point in Kutch offering desert panoramas.", 0.0, "06:00:00", "18:00:00", 90),
            ("Aina Mahal Palace Bhuj", "Heritage", "A palace of mirrors built during the 18th century.", 20.0, "09:00:00", "17:00:00", 60),
            ("Prag Mahal", "Heritage", "An old Italian Gothic style palace next to Aina Mahal.", 20.0, "09:00:00", "17:00:00", 60),
            ("Bhujodi Crafts Village", "Heritage", "A major weavers village displaying Kutch embroidery.", 0.0, "09:00:00", "19:00:00", 120)
        ],
        "season_detail": ("Winter", "November to February", "12°C - 25°C", "Minimal", "Visit during a full moon night for magical desert views.")
    }
]

# We need to reach exactly 75 destinations. Let's add 25 more detailed Indian destinations to make it exactly 75!
extra_dests = [
    {
        "name": "Kodaikanal Valley", "city": "Kodaikanal", "state": "Tamil Nadu", "region": "South", "category": "Hill Station",
        "desc": "A peaceful valley region surrounding Kodaikanal hills, known for pine forests and mist.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2500.0, "rating": 4.5,
        "attractions": [
            ("Pine Forest Kodaikanal", "Nature", "A scenic pine tree forest tract popular with photographers.", 10.0, "08:00:00", "18:00:00", 60),
            ("Dolphin's Nose Kodaikanal", "Nature", "A flat rock cliff offering deep valley drop views.", 0.0, "08:00:00", "17:00:00", 90),
            ("Green Valley View", "Nature", "Formerly called Suicide Point, offering panoramic views.", 0.0, "07:00:00", "18:00:00", 45),
            ("Guna Caves", "Nature", "Deep rock formations popularized by regional movies.", 20.0, "08:00:00", "17:00:00", 60),
            ("Berijam Lake", "Nature", "A pristine calm forest lake situated inside reserve zones.", 100.0, "09:00:00", "15:00:00", 120)
        ],
        "season_detail": ("Summer", "April to June", "15°C - 25°C", "Moderate", "Obtain forest permits early to visit Berijam Lake.")
    },
    {
        "name": "Sunderbans National Park", "city": "Canning", "state": "West Bengal", "region": "East", "category": "Wildlife",
        "desc": "The largest mangrove forest in the world, home to the Royal Bengal tigers and estuarine crocodiles.",
        "season": "Winter", "days": 3, "budget": "Moderate", "cost": 3500.0, "rating": 4.8,
        "attractions": [
            ("Sajnekhali Watch Tower", "Wildlife", "A forest department post watchtower to spot tigers.", 100.0, "07:00:00", "17:00:00", 120),
            ("Sudhanyakhali Watch Tower", "Wildlife", "A popular forest post surrounding a fresh pond.", 100.0, "07:00:00", "17:00:00", 90),
            ("Dobanki Watch Tower", "Wildlife", "A canopy walk cage path inside tiger reserve zones.", 100.0, "07:00:00", "17:00:00", 90),
            ("Netidhopani Watch Tower", "Wildlife", "A historic post containing temple ruins.", 100.0, "07:00:00", "17:00:00", 90),
            ("Bhagatpur Crocodile Project", "Wildlife", "A conservatory hatchery for estuarine crocodiles.", 50.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "15°C - 28°C", "Low", "Explore mangrove channels using local motorized boats.")
    },
    {
        "name": "Rann of Kutch East", "city": "Dholavira", "state": "Gujarat", "region": "West", "category": "Heritage",
        "desc": "The eastern salt flats enclosing Dholavira, a prominent Indus Valley Civilization site.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.7,
        "attractions": [
            ("Dholavira Excavation Site", "Heritage", "The ancient Harappan ruins showing water reservoirs.", 20.0, "08:00:00", "18:00:00", 120),
            ("Kutch Fossil Park", "Nature", "A unique museum showing fossilized bones and wood.", 0.0, "09:00:00", "17:00:00", 60),
            ("Dholavira Museum", "Heritage", "A museum housing artifacts discovered during excavations.", 10.0, "09:00:00", "17:30:00", 60),
            ("Bhanjano Hill", "Nature", "A peak offering desert views of the salt desert flats.", 0.0, "08:00:00", "17:00:00", 90),
            ("Khadir Bet Estuary", "Nature", "A large island ecosystem attracting flamingo flocks.", 0.0, "06:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "12°C - 25°C", "Low", "Dholavira is situated in a remote island region; carry cash.")
    },
    {
        "name": "Tawang Valley", "city": "Tawang", "state": "Arunachal Pradesh", "region": "Northeast", "category": "Nature",
        "desc": "High altitude valleys surrounding Tawang, showcasing crystal streams and peaks.",
        "season": "Spring", "days": 3, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Bum La Pass", "Adventure", "A high mountain pass situated at 15,200 feet near China border.", 0.0, "09:00:00", "15:00:00", 180),
            ("Tawang Monastery Museum", "Spiritual", "A museum housing ancient scriptures inside the monastery.", 10.0, "08:00:00", "17:00:00", 60),
            ("Urgeling Monastery", "Spiritual", "The birthplace of the 6th Dalai Lama.", 0.0, "07:00:00", "18:00:00", 60),
            ("Pangteng Teng Tso Lake", "Nature", "A scenic calm glacial lake situated on slopes.", 0.0, "08:00:00", "16:00:00", 90),
            ("Chakusam Suspension Bridge", "Heritage", "An iron chain suspension bridge built in 15th century.", 0.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Spring", "March to June", "10°C - 20°C", "Moderate", "Special permit is required to visit Bum La Pass.")
    },
    {
        "name": "Coorg Valleys", "city": "Virajpet", "state": "Karnataka", "region": "South", "category": "Nature",
        "desc": "The southern valleys of Coorg, famous for pepper plantations and mountain views.",
        "season": "Autumn", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Iruppu Falls", "Nature", "A sacred forest waterfall next to Shiva temple.", 30.0, "08:00:00", "17:30:00", 90),
            ("Brahmagiri Peak Trek", "Adventure", "A scenic mountain trek offering forest scenery.", 200.0, "07:00:00", "16:00:00", 240),
            ("Nagarhole National Park gate", "Wildlife", "Gateway to the national park tiger reserves.", 250.0, "06:00:00", "17:00:00", 150),
            ("Tadiandamol Peak", "Adventure", "The highest mountain peak in Coorg.", 0.0, "06:00:00", "17:00:00", 240),
            ("Chelavara Falls", "Nature", "A natural waterfall forming a tortoise shape pool.", 0.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Autumn", "October to April", "15°C - 28°C", "Moderate", "Watch out for leeches during forest treks.")
    },
    {
        "name": "Nainital Lakes", "city": "Bhimtal", "state": "Uttarakhand", "region": "North", "category": "Nature",
        "desc": "The lake district lakes enclosing Bhimtal and Sattal, offering quiet resort getaways.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2400.0, "rating": 4.6,
        "attractions": [
            ("Bhimtal Lake", "Nature", "A large natural lake hosting an island aquarium.", 100.0, "08:00:00", "18:00:00", 90),
            ("Sattal Lakes", "Nature", "A group of seven interconnected freshwater forest lakes.", 0.0, "07:00:00", "18:00:00", 120),
            ("Naukuchiatal Lake", "Nature", "A nine-cornered fresh lake popular for paragliding.", 100.0, "08:00:00", "18:00:00", 90),
            ("Bhimtal Island Aquarium", "Nature", "An aquarium set up on the island of Bhimtal lake.", 100.0, "09:00:00", "18:00:00", 60),
            ("Victoria Dam Bhimtal", "Heritage", "An old masonry dam located on the lake side.", 0.0, "08:00:00", "18:00:00", 45)
        ],
        "season_detail": ("Summer", "March to June", "15°C - 28°C", "Low", "Perfect for bird watching near Sattal forest lakes.")
    },
    {
        "name": "Srinagar Outskirts", "city": "Srinagar", "state": "Jammu & Kashmir", "region": "North", "category": "Heritage",
        "desc": "The historical archaeological ruins on the hills surrounding Srinagar valley.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.6,
        "attractions": [
            ("Pari Mahal", "Heritage", "A seven-terraced Mughal garden built by Dara Shikoh.", 25.0, "09:00:00", "18:00:00", 90),
            ("Chashme Shahi", "Heritage", "The royal spring garden, a terraced Mughal layout.", 25.0, "09:00:00", "18:00:00", 60),
            ("Dachigam National Park", "Wildlife", "The sanctuary protecting the endangered hangul deer.", 100.0, "09:00:00", "17:00:00", 180),
            ("Burzahom Archaeological Site", "Heritage", "Neolithic settlement ruins showing pit dwellings.", 0.0, "09:00:00", "17:00:00", 60),
            ("Harwan Garden", "Nature", "A quiet garden featuring water reservoirs from canals.", 25.0, "09:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Summer", "April to September", "15°C - 30°C", "Low", "Excellent sunset views of Dal Lake from Pari Mahal.")
    },
    {
        "name": "Manali Slopes", "city": "Manali", "state": "Himachal Pradesh", "region": "North", "category": "Adventure",
        "desc": "The high mountain ski pass slopes surrounding Rohtang Pass near Manali.",
        "season": "Summer", "days": 2, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Rohtang Pass", "Adventure", "A high mountain pass situated at 3978 meters.", 500.0, "08:00:00", "16:00:00", 240),
            ("Rahala Waterfalls", "Nature", "A scenic waterfall formed by melting glaciers.", 0.0, "08:00:00", "17:00:00", 45),
            ("Beas Kund", "Nature", "A sacred high altitude lake, the source of Beas River.", 0.0, "07:00:00", "16:00:00", 240),
            ("Gulaba Meadows", "Nature", "A green meadow hillside, popular for snow activities.", 0.0, "08:00:00", "17:00:00", 90),
            ("Kothi Village", "Nature", "A picturesque village showing deep gorges of Beas river.", 0.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Summer", "May to October", "5°C - 20°C", "Moderate", "Rohtang Pass requires a vehicle permit. Book online.")
    },
    {
        "name": "Wayanad Hills", "city": "Vythiri", "state": "Kerala", "region": "South", "category": "Nature",
        "desc": "The high forest hills of Wayanad, famous for treehouse stays and tea gardens.",
        "season": "Autumn", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Lakkidi View Point", "Nature", "The gateway viewpoint of Wayanad, showing hairpin curves.", 0.0, "06:00:00", "22:00:00", 60),
            ("Thusharagiri Waterfalls", "Nature", "A multi-tiered forest waterfall popular for trekking.", 30.0, "09:00:00", "17:00:00", 120),
            ("Karalad Lake", "Nature", "A quiet lake offering ziplining and boating.", 30.0, "09:00:00", "17:30:00", 90),
            ("Kuruvadweep Island", "Nature", "A river island delta hosting rare orchids and rafts.", 100.0, "09:00:00", "15:00:00", 150),
            ("Chain Tree Vythiri", "Heritage", "A mythical ficus tree tied with a large chain.", 0.0, "00:00:00", "23:59:59", 30)
        ],
        "season_detail": ("Autumn", "October to April", "18°C - 28°C", "Moderate", "Kuruvadweep remains closed during peak monsoon floods.")
    },
    {
        "name": "Leh Valleys", "city": "Leh", "state": "Ladakh", "region": "North", "category": "Adventure",
        "desc": "The high altitude river valleys including Nubra and Indus valley.",
        "season": "Summer", "days": 4, "budget": "Luxury", "cost": 5000.0, "rating": 4.8,
        "attractions": [
            ("Nubra Valley Sand Dunes", "Adventure", "A high altitude sand desert flat, famous for Bactrian camels.", 50.0, "08:00:00", "19:00:00", 180),
            ("Diskit Monastery", "Spiritual", "The oldest and largest monastery in Nubra Valley.", 50.0, "07:00:00", "18:30:00", 90),
            ("Khardung La Pass", "Adventure", "One of the highest motorable road passes in the world.", 0.0, "00:00:00", "23:59:59", 45),
            ("Hunder Sand Dunes", "Nature", "Desert sand dunes next to mountain rivers.", 0.0, "08:00:00", "19:00:00", 120),
            ("Panamik Hot Springs", "Nature", "Hot sulfur springs located close to Siachen glacier base.", 50.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Summer", "June to September", "10°C - 25°C", "Low", "Inner Line Permit is required to travel to Nubra Valley.")
    },
    {
        "name": "Munnar Valleys", "city": "Munnar", "state": "Kerala", "region": "South", "category": "Nature",
        "desc": "The valleys and waterfalls situated around the lower tea estates of Munnar.",
        "season": "Autumn", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Attukad Waterfalls", "Nature", "A stunning forest waterfall situated among steep hills.", 0.0, "09:00:00", "18:00:00", 90),
            ("Lockhart Gap View", "Nature", "A scenic gap offering panoramic tea valley views.", 0.0, "06:00:00", "18:00:00", 60),
            ("Anayirankal Dam", "Nature", "A dam reservoir surrounded by tea gardens and pine woods.", 30.0, "09:00:00", "17:00:00", 90),
            ("Chinnar Wildlife Sanctuary gate", "Wildlife", "Gateway to the dry deciduous forest reserve.", 100.0, "06:00:00", "18:00:00", 120),
            ("Devikulam Lake", "Nature", "A sacred forest lake known for mineral waters.", 0.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Autumn", "September to May", "15°C - 25°C", "Moderate", "Ideal base for trekking and spice garden tours.")
    },
    {
        "name": "Shimla Ridges", "city": "Kufri", "state": "Himachal Pradesh", "region": "North", "category": "Hill Station",
        "desc": "The high ridge slopes surrounding Kufri near Shimla, popular for snow parks.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.5,
        "attractions": [
            ("Kufri Fun World", "Adventure", "A high altitude amusement park hosting ski slopes.", 250.0, "09:00:00", "18:00:00", 120),
            ("Mahasu Peak Kufri", "Nature", "The highest point in Kufri, accessible by horse ride.", 0.0, "08:00:00", "17:00:00", 90),
            ("Indira Tourist Park", "Nature", "A calm park next to Himalayan Nature Park.", 10.0, "09:00:00", "18:00:00", 60),
            ("Himalayan Nature Park", "Wildlife", "A sanctuary conserving Himalayan musk deer.", 50.0, "09:00:00", "17:00:00", 90),
            ("Fagu View Point", "Nature", "A misty village valley ridge viewpoint.", 0.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "December to March", "-2°C - 12°C", "Heavy Snowfall", "Enjoy yak rides and skiing on slopes.")
    },
    {
        "name": "Dharamshala Hills", "city": "McLeod Ganj", "state": "Himachal Pradesh", "region": "North", "category": "Spiritual",
        "desc": "McLeod Ganj hill tops, the seat of the Tibetan community in exile.",
        "season": "Spring", "days": 2, "budget": "Budget", "cost": 1800.0, "rating": 4.7,
        "attractions": [
            ("Tibet Museum", "Heritage", "A museum showing history of Tibet inside complex.", 10.0, "09:00:00", "17:00:00", 90),
            ("Dharamkot Village", "Nature", "A quiet village hillside, popular for yoga centers.", 0.0, "00:00:00", "23:59:59", 120),
            ("Naddi View Point", "Nature", "A sunset viewpoint overlooking Dhauladhar peaks.", 0.0, "06:00:00", "19:00:00", 60),
            ("Dal Lake McLeod Ganj", "Nature", "A sacred forest pond surrounded by deodar trees.", 0.0, "08:00:00", "18:00:00", 45),
            ("St. John Church McLeod Ganj", "Heritage", "A historic Neo-Gothic style forest church.", 0.0, "09:00:00", "17:00:00", 45)
        ],
        "season_detail": ("Spring", "September to November", "12°C - 24°C", "Low", "Perfect base for meditation courses.")
    },
    {
        "name": "Udaipur Lakes", "city": "Udaipur", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The heritage lake systems surrounding Lake Fatehsagar and Lake Udai Sagar.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.7,
        "attractions": [
            ("Fateh Sagar Lake", "Nature", "A large artificial lake hosting a solar observatory.", 0.0, "06:00:00", "18:00:00", 90),
            ("Nehru Park Udaipur", "Nature", "An island park located inside Fateh Sagar Lake.", 50.0, "09:00:00", "18:00:00", 90),
            ("Udaipur Solar Observatory", "Heritage", "A solar observatory located on a lake island.", 0.0, "10:00:00", "17:00:00", 60),
            ("Moti Magri", "Heritage", "A memorial hill dedicated to Maharana Pratap.", 100.0, "09:00:00", "18:00:00", 90),
            ("Saheli Garden", "Heritage", "Historical court garden showcasing marble fountains.", 50.0, "09:00:00", "19:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "12°C - 28°C", "Low", "Try speedboat rides on Lake Fateh Sagar.")
    },
    {
        "name": "Jaipur Outskirts", "city": "Jaipur", "state": "Rajasthan", "region": "West", "category": "Heritage",
        "desc": "The outer forts and palaces surrounding the Aravalli hills of Jaipur.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Jaigarh Fort", "Heritage", "Fort housing the Jaivana cannon, the world's largest on wheels.", 150.0, "09:00:00", "16:30:00", 120),
            ("Jal Mahal", "Heritage", "A floating palace situated in Man Sagar Lake.", 0.0, "00:00:00", "23:59:59", 45),
            ("Galta Ji Temple", "Spiritual", "Also called Monkey Temple, featuring holy spring basins.", 0.0, "06:00:00", "20:00:00", 90),
            ("Sisodia Rani Palace Garden", "Heritage", "A royal terraced garden showing Radha-Krishna murals.", 50.0, "08:00:00", "18:00:00", 60),
            ("Vidyadhar Garden", "Heritage", "A beautifully landscaped garden built honoring Jaipur architect.", 50.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Observe the massive Jaivana Cannon at Jaigarh Fort.")
    },
    {
        "name": "North Goa Beaches", "city": "Mapusa", "state": "Goa", "region": "West", "category": "Beach",
        "desc": "The beach coves of Vagator and Arambol in North Goa.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.7,
        "attractions": [
            ("Vagator Beach", "Beach", "A dramatic red cliff beach hosting Shiva Carving.", 0.0, "06:00:00", "22:00:00", 120),
            ("Arambol Sweet Water Lake", "Beach", "A sweet water lagoon next to the beach.", 0.0, "06:00:00", "19:00:00", 120),
            ("Morjim Beach", "Beach", "A calm beach famous as Olive Ridley nesting site.", 0.0, "06:00:00", "22:00:00", 120),
            ("Chapora River Estuary", "Nature", "Confluence of Chapora river and Arabian Sea.", 0.0, "00:00:00", "23:59:59", 60),
            ("Shiva Carving Vagator", "Heritage", "A rock carving of Shiva on Vagator beach.", 0.0, "06:00:00", "18:00:00", 45)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Low", "Perfect for watching spectacular sunsets over Vagator cliff.")
    },
    {
        "name": "South Goa Beaches", "city": "Canacona", "state": "Goa", "region": "West", "category": "Beach",
        "desc": "Secluded sandy coves including Butterfly Beach and Agonda in South Goa.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 4000.0, "rating": 4.7,
        "attractions": [
            ("Agonda Beach", "Beach", "A long sandy beach, quiet and popular for nesting turtles.", 0.0, "06:00:00", "22:00:00", 120),
            ("Butterfly Beach", "Beach", "A tiny semi-circular beach cove hosting butterflies.", 0.0, "06:00:00", "18:00:00", 120),
            ("Cola Beach", "Beach", "A beach famous for its freshwater blue lagoon on banks.", 0.0, "06:00:00", "22:00:00", 120),
            ("Cavelossim Beach", "Beach", "Where Sal river meets the sea, hosting black rocks.", 0.0, "06:00:00", "22:00:00", 90),
            ("Agonda Turtle Sanctuary", "Wildlife", "An area dedicated to protecting olive ridley turtle nests.", 0.0, "08:00:00", "18:00:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "20°C - 32°C", "Low", "Hire a boat from Palolem to visit Butterfly Beach.")
    },
    {
        "name": "Varanasi Ghats", "city": "Varanasi", "state": "Uttar Pradesh", "region": "North", "category": "Spiritual",
        "desc": "The historical ghat stairways lining the Ganges in Varanasi.",
        "season": "Winter", "days": 2, "budget": "Budget", "cost": 1500.0, "rating": 4.8,
        "attractions": [
            ("Manikarnika Ghat", "Spiritual", "The primary cremation ghat, an ancient sacred site.", 0.0, "00:00:00", "23:59:59", 60),
            ("Harishchandra Ghat", "Spiritual", "One of two cremation ghats, historic and sacred.", 0.0, "00:00:00", "23:59:59", 45),
            ("Scindia Ghat", "Spiritual", "Ghat containing a partially submerged Shiva temple.", 0.0, "00:00:00", "23:59:59", 45),
            ("Man Mandir Observatory", "Heritage", "An old stone observatory built by Raja Man Singh.", 25.0, "09:00:00", "17:00:00", 60),
            ("Darbhanga Ghat", "Heritage", "A majestic palace ghat built by royal families of Bihar.", 0.0, "00:00:00", "23:59:59", 60)
        ],
        "season_detail": ("Winter", "October to March", "10°C - 25°C", "Low", "Respect privacy; strictly no photography at cremation ghats.")
    },
    {
        "name": "Kochi Ports", "city": "Kochi", "state": "Kerala", "region": "South", "category": "Heritage",
        "desc": "The historic port islands including Willingdon and Bolgatty in Kochi.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.6,
        "attractions": [
            ("Bolgatty Palace", "Heritage", "A historic Dutch mansion now converted to heritage hotel.", 0.0, "09:00:00", "18:00:00", 60),
            ("Willingdon Island Ferry", "Nature", "A passenger ferry line crossing the port waters.", 10.0, "06:00:00", "21:00:00", 45),
            ("Maritime Museum Kochi", "Heritage", "A naval museum showcasing ship models.", 40.0, "09:30:00", "17:00:00", 90),
            ("Vallarpadam Basilica", "Spiritual", "A prominent Roman Catholic national shrine.", 0.0, "06:00:00", "20:00:00", 60),
            ("Gundu Island", "Nature", "The smallest island in Kochi, housing old factories.", 0.0, "08:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Winter", "November to February", "22°C - 32°C", "Moderate", "Take a government ferry to commute between islands cheaply.")
    },
    {
        "name": "Darjeeling Slopes", "city": "Darjeeling", "state": "West Bengal", "region": "East", "category": "Hill Station",
        "desc": "The tea garden slopes and estates surrounding Darjeeling.",
        "season": "Spring", "days": 2, "budget": "Moderate", "cost": 2800.0, "rating": 4.7,
        "attractions": [
            ("Happy Valley Tea Estate", "Nature", "An active tea processing estate founded in 1854.", 100.0, "08:00:00", "16:00:00", 90),
            ("Rock Garden Darjeeling", "Nature", "A terraced garden built cutting through natural waterfalls.", 20.0, "09:00:00", "17:00:00", 90),
            ("Observatory Hill Darjeeling", "Spiritual", "A sacred hilltop hosting temples and Buddhist flags.", 0.0, "07:00:00", "18:00:00", 60),
            ("Lloyd's Botanical Garden", "Nature", "A hillside botanical garden showing orchid blooms.", 20.0, "06:00:00", "17:00:00", 90),
            ("Senchal Lake", "Nature", "A calm forest lake supplying drinking water to town.", 0.0, "08:00:00", "16:00:00", 90)
        ],
        "season_detail": ("Spring", "October to May", "8°C - 20°C", "Moderate", "Buy authentic Darjeeling tea directly from Happy Valley estate.")
    },
    {
        "name": "Ooty Valleys", "city": "Ooty", "state": "Tamil Nadu", "region": "South", "category": "Hill Station",
        "desc": "The lower valley regions of Pykara and Avalanche around Ooty.",
        "season": "Summer", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Pykara Lake", "Nature", "A scenic lake offering speed boats and dams.", 100.0, "09:00:00", "17:30:00", 90),
            ("Pykara Waterfalls", "Nature", "Scenic waterfalls cascading over rocky cliffs.", 20.0, "09:00:00", "17:00:00", 60),
            ("Avalanche Lake Ooty", "Nature", "A pristine forest lake surrounded by mountains.", 0.0, "09:00:00", "15:00:00", 120),
            ("Pine Forest Ooty", "Nature", "A towering pine tree forest slope lining the roads.", 10.0, "08:00:00", "18:00:00", 60),
            ("Kamraj Sagar Dam", "Nature", "A popular film shooting dam reservoir.", 0.0, "09:00:00", "17:00:00", 60)
        ],
        "season_detail": ("Summer", "April to June", "15°C - 25°C", "Moderate", "Book forest department safari for Avalanche Lake.")
    },
    {
        "name": "Pondicherry Streets", "city": "Puducherry", "state": "Puducherry", "region": "South", "category": "Beach",
        "desc": "The coastal beaches and heritage fishing villages of Pondicherry.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Serenity Beach", "Beach", "A quiet beach popular for surfing and sunbathing.", 0.0, "00:00:00", "23:59:59", 120),
            ("Auroville Beach", "Beach", "A beach situated near Auroville, with golden sand.", 0.0, "00:00:00", "23:59:59", 90),
            ("Chunambar Boat House", "Nature", "A backwater gateway offering ferries to Paradise Beach.", 30.0, "09:00:00", "17:00:00", 120),
            ("Matrimandir Viewing Point", "Spiritual", "A viewing garden overlooking the golden dome of Auroville.", 0.0, "09:00:00", "17:00:00", 60),
            ("Pondicherry Botanical Garden", "Nature", "An old French conservatory showcasing exotic flora.", 20.0, "10:00:00", "17:00:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "22°C - 32°C", "Low", "Visit the Auroville Visitor's Center for free passes to view Matrimandir.")
    },
    {
        "name": "Port Blair Outskirts", "city": "Port Blair", "state": "Andaman & Nicobar", "region": "South", "category": "Heritage",
        "desc": "The historical islands surrounding Port Blair including Viper and Mount Harriet.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 3000.0, "rating": 4.6,
        "attractions": [
            ("Mount Harriet National Park", "Nature", "The highest peak in South Andamans offering forest views.", 80.0, "07:00:00", "17:00:00", 120),
            ("Viper Island", "Heritage", "An island containing ruins of gallows built by British.", 0.0, "08:30:00", "16:00:00", 90),
            ("Wandoor Beach", "Beach", "Gateway to the Mahatma Gandhi Marine National Park.", 0.0, "06:00:00", "17:00:00", 120),
            ("Jolly Buoy Island", "Nature", "An island showing underwater corals through glass boat rides.", 750.0, "08:00:00", "14:00:00", 240),
            ("North Bay Island", "Adventure", "Famous for water sports like sea walking and snorkeling.", 0.0, "08:30:00", "16:00:00", 180)
        ],
        "season_detail": ("Winter", "November to April", "22°C - 31°C", "Low", "Jolly Buoy remains closed in monsoons. Obtain forest permits early.")
    },
    {
        "name": "Rann of Kutch West", "city": "Bhuj", "state": "Gujarat", "region": "West", "category": "Nature",
        "desc": "The coastal saltwater creeks and wetlands of western Kutch.",
        "season": "Winter", "days": 2, "budget": "Luxury", "cost": 5000.0, "rating": 4.7,
        "attractions": [
            ("Mandvi Beach Kutch", "Beach", "A clean sandy beach hosting windmills and camel rides.", 0.0, "06:00:00", "21:00:00", 120),
            ("Vijay Vilas Palace", "Heritage", "A majestic summer palace of the rulers of Kutch.", 50.0, "09:00:00", "18:00:00", 90),
            ("Narayan Sarovar", "Spiritual", "One of five sacred lakes in Hindu mythology.", 0.0, "06:00:00", "20:00:00", 90),
            ("Koteshwar Temple", "Spiritual", "An ancient Shiva temple situated on ocean shores.", 0.0, "06:00:00", "20:00:00", 60),
            ("Lakhpat Fort Ruins", "Heritage", "A ghost town fort containing historic tombs.", 0.0, "08:00:00", "18:00:00", 90)
        ],
        "season_detail": ("Winter", "November to February", "12°C - 25°C", "Low", "Witness the beautiful wind farms of Mandvi Beach.")
    },
    {
        "name": "Khajuraho Outskirts", "city": "Khajuraho", "state": "Madhya Pradesh", "region": "Central", "category": "Heritage",
        "desc": "The eastern group of temples and sanctuaries surrounding Khajuraho.",
        "season": "Winter", "days": 2, "budget": "Moderate", "cost": 2600.0, "rating": 4.6,
        "attractions": [
            ("Parsvanatha Temple", "Spiritual", "The largest Jain temple in the Eastern group.", 0.0, "06:00:00", "18:00:00", 60),
            ("Adinatha Temple", "Spiritual", "A fine Jain temple showcasing carvings of musicians.", 0.0, "06:00:00", "18:00:00", 45),
            ("Panna National Park gate", "Wildlife", "Gateway to the tiger reserves next to Ken River.", 250.0, "06:00:00", "17:00:00", 150),
            ("Pandav Falls", "Nature", "A natural waterfall forming a deep circular pool.", 50.0, "08:00:00", "17:00:00", 90),
            ("Ken Gharial Sanctuary", "Wildlife", "A sanctuary for protecting Indian gharials.", 100.0, "08:00:00", "16:30:00", 90)
        ],
        "season_detail": ("Winter", "October to March", "12°C - 26°C", "Low", "Take a boat ride at Ken river to spot gharials.")
    }
]

# Merge lists to reach exactly 75 destinations!
all_destinations = (destinations_data + extra_dests)[:75]

# Verify count is exactly 75
print(f"Total destinations generated: {len(all_destinations)}")

# 1. Write destinations.csv
with open('destinations.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'destination_name', 'city', 'state', 'region', 'category', 'description', 
        'best_season', 'ideal_days', 'budget_level', 'average_cost_per_day', 
        'family_friendly', 'couple_friendly', 'solo_friendly', 'average_rating', 'image'
    ])
    for dest in all_destinations:
        slug = dest['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        writer.writerow([
            dest['name'], dest['city'], dest['state'], dest['region'], dest['category'], dest['desc'],
            dest['season'], dest['days'], dest['budget'], dest['cost'],
            True, True, True, dest['rating'], f"destinations/{slug}.jpg"
        ])

# 2. Write attractions.csv
with open('attractions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'attraction_name', 'destination_name', 'category', 'description', 
        'entry_fee', 'opening_time', 'closing_time', 'average_visit_time', 'image'
    ])
    for dest in all_destinations:
        for idx, attr in enumerate(dest['attractions']):
            # attr is a tuple: (name, category, desc, fee, open, close, time)
            attr_name = attr[0]
            slug = attr_name.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
            writer.writerow([
                attr_name, dest['name'], attr[1], attr[2],
                attr[3], attr[4], attr[5], attr[6], f"attractions/{slug}.jpg"
            ])

# 3. Write packages.csv
with open('packages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'package_name', 'destination_name', 'duration', 'package_type', 'price', 'description', 'image'
    ])
    for dest in all_destinations:
        # Generate 3 packages: Budget, Standard, Luxury
        dest_slug = dest['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        # Budget
        writer.writerow([
            f"Budget Exploration of {dest['name']}", dest['name'], dest['days'], "Budget", 
            round(dest['cost'] * dest['days'] * 0.7, 2), 
            f"An affordable package to explore the best highlights of {dest['name']} including basic lodgings.",
            f"packages/{dest_slug}-budget.jpg"
        ])
        # Standard
        writer.writerow([
            f"Standard Experience in {dest['name']}", dest['name'], dest['days'] + 1, "Standard", 
            round(dest['cost'] * (dest['days'] + 1) * 1.0, 2), 
            f"Enjoy a comfortable tour of {dest['name']} with standard accommodations and guided sightseeing tours.",
            f"packages/{dest_slug}-standard.jpg"
        ])
        # Luxury
        writer.writerow([
            f"Luxury Gateway to {dest['name']}", dest['name'], dest['days'] + 2, "Luxury", 
            round(dest['cost'] * (dest['days'] + 2) * 1.8, 2), 
            f"Indulge in premium luxury travel to {dest['name']} featuring boutique resorts, private cars, and personal guides.",
            f"packages/{dest_slug}-luxury.jpg"
        ])

# 4. Write best_seasons.csv
with open('best_seasons.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'destination_name', 'season', 'peak_months', 'average_temperature', 'rainfall', 'travel_tip'
    ])
    for dest in all_destinations:
        # dest['season_detail'] is a tuple: (season, months, temp, rainfall, tip)
        sd = dest['season_detail']
        writer.writerow([
            dest['name'], sd[0], sd[1], sd[2], sd[3], sd[4]
        ])

print("CSV datasets generated successfully!")
