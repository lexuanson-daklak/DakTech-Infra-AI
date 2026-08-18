from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
TEMPLATE_DIR = BASE_DIR / "templates"

APP_NAME = "DakTech Infra AI"
APP_TAGLINE = "AI quản trị hạ tầng kỹ thuật Đắk Lắk"
VERSION = "MVP v0.7.3"
DEPLOYMENT_MODE = "PUBLIC_DEMO"

DAKLAK_MAP_CENTER = {"latitude": 12.75, "longitude": 108.55, "zoom": 7.6}

DISCLAIMER = (
    "BẢN THỬ NGHIỆM – dữ liệu mẫu và dữ liệu dẫn xuất chỉ phục vụ kiểm chứng mô hình; "
    "không thay thế hồ sơ, cơ sở dữ liệu, kết luận chuyên môn hoặc quyết định của cơ quan nhà nước."
)

MODULES = {
    "road": {"name": "DakRoad AI", "icon": "🛣️", "domain": "Quản lý kết cấu hạ tầng đường bộ"},
    "cemetery": {"name": "DakCemetery AI", "icon": "⚱️", "domain": "Quản lý nghĩa trang và cơ sở hỏa táng"},
    "water": {"name": "DakWater AI", "icon": "💧", "domain": "Quản lý cấp nước sạch"},
    "drain": {"name": "DakDrain AI", "icon": "🌧️", "domain": "Quản lý thoát nước và xử lý nước thải"},
}

ALLOWED_STATUSES = ["ACTIVE", "REVIEW", "RESTRICTED", "LIMITED", "CLOSED", "PLANNED", "INACTIVE"]

REQUIRED_REGISTRY_COLUMNS = [
    "module", "asset_code", "asset_name", "asset_type", "locality",
    "management_unit", "status", "source_id", "updated_at",
]

OPTIONAL_REGISTRY_COLUMNS = ["latitude", "longitude", "investment_need", "geometry_type"]

ASSET_LAYER_FILES = {
    "legal": "asset_legal_links.csv",
    "planning": "asset_planning.csv",
    "investment": "asset_investment.csv",
    "operations": "asset_operations.csv",
    "maintenance": "asset_maintenance.csv",
    "incidents": "asset_incidents.csv",
    "history": "asset_history.csv",
}
