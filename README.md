# 作业目录说明

## 目录结构

```
homework/
├── 原件/                          ← 老师发的原始压缩包，不删不改
│   ├── 快速傅里叶变换与多项式乘法.zip
│   ├── 最近点对.zip
│   ├── dfs-scc.zip
│   └── shortest-paths.zip
├── 答案/                          ← 解压后的答题文件（已填好）
│   ├── 快速傅里叶变换与多项式乘法/
│   │   ├── fft.ipynb
│   │   ├── requirements.txt
│   │   └── .OTTER_LOG
│   ├── 最近点对/
│   │   ├── closest-pair.ipynb
│   │   ├── requirements.txt
│   │   └── .OTTER_LOG
│   ├── dfs-scc/
│   │   ├── dfs-scc.ipynb
│   │   ├── generated_testcases.pkl  ← 评分用的测试数据，不能删
│   │   ├── requirements.txt
│   │   └── .OTTER_LOG
│   └── shortest-paths/
│       ├── shortest-paths.ipynb
│       ├── requirements.txt
│       └── .OTTER_LOG
├── 互评/                          ← 互评收到的他人提交（含解压副本）
├── 交互算法/                      ← 单文件交互式学习页，浏览器直接打开
│   ├── divide-and-conquer.html    ← 分治
│   ├── bellman-ford.html          ← Bellman-Ford / 负权与负环
│   ├── greedy.html                ← 贪心 / 区间调度与 Huffman
│   └── graph-traversal.html       ← BFS / DFS / 拓扑排序 / SCC
├── submission/                    ← 交这里的压缩包
│   ├── fft_2026_10_12T15_47_38_727943.zip              ← otter 官方导出
│   ├── closest-pair_2026_10_12T15_48_56_153532.zip     ← otter 官方导出
│   ├── dfs-scc_2026_10_26T09_04_10_654028.zip          ← otter 官方导出
│   ├── shortest-paths_2026_10_26T09_04_21_523496.zip   ← otter 官方导出
│   └── 备用_手工打包/                                   ← 早期手工备用包
├── .venv38/                       ← Python 3.8 环境（很大，勿手动改）
└── tools/                         ← 辅助脚本，不属于作业内容，不用提交
    ├── otter_export.py            用 3.8 环境跑官方导出，生成提交 zip（通用）
    ├── run_otter_tests.py         本地复现 notebook 里嵌的评分测试（通用）
    ├── fill_solutions.py          10-12 作业填代码的记录（幂等）
    ├── fill_solutions_dfs_sp.py   10-26 DFS/SCC 与最短路填代码的记录（幂等）
    └── reorganize.py              整理目录用的一次性脚本
```

作业文件夹名 = 老师给的压缩包名，**答题文件就是 `答案/该文件夹/` 里的 `.ipynb`**。

## 交互算法页面

`交互算法/` 下是四份自包含的单文件教程，无需安装依赖，直接用浏览器打开即可：

| 页面 | 内容 |
|---|---|
| `divide-and-conquer.html` | 分治思想、归并排序、最大子数组、棋盘覆盖、主定理 |
| `bellman-ford.html` | 单边松弛实验、逐轮松弛演示、可达/不可达负环、正确性直觉、与 Dijkstra 对比 |
| `greedy.html` | 区间调度策略对比、Huffman 合并、找零与 0-1 背包反例、交换论证 |
| `graph-traversal.html` | BFS / DFS / 拓扑排序 / Kosaraju SCC 的逐步演示、队列/栈/时间戳面板 |

## Python 环境（不装 Anaconda）

本机原来只有 Python 3.14，装不了这套作业要的依赖（`requirements.txt` 锁了
`ipython<8.19`，3.14 上无解）。所以另装了 **Python 3.8.10**，并建了独立虚拟环境：

| 项目 | 值 |
|---|---|
| 解释器 | `C:\Users\Shero_Wang\AppData\Local\Programs\Python\Python38\python.exe` |
| 虚拟环境 | `homework\.venv38`（已 gitignore，不提交） |
| 关键包 | otter-grader 4.4.1、ipython 8.12.3、numpy 1.24.4、scipy 1.10.1、matplotlib 3.7.5、networkx 3.1、ipykernel 6.29.5 |
| 内核 | venv **内部**自带 `python3` kernelspec（`.venv38\share\jupyter\kernels\python3`），没有污染全局 Jupyter 配置 |

**切换 Python 版本**：Windows 的 `py` 启动器现在同时认得两个版本——
`py -3.14` 和 `py -3.8`；具体到本项目，直接用 `.venv38\Scripts\python.exe` 即可。

> ⚠️ 这台机器上 **pypi.org / files.pythonhosted.org 被限速到 5~30 KB/s**（应该是
> Pulse Secure 那类企业安全组件拦的），但 `mirrors.aliyun.com` 只有 1.35s 延迟。
> 所以装包**务必加镜像参数**：
> ```
> .venv38\Scripts\python.exe -m pip install --only-binary=:all: \
>   -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com <包名>
> ```
> `--only-binary=:all:` 也很关键：不加的话 pip 会去构建老源码包、疯狂回溯，十分钟都装不完。

## 生成官方提交包

`tools/otter_export.py` 会做 notebook 最后一格 `grader.export(...)` 做的事：
跑一遍所有 `grader.check`、然后生成官方提交 zip。

```bash
cd C:/Users/Shero_Wang/Desktop/homework
.venv38/Scripts/python.exe tools/otter_export.py "答案/快速傅里叶变换与多项式乘法/fft.ipynb"
.venv38/Scripts/python.exe tools/otter_export.py "答案/最近点对/closest-pair.ipynb"
.venv38/Scripts/python.exe tools/otter_export.py "答案/dfs-scc/dfs-scc.ipynb"
.venv38/Scripts/python.exe tools/otter_export.py "答案/shortest-paths/shortest-paths.ipynb"
```

脚本会自动切到该作业目录、并把 pip 指向阿里云镜像（notebook 前几格要跑
`pip install -r requirements.txt`，不换镜像会卡在 pypi.org 上导致执行失败）。
生成的 zip 名为 otter 自己的格式：`<notebook名>_<时间戳>.zip`，出现在作业文件夹里，
再手动挪进 `submission/` 即可。

## 本地验证（不装 otter 也能跑）

这些 notebook 的评分测试是**明文嵌在 `metadata.otter.tests` 里的**：

```bash
.venv38/Scripts/python.exe tools/run_otter_tests.py --list "答案/dfs-scc/dfs-scc.ipynb"   # 有哪些测试、多少分
.venv38/Scripts/python.exe tools/run_otter_tests.py --dump "答案/shortest-paths/shortest-paths.ipynb"  # 打印测试源码 = 评分标准
.venv38/Scripts/python.exe tools/run_otter_tests.py "答案/dfs-scc/dfs-scc.ipynb"          # 全跑，退出码 0 = 全过
```

当前状态（2026-10-26，otter 官方导出结果）：

| 作业 | 测试 | 结果 |
|---|---|---|
| 快速傅里叶变换与多项式乘法 | q1.1 / q1.2 / q1.3 / q1.4 | 4/4 通过 |
| 最近点对 | q1 / q2 / q6 | 3/3 通过 |
| 深度优先搜索与强连通分量 | q1.1 / q1.2 / q2.1 / q2.2 | 4/4 通过 |
| Dijkstra 与 Bellman-Ford | q1 / q2 | 2/2 通过 |

## 在 VS Code 里打开

1. 用 VS Code **打开某个作业文件夹**（不要打开整个 `homework`，否则内核工作目录
   不是 notebook 所在目录，`!pip install -r requirements.txt` 会找不到文件）。
2. 选内核：**`homework\.venv38\Scripts\python.exe`**（Python 3.8.10）。
3. **不要改 notebook 文件名**（里面写死了 `otter.Notebook("xxx.ipynb")`）。
4. Run All。最后一格会在同目录生成官方提交 zip。
5. FFT 那本「运行时间比较」单元格会跑到 n=10⁴ 的朴素 O(n²) 乘法，约 8 秒，属正常；
   Dijkstra 那本的测试会跑满 50 张大图，约 30 秒，也属正常。

## 以后加新作业

1. 新压缩包放 `原件/`（原包不删不改），解压到**`答案/同名文件夹`**，填好 `.ipynb`；
   若压缩包自带测试数据（如 `generated_testcases.pkl`），一并解压，不能漏。
2. 本地验证：`.venv38/Scripts/python.exe tools/run_otter_tests.py "答案/新作业文件夹/xxx.ipynb"`
3. 生成官方包：`.venv38/Scripts/python.exe tools/otter_export.py "答案/新作业文件夹/xxx.ipynb"`
   （依赖一般和这次一样，`.venv38` 可直接复用；若 `requirements.txt` 有新包，用上面的镜像命令补装）
4. 生成的 `*_<时间戳>.zip` 挪进 `submission/`。
