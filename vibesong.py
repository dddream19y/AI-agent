from fastmcp import FastMCP
import asyncio   
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

mcp = FastMCP(name="spotify_mood_server")

# 初始化 Spotify 客戶端 (如果沒填 ID 會報錯喔)
try:
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("✅ Spotify API 連線成功！")
except Exception as e:
    print(f"⚠️ Spotify 設定有誤: {e}")
    sp = None

# --- Spotify 搜尋函式  ---
def _search_spotify(keyword):
    if not sp:
        return []
    
    print(f"DEBUG: 正在向 Spotify 搜尋: {keyword}")
    # type='playlist' 代表只搜歌單，limit=3 代表抓前三筆
    results = sp.search(q=keyword, type='playlist', limit=3)
    
    items = results['playlists']['items']
    clean_results = []
    
    for item in items:
        if item:
            clean_results.append({
                "title": item['name'],
                "url": item['external_urls']['spotify'], # 這是 Spotify 的開啟連結
                "description": item['description'] or "無描述",
                "tracks": item['tracks']['total']
            })
    return clean_results

@mcp.tool
async def get_mood_playlist(mood_keyword: str) -> str:
    """
    根據心情關鍵字，搜尋 Spotify 上的播放清單。
    """
    if SPOTIPY_CLIENT_ID == '你的_CLIENT_ID_貼在這裡':
        return "❌ 錯誤：請先在 server.py 填入 Spotify Client ID！"

    try:
        # 使用 to_thread 把網路請求丟到背景，避免卡死 Server
        playlists = await asyncio.to_thread(_search_spotify, mood_keyword)
        
        if not playlists:
            return f"抱歉，在 Spotify 上找不到關於「{mood_keyword}」的歌單。"

        text = f"【Spotify 搜尋結果】為您找到關於「{mood_keyword}」的精選歌單：\n"
        for p in playlists:
            text += f"- 🎵 {p['title']} (歌曲數: {p['tracks']})\n"
            text += f"  🔗 連結: {p['url']}\n"
            
        return text

    except Exception as e:
        return f"搜尋時發生錯誤: {str(e)}"

# 啟動
if __name__ == "__main__":
    mcp.run(transport="sse", port=8001)
