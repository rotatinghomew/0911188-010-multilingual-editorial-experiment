# 多语种推送表现概览

多语种推送活动、匿名受众组和推送事件。当前总览只按文案版本汇总打开次数。

样例数据均为本地合成记录，不对应真实个人、媒体、机构或交易。项目使用 Python 3.12 标准库，数据随项目保存，不访问外部服务。

## 使用

在项目根目录运行 `python3 -m app summary` 查看按当前基础口径生成的 JSON 总览。

## 验证

运行 `python3 -m unittest discover -s tests -v` 和 `python3 -m compileall -q app tests`。

## 结构

`data/data.json` 保存领域记录与基础汇总口径；`app/storage.py` 读取并检查数据形状；`app/analysis.py` 计算基础分组统计；`app/service.py` 组合数据读取和统计；`tests/` 验证产品入口及无效数据处理。
