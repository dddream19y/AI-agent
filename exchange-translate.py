from fastmcp import FastMCP
from deep_translator import GoogleTranslator
import httpx
import os
from dotenv import load_dotenv

# 載入 .env 檔案中的 API Key
load_dotenv()
API_KEY = os.getenv("EXCHANGERATE_API_KEY")

# 初始化 MCP Server
mcp = FastMCP("Travel Helper (Exchange & Translate)")

# ExchangeRate-API 的基礎網址
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

@mcp.tool()
async def get_exchange_rates(base: str = "TWD") -> str:
    """
    查詢指定貨幣對其他主要貨幣的匯率。
    
    Args:
        base: 基準貨幣代碼 (例如: TWD, USD, JPY)。預設為 TWD。
    """
    if not API_KEY:
        return "錯誤: 伺服器未設定 EXCHANGERATE_API_KEY，請檢查 .env 檔案。"

    # ExchangeRate-API 的標準查詢端點
    url = f"{BASE_URL}/latest/{base.upper()}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            # 檢查是否 API Key 錯誤或其他 HTTP 錯誤
            if response.status_code == 403:
                return "API Key 無效，請檢查設定。"
            response.raise_for_status()
            
            data = response.json()
            if data.get("result") != "success":
                return f"API 回傳錯誤: {data.get('error-type')}"

            rates = data.get("conversion_rates", {})
            
            # 為了避免回傳 160 種貨幣太多，我們只列出旅遊常用的幾種
            common_currencies = ["USD", "EUR", "JPY", "KRW", "CNY", "TWD", "HKD", "GBP", "AUD", "THB"]
            
            result = f"【匯率快報】基準貨幣: {base.upper()}\n"
            found_any = False
            for curr in common_currencies:
                if curr in rates and curr != base.upper():
                    result += f"- {curr}: {rates[curr]}\n"
                    found_any = True
            
            if not found_any:
                result += "(無常用貨幣匯率資料)"
                
            return result
            
        except httpx.HTTPStatusError as e:
            return f"連線錯誤: {e.response.status_code}"
        except Exception as e:
            return f"發生未預期的錯誤: {str(e)}"

@mcp.tool()
async def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    """
    精確換算貨幣金額 (例如: 1000 JPY 等於多少 TWD)。

    Args:
        amount: 金額 (例如: 1000)
        from_curr: 持有貨幣 (例如: JPY)
        to_curr: 想換成的貨幣 (例如: TWD)
    """
    if not API_KEY:
        return "錯誤: 伺服器未設定 API Key。"

    # 使用 Pair Conversion API 直接換算
    url = f"{BASE_URL}/pair/{from_curr.upper()}/{to_curr.upper()}/{amount}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 403:
                return "API Key 無效。"
            response.raise_for_status()

            data = response.json()
            if data.get("result") != "success":
                return f"換算失敗: {data.get('error-type')}"

            # 取得換算後的結果
            converted_res = data.get("conversion_result")
            rate = data.get("conversion_rate")

            return (f"{amount} {from_curr.upper()} ≈ {converted_res} {to_curr.upper()}\n"
                    f"(當前匯率: 1 {from_curr.upper()} = {rate} {to_curr.upper()})")

        except Exception as e:
            return f"換算發生錯誤: {str(e)}"


@mcp.tool()
def get_translate(text: str, target_lang: str) -> str:
    """
    旅遊翻譯小幫手。可以將文字翻譯成指定語言。
    
    Args:
        text: 想翻譯的句子 (例如: "廁所在哪裡？", "這個多少錢？")
        target_lang: 目標語言代碼 (例如: "en" 是英文, "ja" 是日文, "ko" 是韓文, "th" 是泰文, "fr" 是法文)
    """
    try:
        # 自動偵測來源語言，翻譯成目標語言
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text)
        
        return f"【翻譯結果】\n原文: {text}\n譯文 ({target_lang}): {translated_text}"
    except Exception as e:
        return f"翻譯失敗: {str(e)}"

    
if __name__ == "__main__":
    mcp.run(transport="stdio")

