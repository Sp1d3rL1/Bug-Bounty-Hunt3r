---
id: clk-mobile-android-ios
title: Mobile Android & iOS
owasp_anchor: [MASVS-AUTH, MASVS-NETWORK, MASVS-CRYPTO, MASVS-STORAGE, MASTG]
cwe: [CWE-925, CWE-296, CWE-200]
severity_typical: P2-P3
playbook: playbooks/mobile_android_ios.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# Mobile Android & iOS Checklist

> 双语 / Bilingual: Android Intent / Deep Link / WebView / Pinning / Storage；iOS URL Scheme / Universal Link / Keychain / Pinning。MASVS + MASTG 对齐。
> 用法：Recon 拆 APK / IPA → 列 attack surface（exported / scheme / pinning）→ 跑 Frida 动态回归。
> Authorization-only：测自有设备 build；不上传他人 token；root / jailbreak 在私有 lab 设备做。

---

## 1. Recon & Static Surface

- [ ] APK：`apktool d app.apk` / `jadx-gui app.apk` 看 manifest + smali / java
- [ ] IPA：`unzip` → `Payload/<App>.app/Info.plist` + `class-dump` / `Hopper` / `Ghidra`
- [ ] minSdk / targetSdk / `MinimumOSVersion`；hardcoded secret（API key / Firebase / S3 / Stripe）
- [ ] Android：`network_security_config.xml`、`provider_paths.xml`
- [ ] iOS Info.plist：`NSAppTransportSecurity` / `CFBundleURLTypes` / `applinks` / `LSApplicationQueriesSchemes`
- [ ] 第三方 SDK；混淆（ProGuard / R8 / Hermes）

## 2. Android: Exported Components / Intent

- [ ] `<activity/service/receiver/provider exported="true">` 列出
- [ ] targetSdk ≥ 31 时 exported 必须显式声明，旧 app 默认 exported
- [ ] `intent-filter` 含 `BROWSABLE` + `DEFAULT` → 浏览器可直接 fire
- [ ] `getIntent().getStringExtra(...)` 未校验拼到 URL / SQL / 文件路径
- [ ] `PendingIntent` 用 `FLAG_MUTABLE`；隐式 Intent 携 sensitive extras
- [ ] `setResult` 把 token 经 `onActivityResult` 回传给恶意 caller
- [ ] ContentProvider `grantUriPermissions` + `pathPermission` 错配 → 越权 `content://`
- [ ] FileProvider `provider_paths.xml` 暴露 `/data/data/<pkg>/`
- [ ] Task hijacking：`taskAffinity` 共享 → StrandHogg；WebView `intent://` `parseUri` 注入

## 3. Android: Deep Link / App Link / WebView

- [ ] `<data scheme="myapp" host="..."/>` 是否限制 host
- [ ] App Link `autoVerify="true"` → `/.well-known/assetlinks.json` 内容正确
- [ ] 自定义 scheme 重叠（另一恶意 app 同 scheme）
- [ ] deep link 参数直接走登录 / 重置密码 / 支付
- [ ] WebView `JavaScriptEnabled` + `addJavascriptInterface` → JS bridge RCE [example: CVE-2012-XXXX 类]
- [ ] `setAllowFileAccess` / `AllowFileAccessFromFileURLs` / `UniversalAccessFromFileURLs`
- [ ] `shouldOverrideUrlLoading` 缺校验 → open redirect；`onReceivedSslError.proceed()`；WebView cookie/localStorage 与 native 共享

## 4. Android: SSL Pinning + Storage / Crypto

- [ ] `network_security_config.xml` 是否 `<pin-set>`；OkHttp `CertificatePinner` / TrustKit
- [ ] release `cleartextTrafficPermitted="false"`；`<certificates src="user"/>` → MitM 容易
- [ ] WebView 是否独立 pin（默认不 pin）
- [ ] SharedPreferences / SQLite 明文（应 EncryptedSharedPreferences / SQLCipher）
- [ ] external storage 写敏感；`allowBackup="true"` → `adb backup`
- [ ] Keystore：`setUserAuthenticationRequired(true)` / StrongBox / TEE
- [ ] 弱算法：DES / RC4 / MD5 / ECB / 静态 IV / 硬编码 key；root 检测可被 Magisk / Frida 绕

## 5. iOS: URL Scheme / Universal Link / WebView

- [ ] `Info.plist` `CFBundleURLSchemes` 列出
- [ ] `application(_:open:options:)` 入参做 host / path 校验
- [ ] scheme 抢注（iOS 无强制唯一）；Universal Link `apple-app-site-association` 托管 `/.well-known/`
- [ ] 冷启动 deep link 是否绕过登录态
- [ ] `SFSafariViewController` 与 `WKWebView` cookie 隔离差异
- [ ] x-callback-url：`?x-success=callback://...` 跨 app 凭据外送
- [ ] `WKUserContentController.addScriptMessageHandler` JS bridge 过滤；deprecated `UIWebView`
- [ ] `allowsArbitraryLoads = YES`；`evaluateJavaScript` 拼接用户输入
- [ ] WebKit JIT exploit [example: CVE-2024-XXXX 类] minimum iOS

## 6. iOS: Keychain / Storage / Pinning

- [ ] Keychain `kSecAttrAccessible`：`WhenUnlockedThisDeviceOnly` vs `Always`（备份可读）
- [ ] `kSecAttrAccessGroup` 含他 app；iCloud Keychain 同步敏感
- [ ] `NSUserDefaults` / Core Data / SQLite 明文；`NSFileProtectionComplete` vs `None`
- [ ] CommonCrypto 弱算法；ATS 例外 `NSAllowsArbitraryLoads`
- [ ] TrustKit / Alamofire / 自实现 `urlSession(_:didReceive:)` pinning
- [ ] 主域 pin 但 WebView 子域不 pin；objection / Frida 绕过路径

## 7. 自动化辅助

```bash
# Android 静态
apktool d app.apk -o out/ ; jadx-gui app.apk
aapt dump xmltree app.apk AndroidManifest.xml | /usr/bin/grep -E 'activity|service|provider|exported'

# drozer
adb forward tcp:31415 tcp:31415 && drozer console connect
# > run app.package.attacksurface com.target.app
# > run scanner.provider.finduris -a com.target.app

# Frida + objection (pin/root bypass)
objection -g com.target.app explore
# https://codeshare.frida.re/@pcipolloni/universal-android-ssl-pinning-bypass-with-frida/
# https://github.com/httptoolkit/frida-interception-and-unpinning

# iOS
class-dump -H <App.app/App> -o headers/
frida-trace -U -f <bundle> -m '-[NSURLSession *]'
xcrun simctl openurl booted https://app.example.com/path

# AASA / assetlinks / intent / MobSF / qark / Nuclei
curl -sL https://app.example.com/.well-known/apple-app-site-association | jq .
curl -sL https://app.example.com/.well-known/assetlinks.json | jq .
adb shell am start -a android.intent.action.VIEW -d "myapp://victim/?next=//evil"
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf
qark --apk app.apk
nuclei -tags firebase,exposed-tokens,mobile -u https://api.target.com
# CA system store: https://github.com/NVISOsecurity/MagiskTrustUserCerts
```

```python
# Android intent extras fuzz
import subprocess
PKG = "com.target.app/.LoginActivity"
P = ["javascript:alert(1)","file:///etc/hosts","../../etc/passwd",
     "myapp://x?next=//evil","%00","${jndi:ldap://x}","<script>"]
for p in P: subprocess.run(["adb","shell","am","start","-n",PKG,"--es","next",p])
```

## 8. Reporting Angle

* **Title**：`<platform> <component> <flaw> allows <attacker> to <impact>`（例：`Android exported LoginActivity accepts arbitrary deep link host, allowing token theft via OAuth callback redirect`）
* **CVSS 3.1 上下界**：
  * 远程 deep link → 账号接管：8.0-9.0 / VRT P1
  * WebView JS bridge → in-app RCE：8.0-9.0 / VRT P2
  * 本地恶意 app + IPC token 窃取：6.5-8.0 / VRT P2
  * Keychain / Keystore 配错（备份可读）：5.5-7.0 / VRT P3
  * SSL pinning 缺失：5.5-6.5 / VRT P3
  * Hardcoded secret：4.0-7.5 / VRT P3-P4
* **CWE 推荐**：CWE-295/296（pinning）、CWE-327/328（弱加密）、CWE-312/922/925（存储）、CWE-926/927（exported）、CWE-502（intent extras）、CWE-200
* **PoC 必须**：设备 / OS / app 版本；自有账号；adb/xcrun + 截图；token 脱敏；pinning 绕过附 Frida script；明确 "本地 vs 远程" 威胁模型
* **Suggested Fix**（≥ 2 条）：
  * Android：exported 显式声明 + signature-level permission；deep link 校验 host + 二次确认
  * Android：WebView 关 `allowFileAccess*`；untrusted 内容禁 `addJavascriptInterface`；`network_security_config.xml` 强制 pin + 关 user CA + 禁 cleartext
  * Android：EncryptedSharedPreferences + Keystore（StrongBox）+ 禁 `allowBackup`
  * iOS：Keychain `WhenUnlockedThisDeviceOnly`；Universal Link 仅信 AASA paths；强制 ATS；WKWebView 关 file URL；JS bridge schema 校验
  * 通用：根/越狱多点检测 + 后端风控；防 OTA 回滚

## 9. 已迁移技法（来自 KB）

- [[techniques/android_exported_intent_takeover|Exported Activity 接管]]
- [[techniques/android_deeplink_oauth_steal|Deep Link OAuth 劫持]]
- [[techniques/android_webview_jsbridge_rce|WebView JS Bridge RCE]]
- [[techniques/android_ssl_pinning_bypass_frida|Frida 绕 SSL pinning]]
- [[techniques/ios_url_scheme_hijack|iOS URL Scheme 抢注]]
- [[techniques/ios_universal_link_misconfig|Universal Link AASA 错配]]
- [[techniques/ios_keychain_misconfig|Keychain 备份可读]]
