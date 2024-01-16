## 中国电子普通发票识别和统计
## 原理是识别发票中的二维码. 
## 具有提取二维码中金额,进行统计. 合并发票的功能

## 编译命令  pyinstaller .\merge.spec

## 执行一下命令 即可运行

```
.\dist\merge.exe path\to\your\invoice\folder
```

### 2024-01-16 
- fix bug: 第一个文件没有merge进去