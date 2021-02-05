# auto-SSR-update
Linux 系统下 SSR 订阅的自动更新和网站访问测试
对配置文件中所记录的 SSR 订阅信息进行解析，之后更新本地 SSR 配置信息并重启。  
在对所有需要测试的网站访问通过后结束，否在则换至下一个节点再更新配置，如此往复。  
需要环境：Linux, Python3  
使用方法：  

```bash
git clone https://github.com/senjianlu/auto-SSR-update.git --recurse
cd auto-SSR-login
python3 update_ssr.py
```

**没有 SSR 需要先安装**

```bash
mv ssr /usr/local/bin
chmod +x /usr/local/bin/ssr
ssr install
```
