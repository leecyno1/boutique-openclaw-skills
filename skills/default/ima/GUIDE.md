# IMA 使用指南

## 1. 功能定位
- 连接 IMA 笔记、笔记本与知识库，让 OpenClaw/Hermes 能读取和查询个人知识内容。
- 默认档位：标准包默认安装。
- 仓库目录：`skills/default/ima`
- 安装后目录：`~/.openclaw/skills/ima`

## 2. 使用前准备
- IMA 账号或工作区授权。
- 受控配置中的 API Key / Client ID / Base URL；不要在聊天里粘贴真实密钥。

## 3. 配置步骤
1. 优先在官网控制台的 IMA 面板完成授权。
2. 如需手动配置，把密钥写入受控环境文件，例如 `~/.openclaw/env` 或 `~/.openclaw/ima.env`。
3. 推荐变量名：
   ```bash
   IMA_API_KEY=...
   IMA_CLIENT_ID=...
   IMA_BASE_URL=...
   ```
4. 完成后让 Agent 执行只读测试：读取笔记本、最近笔记、知识库列表。

## 4. 推荐提问方式
- 请检查 IMA 是否已授权，并读取我的笔记本列表。
- 请读取 IMA 最近 5 条笔记，只返回标题和更新时间。
- 请查询 IMA 知识库中关于某主题的资料，并列出来源。

## 5. 手动验证
```bash
test -d ~/.openclaw/skills/ima && echo "IMA skill installed"
```

## 6. 安全约束
- 不要在聊天中发送真实 API Key、Client Secret、Cookie 或刷新令牌。
- 排查时只展示“已配置/未配置”，不要输出密钥内容。
