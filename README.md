# doi2toml

## 输入文件格式

在`dois.txt`按照格式逐条记录文献，每个文献占一行：

```
doi|publish|category|summary
```

例如：

```
10.1007/s12144-023-04806-8|11 July, 2023|Emotion|自信程度与可信度的关系
10.1016/j.chb.2023.107875|15 July, 2023|Art|AI生成的艺术也可以传递人类情绪
```

### ！！！注意！！！

- 不能有空行
- 一行中字段分隔符为`|`，分隔符两边不能有空格
- doi不能带有`https://doi.org/`
- 所有字段必须存在，但可以为空，比如`10.1016/j.chb.2023.107875||Art|`

## 运行脚本

建议使用Python虚拟环境（需要通过`pip`安装`virtualenv`）：

```bash
virtualenv venv
```

用`pip`安装依赖：

```bash
pip install -r requirements.txt
```

确保`dois.txt`和脚本在同一个目录下，并符合上面的[标准格式](##输入文件格式)

运行脚本：

```bash
python doi2toml.py
```

运行时会输出信息提示是否转换成功，用了什么样的[方法](##转换方法)

运行结束后输出文件`out.toml`即转换结果，需要手动补全其中缺少的信息

## 转换方法

目前有2种方法：

1. scopus

使用`pybliometrics`包，基本上可以获取所有相关信息，包括abstract、keywords等

2. doi2bib

使用`doi2bib`，无法获取abstract和keywords，其他信息基本可以获取
