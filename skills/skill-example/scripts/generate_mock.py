#!/usr/bin/env python3
"""Mock data generator — fills missing, null, and empty JSON fields with realistic values."""

import json
import re
import sys
import random
import uuid
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

# ── Realistic data pools ──────────────────────────────────────────────

CHINESE_NAMES = [
    "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十",
    "郑小明", "冯大华", "陈静", "林峰", "黄丽", "徐强", "马超", "朱婷",
    "胡建平", "郭美玲", "何志远", "高秀英", "罗文博", "梁思琪", "宋佳",
    "谢天华", "韩雪", "唐亮", "曹颖", "许磊", "邓薇", "萧然",
]

ENGLISH_NAMES = [
    "John Doe", "Jane Smith", "Alice Johnson", "Bob Williams",
    "Charlie Brown", "Diana Prince", "Eve Davis", "Frank Miller",
    "Grace Lee", "Henry Wilson", "Ivy Chen", "Jack Taylor",
]

CHINESE_ADDRESSES = [
    "北京市朝阳区建国路88号",
    "上海市浦东新区世纪大道100号",
    "广州市天河区体育西路56号",
    "深圳市南山区科技园南区",
    "杭州市西湖区文三路200号",
    "成都市高新区天府大道666号",
    "南京市鼓楼区中山路321号",
    "武汉市洪山区光谷大道88号",
]

DEPARTMENTS = [
    "技术研发部", "产品部", "设计部", "运营部", "市场部",
    "人力资源部", "财务部", "法务部", "客服部", "数据分析部",
]

DOMAINS = ["example.com", "test.com", "mock.io", "demo.org", "sample.net"]

AVATARS = [
    "https://picsum.photos/200",
    "https://i.pravatar.cc/200",
    "https://api.dicebear.com/7.x/adventurer/svg",
]

# ── Field pattern matching ────────────────────────────────────────────

FIELD_PATTERNS: list[tuple[re.Pattern, callable]] = []

def pattern(regex: str):
    """Decorator to register a field pattern."""
    def decorator(fn):
        FIELD_PATTERNS.append((re.compile(regex, re.IGNORECASE), fn))
        return fn
    return decorator

@pattern(r'.*email.*')
def mock_email(field: str, ctx: dict) -> str:
    name = ctx.get("tenant", "user")
    uid = ctx.get("id", random.randint(1000, 9999))
    domain = ctx.get("domain", random.choice(DOMAINS))
    return f"{name}{uid}@{domain}"

@pattern(r'.*(phone|mobile|tel).*')
def mock_phone(field: str, ctx: dict) -> str:
    prefixes = ["138", "139", "150", "151", "186", "187", "176", "185"]
    return random.choice(prefixes) + "".join(str(random.randint(0, 9)) for _ in range(8))

@pattern(r'.*name.*')
def mock_name(field: str, ctx: dict) -> str:
    if ctx.get("locale") == "en":
        return random.choice(ENGLISH_NAMES)
    return random.choice(CHINESE_NAMES)

@pattern(r'.*(first_name|last_name).*')
def mock_split_name(field: str, ctx: dict) -> str:
    if "first" in field.lower():
        return random.choice(["三", "四", "五"]) if ctx.get("locale") != "en" else random.choice(["John", "Jane", "Alice"])
    return random.choice(["张", "李", "王"]) if ctx.get("locale") != "en" else random.choice(["Doe", "Smith", "Johnson"])

@pattern(r'.*address.*')
def mock_address(field: str, ctx: dict) -> str:
    return random.choice(CHINESE_ADDRESSES)

@pattern(r'.*(city|province|state|country).*')
def mock_location(field: str, ctx: dict) -> str:
    locations = ["北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉"]
    return random.choice(locations)

@pattern(r'.*zip.*code.*|.*postal.*')
def mock_zip(field: str, ctx: dict) -> str:
    return f"{random.randint(100000, 999999)}"

@pattern(r'.*(avatar|image|photo|picture|thumb).*')
def mock_image(field: str, ctx: dict) -> str:
    return random.choice(AVATARS) + f"?seed={uuid.uuid4().hex[:8]}"

@pattern(r'.*(url|link|href).*')
def mock_url(field: str, ctx: dict) -> str:
    base = ctx.get("base_url", "https://example.com")
    return f"{base}/resource/{uuid.uuid4().hex[:8]}"

@pattern(r'.*title.*|.*subject.*|.*heading.*')
def mock_title(field: str, ctx: dict) -> str:
    titles = [
        "高级软件工程师", "产品经理", "UI设计师", "项目经理",
        "数据分析报告", "季度总结", "项目计划书", "技术方案",
    ]
    return random.choice(titles)

@pattern(r'.*(description|bio|summary|content|body|remark|note).*')
def mock_text(field: str, ctx: dict) -> str:
    descriptions = [
        "拥有5年以上相关工作经验，擅长后端架构设计与团队协作。熟悉微服务架构、分布式系统和高并发场景。",
        "Full-stack developer with expertise in building scalable web applications. Passionate about clean code and user experience.",
        "负责核心业务模块的开发与维护，主导了多个重要项目的技术选型和架构设计。",
        "Experienced professional specializing in data analysis, system optimization, and cross-functional collaboration.",
        "具备良好的沟通能力和问题解决能力，善于在复杂业务场景中找到最优技术方案。",
    ]
    return random.choice(descriptions)

@pattern(r'.*(company|org|tenant|enterprise|corp).*')
def mock_company(field: str, ctx: dict) -> str:
    tenant = ctx.get("tenant", "")
    if tenant:
        return f"{tenant.title()}科技有限公司"
    companies = ["阿里巴巴", "腾讯", "字节跳动", "百度", "网易", "美团", "京东", "小米"]
    return f"{random.choice(companies)}科技有限公司"

@pattern(r'.*department.*')
def mock_department(field: str, ctx: dict) -> str:
    return random.choice(DEPARTMENTS)

@pattern(r'.*status.*')
def mock_status(field: str, ctx: dict) -> str:
    return random.choice(["active", "pending", "completed", "enabled", "published"])

@pattern(r'.*(created|updated|deleted|published|modified).*at.*')
def mock_timestamp(field: str, ctx: dict) -> str:
    now = datetime.now(timezone.utc)
    days_ago = random.randint(0, 365)
    ts = now.replace(day=max(1, now.day - days_ago))
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")

@pattern(r'.*date.*|.*time.*')
def mock_datetime(field: str, ctx: dict) -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")

@pattern(r'.*(count|total|amount|quantity|num).*')
def mock_number(field: str, ctx: dict) -> int:
    return random.randint(1, 10000)

@pattern(r'.*price.*|.*cost.*|.*fee.*|.*salary.*|.*income.*')
def mock_price(field: str, ctx: dict) -> float:
    return round(random.uniform(9.99, 9999.99), 2)

@pattern(r'.*id$|.*_id$')
def mock_id(field: str, ctx: dict) -> str | int:
    return str(uuid.uuid4())[:8]

@pattern(r'.*color.*')
def mock_color(field: str, ctx: dict) -> str:
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F0E68C", "#FF69B4", "#00CED1"]
    return random.choice(colors)

@pattern(r'.*role.*|.*permission.*|.*scope.*')
def mock_role(field: str, ctx: dict) -> list:
    return random.sample(["admin", "editor", "viewer", "member", "owner", "moderator"], k=random.randint(1, 3))

@pattern(r'.*tag.*|.*label.*|.*category.*')
def mock_tags(field: str, ctx: dict) -> list:
    return random.sample(["技术", "产品", "设计", "运营", "前端", "后端", "AI", "数据分析"], k=random.randint(1, 4))

@pattern(r'.*password.*|.*token.*|.*secret.*|.*key.*')
def mock_secret(field: str, ctx: dict) -> str:
    return uuid.uuid4().hex

# ── Context extraction ────────────────────────────────────────────────

def extract_context(url: str, cookie: str = "", json_data: dict = None) -> dict:
    """Extract contextual clues from URL, cookie, and JSON data."""
    ctx = {"locale": "zh", "domain": random.choice(DOMAINS)}

    if url:
        parsed = urlparse(url)
        ctx["base_url"] = f"{parsed.scheme}://{parsed.netloc}"
        path = parsed.path.lower()

        # Infer locale from URL
        if any(kw in path for kw in ["/en", "/us", "/uk", "/eu"]):
            ctx["locale"] = "en"

        # Infer domain from path
        if any(kw in path for kw in ["user", "member", "profile", "account"]):
            ctx["domain"] = "users.example.com"
        elif any(kw in path for kw in ["order", "purchase", "cart"]):
            ctx["domain"] = "orders.example.com"
        elif any(kw in path for kw in ["product", "item", "goods"]):
            ctx["domain"] = "products.example.com"
        elif any(kw in path for kw in ["payment", "bill", "invoice"]):
            ctx["domain"] = "payments.example.com"

    if cookie:
        # Parse cookie for tenant/user info
        for part in cookie.split(";"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                k, v = k.strip().lower(), v.strip()
                if k in ("tenant", "org", "company"):
                    ctx["tenant"] = v
                elif k in ("user_id", "uid", "id"):
                    ctx["id"] = v
                elif k in ("locale", "lang", "language"):
                    ctx["locale"] = "en" if v.lower() in ("en", "en-us", "en-gb") else "zh"

    if json_data and isinstance(json_data, dict):
        if "id" in json_data:
            ctx["id"] = json_data["id"]

    return ctx


# ── Empty object templates ────────────────────────────────────────────

EMPTY_OBJECT_TEMPLATES = {
    "address": {"street": "", "city": "", "state": "", "zip_code": "", "country": "中国"},
    "user": {"id": "", "name": "", "email": ""},
    "profile": {"username": "", "bio": "", "avatar": ""},
    "location": {"latitude": 0.0, "longitude": 0.0},
    "meta": {"page": 1, "per_page": 20, "total": 0},
    "config": {"enabled": True, "theme": "default"},
    "shipping": {"method": "standard", "carrier": "顺丰", "tracking_number": ""},
    "billing": {"method": "credit_card", "last4": "4242"},
    "contact": {"phone": "", "email": ""},
    "company": {"name": "", "industry": "", "size": ""},
}

def get_empty_object_template(field: str) -> dict | None:
    """Return a template for empty objects based on field name."""
    field_lower = field.lower()
    for key, template in EMPTY_OBJECT_TEMPLATES.items():
        if key in field_lower:
            return dict(template)
    return None

# ── Core generation logic ────────────────────────────────────────────

def generate_for_field(field: str, ctx: dict, depth: int = 0) -> Any:
    """Generate a mock value for a given field name using registered patterns."""
    if depth > 3:
        return None

    for pat, fn in FIELD_PATTERNS:
        if pat.match(field):
            return fn(field, ctx)

    # Fallback: return field name as placeholder
    return f"<{field}>"


def is_empty(value: Any) -> bool:
    """Check if a value is empty (null, empty string, empty array, empty object)."""
    return value is None or value == "" or value == [] or value == {}


def fill_json(data: Any, ctx: dict, depth: int = 0) -> dict:
    """Recursively fill missing/null/empty fields in JSON data."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            # Handle lists separately (including empty) so they stay as lists
            if isinstance(value, list):
                if len(value) == 0:
                    # Empty array — generate 1-3 items
                    count = random.randint(1, 3)
                    # Try to infer item schema from field name
                    item = generate_for_field(key, ctx, depth)
                    if isinstance(item, list):
                        # Pattern already returns a complete list (e.g., roles, tags) — use directly
                        result[key] = item
                    elif isinstance(item, dict):
                        result[key] = [fill_json(item, ctx, depth + 1) for _ in range(count)]
                    else:
                        # Try singular form, then generate a dict item for common array fields
                        singular = key.rstrip("s")
                        singular_item = generate_for_field(singular, ctx, depth)
                        if isinstance(singular_item, dict):
                            result[key] = [fill_json(singular_item, ctx, depth + 1) for _ in range(count)]
                        else:
                            # Default: generate simple dict items for unknown array fields
                            result[key] = [{"id": str(uuid.uuid4())[:8], "name": f"{singular}_{i+1}"} for i in range(count)]
                else:
                    result[key] = [fill_json(v, ctx, depth + 1) if isinstance(v, (dict, list)) else v for v in value]
            elif is_empty(value):
                # Handle empty objects with templates
                if value == {}:
                    template = get_empty_object_template(key)
                    if template:
                        result[key] = fill_json(template, ctx, depth + 1)
                        continue
                result[key] = generate_for_field(key, ctx, depth)
                # If the generated value should be a nested structure, recurse
                if isinstance(result[key], dict):
                    result[key] = fill_json(result[key], ctx, depth + 1)
            elif isinstance(value, dict):
                result[key] = fill_json(value, ctx, depth + 1)
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        return [fill_json(item, ctx, depth + 1) if isinstance(item, (dict, list)) else item for item in data]
    return data


def detect_issues(original: dict, filled: dict, path: str = "") -> list[dict]:
    """Detect what issues were found and fixed."""
    issues = []

    if isinstance(original, dict) and isinstance(filled, dict):
        # Check for missing fields (in filled but not original)
        for key in filled:
            if key not in original:
                issues.append({
                    "field": f"{path}{key}" if not path else f"{path}.{key}",
                    "issue": "missing",
                    "original": None,
                    "generated": filled[key],
                })

        for key in original:
            current_path = f"{path}.{key}" if path else key
            orig_val = original[key]
            fill_val = filled.get(key)

            if orig_val is None:
                issues.append({"field": current_path, "issue": "null", "original": None, "generated": fill_val})
            elif orig_val == "" and fill_val != "":
                issues.append({"field": current_path, "issue": "empty_string", "original": "(empty)", "generated": fill_val})
            elif orig_val == [] and fill_val != []:
                issues.append({"field": current_path, "issue": "empty_array", "original": "[]", "generated": f"[{len(fill_val)} items]"})
            elif orig_val == {} and fill_val != {}:
                issues.append({"field": current_path, "issue": "empty_object", "original": "{}", "generated": "{...}"})
            elif isinstance(orig_val, dict) and isinstance(fill_val, dict):
                issues.extend(detect_issues(orig_val, fill_val, current_path))
            elif isinstance(orig_val, list) and isinstance(fill_val, list):
                for i, (o, f) in enumerate(zip(orig_val, fill_val)):
                    if isinstance(o, dict) and isinstance(f, dict):
                        issues.extend(detect_issues(o, f, f"{current_path}[{i}]"))

    return issues


# ── CLI entry point ──────────────────────────────────────────────────

def main():
    """CLI: python generate_mock.py --url URL --json JSON --cookie COOKIE"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate mock API response data")
    parser.add_argument("--url", required=True, help="API endpoint URL")
    parser.add_argument("--json", required=True, help="JSON sample (string or file path)")
    parser.add_argument("--cookie", default="", help="Cookie string")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty-print JSON output")
    args = parser.parse_args()

    # Parse JSON input
    json_str = args.json
    if json_str.endswith(".json"):
        with open(json_str) as f:
            json_str = f.read()

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    ctx = extract_context(args.url, args.cookie, data)
    filled = fill_json(data, ctx)
    issues = detect_issues(data, filled)

    # Output
    output = {
        "url": args.url,
        "issues_found": len(issues),
        "issues": issues,
        "mock_data": filled,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
