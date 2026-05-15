# 第三环节 Skill 合并分析

## 现有 Skill 盘点

### 1. `dasheng-daily-material`
**优点**
- 已接入主流程，直接写回 `run_manifest.json`
- 能产出 `material-packs.json` 与 `material-workflow-v2-results.json`
- 与第二环节 `phase2`、下一环节 `outline` 的衔接最完整

**问题**
- 早期重点是“跑通第三环节”，对视频可复用性没有单独质量层
- 素材结构虽然可用，但没有把查询审计与质量告警显式纳入主产物

### 2. `material-pack-builder`
**优点**
- 把 Material Pack 的结构讲清楚了：text/image/video/data/gaps/next_step
- 适合作为 schema 与 reference

**问题**
- 只有方法论，没有可执行入口
- 不负责 CDP、Douyin fallback、真实下载与报告落盘

### 3. `reusable-footage-material`
**优点**
- 强化了“非口播、可剪辑、偏资料片”的视频质量目标
- 新增 `quality_summary`
- 新增 `video-search-sources.json` 作为查询与来源审计

**问题**
- 如果单独作为第三环节默认 skill，会与已有主流程入口重复
- 不负责 manifest 链路与 Material Pack 的全流程主入口语义

## 合并原则
1. **默认入口不变**：第三环节仍以 `dasheng-daily-material` 为统一入口
2. **结构保留**：继承 `material-pack-builder` 的 Material Pack 组织方式
3. **质量升级**：吸收 `reusable-footage-material` 的视频质量门槛、拒绝词、query 审计
4. **流程不分叉**：避免同时存在两个“默认可执行第三环节 skill”

## 合并后设计
- `dasheng-daily-material`
  - 默认第三环节 skill
  - 负责 manifest / packs / next step
  - 内部调用统一视频质量执行器
- `material-pack-builder`
  - 降级为 schema / reference skill
- `reusable-footage-material`
  - 保留为独立调优 skill（用于单点视频质量验证、策略试验）

## 合并收益
- 用户只需要记住一个第三环节默认入口
- 主流程结果与质量审计同时具备
- 素材补全从“能下素材”升级到“尽量下可剪素材”
- 后续可以继续加 OCR / 人脸检测等质检，而不改调用入口
