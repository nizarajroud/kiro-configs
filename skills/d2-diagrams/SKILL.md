---
name: d2-diagrams
description: Generate D2 diagrams with sketch mode, themes, and file output. Activates when the user asks to create, generate, or build a D2 diagram, architecture diagram in D2, flowchart, sequence diagram, or any visual in D2 format.
---

## Instructions

Generate D2 diagrams using the `d2-mcp` MCP server for validation, rendering, and file output.

### Workflow (3 steps — always follow this order)

#### Step 1: Write D2 Code
- Write the D2 source code based on the user's request
- Use the `fetch_d2_cheat_sheet` MCP tool if unsure about D2 syntax
- Save the `.d2` source file to AI-GENERATED:
  `/mnt/c/Users/nizar/Documents/AI-GENERATED/<month-year>/<domain>/<subject>/d2/<name>.d2`

#### Step 2: Validate
- Use the `compile-d2` MCP tool to check for syntax errors
- Fix any errors before rendering

#### Step 3: Render + Save to Disk
- Use the `render-d2` MCP tool with `file_path` pointing to the saved .d2 file
- The MCP server automatically saves the SVG next to the .d2 file
- OR use `output_path` parameter to specify where to save
- Always save BOTH the `.d2` source and the rendered SVG output

### File Output Rules (MANDATORY)

Follow the standard AI-GENERATED output rules:
```
/mnt/c/Users/nizar/Documents/AI-GENERATED/<month-year>/<domain>/<subject>/d2/<name>.d2
/mnt/c/Users/nizar/Documents/AI-GENERATED/<month-year>/<domain>/<subject>/svg/<name>.svg
```

Always save BOTH files. NEVER return only inline base64 — always persist to disk.

### Page Size Rules (CRITICAL)

**Default: do NOT pass `page_size` at all.** The MCP defaults to `fit` mode which makes the SVG fill the viewer width perfectly — no zooming, no empty space.

| Situation | page_size value | Result |
|-----------|----------------|--------|
| On-screen viewing (default) | omit / `"fit"` | width=100%, height=auto — perfect display |
| User asks for PDF/print/PowerPoint | `"a4-landscape"` | Fixed 1122×794 for print |
| User asks for specific size | `"WxH"` (e.g. `"1920x1080"`) | Custom fixed dimensions |
| Raw output for debugging | `"none"` | Untouched layout engine output |

**❌ NEVER pass `page_size: "a4-landscape"` unless the user explicitly asks for print/PDF format.**
**✅ ALWAYS omit page_size for normal diagram generation (screen viewing).**

### MCP Tool Usage

The `d2-mcp` server provides 3 tools:
- `compile-d2` — validate syntax (use BEFORE rendering)
- `render-d2` — render to SVG/ASCII + save to file. Parameters:
  - `code` or `file_path` — D2 source
  - `format` — svg, ascii
  - `sketch` — true (default) for hand-drawn, false for clean
  - `theme` — integer theme ID (see table below)
  - `output_path` — where to save the rendered output
- `fetch_d2_cheat_sheet` — D2 syntax reference

### CLI Options Reference

| Option          | Values                              | Default  | Description                      |
|-----------------|-------------------------------------|----------|----------------------------------|
| `--sketch`      | (flag)                              | off      | Hand-drawn look                  |
| `--theme`       | 0-300+ (see themes below)           | 0        | Color theme                      |
| `--layout`      | dagre, elk, tala                    | dagre    | Layout engine                    |
| `--pad`         | integer                             | 10       | Padding in px around diagram     |
| `--animate-interval` | ms                             | 0        | Animation speed for layers       |
| `--font-regular`| path                                | -        | Custom font                      |

### Themes (most useful)

| ID  | Name              | Style              |
|-----|-------------------|--------------------|
| 0   | Neutral Default   | Clean, minimal     |
| 1   | Neutral Grey      | Soft grey           |
| 3   | Flagship Terrastruct | Brand colors    |
| 4   | Cool Classics     | Blue tones          |
| 5   | Mixed Berry Blue  | Purple/blue         |
| 6   | Grape Soda        | Purple (MCP default)|
| 8   | Aubergine         | Dark purple         |
| 100 | Origami           | Warm paper          |
| 101 | Shirley Temple    | Pink/coral          |
| 102 | Earth Tones       | Natural greens      |
| 103 | Everglade         | Forest green        |
| 104 | Buttered Toast    | Warm yellow         |
| 200 | Terminal          | Dark terminal       |
| 201 | Terminal Grayscale| B&W terminal        |
| 300 | Dark Mauve        | Dark mode purple    |
| 301 | Dark Flagship     | Dark mode brand     |

### Output Format Decision

| User request         | Format | Command                                      |
|----------------------|--------|----------------------------------------------|
| "diagram" (default)  | SVG    | `d2 --sketch input.d2 output.svg`            |
| "PNG image"          | PNG    | `d2 --sketch input.d2 output.png`            |
| "ASCII / text"       | ASCII  | Use `renderd2` MCP with format=ascii         |
| "dark mode"          | SVG    | `d2 --sketch --theme 300 input.d2 output.svg`|

### D2 Language Patterns

#### Simple Architecture (left-to-right)
```d2
direction: right

client: Client {shape: person}
api: API Gateway
lambda: Lambda {shape: hexagon}
db: DynamoDB {shape: cylinder}

client -> api -> lambda -> db
```

#### AWS-Style with Icons
```d2
direction: right

vpc: VPC {
  style.stroke-dash: 5
  
  alb: ALB
  ecs: ECS Cluster {
    service: Service
  }
}

users: Users {shape: person}
rds: RDS {shape: cylinder}

users -> vpc.alb -> vpc.ecs.service -> rds
```

#### Sequence Diagram
```d2
shape: sequence_diagram

client: Browser
api: API Gateway  
auth: Cognito
lambda: Lambda

client -> api: POST /login
api -> auth: Validate token
auth -> api: Token valid
api -> lambda: Invoke handler
lambda -> api: 200 OK
api -> client: Response
```

#### Container Nesting (groups)
```d2
aws: AWS Cloud {
  vpc: VPC {
    public: Public Subnet {
      alb: ALB
    }
    private: Private Subnet {
      ecs: ECS
      rds: RDS {shape: cylinder}
    }
  }
}

internet: Internet {shape: cloud}
internet -> aws.vpc.public.alb -> aws.vpc.private.ecs -> aws.vpc.private.rds
```

### Rendering Defaults

Unless the user specifies otherwise:
- **Always use `--sketch`** (hand-drawn look is the primary value of D2 over draw.io)
- **Theme**: 0 (Neutral) unless user requests a specific style
- **Layout**: dagre (good for most diagrams, more compact than elk)
- **Format**: SVG (vector, browser-openable)
- **Labels on arrows**: MAX 3-4 words. Details go in the legend, not on the edge.
- **Page size**: `a4-landscape` when using `renderd2` MCP (pass `page_size` parameter)

### Compact Layout Rules (MANDATORY)

These rules produce readable diagrams that fit on screen without excessive whitespace:

1. **Edge labels = short** — Max 3-4 words on an arrow. Use numbered steps `【1】 Invoke` not `【1】 Invoke Lambda function with JSON payload`
2. **Details in legend** — Technical specs (protocols, ports, encodings) go in a `legend` container at the bottom, referenced by step number
3. **Layout engine = dagre** — Default. More compact than elk. Only use elk if dagre produces overlaps.
4. **Padding = 5** — D2 default. Don't increase it.
5. **Avoid deeply nested labels** — `LiveKit` not `LiveKit Server (SFU — Selective Forwarding Unit)` on the node. Full name goes in the legend.

**Example — Edge label DO vs DON'T:**
```d2
# ❌ BAD — forces huge gaps
user -> sfu: "【3】 RTP (Opus, UDP, DTLS-SRTP encrypted)"

# ✅ GOOD — compact
user -> sfu: "【3】 RTP stream"
```

**Example — Legend for details:**
```d2
legend: Legend {
  near: bottom-center
  style.fill: "#fffff0"
  style.stroke: "#cccccc"
  style.border-radius: 8

  content: |md
    **【1】** Load React frontend (HTTPS)
    **【2】** JWT Token + Room credentials (REST)
    **【3】** RTP audio stream (Opus codec, UDP, DTLS-SRTP encrypted)
    **【4】** Forward to VAD pipeline (internal gRPC)
    **【5】** Synthesized audio response (Opus)
    **【6】** RTP response back to client WebRTC peer
  |
}
```

### Presets

#### Preset: Professional AWS Architecture

**Trigger**: User asks for "professional", "enterprise", "corporate", "standard AWS" style, or any diagram intended for official documentation, client deliverables, or presentations.

**CLI command**: `d2 --theme 0 --layout dagre input.d2 output.svg` (NO `--sketch`)

**Style rules:**

| Aspect                | Value                                                    |
|-----------------------|----------------------------------------------------------|
| Sketch mode           | **OFF** — never use `--sketch`                           |
| Layout                | `dagre` (compact layout — fits A4 better than elk)       |
| Theme                 | `0` (Neutral)                                            |
| Diagram background    | `#ffffff` (pure white)                                   |
| Border-radius         | `0` (sharp corners everywhere)                           |
| Animations            | **NONE** — no `style.animated` (static for PDF/docs)     |
| Font-size services    | `14`                                                     |
| Font-size tier/groups | `16`, bold                                               |
| Font-size step labels | `20` on connections                                      |
| Arrowheads            | `triangle` (default — never fancy)                       |
| Icons                 | Always `unpkg.com/aws-icons@3.3.0`                       |

**AWS Color Palette (MANDATORY for this preset):**

| Usage                    | Hex       | Where to apply                        |
|--------------------------|-----------|---------------------------------------|
| AWS Dark                 | `#232F3E` | Text, default stroke, connection lines |
| AWS Orange               | `#FF9900` | AWS Cloud container stroke only        |
| AWS Blue (links/numbers) | `#017abc` | Step numbers, legend highlights        |
| Region stroke            | `#147eba` | Region container border                |
| VPC Green                | `#248814` | VPC container border                   |
| Security Red             | `#dd3522` | Auth/security flows (stroke-dash: 5)   |
| Sidebar/Legend bg        | `#ebecee` | Legend container fill                  |
| Container bg light       | `#f7f8fa` | AWS Cloud fill                         |
| Region fill              | `#ffffff` | Region container                       |
| Public subnet fill       | `#e9f3e8` | Public-facing services                 |
| Private subnet fill      | `#e6f2f8` | Backend/private services               |

**Container hierarchy (boundaries):**

```d2
aws: AWS Cloud {
  style.stroke: "#FF9900"
  style.stroke-width: 2
  style.fill: "#f7f8fa"

  region: Region (us-east-1) {
    style.stroke: "#147eba"
    style.stroke-width: 2
    style.fill: "#ffffff"

    vpc: VPC {
      style.stroke: "#248814"
      style.stroke-width: 2
      style.fill: "#ffffff"

      public-subnet: Public Subnet {
        style.fill: "#e9f3e8"
        style.stroke: "#248814"
        style.stroke-dash: 3
      }

      private-subnet: Private Subnet {
        style.fill: "#e6f2f8"
        style.stroke: "#147eba"
        style.stroke-dash: 3
      }
    }
  }
}
```

**Connection styles:**

```d2
# Normal data flow
a -> b: "【1】 Label" {
  style.stroke: "#232F3E"
  style.font-size: 20
}

# Auth/security flow
a -> b: "【2】 Validate" {
  style.stroke: "#dd3522"
  style.stroke-dash: 5
  style.font-size: 20
}
```

**Legend:**

```d2
legend: Legend {
  near: bottom-center
  style.fill: "#ebecee"
  style.stroke: "#cccccc"
  style.border-radius: 0

  content: |md
    **【1】** Step description here
  |
}
```

**What changes vs sketch mode:**
- ❌ `--sketch` → removed
- ❌ `style.animated` → removed (static output)
- ❌ Colorful fills (green, pink, yellow) → neutral grey/blue AWS palette
- ❌ `border-radius: 8` → sharp corners (0)
- ✅ `dagre` layout → kept (compact = fits A4 pages)
- ✅ AWS icons → kept
- ✅ 【1】【2】 numbered steps → kept with font-size 20

### File Output Rules

Follow the standard AI-GENERATED output rules:
```
/mnt/c/Users/nizar/Documents/AI-GENERATED/<month-year>/<domain>/<subject>/svg/<name>.svg
/mnt/c/Users/nizar/Documents/AI-GENERATED/<month-year>/<domain>/<subject>/d2/<name>.d2
```

Always save BOTH the `.d2` source file AND the rendered output.

### Embedding SVGs in Markdown (Responsive)

**NEVER** use plain markdown `![alt](path)` for D2 SVGs — they render at native size (often 1600-3000px wide) which is way too big.

**ALWAYS** use clickable HTML with fixed width:

```html
<a href="path/to/diagram.svg">
  <img src="path/to/diagram.svg" width="900" alt="Diagram Title" />
</a>
```

- `width="900"` — renders at readable size in any markdown viewer
- `<a href>` — click opens full-size SVG in browser (zoomable, pannable)
- No `max-width` div — that caused tiny rendering in narrow panels

**Why not `![](path)`:** No size control, renders at native 2000-3500px dimensions.

**Why not `<div max-width>` + `width="100%"`:** In narrow panels (VS Code, GitHub sidebar), shrinks to container width → unreadable and not zoomable.

### When to Use D2 vs Other Tools

| Scenario                                  | Tool           |
|-------------------------------------------|----------------|
| Quick architecture sketch                 | **D2** ✓       |
| AWS diagram with console links            | draw.io        |
| Hand-drawn style flowchart                | **D2** ✓       |
| Sequence diagram                          | **D2** ✓       |
| ERD / database schema                     | **D2** ✓       |
| Arabic/RTL text diagrams                  | rtl-visual-mcp |
| Complex AWS with 10+ services + links     | draw.io        |
| Quick ASCII diagram for terminal/chat     | **D2** (ascii) |

### MCP Tool Usage

The `d2-mcp` server provides 3 tools:
- `compile-d2` — validate syntax (use BEFORE rendering)
- `render-d2` — render to SVG/ASCII + save to file. Parameters:
  - `code` or `file_path` — D2 source
  - `format` — svg, ascii
  - `sketch` — true (default) for hand-drawn, false for clean
  - `theme` — integer theme ID (see table below)
  - `output_path` — where to save the rendered output
- `fetch_d2_cheat_sheet` — D2 syntax reference

**Important**: `render-d2` does NOT write files to disk. Always use the `d2` CLI for file output.

### AWS Icons in D2

D2 supports icons via `style.icon` with any URL. For AWS architecture diagrams, use the **D2 hosted icons** or the **aws-icons CDN**.

#### D2 Hosted Icons (recommended)
Base URL: `https://icons.d2lang.com/aws%2F<Category>%2F<ServiceName>.svg`

| AWS Service        | Icon URL                                                                    |
|--------------------|-----------------------------------------------------------------------------|
| Lambda             | `https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg`                   |
| EC2                | `https://icons.d2lang.com/aws%2FCompute%2FAmazon-EC2.svg`                   |
| S3                 | `https://icons.d2lang.com/aws%2FStorage%2FAmazon-Simple-Storage-Service.svg` |
| DynamoDB           | `https://icons.d2lang.com/aws%2FDatabase%2FAmazon-DynamoDB.svg`             |
| API Gateway        | `https://icons.d2lang.com/aws%2FApp%20Integration%2FAmazon-API-Gateway.svg` |
| CloudFront         | `https://icons.d2lang.com/aws%2FNetworking%20&%20Content%20Delivery%2FAmazon-CloudFront.svg` |
| Route 53           | `https://icons.d2lang.com/aws%2FNetworking%20&%20Content%20Delivery%2FAmazon-Route-53.svg` |
| RDS                | `https://icons.d2lang.com/aws%2FDatabase%2FAmazon-RDS.svg`                  |
| SQS                | `https://icons.d2lang.com/aws%2FApp%20Integration%2FAmazon-Simple-Queue-Service.svg` |
| SNS                | `https://icons.d2lang.com/aws%2FApp%20Integration%2FAmazon-Simple-Notification-Service.svg` |
| ECS                | `https://icons.d2lang.com/aws%2FCompute%2FAmazon-Elastic-Container-Service.svg` |
| EKS                | `https://icons.d2lang.com/aws%2FCompute%2FAmazon-Elastic-Kubernetes-Service.svg` |
| Fargate            | `https://icons.d2lang.com/aws%2FCompute%2FAWS-Fargate.svg`                  |
| CloudWatch         | `https://icons.d2lang.com/aws%2FManagement%20&%20Governance%2FAmazon-CloudWatch.svg` |
| IAM                | `https://icons.d2lang.com/aws%2FSecurity%2C%20Identity%2C%20&%20Compliance%2FAWS-Identity-and-Access-Management.svg` |
| Cognito            | `https://icons.d2lang.com/aws%2FSecurity%2C%20Identity%2C%20&%20Compliance%2FAmazon-Cognito.svg` |
| Step Functions     | `https://icons.d2lang.com/aws%2FApp%20Integration%2FAWS-Step-Functions.svg`  |
| Bedrock            | `https://icons.d2lang.com/aws%2FMachine%20Learning%2FAmazon-Bedrock.svg`    |
| VPC                | `https://icons.d2lang.com/aws%2F_Group%20Icons%2FVirtual-private-cloud-VPC_light-bg.svg` |
| NAT Gateway        | `https://icons.d2lang.com/aws%2FNetworking%20&%20Content%20Delivery%2FAWS-NAT-Gateway.svg` |
| Internet Gateway   | `https://icons.d2lang.com/aws%2FNetworking%20&%20Content%20Delivery%2FAmazon-VPC_Internet-Gateway_light-bg.svg` |

#### Alternative: aws-icons CDN (RECOMMENDED for D2 CLI rendering)
Base URL: `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/<PascalCaseName>.svg`

**CRITICAL**: Names are PascalCase WITHOUT hyphens. Pin version `@3.3.0` (not `@latest` which returns 404 via redirect).

| AWS Service        | Correct URL                                                                          |
|--------------------|--------------------------------------------------------------------------------------|
| Lambda             | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AWSLambda.svg`         |
| API Gateway        | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonAPIGateway.svg`  |
| DynamoDB           | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonDynamoDB.svg`    |
| CloudFront         | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonCloudFront.svg`  |
| Cognito            | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonCognito.svg`     |
| S3                 | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonSimpleStorageService.svg` |
| SQS                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonSimpleQueueService.svg` |
| SNS                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonSimpleNotificationService.svg` |
| Step Functions     | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AWSStepFunctions.svg`  |
| EventBridge        | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonEventBridge.svg` |
| Bedrock            | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonBedrock.svg`     |
| ECS                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonElasticContainerService.svg` |
| EKS                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonElasticKubernetesService.svg` |
| RDS                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonRDS.svg`         |
| CloudWatch         | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonCloudWatch.svg`  |
| Route 53           | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonRoute53.svg`     |
| ELB                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/ElasticLoadBalancing.svg` |
| Fargate            | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AWSFargate.svg`        |
| SageMaker          | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonSageMaker.svg`   |
| EC2                | `https://unpkg.com/aws-icons@3.3.0/icons/architecture-service/AmazonEC2.svg`         |

**Fallback rule**: `icons.d2lang.com` returns 403 for many services (API Gateway, S3, IAM, etc.). ALWAYS use `unpkg.com/aws-icons@3.3.0` as the PRIMARY source for D2 CLI rendering. The D2 CLI bundles icons at compile time and needs a direct 200 response (no redirects).

### Other Icon Sources (beyond AWS)

D2 can use ANY URL as an icon. The hosted library at `icons.d2lang.com` provides 3 categories:

#### 1. `aws/` — AWS Architecture Icons
Pattern: `https://icons.d2lang.com/aws%2F<Category>%2F<ServiceName>.svg`

Categories: Compute, Database, Storage, App Integration, Networking & Content Delivery, Security Identity & Compliance, Machine Learning, Management & Governance, _Group Icons

#### 2. `dev/` — Developer & Technology Icons
Pattern: `https://icons.d2lang.com/dev%2F<name>.svg`

| Icon | URL |
|------|-----|
| React | `https://icons.d2lang.com/dev%2Freact.svg` |
| Python | `https://icons.d2lang.com/dev%2Fpython.svg` |
| Go | `https://icons.d2lang.com/dev%2Fgo.svg` |
| Rust | `https://icons.d2lang.com/dev%2Frust.svg` |
| TypeScript | `https://icons.d2lang.com/dev%2Ftypescript.svg` |
| Java | `https://icons.d2lang.com/dev%2Fjava.svg` |
| Docker | `https://icons.d2lang.com/dev%2Fdocker.svg` |
| PostgreSQL | `https://icons.d2lang.com/dev%2Fpostgresql.svg` |
| Redis | `https://icons.d2lang.com/dev%2Fredis.svg` |
| Nginx | `https://icons.d2lang.com/dev%2Fnginx.svg` |
| GitHub | `https://icons.d2lang.com/dev%2Fgithub.svg` |
| GitLab | `https://icons.d2lang.com/dev%2Fgitlab.svg` |

#### 3. `infra/` — Generic Infrastructure Icons
Pattern: `https://icons.d2lang.com/infra%2F<number>-<name>.svg`

Example: `https://icons.d2lang.com/infra%2F002-backup.svg`

(Numbered series — generic server, network, backup, cloud pictograms)

#### 4. External Sources (any URL works)

| Source | Pattern | Best for |
|--------|---------|----------|
| GCP Icons | `https://cloud.google.com/icons/images/` | Google Cloud services |
| Kubernetes | `https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/` | K8s resources |
| Simple Icons | `https://simpleicons.org/icons/<name>.svg` | Brand logos (5000+) |
| Devicon | `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/<name>/<name>-original.svg` | Dev tools |
| Heroicons | `https://unpkg.com/heroicons@2.0.18/24/outline/<name>.svg` | UI/generic icons |

#### How to use icons in D2

**As icon inside a shape (label + icon):**
```d2
lambda: AWS Lambda {
  icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
}
```

**As standalone image (icon only, no border):**
```d2
lambda: {
  shape: image
  icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
}
```

**Full AWS serverless example:**
```d2
direction: right

user: User {shape: person}
apigw: API Gateway {
  icon: https://icons.d2lang.com/aws%2FApp%20Integration%2FAmazon-API-Gateway.svg
}
lambda: Lambda {
  icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
}
dynamo: DynamoDB {
  icon: https://icons.d2lang.com/aws%2FDatabase%2FAmazon-DynamoDB.svg
}

user -> apigw: HTTPS
apigw -> lambda: invoke
lambda -> dynamo: read/write
```

**Browse all available icons:** https://icons.d2lang.com

---

### Step-by-Step Progressive Animation (Slideshow SVG)

**Trigger**: User asks for "step by step", "slideshow", "progressive", "one at a time", "diaporama", "apparition progressive", "animate it", "like a PowerPoint".

**Workflow (3 steps):**

1. **Generate** the D2 diagram normally (pro preset or sketch depending on context)
2. **Render** the SVG via `renderd2` MCP tool (save to a relative output path)
3. **Animate** by calling `animated2` MCP tool on the rendered SVG

**`animated2` parameters:**

| Parameter     | Description                                                         | Default |
|---------------|---------------------------------------------------------------------|---------|
| `file_path`   | Path to the rendered SVG (required)                                 | -       |
| `steps`       | Comma-separated order of appearance (nodes first, then edges)       | SVG order |
| `timing`      | Duration per step in seconds                                        | 1.5     |
| `edge_draw_in`| Progressive edge drawing from source to destination                 | true    |
| `output_path` | Where to save the animated SVG (optional, overwrites input if omitted) | -    |

**Convention for `steps` ordering:**
1. Containers/nodes first — left-to-right or top-to-bottom
2. Connections after — in chronological flow order (matching 【1】【2】【3】 numbering)
3. Format: `"node1, node2, node3, source1 -> target1, source2 -> target2"`

**Example:**
```
renderd2(file_path="input.d2", output_path="diagram.svg", sketch=false, theme=0)

animated2(
  file_path="diagram.svg",
  steps="user, app-tier, sfu-tier, worker-tier, user -> app-tier, app-tier -> user, user -> sfu-tier, sfu-tier -> worker-tier, worker-tier -> sfu-tier, sfu-tier -> user",
  timing=1.5,
  edge_draw_in=true,
  output_path="diagram-progressive.svg"
)
```

**File naming:** `<name>-progressive.svg` alongside the static SVG.

**When NOT to use:**
- If user just wants static diagrams
- If user asks for animated arrows (use `style.animated: true` in D2 source instead)
- If user explicitly asks for GIF (use layers + Puppeteer + ImageMagick workflow)

**Convention d'ordre — Logique métier (OBLIGATOIRE):**

L'ordre des steps DOIT suivre la logique métier de l'architecture, PAS l'ordre SVG ni le topological sort automatique.

**Règle : Source → Flèche → Destination (granularité enfant)**

1. Décomposer chaque container en ses composants enfants
2. Afficher le composant SOURCE d'abord (du plus externe au plus interne)
3. Puis la FLÈCHE sortante de ce composant
4. Puis le composant DESTINATION (qui est la cible de la flèche)
5. Répéter pour chaque étape du flow

**Règle de décomposition** : Si un container contient des sous-composants, les afficher un par un (parent → enfant → sous-enfant) AVANT la première flèche qui en sort.

**Exemple — Architecture 3-tier :**
```
steps="
  user,                                 # Frame parent
  user.browser,                         # Sous-composant
  user.browser.webrtc,                  # Sous-sous-composant (source de la 1ère flèche)
  user.browser.webrtc -> app.frontend,  # 【1】 Flèche sortante
  app.frontend,                         # Destination apparaît
  app.backend,                          # Autre enfant du même container
  app.frontend -> app.backend,          # Connexion interne
  app.backend -> user.browser.webrtc,   # 【2】 Flèche retour
  user.browser.webrtc -> sfu.server,    # 【3】 Flèche vers prochain tier
  sfu.server,                           # Destination apparaît
  sfu.server -> worker.vad,             # 【4】 Flèche vers worker
  worker.vad,                           # Pipeline interne...
  worker.stt,
  worker.llm,
  worker.tts,
  worker.tts -> sfu.server,             # 【5】 Retour
  sfu.server -> user.browser.webrtc     # 【6】 Retour final
"
```

**❌ JAMAIS** utiliser `auto_order=topological` pour des diagrammes métier — l'ordre BFS ne correspond pas à la logique fonctionnelle.

**❌ JAMAIS** afficher un container entier d'un coup s'il contient des sous-composants impliqués dans le flow.

**✅ TOUJOURS** descendre au niveau du composant qui est la source/destination réelle de chaque flèche.

---

### PNG Export (Pixel-Perfect)

D2 CLI's native PNG export depends on Playwright which may fail (version 404). The **only reliable method** for 100% faithful PNG (including markdown legends in `foreignObject` and remote icons) is **Puppeteer + Chromium headless**.

**Why other tools fail:**
- `rsvg-convert` — does NOT render `<foreignObject>` (legend will be empty), does NOT fetch remote icons
- `ImageMagick convert` — grayscale output, poor SVG support
- `d2 --output .png` — depends on Playwright (often broken, 404 on CDN)
- **Puppeteer + Chromium** — renders EXACTLY like a browser (100% faithful, fetches remote icons)

#### Étape 1 — Rendre le SVG source avec `page_size: "none"` (OBLIGATOIRE)

TOUJOURS utiliser `page_size: "none"` pour le SVG qui sera converti en PNG.
- `"none"` = D2 génère les dimensions naturelles du layout (ex: 1552×1289)
- Le SVG aura `width="XXXX" height="YYYY"` en valeurs absolues (px)

**❌ JAMAIS utiliser un autre page_size pour le SVG source du PNG :**
- `fit` (défaut si omis) → produit `width="100%" height="99999"` → Puppeteer crash/infinite
- `a4-landscape` sur un diagramme dense (>8 nœuds) → compresse le texte, illisible
- `"1920x1080"` ou autre valeur arbitraire → non documenté, résultat imprévisible

#### Étape 2 — Déterminer le deviceScaleFactor selon la largeur naturelle

| Largeur naturelle du SVG | deviceScaleFactor | PNG résultant | Cas d'usage |
|---|---|---|---|
| ≤ 1200 px | 2 | ~2400 px wide | Petit diagramme, besoin de netteté |
| 1200–2000 px | 1 | taille native | Diagramme moyen, déjà assez grand |
| > 2000 px | 1 | taille native | Grand diagramme, pas besoin de grossir |

**Règle :** si le SVG fait déjà > 1200px de large, `deviceScaleFactor: 1` suffit.
Ne JAMAIS utiliser `deviceScaleFactor: 2` sur un SVG > 1500px (produit un PNG de 3000-4000px inutilement lourd).

#### Étape 3 — Script Puppeteer (CANONICAL — remplace toute version précédente)

```javascript
const puppeteer = require('/home/nizar/.npm-global/lib/node_modules/markdown2pdf-mcp/node_modules/puppeteer');
const fs = require('fs');

(async () => {
  const svgPath = '<ABSOLUTE_SVG_PATH>';
  const pngPath = '<ABSOLUTE_PNG_PATH>';

  const svgContent = fs.readFileSync(svgPath, 'utf8');
  const width = parseInt(svgContent.match(/width="(\d+)"/)?.[1] || 1600);
  const height = parseInt(svgContent.match(/height="(\d+)"/)?.[1] || 800);

  // Scale factor: 2 for small SVGs, 1 for large ones (already big enough)
  const scale = width <= 1200 ? 2 : 1;

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/usr/bin/chromium-browser',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: scale });
  await page.goto('file://' + svgPath, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.screenshot({ path: pngPath, fullPage: false, omitBackground: false });

  await browser.close();
})();
```

**Paramètres CRITIQUES :**
- `executablePath: '/usr/bin/chromium-browser'` — Chromium installé via snap (pas google-chrome)
- `deviceScaleFactor` — calculé dynamiquement selon la largeur du SVG
- `fullPage: false` — OBLIGATOIRE. Avec `true`, Puppeteer capture du vide infini si le viewBox dépasse le content
- `waitUntil: 'networkidle0'` — attend que toutes les icônes distantes soient téléchargées

#### Anti-patterns PNG (JAMAIS faire)

| ❌ Anti-pattern | Pourquoi ça casse |
|---|---|
| `page_size: "1920x1080"` | Arbitraire, pas dans le spec, force un SVG énorme |
| `page_size: "a4-landscape"` + >8 nœuds | Texte compressé illisible |
| `deviceScaleFactor: 2` + SVG > 1500px | PNG de 4000+ px, inutilement lourd |
| `fullPage: true` + SVG responsive | Screenshot infini (height=99999) |
| `page_size` omis (= `fit`) pour PNG | width="100%", Puppeteer ne sait pas dimensionner |
| `viewport: { width: width * 2, height: height * 2 }` | Doubler le viewport ET le scale = quadrupler la taille |

#### Rappel : page_size selon le livrable

| Livrable | page_size | Pourquoi |
|---|---|---|
| SVG pour browser/README | Omis (= `fit`) | Responsive, remplit le viewer |
| SVG source pour PNG export | `"none"` | Dimensions fixes, Puppeteer-compatible |
| SVG pour impression/PDF | `"a4-landscape"` | Uniquement si ≤8 nœuds simples |

#### Workflow complet D2 → SVG + PNG

1. Écrire le .d2
2. Compiler (`compiled2`) pour vérifier la syntaxe
3. Rendre SVG avec `page_size: "none"` (`renderd2`)
4. Lire width/height du SVG généré
5. Puppeteer screenshot avec scale adapté
6. Sauvegarder les deux dans AI-GENERATED (sous-dossiers `svg/` et `png/`) + dans le projet

---

### Numbered Steps on Connections

When the user asks for numbered steps on arrows/connections:

**Format OBLIGATOIRE** : Utiliser les crochets japonais fullwidth `【1】【2】【3】...` — plus gros et contrastés que les cercles ①②③.

**Style OBLIGATOIRE** : `style.font-size: 20` sur chaque connexion numérotée (par défaut ~16, trop petit).

**Exemple :**
```d2
a -> b: "【1】 Origin request" {
  style.animated: true
  style.font-size: 20
}
b -> c: "【2】 Invoke" {
  style.animated: true
  style.font-size: 20
}
```

**Légende** : Toujours ajouter un bloc légende qui explique chaque étape. Utiliser un container avec markdown :
```d2
legend: Legend {
  near: bottom-center
  style.fill: "#fffff0"
  style.stroke: "#cccccc"
  style.border-radius: 8

  content: |md
    **【1】** Description of step 1

    **【2】** Description of step 2
  |
}
```

**❌ JAMAIS** utiliser ① ② ③ (trop petits, illisibles sur les flèches)
**✅ TOUJOURS** utiliser 【1】【2】【3】 avec font-size: 20

---

### RTL Labels (Arabic/Tunisian text in D2)

When connection labels or shape labels contain Arabic/RTL text mixed with English (e.g., Tunisian explanations), the bidi algorithm breaks rendering in SVG. You MUST wrap RTL labels with Unicode directional marks.

**Required characters:**
- U+202B (Right-to-Left Embedding) = UTF-8 bytes `\xe2\x80\xab`
- U+202C (Pop Directional Formatting) = UTF-8 bytes `\xe2\x80\xac`

**Problem:** `fs_write` treats `\u202B` as literal text (6 chars), not as a Unicode codepoint. The file ends up with the literal string `\u202B` instead of the actual byte.

**Workflow OBLIGATOIRE (2-pass):**

1. **Write the .d2 file** with placeholders in labels:
```d2
a -> b: "__RTL__⑦ يقرا/يكتب في DynamoDB__ENDRTL__" {
  style.animated: true
}
```

2. **Substitute placeholders with real UTF-8 bytes** via bash:
```bash
sed -i 's/__RTL__/\xe2\x80\xab/g; s/__ENDRTL__/\xe2\x80\xac/g' file.d2
```

3. Then compile and render normally.

**Scope:** This applies to ALL text that mixes Arabic script with Latin/numbers — connection labels, shape labels, container titles. The markdown legend block (`|md ... |`) handles RTL correctly on its own (paste `‫` directly), so no placeholder needed there.

**Verification:** After sed, confirm bytes are present:
```bash
hexdump -C file.d2 | grep "e2 80 ab"
```

**❌ NEVER** write `\u202B` literally in `fs_write` — it will NOT be interpreted as Unicode.
**✅ ALWAYS** use the placeholder + sed approach for RTL labels in D2 files.
