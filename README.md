# mycoid / rayoid — 本地离线站点

Framer 站点 `https://witty-goal-587605.framer.app/` 的完整本地镜像，可完全离线运行。

## 启动

双击 `start.bat`，或在此目录运行：

```
python serve.py 8848
```

然后浏览器打开 **http://127.0.0.1:8848/**

> 必须用这个 `serve.py` 启动，不能直接双击 HTML 文件，也不能用普通的 `python -m http.server`。
> 原因：Framer 的 CMS（`/docs` 文档列表）用一种自定义的「字节范围」协议加载数据，
> `serve.py` 专门处理了这个协议；普通静态服务器会导致文档页空白。

## 包含内容

- 8 个页面：首页、`/tracks`、`/docs` 文档列表 + 5 篇文档详情
- 全部资源本地化：JS 模块、CSS、图片、字体（Inter / Fragment Mono / Fontshare）
- 首页 RAYOID logo 的**动态抖动（dithering）着色器动画**正常运行
- 已移除 Framer 编辑器脚本和遥测（`events.framer.com`），不再向外部发任何请求

## 目录结构

```
site/
├── index.html                 首页
├── tracks/index.html
├── docs/index.html            文档列表（CMS）
├── docs/<slug>/index.html     5 篇文档
└── _assets/                   所有本地化资源
    ├── framerusercontent.com/ JS 模块 / 图片 / 字体 / CMS 数据块
    └── fonts.gstatic.com/     Google 字体
serve.py                       支持 CMS range 协议的本地服务器
start.bat                      一键启动
```

## 抓取/修复脚本（记录用途，正常运行无需再跑）

- `scrape.py` — 抓取页面与资源、改写为本地路径、剥离遥测
- `fetch_modules.py` — 递归补齐 JS 之间相对引用的模块
- `fix_assets.py` — 把 JS/CSS 里内嵌的字体等 URL 本地化
- `fix_cms.py` — 下载 CMS 数据块并修正 `new URL()` 基址
- `verify_refs.py` — 校验所有本地资源引用都能命中文件
