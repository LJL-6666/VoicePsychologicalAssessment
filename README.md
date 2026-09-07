# 语音端到端情绪系统

端到端的语音情绪识别与心理评估报告生成：输入一个 `recordId`，索引该用户音频目录下的全部音频
（排除预热标签的题目），输出 8 个情绪得分与 3 维度量表得分，并生成 HTML 心理评估报告与 JSON 结果。

---

## 关于示例数据（必读）

`dataset/10001.txt`、`dataset/10002.txt`、`api_data/*.txt` 与 `data_generator.py` 中的样例记录
**均为合成数据，不对应任何真实个人**：

| 字段 | 说明 |
|---|---|
| `recordId` | `10001` / `10002`，虚构编号 |
| `personInfo` | 出生日期、年龄、测试时间均为虚构值；`工种`（`普通职工`）与 `行业` 是通用取值 |
| `fileList[].file_address` | 指向 `example.invalid`——保留域名，不可解析，仅用于展示 URL 结构 |
| 量表得分 | 保留真实的量表结构（PHQ-9 / GAD-7 / GHQ-12 / CPSS / MBI-GS / Mini-IPIP / PSSS / MSQ / PERMA）与分数区间定义，分数本身为示例值 |

跑通完整流程需要自备真实音频与测评数据。**接入真实数据时请注意：**

- 测评结果属健康信息、音频属生物识别信息，在《个人信息保护法》下均为**敏感个人信息**，处理需取得单独同意；
- 不要把含手机号、精确出生日期、真实 `recordId` 或可解析音频直链的记录提交进版本库；
- 生成产物（`api_results/`、`temp_data/`）已在 `.gitignore` 中排除，请勿强制添加。

---

## 快速开始

```bash
# 为单条记录生成完整报告（情绪分析 + 图表 + HTML 报告）
python generate_complete_report.py --json_file dataset/10001.txt

# 或起 API 服务
python api_server.py
python test_api.py
```

脚本使用相对路径，请在仓库根目录执行，勿改动目录结构。

### 可选环境变量

`user_id` 模式与报告中间产物目录的默认路径原先写死为开发机上的 Windows 绝对路径，现改为可配置：

| 变量 | 用途 | 未设置时 |
|---|---|---|
| `VPA_DATA_ROOT` | 外部数据根目录（`--data_dir` / `--user_report` 的默认值来源） | 回退到仓库内 `data/` |
| `VPA_TEMP_DATA` | 报告中间产物目录（`--temp_data_dir` 的默认值） | 回退到仓库内 `temp_data/` |

两者也可直接用命令行参数覆盖，行为不变。

## 环境依赖

```bash
conda create -n ml python=3.10
conda activate ml

conda install pytorch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 pytorch-cuda=11.8 -c pytorch -c nvidia
python -m pip install mser -U -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```

使用 Emotion2Vec 特征提取方法时，另需安装 `funasr`。

## 注意事项

1. 本项目使用相对路径，确保不要修改目录结构
2. 预测脚本会自动处理路径问题，即使 `config.py` 导入失败也能正常工作
3. 报告 HTML 与中间产物写入 `api_results/` 与 `temp_data/`，均不入库

## 许可证

代码以 MIT 发布，见 [`LICENSE`](LICENSE)。
`models/iic/` 下的 Emotion2Vec 权重与配置来自上游模型，适用其原许可。
