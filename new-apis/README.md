# API 元数据生成工具

本工具集用于处理从源 JSON 文件生成的阿里云 OpenAPI 元数据。它能解决同一产品存在多个版本API文件的问题，并将它们合并与转换为项目所需的最终格式。

## 工作流程

整个流程由 `generate-metadata.sh` 脚本驱动，分为以下几个主要步骤：

1.  **环境设置**:
    *   脚本首先会使用 `uv sync` 来安装在 `pyproject.toml` 中定义的 Python 依赖（主要是 `natsort`）。
    *   然后，它会激活本地的 Python 虚拟环境 (`.venv`)，以确保脚本在隔离的环境中运行。

2.  **合并多版本 API 文件**:
    *   对于像 `ecd` 这样拥有多个版本文件（例如 `ecd-20200930.apis.json`, `ecd-20201002.apis.json`）的产品，脚本会调用 `merge_apis.py`。
    *   `merge_apis.py` 会将这些文件智能地合并成一个单一的 `apis/<product_name>.apis.json` 文件。
    *   **合并策略**:
        *   **API**: 保留最新版本文件中的 API 定义。
        *   **Endpoints**: 合并所有文件中的端点并去重。
        *   **Info**: 使用最新版本文件中的产品信息。

3.  **转换元数据**:
    *   脚本会遍历一个预定义的产品列表 (`ecd`, `eds-user`, `workorder`)。
    *   对于列表中的每一个产品，它会调用 `convert_api.py` 脚本。
    *   `convert_api.py` 负责读取（合并后的）`apis/<product_name>.apis.json` 文件，并将其转换为 `metadatas/`、`zh-CN/` 和 `en-US/` 目录下所需的最终 JSON 格式。同时，它也会更新相应的 `products.json` 文件。

4.  **环境清理**:
    *   所有操作完成后，脚本会执行 `deactivate` 来退出 Python 虚拟环境。

## 如何使用

要生成所有预定义产品的元数据，只需运行主脚本：

```bash
bash new-apis/generate-metadata.sh
```

## 脚本详解

### `generate-metadata.sh`
这是主执行脚本，它自动化了整个元数据生成流程。

### `merge_apis.py`
*   **功能**: 解决同一产品多个API版本文件的问题。
*   **用法**: `python3 merge_apis.py <product_name>`
*   **逻辑**: 查找 `apis/` 目录下所有匹配 `<product_name>-*.apis.json` 的文件，然后根据上述合并策略将它们合并成 `apis/<product_name>.apis.json`。

### `convert_api.py`
*   **功能**: 将单个产品的 API JSON 文件转换为项目所需的元数据格式。
*   **用法**: `python3 convert_api.py <product_name>`
*   **逻辑**: 读取 `apis/<product_name>.apis.json`，生成对应的目录结构和文件，并更新 `products.json`。

### `pyproject.toml`
定义了本 Python 项目的元数据和依赖项。
*   **依赖**: `natsort` - 用于对版本号进行自然排序，确保 `20201002` 总是在 `20200930` 之前。
