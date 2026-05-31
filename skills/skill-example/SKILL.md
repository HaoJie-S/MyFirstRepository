---
name: mock-data-generator
description: 基于 URL、JSON 样本/模式和 Cookie 生成 mock API 响应数据。适用于用户提供 API 端点 URL 和 JSON 数据并希望生成 mock 数据，特别是在处理缺失字段、null 值、空数组/对象或数据完整性问题时。触发条件包括用户提到 mock 数据、假 API 响应、JSON 完整性、字段验证，或提供 URL 和 JSON 并要求生成测试数据。
---

# 模拟数据生成器

通过分析提供的 URL、JSON 样本和 Cookie，生成真实感的 mock API 响应数据。本技能处理缺失字段、null 值、空数组/对象和类型不匹配等数据完整性问题。

## 脚本

本技能捆绑了 `scripts/generate_mock.py`，这是一个用于程序化填充 JSON 数据的 Python 脚本。 当用户通过 CLI 提供结构化输入时使用：

```bash
python scripts/generate_mock.py \
  --url "https://api.example.com/v1/users/123" \
  --json '{"id": 123, "email": null, "roles": []}' \
  --cookie "session=abc; tenant=mycompany"
```

对于对话式输入（用户在聊天中粘贴 URL/JSON/cookie），请改用下面的手工流程。

## 工作流程

### 步骤 1：收集输入

从用户处收集以下三个要素：

1. **API URL** — 需要模拟的接口地址（例如 `https://api.example.com/v1/users`）
2. **JSON 样本** — 用于展示预期结构的响应示例或模式
3. **Cookie** — 用于上下文推断的认证/会话 Cookie（可选，但可帮助推断租户/组织相关数据）

如果缺少任何要素，请在继续前询问用户补充。

### Step 2: Analyze the JSON Structure

Parse the provided JSON and identify:

- **Missing fields** — fields that exist in the schema but are absent in the sample
- **Null values** — fields explicitly set to `null` that should have real data
- **Empty values** — empty strings `""`, empty arrays `[]`, empty objects `{}`
- **Type hints** — infer expected types from field names (e.g., `email` → string email, `created_at` → ISO datetime, `count` → number)
- **Nested structures** — recurse into nested objects and arrays

### Step 3: Infer Field Semantics from URL and Cookie

Use the URL path and cookie to add context:

| URL Pattern | Inferred Domain |
|---|---|
| `/users`, `/members` | User/member data |
| `/orders`, `/purchases` | E-commerce order data |
| `/products`, `/items` | Product catalog data |
| `/analytics`, `/stats` | Metrics/analytics data |
| `/auth`, `/login` | Authentication data |
| `/payments`, `/billing` | Financial data |

Cookie values may contain session IDs, tenant IDs, or user tokens — use these to generate consistent, plausible data (e.g., if cookie contains `tenant=acme`, generate data relevant to "Acme Corp").

### Step 4: Generate Mock Data

Apply these rules for each field type:

#### Missing Fields
Generate realistic values based on the field name:

| Field Name Pattern | Generated Value |
|---|---|
| `*email*` | `"user{random}@example.com"` |
| `*name*`, `*user*` | Realistic name like `"张三"`, `"John Doe"` |
| `*phone*`, `*mobile*` | `"13800138000"` |
| `*date*`, `*time*`, `*at*` | `"2026-01-15T10:30:00Z"` |
| `*id*`, `*_id` | UUID or sequential number |
| `*url*`, `*link*` | `"https://example.com/resource/{id}"` |
| `*avatar*`, `*image*`, `*photo*` | `"https://picsum.photos/200"` |
| `*address*`, `*location*` | `"北京市朝阳区xxx街道"` |
| `*count*`, `*total*`, `*amount*` | Random positive number |
| `*status*` | Contextual: `"active"`, `"pending"`, `"completed"` |
| `*description*`, `*bio*`, `*summary*` | Realistic paragraph |
| `*color*` | `"#FF5733"` |
| `*price*` | `"99.99"` |
| `*title*`, `*subject*` | Realistic title |

#### Null Values
Replace `null` with plausible defaults:
- String fields → realistic non-empty string
- Number fields → `0` or contextually appropriate number
- Boolean fields → `false` (or `true` if field suggests positive state like `*active*`, `*enabled*`)
- Array fields → `[]` with 1-3 sample items
- Object fields → `{}` with required sub-fields populated

#### Empty Values
Fill empty containers with realistic content:
- `""` → meaningful string based on field name
- `[]` → array with 1-5 representative items matching the array's item schema
- `{}` → object with all expected sub-fields populated

### Step 5: Output Format

Return the generated mock data in this structure:

```markdown
## Mock Data for {URL}

**Original issues found:**
- Missing fields: `field1`, `field2`
- Null values: `field3`, `field4`
- Empty values: `field5` (empty string), `field6` (empty array)

**Generated mock data:**

```json
{
  ...
}
```

**Field-by-field change log:**

| Field | Issue | Generated Value |
|---|---|---|
| `email` | null | `"zhangsan@example.com"` |
| `roles` | empty array | `["admin", "editor"]` |
| `bio` | missing | `"Full-stack developer with 5 years..."` |
```
```

## Configuration

If the user specifies custom requirements, respect them:

- **Specific values** — if user says "make the status always 'active'", do that
- **Data count** — if user says "generate 10 items", produce an array of 10
- **Locale** — default to Chinese (中文) data for names/addresses since the user communicates in Chinese; switch to English if the URL/context suggests international data
- **Response language** — skill replies should be written in Chinese unless the user explicitly requests another language
- **Realism level** — default to realistic data; if user wants obviously fake data (e.g., `"test@test.com"`), use placeholder patterns

## Example

**User input:**
```
URL: https://api.example.com/v1/users/123
Cookie: session=abc123; tenant=mycompany
JSON: {"id": 123, "name": "张三", "email": null, "roles": [], "bio": "", "created_at": "2025-01-01T00:00:00Z"}
```

**Output:**
```json
{
  "id": 123,
  "name": "张三",
  "email": "zhangsan@mycompany.com",
  "roles": ["admin", "member"],
  "bio": "高级软件工程师，负责后端架构设计和团队建设",
  "phone": "13800138000",
  "department": "技术研发部",
  "avatar": "https://picsum.photos/200?user=123",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2026-05-28T14:30:00Z",
  "status": "active"
}
```

## 中文说明

`generate_mock.py` 的作用是根据用户提供的 `URL`、`JSON` 样本和可选的 `Cookie`，自动推断字段语义并为缺失字段、`null` 值、空字符串、空数组或空对象生成真实感的 mock 数据。它会分析字段名和 URL 上下文，补全完整的 API 响应结构，并输出生成后的 mock 数据以及发现的问题列表。

`skill-example` 中的 skill 使用方式是：用户提供一个 API `URL`、一个 JSON 结构样本（或示例响应）和可选的 `Cookie`，然后通过该 skill 调用 `scripts/generate_mock.py` 来生成填充后的 mock 数据。该 skill 适合用于测试 API 响应、验证数据完整性、模拟接口返回值，以及快速创建缺失字段的样例数据。
```
