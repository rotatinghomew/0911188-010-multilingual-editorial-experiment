# 多语种推送表现概览

多语种推送活动、匿名受众组和推送事件。当前总览只按文案版本汇总打开次数。

样例数据均为本地合成记录，不对应真实个人、媒体、机构或交易。项目使用 Python 3.11.14 标准库，数据随项目保存，不访问外部服务。

## 使用

在项目根目录运行 `python3 -m app summary` 查看按当前基础口径生成的 JSON 总览。

## 验证

运行 `python3 -m unittest discover -s tests -v` 和 `python3 -m compileall -q app tests`。

## 结构

`data/data.json` 保存领域记录与基础汇总口径；`app/storage.py` 读取并检查数据形状；`app/analysis.py` 计算基础分组统计；`app/service.py` 组合数据读取和统计；`tests/` 验证产品入口及无效数据处理。

## 工作台

`python3 -m app enrollment` 查看当前有效分组；`metrics` 按实际发出的版本汇总停止时间之前的曝光和打开。`decision` 在达到最低曝光数后比较打开率；`broadcast` 归档推广通知，加试验号可回读。

分组是按 `unit` 随机分配时登记的版本，不保证实际收到的 `arm` 相同。`active` 是当前使用状态，`withdrawals` 保留时间证据；时间使用 UTC。`look_plan` 保存事先约定的计划结束、必查语种和最大允许触达下降百分点，不参与当前按实际投放版本比较的逻辑。

操作数据在 `data/workbench.json`。工作台涉及的领域代码：`enrollment` 核登记分组及纳入名单, `measurement` 汇总实际曝光与打开, `editor` 根据投放数字作推广决定。已有总览仍使用 `data/data.json`。
