# data-profiler-lite

CSV 数据画像小工具。类型推断、缺失率、唯一值、数值分布、top 频次。零第三方依赖。

## 功能

- 每列自动推断 number / string 类型；
- 缺失数与缺失率；
- 唯一值数；
- 数值列 min/max/mean；
- top 频次前 3。

## 快速开始

```bash
python3 cli.py data.csv
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，全部本地统计。

## 目录结构

```
data-profiler-lite/
├── profiler.py   # 类型推断、缺失率、唯一值、分布、top
├── cli.py
├── tests/test_profiler.py
├── README.md / LICENSE / .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
