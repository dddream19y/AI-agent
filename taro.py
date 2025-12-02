import random
from typing import Dict, Any, List
from fastmcp import FastMCP

mcp = FastMCP("travel_tarot_server")

# 旅遊大秘儀塔羅牌牌組（JSON 結構）
TRAVEL_TAROT_DECK: List[Dict[str, Any]] = [
    {
        "id": 0,
        "name_en": "The Fool",
        "name_zh": "愚者",
        "upright": {
            "keywords": ["啟程", "自發", "意外收穫"],
            "travel_meaning": "適合踏入沒去過的區域與路線，迷路反而可能踩到隱藏版景點。",
            "advice": "今天可以刻意走進沒規劃的小巷，把地圖收起來五分鐘，讓旅程自己展開。",
        },
        "reversed": {
            "keywords": ["衝動", "準備不足", "重複犯錯"],
            "travel_meaning": "行程容易因一時興起而失控，可能錯過重要時間或交通。",
            "advice": "想臨時改行程前，先確認車班、票券與預算，別把愚者玩成魯莽。",
        },
    },
    {
        "id": 1,
        "name_en": "The Magician",
        "name_zh": "魔術師",
        "upright": {
            "keywords": ["掌控", "資源整合", "高效率"],
            "travel_meaning": "適合排多景點串聯行程，你有能力把交通與時間精準接起來。",
            "advice": "善用地圖、票券、時刻表等工具，今天可以安排一條看起來有點瘋狂但其實可行的路線。",
        },
        "reversed": {
            "keywords": ["分心", "過度自信", "溝通不清"],
            "travel_meaning": "行程安排過滿，容易出現溝通失誤或有人跟不上節奏。",
            "advice": "請把『能做到』跟『會不會累死大家』分開來想，預留緩衝時間。",
        },
    },
    {
        "id": 2,
        "name_en": "The High Priestess",
        "name_zh": "女祭司",
        "upright": {
            "keywords": ["直覺", "安靜", "內在節奏"],
            "travel_meaning": "適合安靜的室內景點，博物館、書店、咖啡廳會比打卡名勝更對味。",
            "advice": "把行程放慢，給自己一段不被打擾的時間，讓旅程也服務你的情緒。",
        },
        "reversed": {
            "keywords": ["壓抑", "逃避", "不想面對"],
            "travel_meaning": "你可能在硬撐行程表，實際上身心都不太想動。",
            "advice": "承認自己今天不適合硬衝景點，刪掉一個行程不會讓世界毀滅。",
        },
    },
    {
        "id": 3,
        "name_en": "The Empress",
        "name_zh": "皇后",
        "upright": {
            "keywords": ["享樂", "美感", "豐盛"],
            "travel_meaning": "美食、美景、美照同時在線，適合悠閒吃飯、拍照與慢慢逛街。",
            "advice": "允許自己為好吃的東西、好看的景色多花一點時間和錢，這些會變成之後的快樂記憶。",
        },
        "reversed": {
            "keywords": ["過度依賴舒適圈", "懶散", "過度消費"],
            "travel_meaning": "容易一路躺平或瘋狂購物，結果行程結束只剩戰利品與疲憊。",
            "advice": "適度享樂可以，但請記得你是來旅行，不是來逃避所有現實設定。",
        },
    },
    {
        "id": 4,
        "name_en": "The Emperor",
        "name_zh": "皇帝",
        "upright": {
            "keywords": ["結構", "主導", "穩定"],
            "travel_meaning": "適合你掌控行程，訂計畫、拍板定案、扛起大家的時間管理。",
            "advice": "勇敢當今天的決策者，但也記得留下可以被討論的空間。",
        },
        "reversed": {
            "keywords": ["控制欲", "固執", "僵化"],
            "travel_meaning": "你可能把行程排成軍事作戰，別人只想請假。",
            "advice": "試著問一句：『大家真的想這樣走嗎？』然後認真聽答案。",
        },
    },
    {
        "id": 5,
        "name_en": "The Hierophant",
        "name_zh": "教皇",
        "upright": {
            "keywords": ["文化", "傳統", "規則"],
            "travel_meaning": "適合拜訪寺廟、歷史建築、在地文化景點，會對這座城市多一層理解。",
            "advice": "尊重當地習俗與規範，試著理解它們存在的理由，而不是只當背景。",
        },
        "reversed": {
            "keywords": ["刻板", "形式化", "照本宣科"],
            "travel_meaning": "可能只是在走標準觀光路線，沒有真的連結到這個地方。",
            "advice": "問一個在地人：『你們自己會去的地方是哪裡？』行程會有質變。",
        },
    },
    {
        "id": 6,
        "name_en": "The Lovers",
        "name_zh": "戀人",
        "upright": {
            "keywords": ["連結", "選擇", "關係和諧"],
            "travel_meaning": "和同行的人默契不錯，適合一起做決定、一起迷路、一起笑場。",
            "advice": "把行程的一部分交給對方選，旅程會變成真正的『一起』。",
        },
        "reversed": {
            "keywords": ["分歧", "誤會", "價值觀碰撞"],
            "travel_meaning": "對行程或花費的期待可能不同，容易出現小摩擦。",
            "advice": "在吵起來之前，先把『各自最在意的是什麼』講清楚。",
        },
    },
    {
        "id": 7,
        "name_en": "The Chariot",
        "name_zh": "戰車",
        "upright": {
            "keywords": ["前進", "效率", "跨區移動"],
            "travel_meaning": "適合長距離交通與走行程，車班與轉乘多半會順利。",
            "advice": "可以大膽排跨城或多站行程，但仍保留一點延誤的緩衝時間。",
        },
        "reversed": {
            "keywords": ["拖延", "錯車", "方向混亂"],
            "travel_meaning": "容易遇到塞車、誤點或走錯方向，導致行程變形。",
            "advice": "請先確認下一班車的時間，再決定要不要『再多拍兩張』。",
        },
    },
    {
        "id": 8,
        "name_en": "Strength",
        "name_zh": "力量",
        "upright": {
            "keywords": ["溫柔的堅持", "內在穩定", "慢熱耐力"],
            "travel_meaning": "體力與心情都在穩定狀態，可以挑戰稍微吃力但值得的行程。",
            "advice": "選一個『有點累但回憶值高』的活動，例如登高、健走或長時間步行。",
        },
        "reversed": {
            "keywords": ["疲憊", "心累", "強撐"],
            "travel_meaning": "你可能在硬撐，他人看起來玩得很嗨，但你的電量已經見底。",
            "advice": "承認自己需要休息，比假裝沒事更有勇氣。適時縮短行程。",
        },
    },
    {
        "id": 9,
        "name_en": "The Hermit",
        "name_zh": "隱者",
        "upright": {
            "keywords": ["獨處", "內省", "安靜探索"],
            "travel_meaning": "一個人走會比一群人走更自在，適合自由散步與安靜角落。",
            "advice": "留一段時間不要講話，只是走路、觀察、聽城市的聲音。",
        },
        "reversed": {
            "keywords": ["孤立", "封閉", "不想參與"],
            "travel_meaning": "你可能下意識把自己抽離群體，既不想跟又怕被說不合群。",
            "advice": "選擇一小段行程獨行就好，不需要整天消失，給自己空間也給他人交代。",
        },
    },
    {
        "id": 10,
        "name_en": "Wheel of Fortune",
        "name_zh": "命運之輪",
        "upright": {
            "keywords": ["轉機", "偶然驚喜", "節奏變化"],
            "travel_meaning": "行程會臨時變動，但大多數是朝好方向偏移。",
            "advice": "當計畫被打亂時，先觀察一下新選項，也許其實更適合你現在的狀態。",
        },
        "reversed": {
            "keywords": ["延誤", "卡關", "覺得運氣不好"],
            "travel_meaning": "你可能連續遇到小麻煩，讓你懷疑是不是被詛咒。",
            "advice": "把今天當成『低潮日』看待就好，別做重大決定，維持基本安全即可。",
        },
    },
    {
        "id": 11,
        "name_en": "Justice",
        "name_zh": "正義",
        "upright": {
            "keywords": ["平衡", "決策", "責任"],
            "travel_meaning": "適合處理預算分配與行程取捨，理性能運轉得不錯。",
            "advice": "重新檢查花費、時間與體力分配，調整到你覺得『剛好』的位置。",
        },
        "reversed": {
            "keywords": ["失衡", "偏頗", "不公平感"],
            "travel_meaning": "有人可能覺得行程或花費分配不太公平，但沒說出口。",
            "advice": "主動開口詢問大家感受，比等爆炸之後再收拾輕鬆很多。",
        },
    },
    {
        "id": 12,
        "name_en": "The Hanged Man",
        "name_zh": "倒吊人",
        "upright": {
            "keywords": ["暫停", "換位思考", "強迫停留"],
            "travel_meaning": "行程可能因天氣、排隊或交通被迫放慢，你會看到原本沒打算看的風景。",
            "advice": "與其抱怨，不如用這段時間觀察細節或拍照，這些空檔會變成旅程的註腳。",
        },
        "reversed": {
            "keywords": ["拖延", "僵持", "不願放手"],
            "travel_meaning": "你明明知道某個行程不適合，卻死不刪除，結果拖累整體。",
            "advice": "問自己一句：『如果今天重排，我還會保留這個行程嗎？』誠實面對答案。",
        },
    },
    {
        "id": 13,
        "name_en": "Death",
        "name_zh": "死神",
        "upright": {
            "keywords": ["結束", "轉換", "斷捨離"],
            "travel_meaning": "不是壞預兆，而是提醒你該放掉不適合的行程或期待，換來更輕盈的旅程。",
            "advice": "刪掉一個讓你壓力很大的景點，換成真正想去的地方或純休息。",
        },
        "reversed": {
            "keywords": ["停滯", "抗拒改變", "無法結束"],
            "travel_meaning": "你可能暗自覺得這趟旅程和現實都卡住，只是勉強照表演出。",
            "advice": "允許自己承認『這樣玩我其實不快樂』，從小調整開始。",
        },
    },
    {
        "id": 14,
        "name_en": "Temperance",
        "name_zh": "節制",
        "upright": {
            "keywords": ["調和", "節奏穩定", "剛剛好"],
            "travel_meaning": "最適合慢旅行的一天，一切都可以不急不徐地完成。",
            "advice": "用散步或短程交通銜接景點，讓行程留有空氣感。",
        },
        "reversed": {
            "keywords": ["過度", "失衡", "忽快忽慢"],
            "travel_meaning": "有時過度活動，有時又完全放空，身體跟不上這樣的切換。",
            "advice": "決定今天到底要『慢行』還是『衝刺』，不要兩種都試。",
        },
    },
    {
        "id": 15,
        "name_en": "The Devil",
        "name_zh": "惡魔",
        "upright": {
            "keywords": ["誘惑", "成癮", "過度享樂"],
            "travel_meaning": "購物、宵夜、二刷景點的衝動變強，很容易失控。",
            "advice": "在刷卡前先問自己：『回家拆帳單時還會開心嗎？』願意負責再下手。",
        },
        "reversed": {
            "keywords": ["解脫", "看清束縛", "戒掉壞習慣"],
            "travel_meaning": "你有機會跳脫以往固定的旅遊模式，試試不一樣的玩法。",
            "advice": "換一種跟平常完全不同的行程類型，你會發現自己其實沒那麼被綁死。",
        },
    },
    {
        "id": 16,
        "name_en": "The Tower",
        "name_zh": "高塔",
        "upright": {
            "keywords": ["突發", "劇烈變動", "打掉重練"],
            "travel_meaning": "天氣、交通或其他不可控因素可能讓計畫整個翻掉。",
            "advice": "先處理安全，再重新規劃。被迫改變不代表今天就報廢，只是路線重畫。",
        },
        "reversed": {
            "keywords": ["延遲爆炸", "僥倖", "累積問題"],
            "travel_meaning": "你一直在硬拖著有問題的計畫，遲早會集中爆發。",
            "advice": "現在主動調整，比等到全部崩盤時被迫收拾理智得多。",
        },
    },
    {
        "id": 17,
        "name_en": "The Star",
        "name_zh": "星星",
        "upright": {
            "keywords": ["希望", "療癒", "靈感"],
            "travel_meaning": "旅程會給你某種溫柔的啟發，也許是一句話、一個畫面、一段風。",
            "advice": "帶上筆記本或開個備忘錄，記下那些讓你心情變柔軟的瞬間。",
        },
        "reversed": {
            "keywords": ["失望感", "疲乏", "提不起勁"],
            "travel_meaning": "你對旅程的期待可能過高，現實自然很難追上幻想。",
            "advice": "把標準從『完美之旅』調整成『今天有一件小事讓我開心』就好。",
        },
    },
    {
        "id": 18,
        "name_en": "The Moon",
        "name_zh": "月亮",
        "upright": {
            "keywords": ["直覺", "迷霧", "情緒敏感"],
            "travel_meaning": "地圖與實際可能有落差，迷路或誤會資訊的機率增加。",
            "advice": "白天可以跟著直覺探索，晚上請務必顧慮安全與回程時間。",
        },
        "reversed": {
            "keywords": ["看清事實", "從混亂中醒來", "不再自我嚇自己"],
            "travel_meaning": "你開始看懂這座城市的節奏，之前的不安感會慢慢退去。",
            "advice": "把原本害怕嘗試的某件小事，改成『稍微推自己一把』試試看。",
        },
    },
    {
        "id": 19,
        "name_en": "The Sun",
        "name_zh": "太陽",
        "upright": {
            "keywords": ["高能量", "順利", "黃金旅遊日"],
            "travel_meaning": "氣候、人際與體力都在線，適合戶外、大景、拍照與玩到飽。",
            "advice": "今天是排重點行程的好日子，記得多補水、多防曬，然後好好玩。",
        },
        "reversed": {
            "keywords": ["過勞", "曬傷", "表面開心"],
            "travel_meaning": "你可能硬撐著玩到全身過熱，心情反而變得敏感暴躁。",
            "advice": "比起再多一個景點，體力與皮膚比較重要，適時收工是智慧。",
        },
    },
    {
        "id": 20,
        "name_en": "Judgment",
        "name_zh": "審判",
        "upright": {
            "keywords": ["覺醒", "重新選擇", "總結"],
            "travel_meaning": "你會突然看懂這趟旅程真正給你的東西，並做出新的選擇。",
            "advice": "問自己：『如果明天就回家，今天我最想完成的是什麼？』然後去做那件事。",
        },
        "reversed": {
            "keywords": ["遲疑", "卡在過去", "不願評估"],
            "travel_meaning": "你可能在逃避檢視這趟旅程是否真的符合你的期待。",
            "advice": "花五分鐘回顧一下這趟旅行，誠實寫下『下一次我想改變什麼』。",
        },
    },
    {
        "id": 21,
        "name_en": "The World",
        "name_zh": "世界",
        "upright": {
            "keywords": ["完成", "整合", "圓滿"],
            "travel_meaning": "行程與體驗會自然收束成一個完整故事，你會帶著滿足回家。",
            "advice": "整理照片、收好票根與小物，給這趟旅程一個有儀式感的結尾。",
        },
        "reversed": {
            "keywords": ["未完", "卡在中途", "不甘心"],
            "travel_meaning": "旅程結束時，你可能覺得『好像還差一點什麼』。",
            "advice": "接受旅程不一定要完美收尾，保留一點意猶未盡，才有再訪的理由。",
        },
    },
]


@mcp.tool()
def draw_travel_tarot() -> Dict[str, Any]:
    """抽取一張旅遊塔羅運勢牌（單張牌版本）。

    - 每次呼叫會從 22 張大秘儀中抽出一張，不重複不重要，重點是『靈感』。
    - 正位 / 逆位隨機決定，用於提供不同角度的旅遊建議。
    - 若需要可重現結果，請在外層自行管理亂數種子或記錄抽出的牌。"""

    deck = TRAVEL_TAROT_DECK.copy()
    random.shuffle(deck)
    card = deck[0]

    is_reversed = random.choice([True, False])
    orientation = "reversed" if is_reversed else "upright"
    data = card[orientation]

    return {
        "card": {
            "id": card["id"],
            "name_en": card["name_en"],
            "name_zh": card["name_zh"],
            "orientation": orientation,  # "upright" or "reversed"
            "keywords": data["keywords"],
            "travel_meaning": data["travel_meaning"],
            "advice": data["advice"],
        },
        "meta": {
            "deck_size": len(TRAVEL_TAROT_DECK),
            "note": "本結果為隨機抽取，用於旅遊情境下的靈感與反思，非現實保證。",
        },
    }


if __name__ == "__main__":
    mcp.run(transport="sse", port=5002)
