
# 飞书权限配置检查清单

## 必需权限
- [ ] bitable:app:readonly - 多维表格应用只读权限
- [ ] bitable:app - 多维表格应用权限
- [ ] base:app:read - 基础应用读取权限
- [ ] base:table:read - 基础表格读取权限
- [ ] base:record:retrieve - 基础记录检索权限
- [ ] base:record:create - 基础记录创建权限
- [ ] base:record:update - 基础记录更新权限

## 可选权限
- [ ] base:record:delete - 基础记录删除权限
- [ ] base:field:read - 基础字段读取权限
- [ ] base:field:create - 基础字段创建权限

## 发布步骤
- [ ] 权限申请完成
- [ ] 创建新版本
- [ ] 填写版本信息
- [ ] 申请发布
- [ ] 管理员审核通过
- [ ] 权限测试通过

## 测试命令
```bash
# 测试权限配置
python3 test_feishu_tokens.py

# 测试完整功能
python3 test_feishu_config.py
```
