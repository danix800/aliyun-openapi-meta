# API 转换规则：从 ecd.apis.json 到 aliyun-openapi-meta

本文档定义了将 `ecd.apis.json` 中的 API 定义转换为 `aliyun-openapi-meta` 格式的规则。

## 目标目录

转换后的 JSON 文件应存放于 `aliyun-openapi-meta/metadatas/ecd/` 目录下。

## 文件命名

每个生成的文件都以其对应的 API 名称命名，例如 `ActivateOfficeSite.json`。

## 字段转换规则

| 目标字段      | 源字段/逻辑                                                                                                                                                           | 示例                                       |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| `name`        | 直接使用 API 的名称（`apis` 对象中的键）。                                                                                                                            | `ActivateOfficeSite`                       |
| `protocol`    | - 检查源数据中是否存在 `schemes` 或 `protocol` 字段。<br>- 将数组中的所有值转换为大写。<br>- 使用 `|` 符号连接。                                                        | `["http", "https"]` -> `"HTTP|HTTPS"`       |
| `method`      | - 检查源数据中是否存在 `methods` 或 `method` 字段。<br>- 将数组中的所有值转换为大写。<br>- 使用 `|` 符号连接。                                                          | `["get", "post"]` -> `"GET|POST"`          |
| `pathPattern` | - 如果源数据中存在 `pathPattern` 字段，则直接使用其值。<br>- 如果不存在，则默认为空字符串 `""`。                                                                       | `""`                                       |
| `summary`     | 使用 `summary` 字段的值。如果不存在，则默认为空字符串 `""`。                                                                                                         | `"解锁办公网络"`                           |
| `description` | 使用 `description` 字段的值。如果不存在，则默认为空字符串 `""`。                                                                                                     | `"对于基于便捷账号的办公网络..."`          |
| `parameters`  | 这是一个数组，需要遍历源 `parameters` 数组并对每个参数对象进行转换。如果源 `parameters` 不存在或为空，则生成一个空数组 `[]`。 |                                            |

### `parameters` 内部字段转换

| 目标字段   | 源字段/逻辑                                                                                                                            | 示例                               |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `name`     | 直接使用 `name` 字段。                                                                                                                 | `"RegionId"`                       |
| `position` | - 使用 `in` 字段的值。<br>- 将其首字母大写。                                                                                           | `"query"` -> `"Query"`             |
| `type`     | - 使用 `schema.type` 的值。<br>- 将其首字母大写。<br>- **特殊情况**: 如果 `schema.format` 为 `int64`，则类型应为 `Long`。                | `"string"` -> `"String"`<br/>`"integer"` (format: `int64`) -> `"Long"` |
| `required` | 直接使用 `schema.required` 的布尔值。                                                                                                  | `true`                             |
| `description` | 使用 `description` 字段的值。如果不存在，则默认为空字符串 `""`。                                                                                                     | `"地域ID"`          |
