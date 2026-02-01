from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

# Mock database of gaming laptops
LAPTOPS = [
    {
        "model": "ASUS TUF Gaming F15",
        "price": 800,
        "specs": "i5-11400H, RTX 3050, 16GB RAM, 512GB SSD",
        "image": "https://m.media-amazon.com/images/I/81+f4okbeBL._AC_SL1500_.jpg" 
    },
    {
        "model": "Lenovo Legion 5",
        "price": 1200,
        "specs": "Ryzen 7 5800H, RTX 3060, 16GB RAM, 1TB SSD",
        "image": "https://m.media-amazon.com/images/I/71fL6h0eT+L._AC_SL1500_.jpg"
    },
    {
        "model": "Acer Predator Helios 300",
        "price": 1400,
        "specs": "i7-11800H, RTX 3060, 16GB RAM, 512GB SSD",
        "image": "https://m.media-amazon.com/images/I/7180U1k2TXL._AC_SL1500_.jpg"
    },
    {
        "model": "Razer Blade 15",
        "price": 2500,
        "specs": "i7-12800H, RTX 3070 Ti, 32GB RAM, 1TB SSD",
        "image": "https://m.media-amazon.com/images/I/61Z7F4r5O2L._AC_SL1500_.jpg"
    },
    {
        "model": "MSI Raider GE76",
        "price": 3500,
        "specs": "i9-12900HK, RTX 3080 Ti, 64GB RAM, 2TB SSD",
        "image": "https://m.media-amazon.com/images/I/715JO8R8H+L._AC_SL1500_.jpg"
    },
    {
        "model": "Alienware x17 R2",
        "price": 4000,
        "specs": "i9-12900HK, RTX 3080 Ti, 64GB RAM, 4TB SSD",
        "image": "https://m.media-amazon.com/images/I/71y7J7X-X+L._AC_SL1500_.jpg"
    }
]

def get_gaming_laptop_recommendations(min_price: int, max_price: int) -> dict:
    """
    Returns a list of gaming laptops within the specified price range.
    Args:
        min_price: The minimum price in USD.
        max_price: The maximum price in USD.
    """
    recommendations = [
        laptop for laptop in LAPTOPS 
        if min_price <= laptop["price"] <= max_price
    ]
    
    if not recommendations:
        return {
            "status": "success",
            "message": f"No laptops found between ${min_price} and ${max_price} in local database.",
            "laptops": []
        }
        
    return {
        "status": "success",
        "message": f"Found {len(recommendations)} laptops in your range.",
        "laptops": recommendations
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='gaming_laptop_advisor',
    description="Helps users find the best gaming laptop for their budget.",
    instruction="""
    You are an expert Gaming Laptop Advisor. Your goal is to help users find the perfect machine.
    
    1.  If the user provides a budget, use `get_gaming_laptop_recommendations` to check local stock.
    2.  If the user asks for "cheapest", "best", "newest", or specific models without a price, use `google_search` or logic to answer directly. DO NOT ask for a budget if the user's intent is clear (e.g., "cheapest RTX 4060").
    3.  Only ask for a budget if the user's request is too vague (e.g., "I want a laptop").
    4.  Refuse to answer questions unrelated to gaming laptops.
    5.  Present recommendations with enthusiasm, highlighting key specs (GPU/CPU).
    6.  Be concise but helpful.
    """,
    tools=[get_gaming_laptop_recommendations, GoogleSearchTool(bypass_multi_tools_limit=True)],
)
