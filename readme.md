### 删除所有.pyc文件命令
```
find 路径 -type f -name  "*.pyc"  | xargs -i -t rm -f {}
```

### 结束进程
```
lsof -i:8001 |sed '1d'| awk '{print $2}' | xargs kill -9
```







