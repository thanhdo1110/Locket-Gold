import os

BOT_TOKEN = os.environ.get("8261455751:AAE7UVdgp4dyIE5_LIPBNTCFRP_VuYMFfAA", "")
NEXTDNS_KEY = os.environ.get("0fcd3a75e90555ae487e22c2c3ef8d3582b5bcce", "")

TOKEN_SETS = [
    {
        "fetch_token": "",
        "app_transaction": "",
        "hash_params": "",
        "hash_headers": "",
        "is_sandbox": True,
    },
    {
        "fetch_token": "",
        "app_transaction": "",
        "hash_params": "",
        "hash_headers": "",
        "is_sandbox": False,
    },
]

ADMIN_ID = 5431097885
NUM_WORKERS = 2
DONATE_PHOTO = "AgACAgUAAxkBAAEhBOdpjtu4_D_90mzmM3ax-jLUQbW7HwACjA5rGyK6eFQz2Vzy6zHTMwEAAwIAA3kAAzoE"

E_LOADING = '<tg-emoji emoji-id="5350752364246606166">✍️</tg-emoji>'
E_LIMIT   = '<tg-emoji emoji-id="5424857974784925603">🚫</tg-emoji>'
E_SUCCESS = '<tg-emoji emoji-id="5260463209562776385">✅</tg-emoji>'
E_ERROR   = '<tg-emoji emoji-id="5318840353510408444">🔴</tg-emoji>'
E_TIP     = '<tg-emoji emoji-id="4968003407315993509">💡</tg-emoji>'
E_MENU    = '<tg-emoji emoji-id="5449601904147440135">👑</tg-emoji>'

E_USER    = '<tg-emoji emoji-id="5974048815789903111">👤</tg-emoji>'
E_ID      = '<tg-emoji emoji-id="5974526806995242353">🆔</tg-emoji>'
E_TAG     = '<tg-emoji emoji-id="5240228673738527951">🏷️</tg-emoji>'
E_STAT    = '<tg-emoji emoji-id="4967519884192777037">📊</tg-emoji>'
E_GLOBE   = '<tg-emoji emoji-id="5231489647946768652">🌐</tg-emoji>'
E_SOS     = '<tg-emoji emoji-id="6301027265899661025">🆘</tg-emoji>'
E_SHIELD  = '<tg-emoji emoji-id="5352888345972187597">🛡️</tg-emoji>'
E_CALENDAR = '<tg-emoji emoji-id="5413879192267805083">📅</tg-emoji>'
E_IOS     = '<tg-emoji emoji-id="5350556204500263431">🍏</tg-emoji>'
E_ANDROID = '<tg-emoji emoji-id="5303145396254563405">🤖</tg-emoji>'


DEFAULT_LANG = "VI"

TEXTS = {
    "VI": {
        "welcome": f"{E_SUCCESS} <b>Locket Gold Activator</b>\n\nChào mừng! Vui lòng chọn ngôn ngữ hoặc sử dụng menu bên dưới.",
        "menu_msg": f"{E_MENU} <b>Bảng Điều Khiển</b>\n\n👇 Bấm nút bên dưới để nhập Username kích hoạt Gold.",
        "btn_input": "🔑 Nhập User Locket",
        "btn_lang": "🌐 Đổi Ngôn Ngữ",
        "btn_help": "🆘 Hỗ Trợ",
        "prompt_input": f"{E_LOADING} Vui lòng nhập <b>Username</b> hoặc <b>Link Locket</b> của bạn vào tin nhắn trả lời bên dưới:",
        "lang_select": "🌐 Vui lòng chọn ngôn ngữ / Please select language:",
        "lang_set": f"{E_SUCCESS} Đã cài đặt ngôn ngữ: Tiếng Việt",
        "help_msg": (
            f"<b>{E_MENU} Danh Sách Lệnh:</b>\n\n"
            f"/start - Khởi động bot & Menu chính\n"
            f"/setlang - Đổi ngôn ngữ (VI/EN)\n"
            f"/help - Xem trợ giúp này\n\n"
            f"<b>{E_TIP} Cách dùng:</b>\n"
            f"1. Bấm nút '🔑 Nhập User Locket'\n"
            f"2. Điền Username hoặc Link\n"
            f"3. Bot sẽ kiểm tra và kích hoạt Gold."
        ),
        "resolving": f"{E_LOADING} <b>Đang phân giải UID...</b>",
        "not_found": f"{E_ERROR} Không tìm thấy User.",
        "limit_reached": f"{E_LIMIT} Đã đạt giới hạn request (5/5).",
        "queue_almost": f"{E_LOADING} <b>Sắp đến lượt bạn!</b>\nCòn <b>2 người</b> nữa là đến lượt bạn. Hãy chuẩn bị sẵn sàng! 🚀",
        "admin_noti_sent": f"{E_SUCCESS} Đã gửi thông báo đến tất cả user.",
        "admin_reset": f"{E_SUCCESS} Đã reset lượt dùng cho user {{}}.",
        "admin_only": f"{E_ERROR} Bạn không có quyền sử dụng lệnh này.",
        "checking_status": f"{E_LOADING} <b>Đang kiểm tra Entitlement...</b>",
        "free_status": "Free (Chưa Active)",
        "gold_active": f"{E_SUCCESS} <b>Gold Đã Active</b> (Hết hạn: {{}})",
        "user_info_title": f"{E_USER} <b>User Information</b>",
        "btn_upgrade": "🚀 KÍCH HOẠT NGAY",
        "queued": f"{E_LOADING} <b>Đã thêm vào hàng chờ</b>\nTarget: <code>{{0}}</code>\nVị trí: <b>#{{1}}</b> (Còn {{2}} người trước bạn)...",
        "processing": (
            f"{E_LOADING} <b>⚡ SYSTEM EXPLOIT RUNNING...</b>\n"
            f"<pre>"
            f"[*] Target:  {{}}\n"
            f"[*] Method:  RevenueCat_Bypass_v2\n"
            f"[>] Action:  Injecting Malicious Receipt\n"
            f"[>] Status:  Bypassing Validation...\n"
            f"[?] Waiting: Server Response..."
            f"</pre>"
        ),
        "success_title": f"{E_SUCCESS} <b>KÍCH HOẠT THÀNH CÔNG</b>",
        "generating_dns": f"{E_SHIELD} Đang tạo Anti-Revoke DNS...",
        "fail_title": f"{E_ERROR} <b>Kích hoạt thất bại</b>",
        "dns_msg": (
            f"{E_SHIELD} <b>HƯỚNG DẪN QUAN TRỌNG</b>:\n"
            f"1️⃣ Vào App Locket kiểm tra đã có <b>Gold</b> chưa.\n"
            f"2️⃣ Nếu đã có, tiến hành <b>CÀI DNS NGAY</b> (trong 45s):\n\n"
            f"{E_IOS} <b>iOS</b>: <a href='{{}}'>Bấm vào đây để cài</a>\n"
            f"(Mở link bằng <b>Safari</b> -> Cho phép -> Cài đặt Profile)\n\n"
            f"{E_ANDROID} <b>Android</b>: <code>{{}}.dns.nextdns.io</code>\n"
            f"(Cài đặt → Mạng → Private DNS)\n\n"
            f"{E_TIP} <b>Lưu ý</b>: Bắt buộc cài DNS để không bị mất Gold!"
        )
    },
    "EN": {
        "welcome": f"{E_SUCCESS} <b>Locket Gold Activator</b>\n\nWelcome! Please select your language or use the menu below.",
        "menu_msg": f"{E_MENU} <b>Control Panel</b>\n\n👇 Click the button below to enter Username.",
        "btn_input": "🔑 Input Locket User",
        "btn_lang": "🌐 Change Language",
        "btn_help": "🆘 Help",
        "prompt_input": f"{E_LOADING} Please enter your <b>Username</b> or <b>Locket Link</b> in the reply below:",
        "lang_select": "🌐 Please select language:",
        "lang_set": f"{E_SUCCESS} Language set: English",
        "help_msg": (
            f"<b>{E_MENU} Commands:</b>\n\n"
            f"/start - Main Menu\n"
            f"/setlang - Change Language\n"
            f"/help - Show this help\n\n"
            f"<b>{E_TIP} How to use:</b>\n"
            f"1. Click '🔑 Input Locket User'\n"
            f"2. Enter Username or Link\n"
            f"3. Bot will activate Gold."
        ),
        "resolving": f"{E_LOADING} <b>Resolving UID...</b>",
        "not_found": f"{E_ERROR} User not found.",
        "limit_reached": f"{E_LIMIT} Daily limit reached (5/5).",
        "queue_almost": f"{E_LOADING} <b>Almost your turn!</b>\n<b>2 people</b> ahead of you. Get ready! 🚀",
        "admin_noti_sent": f"{E_SUCCESS} Notification sent to all users.",
        "admin_reset": f"{E_SUCCESS} Usage reset for user {{}}.",
        "admin_only": f"{E_ERROR} You don't have permission.",
        "checking_status": f"{E_LOADING} <b>Checking Entitlements...</b>",
        "free_status": "Free (Inactive)",
        "gold_active": f"{E_SUCCESS} <b>Gold Active</b> (Exp: {{}})",
        "user_info_title": f"{E_USER} <b>User Information</b>",
        "btn_upgrade": "🚀 ACTIVATE NOW",
        "queued": f"{E_LOADING} <b>Added to Queue</b>\nTarget: <code>{{0}}</code>\nPosition: <b>#{{1}}</b> ({{2}} people ahead)...",
        "processing": (
            f"{E_LOADING} <b>⚡ SYSTEM EXPLOIT RUNNING...</b>\n"
            f"<pre>"
            f"[*] Target:  {{}}\n"
            f"[*] Method:  RevenueCat_Bypass_v2\n"
            f"[>] Action:  Injecting Malicious Receipt\n"
            f"[>] Status:  Bypassing Validation...\n"
            f"[?] Waiting: Server Response..."
            f"</pre>"
        ),
        "success_title": f"{E_SUCCESS} <b>ACTIVATION SUCCESSFUL</b>",
        "generating_dns": f"{E_SHIELD} Generating Anti-Revoke DNS...",
        "fail_title": f"{E_ERROR} <b>Activation Failed</b>",
        "dns_msg": (
            f"{E_SHIELD} <b>IMPORTANT INSTRUCTIONS</b>:\n"
            f"1️⃣ Check Locket App for <b>Gold</b> status.\n"
            f"2️⃣ If active, <b>INSTALL DNS IMMEDIATELY</b> (within 45s):\n\n"
            f"{E_IOS} <b>iOS</b>: <a href='{{}}'>Click to Install</a>\n"
            f"(Open link in <b>Safari</b> -> Allow -> Install Profile)\n\n"
            f"{E_ANDROID} <b>Android</b>: <code>{{}}.dns.nextdns.io</code>\n"
            f"(Settings → Network → Private DNS)\n\n"
            f"{E_TIP} <b>Note</b>: DNS is required to keep Gold active!"
        )
    }
}

def T(key, lang=None):
    if not lang:
        lang = DEFAULT_LANG
    return TEXTS.get(lang, TEXTS["VI"]).get(key, key)
