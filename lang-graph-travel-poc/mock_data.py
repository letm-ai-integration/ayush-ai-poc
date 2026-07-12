FLIGHTS = {
    "Tokyo": [
        {
            "airline": "ANA",
            "departure_city": "Delhi",
            "arrival_city": "Tokyo Narita",
            "price_usd": 850,
            "duration_hours": 9.5,
            "stops": 0,
            "class_type": "economy",
        },
        {
            "airline": "IndiGo",
            "departure_city": "Delhi",
            "arrival_city": "Tokyo Haneda",
            "price_usd": 620,
            "duration_hours": 11.0,
            "stops": 1,
            "class_type": "economy",
        },
    ],
    "Bali": [
        {
            "airline": "Garuda",
            "departure_city": "Delhi",
            "arrival_city": "Denpasar",
            "price_usd": 480,
            "duration_hours": 8.0,
            "stops": 1,
            "class_type": "economy",
        }
    ],
    "Barcelona": [
        {
            "airline": "Qatar Airways",
            "departure_city": "Delhi",
            "arrival_city": "Barcelona",
            "price_usd": 690,
            "duration_hours": 11.5,
            "stops": 1,
            "class_type": "economy",
        }
    ],
    "Switzerland": [
        {
            "airline": "Swiss Air",
            "departure_city": "Delhi",
            "arrival_city": "Zurich",
            "price_usd": 780,
            "duration_hours": 9.0,
            "stops": 0,
            "class_type": "economy",
        },
        {
            "airline": "Lufthansa",
            "departure_city": "Delhi",
            "arrival_city": "Geneva",
            "price_usd": 650,
            "duration_hours": 10.5,
            "stops": 1,
            "class_type": "economy",
        },
    ],
}

HOTELS = {
    "Tokyo": [
        {
            "name": "Shinjuku Budget Inn",
            "price_per_night_usd": 45,
            "rating": 3.9,
            "style": "hostel",
        },
        {
            "name": "Asakusa Boutique Stay",
            "price_per_night_usd": 110,
            "rating": 4.5,
            "style": "boutique",
        },
    ],
    "Bali": [
        {
            "name": "Ubud Jungle Villa",
            "price_per_night_usd": 90,
            "rating": 4.7,
            "style": "boutique",
        }
    ],
    "Barcelona": [
        {
            "name": "Gothic Quarter Hostel",
            "price_per_night_usd": 30,
            "rating": 4.0,
            "style": "hostel",
        }
    ],
    "Switzerland": [
        {
            "name": "Interlaken Alpine Lodge",
            "price_per_night_usd": 180,
            "rating": 4.6,
            "style": "boutique",
        },
        {
            "name": "Zurich City Hostel",
            "price_per_night_usd": 65,
            "rating": 4.1,
            "style": "hostel",
        },
    ],
}

ACTIVITIES = {
    "Tokyo": [
        {
            "name": "Senso-ji Temple visit",
            "category": "culture",
            "cost_usd": 0,
            "time_of_day": "morning",
        },
        {
            "name": "Ramen tasting in Shinjuku",
            "category": "food",
            "cost_usd": 15,
            "time_of_day": "evening",
        },
    ],
    "Bali": [
        {
            "name": "Uluwatu Temple sunset",
            "category": "culture",
            "cost_usd": 5,
            "time_of_day": "evening",
        }
    ],
    "Barcelona": [
        {
            "name": "Sagrada Familia tour",
            "category": "culture",
            "cost_usd": 26,
            "time_of_day": "morning",
        }
    ],
    "Switzerland": [
        {
            "name": "Jungfraujoch Top of Europe",
            "category": "adventure",
            "cost_usd": 210,
            "time_of_day": "morning",
        },
        {
            "name": "Lake Geneva boat cruise",
            "category": "leisure",
            "cost_usd": 45,
            "time_of_day": "afternoon",
        },
        {
            "name": "Grindelwald hiking trail",
            "category": "adventure",
            "cost_usd": 0,
            "time_of_day": "morning",
        },
        {
            "name": "Old Town Bern walking tour",
            "category": "culture",
            "cost_usd": 20,
            "time_of_day": "afternoon",
        },
        {
            "name": "Swiss chocolate and cheese tasting",
            "category": "food",
            "cost_usd": 35,
            "time_of_day": "evening",
        },
    ],
}

WEATHER = {
    "Tokyo": {"avg_temp_celsius": 17, "conditions": "mixed", "warnings": []},
    "Bali": {"avg_temp_celsius": 29, "conditions": "sunny", "warnings": []},
    "Barcelona": {"avg_temp_celsius": 15, "conditions": "cloudy", "warnings": []},
    "Switzerland": {"avg_temp_celsius": 8, "conditions": "snowy/alpine", "warnings": ["Pack warm layers", "Check mountain pass conditions"]},
}

SAMPLE_INPUTS = [
    {
        "id": "budget-japan",
        "input": "5 days in Japan, April, $3000 budget, I love temples and ramen.",
        "expected_destination": "Tokyo",
    },
    {
        "id": "tight-budget-europe",
        "input": "Backpacking Barcelona, 10 days, only $1500, art museums and street food.",
        "expected_destination": "Barcelona",
    },
]
