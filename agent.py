import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset, StdioServerParameters, SseConnectionParams,
    )
from google.adk.models.lite_llm import LiteLlm
import requests
import os
from dotenv import load_dotenv, dotenv_values
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

# Load environment variables from .env file
load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city for which to retrieve the weather report.
        The city name must be in English.
    Returns:
        dict: status and result or error msg.
    """
    # if city.lower() == "new york":
    #     return {
    #         "status": "success",
    #         "report": (
    #             "The weather in New York is sunny with a temperature of 25 degrees"
    #             " Celsius (77 degrees Fahrenheit)."
    #         ),
    #     }
    # else:
    #     return {
    #         "status": "error",
    #         "error_message": f"Weather information for '{city}' is not available.",
    #     }
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "API key for OpenWeatherMap is not set.",
        }
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        # print(data)
        if data["cod"] != 200:
            return {
                "status": "error",
                "error_message": f"Weather information for '{city}' is not available.",
            }
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        report = (
            f"The weather in {city} is {weather_description} with a temperature of "
            f"{temperature} degrees Celsius."
        )
        return {"status": "success", "report": report}
    except Exception as e:
        print(f"ERROR inside get_weather: {e}") # 這裡印簡單英文除錯還可以
        return {
            "status": "error",
            "error_message": f"Critical error in get_weather: {str(e)}",
        }
    # except requests.exceptions.RequestException as e:
    #     return {
    #         "status": "error",
    #         "error_message": f"An error occurred while fetching the weather data: {str(e)}",
    #     }


def get_current_time(tz_identifier: str) -> dict:
    """Returns the current time in a specified time zone identifier.
    Args:
        tz_identifier (str): The time zone identifier for which to retrieve the current time.
        ex. "America/New_York", "Asia/Taipei", etc.
    Returns:
        dict: status and result or error msg.
    """

    # city_taiwan = ["taipei", "zhongli", "taoyuan", "kaohsiung", "taichung"]

    # if city.lower() == "new york":
    #     tz_identifier = "America/New_York"
    # elif city.lower() in city_taiwan:
    #     tz_identifier = "Asia/Taipei"
    # else:
    #     return {
    #         "status": "error",
    #         "error_message": (f"Sorry, I don't have timezone information for {city}."),
    #     }
    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'The current time is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while fetching the current time: {str(e)}",
        }
    

# ===========【變數設定】===========
if os.getenv("BRAVE_API_KEY"):
    brave_api_key = os.getenv("BRAVE_API_KEY")
else:
    print("Warning: BRAVE_API_KEY not found in environment variables.")
    brave_api_key = ""


root_agent = LlmAgent(
    name="travel_plan_agent",
    model="gemini-2.5-flash",
    description=("Agent to answer questions about a travel planning."),
    instruction=(
        """
        You are a professional travel itinerary planner.
        Your goal is to help users plan their trips, check the weather and time and location, and suggest packing lists.
        When you call a tool, you must use English for the city name.

        你的工具箱與使用時機：
        1. **get_weather**: 規劃行程的第一步！務必先查詢目的地天氣。
        2. **get_travel_equipment** (本地): 查完天氣後，**一定要**呼叫此工具，根據天氣給使用者打包建議 。
        3. **get_current_time**: 當使用者問「現在幾點」、「當地時間」或任何跟時間有關的問題時，請使用此工具。
        4. **brave_search**: 當使用者問「哪裡有...」、「推薦餐廳」、「景點評價」或任何你不知道的地點資訊時，請使用此工具。
            **搜尋策略：**
            當使用者查詢地點或店
            家時（例如找麥當勞），**請優先使用 `brave_web_search` (網頁搜尋)**，
            因為地圖搜尋可能資料不足。
            只有在使用者明確要求「座標」或「地圖」時，才嘗試用 `brave_local_search`。
        5. **filesystem**:  當使用者的需求跟檔案存取有關時，請先取得 list_allowed_directories 的結果。
        這個資料夾就是預設檔案存取的位置。
        6. **draw_travel_tarot** (遠端): 當使用者要求「旅遊運勢」時，請使用此工具，並根據塔羅牌結果給予建議。
        8. **get_exchange_rates**、**convert_currency** : 當使用者要求「匯率轉換」時，請使用此工具，並將金額轉換成指定貨幣。
        9. **get_translate** : 當使用者要求「翻譯」時，請使用此工具，並將文字翻譯成指定語言。
        10.**vibesong_playlist* (遠端): 當使用者要求「旅遊歌單」時，請使用此工具，並根據使用者的旅遊地點與偏好，推薦適合的音樂歌單。
        11.**calculate_budget** : 當使用者要求「預算規劃」時，請使用此工具，並根據使用者的需求，計算並規劃旅遊預算。
        
        SYSTEM PROMPT:請用繁體中文回答問題。
        
        """
    ),

    tools=[
        get_weather,
        get_current_time, 
        
        # 1. Filesystem 
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx.cmd", 
                args=[
                    "-y", 
                    "@modelcontextprotocol/server-filesystem",
                    "C:\\Users\\JINGYI\\Desktop\\AIshare",
                ],
                env=os.environ, 
            ),
        ),

        # 2. Brave Search 
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx.cmd",  
                args=[
                    "-y",
                    "@modelcontextprotocol/server-brave-search",
                ],
                env={
                    "BRAVE_API_KEY": brave_api_key, 
                    **os.environ 
                }
            ),
        ),

        # 3. Weather2mood 
        MCPToolset(
            connection_params=StdioServerParameters(
                command=r"C:\Users\JINGYI\Desktop\1013Weather2mood\.venv\Scripts\python.exe",
                
                args=[
                    r"C:\Users\JINGYI\Desktop\1013Weather2mood\server.py"
                ],                
                
                cwd=r"C:\Users\JINGYI\Desktop\1013Weather2mood",
                env=os.environ
            ),
        ),

        # 4. Travel Translation、Currency Conversion 
        MCPToolset(
            connection_params=StdioServerParameters(
                command=r"C:\Users\JINGYI\Desktop\TravelTranslator\.venv\Scripts\python.exe",
                
                args=[
                    r"C:\Users\JINGYI\Desktop\TravelTranslator\server.py"
                ],

                cwd=r"C:\Users\JINGYI\Desktop\TravelTranslator",     
                # env=os.environ
            ),
        ),

        # # # 5. CoinGecko 
        # # MCPToolset(
        # #     connection_params=SseConnectionParams(
        # #         url="https://mcp.api.coingecko.com/sse", 
        # #     ),
        # # ),
        
        # 6. Lucky draw (塔羅運勢) 
        MCPToolset(
            connection_params=SseConnectionParams(
                url="http://127.0.0.1:5002/sse", 
            ),
        ),

        # 7. vibesong_playlist
        MCPToolset(
            connection_params=SseConnectionParams(
                url="http://127.0.0.1:8001/sse", 
            ), 
        ),

        #8.calculate_budget
        MCPToolset(
            connection_params=SseConnectionParams(
                url="http://127.0.0.1:5004/sse",
            ),
        ),
    ],
)


