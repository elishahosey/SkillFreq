# Requirement extraction impact

Before: `data\outputs\results-db-90-days-ecosystem.csv`
After: `data\outputs\results-db-90-days-requirements.csv`

Only requirement grammar/section behavior changed in this replay; lane policy and thresholds were unchanged.

Changed jobs: **1164**

## Aggregate movement

- Lane counts: `{'target_lane': 264, 'wrong_lane': 6256, 'secondary_lane': 1472, 'bridge_lane': 700}` → `{'target_lane': 264, 'wrong_lane': 6256, 'secondary_lane': 1472, 'bridge_lane': 700}`
- Apply decisions: `{'skip': 6336, 'manual_review': 2257, 'apply_now': 99}` → `{'manual_review': 2273, 'skip': 6314, 'apply_now': 105}`
- Fit quality: `{'weak_fit': 6325, 'good_fit': 861, 'possible_fit': 1506}` → `{'possible_fit': 1485, 'weak_fit': 6303, 'good_fit': 904}`
- Average fit: `31.211` → `31.353`
- Nonzero learning: `886` → `886`

- required atomic gaps: 754
- preferred atomic gaps: 545
- fit score: 341
- apply decision: 28
- AI review: 0

## Changed examples

### Spacecraft Functional Test Engineer II (`in-007d8b0ccd9edb7d`)

Changed: required
- Required gaps: `['Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): familiarity with test automation frameworks and scripting languages (e.g., python, c\\+\\+, or similar). — skills ['Python']; satisfied ['Python']
- Source (any_of): background in test data visualization or analytics (e.g., power bi, grafana, or custom dashboards). — skills ['Power BI']; satisfied []

### OneStream Integration Lead (`in-05cb02298d0c1b4f`)

Changed: required, fit
- Required gaps: `['Snowflake']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `64.0` / `manual_review` / `True` → `67.0` / `manual_review` / `True`
- Source (any_of): minimum of 2 years experience designing \\& building end\\-to\\-end data integration solutions between onestream and external data source systems (sap, oracle, workday, snowflake, etc.) leveraging rest api and/or sic — skills ['Snowflake']; satisfied []

### Senior Cybersecurity Engineer (`in-0622f63902d59919`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Google Cloud', 'Kubernetes']` → `['Google Cloud', 'Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): hands on experience in automation (powershell and/or python or a similar language, can be a beginner to intermediate level). — skills ['Python']; satisfied ['Python']
- Source (all_of): 3\\+ years experience in azure devops environment — skills ['Azure']; satisfied ['Azure']
- Source (all_of): 3\\+ years experience in azure monitoring — skills ['Azure']; satisfied ['Azure']

### Project Management Engineer (`in-0650593b8d821509`)

Changed: required
- Required gaps: `['Snowflake', 'Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (any_of): + power bi, sql, python, snowflake or similar cloud‑based data warehouses — skills ['SQL', 'Python', 'Snowflake', 'Power BI']; satisfied ['SQL', 'Python']

### Forward Deployed AI Engineer (`in-07070bc3c705ab9f`)

Changed: required
- Required gaps: `['AWS', 'Google Cloud', 'Kubernetes', 'Terraform']` → `['Kubernetes', 'AWS', 'Google Cloud', 'Terraform']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): kubernetes — skills ['Kubernetes']; satisfied []
- Source (all_of): cloud environments (aws/gcp and azure) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (all_of): infrastructure\\-as\\-code (like terraform/pulumi) — skills ['Terraform']; satisfied []
- Source (all_of): building kubernetes and cloud native applications — skills ['Kubernetes']; satisfied []

### Release Readiness Engineer / Technical Writer (`in-070c5e050348a635`)

Changed: required
- Required gaps: `['AWS', 'Google Cloud', 'Kubernetes', 'Terraform']` → `['Kubernetes', 'AWS', 'Google Cloud', 'Terraform']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): kubernetes — skills ['Kubernetes']; satisfied []
- Source (all_of): cloud environments (aws/gcp and azure) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (all_of): infrastructure\\-as\\-code (like terraform/pulumi) — skills ['Terraform']; satisfied []
- Source (all_of): building kubernetes and cloud native applications — skills ['Kubernetes']; satisfied []

### ML Engineer ((GCP) – Finance Data & AI Platform) (`in-08ee595f70e46b33`)

Changed: required
- Required gaps: `['Spark', 'Google Cloud', 'BigQuery', 'Terraform']` → `['Google Cloud', 'BigQuery', 'Spark', 'Terraform']`
- Preferred gaps: `['Power BI', 'Tableau']` → `['Power BI', 'Tableau']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): 4\\+ years of hands\\-on experience implementing ml solutions on gcp. — skills ['Google Cloud']; satisfied []
- Source (all_of): gcp technologies — skills ['Google Cloud']; satisfied []
- Source (all_of): bigquery / bigquery ml — skills ['BigQuery']; satisfied []
- Source (all_of): python — skills ['Python']; satisfied ['Python']
- Source (all_of): sql — skills ['SQL']; satisfied ['SQL']
- Source (all_of): pyspark / spark — skills ['Spark']; satisfied []
- Source (all_of): terraform — skills ['Terraform']; satisfied []

### Senior Data Scientist (`in-090a3307254d29c9`)

Changed: preferred
- Required gaps: `['Spark']` → `['Spark']`
- Preferred gaps: `['Power BI', 'Tableau']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): utilize modern distributed systems and data science tools (e.g., hadoop, hive/sql, apache spark, tensorflow, pytorch, scikit\\-learn). — skills ['SQL', 'Spark']; satisfied ['SQL']

### Software Engineer (Early Career Professional) (`in-09415ae61dac6086`)

Changed: preferred, fit
- Required gaps: `['AWS']` → `['AWS']`
- Preferred gaps: `['Docker', 'Terraform']` → `['Docker']`
- Fit / decision / AI: `74.91` / `manual_review` / `False` → `75.41` / `manual_review` / `False`
- Source (all_of): build and maintain scalable, cloud\\-native services on aws as part of a collaborative engineering team — skills ['AWS']; satisfied []
- Source (any_of): write clean, well\\-tested code in typescript, python or java following engineering best practices — skills ['Python']; satisfied ['Python']
- Source (any_of): foundational knowledge of at least one backend language — typescript or python or java — skills ['Python']; satisfied ['Python']

### Technology Support III (`in-0984d2056d5c1052`)

Changed: required
- Required gaps: `['Kafka', 'AWS', 'Terraform']` → `['AWS', 'Kafka', 'Terraform']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (all_of): proactively monitor, troubleshoot, and resolve incidents using grafana, aws cloudwatch, splunk, dynatrace, apica. — skills ['AWS']; satisfied []
- Source (all_of): maintain and enhance automated control\\-m workflows; manage real\\-time data streaming via kafka. — skills ['Kafka']; satisfied []
- Source (all_of): deploy, manage, and enhance aws solutions (ec2, s3, lambda, rds, iam, ecs fargate, athena, emr, cloudwatch, terraform). — skills ['AWS', 'Terraform']; satisfied []
- Source (all_of): operational support experience in control\\-m, kafka, jenkins, github, bitbucket, jira. — skills ['Kafka']; satisfied []

### Staff Software Engineer- Cloud Infrastructure and DevOps (`in-0a160ef50ef65500`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Senior Content Delivery Network Engineer (`in-0ae554c9ce94285a`)

Changed: required
- Required gaps: `['AWS', 'Google Cloud', 'Terraform']` → `['AWS', 'Google Cloud']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): 3\\+ years of experience with cdn platforms such as akamai, cloudflare, fastly, imperva, and aws cloudfront. — skills ['AWS']; satisfied []
- Source (all_of): 3\\+ years of experience with distributed environments: client\\-server, vms, aws, and gcp. — skills ['AWS', 'Google Cloud']; satisfied []
- Source (any_of): 3\\+ years of experience in two or more programming/scripting languages: go, python, node.js, java, etc. — skills ['Python']; satisfied ['Python']
- Source (any_of): 3\\+ years of hands\\-on experience building automation using python, terraform, gitops, or similar tools. — skills ['Python', 'Terraform']; satisfied ['Python']

### Readiness, Response & Recovery Security AI Developer (`in-0ae95f3b8b0a9da1`)

Changed: required
- Required gaps: `['Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): minimum of 2 years of hands\\-on experience in microsoft azure environments; familiarity with azure data and analytics services is a strong plus — skills ['Azure']; satisfied ['Azure']
- Source (any_of): minimum of 4 years of demonstrated experience in least one data or development layer: python, power bi, power apps/automate, sql, or a comparable stack — skills ['SQL', 'Python', 'Power BI']; satisfied ['SQL', 'Python']
- Source (any_of): you have experience with kql, sentinel workbooks, or similar query/visualization layers in azure — skills ['Azure']; satisfied ['Azure']

### Lead Commercial Loan Servicing Specialist (`in-0b3047607ae99308`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): experience with data analysis tools (e.g., sql, excel, tableau, power bi, or similar) — skills ['SQL', 'Power BI', 'Tableau']; satisfied ['SQL']

### Manufacturing IT Systems Engineer (`in-0c950d6b62dcc542`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Manager, Sales Operations (`in-0d2fb9cc85437a13`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Snowflake', 'Tableau']` → `['Snowflake']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Software Engineer (`in-0d81ea8b1df68b65`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['MySQL']` → `[]`
- Fit / decision / AI: `85` / `manual_review` / `False` → `85` / `manual_review` / `False`

### Senior Solutions Architect, CCOE-GSP Sales (`in-0d8b712a5677237a`)

Changed: required
- Required gaps: `['AWS', 'Terraform']` → `['Terraform', 'AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): create reusable assets — reference implementations, starter kits, deployment templates (cdk, cloudformation, terraform), and documentation that partner delivery teams can scale across engagements — skills ['Terraform']; satisfied []
- Source (all_of): own the technical relationship with large consulting partner customers — serve as the trusted hands\\-on advisor as they grow their aws practice — skills ['AWS']; satisfied []
- Source (all_of): drive adoption through building — demonstrate what's possible by delivering working software and turning proof\\-of\\-concepts into reusable patterns that drive long\\-term aws adoption — skills ['AWS']; satisfied []
- Source (all_of): contribute thought leadership — author aws blogs, whitepapers, and open\\-source projects; present at aws summit and re:invent based on real solutions you've built — skills ['AWS']; satisfied []
- Source (all_of): act as the voice of the partner — provide feedback to aws service teams based on real deployment experience and submit feature requests that improve developer experience — skills ['AWS']; satisfied []
- Source (all_of): aws values diverse experiences. — skills ['AWS']; satisfied []
- Source (equivalent): 3\\+ years of experience designing, building, and deploying applications on aws or equivalent cloud platforms — skills ['AWS']; satisfied []
- Source (any_of): proficiency in one or more programming languages (python, java, typescript, go) with demonstrated ability to build customer\\-facing applications and automation — skills ['Python']; satisfied ['Python']
- Source (any_of): experience with infrastructure\\-as\\-code (cloudformation, cdk, or terraform) and ci/cd pipeline design — skills ['Terraform']; satisfied []

### Data and Analytics Engineer (`in-0e03f1dd00a97a00`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['BigQuery', 'Google Cloud', 'dbt']` → `['BigQuery', 'Google Cloud']`
- Fit / decision / AI: `85` / `manual_review` / `False` → `85` / `manual_review` / `False`

### Sr Software Engineer- Cloud Infrastructure and DevOps (`in-0f009a5955e4c7c5`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Senior Manager, Supply Chain & Customer Operations (`in-0fe0131b1a8f9924`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Tableau']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`

### Technical Architect (`in-10f7e6768324319c`)

Changed: required
- Required gaps: `['AWS']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): relevant certifications such as aws certified solutions architect \\- professional, microsoft certified: azure solutions architect expert, or similar. — skills ['AWS', 'Azure']; satisfied ['Azure']
- Source (all_of): expert knowledge of front\\-end and back\\-end technologies, including but not limited to javascript, react, angular, node.js, java, python, and database management systems. — skills ['Python']; satisfied ['Python']

### Architect Solution (`in-1532a9e07553e759`)

Changed: required
- Required gaps: `['AWS', 'Google Cloud', 'Power BI']` → `['Power BI', 'AWS', 'Google Cloud']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `64.6` / `manual_review` / `True` → `64.6` / `manual_review` / `True`
- Source (all_of): proficiency with microsoft office, visio, power platform, power bi, and business intelligence/data visualization tools — skills ['Power BI']; satisfied []
- Source (all_of): experience with cloud computing platforms such as aws, google cloud, and microsoft azure, including containerization and orchestration tools — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Senior Software Engineer (`in-15c73198b797b2a1`)

Changed: required
- Required gaps: `['Kafka', 'AWS']` → `['AWS', 'Kafka']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `70.64` / `manual_review` / `False` → `70.64` / `manual_review` / `False`
- Source (all_of): cloud proficiency:** hands\\-on experience with **aws** (specifically serverless architectures). — skills ['AWS']; satisfied []
- Source (all_of): data \\& messaging:** proficiency in **nosql databases (mongodb)** and event\\-driven integration patterns (**kafka/kinesis**). — skills ['Kafka']; satisfied []

### MLOps Platform Engineer (Sagemaker) (`in-1612668b5798feab`)

Changed: required
- Required gaps: `['Snowflake', 'Airflow', 'AWS']` → `['AWS', 'Snowflake']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): 5\\+ years hands\\-on with aws, including deep expertise in amazon sagemaker (studio classic studio, pipelines, model registry, endpoints, feature store) — skills ['AWS']; satisfied []
- Source (any_of): sagemaker pipelines or similar workflow orchestration (airflow, step functions) — skills ['Airflow']; satisfied []
- Source (all_of): toyota financial services enterprise platforms team is looking for a senior ml platform engineer to design, build, and operationalize an enterprise ml platform on aws sagemaker unified studio. — skills ['AWS']; satisfied []
- Source (all_of): you will migrate the organization from a fragmented ml toolchain to a unified, governed platform on aws landing zone 2, covering the full ml lifecycle from data discovery through model deployment and monitoring. — skills ['AWS']; satisfied []
- Source (all_of): build mlops pipelines using sagemaker pipelines — data extraction from snowflake, preprocessing, training, evaluation, and model registration — skills ['Snowflake']; satisfied []

### AI Workflow/ Solutions Analyst, Value Added Services (`in-172396485eb847e0`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): experience building analyses using tools such as excel, sql, tableau, power bi, or similar. — skills ['SQL', 'Power BI', 'Tableau']; satisfied ['SQL']

### Director of Engineering (Data Platform) (`in-1776b42bedfa3888`)

Changed: preferred
- Required gaps: `['Databricks', 'Spark']` → `['Databricks', 'Spark']`
- Preferred gaps: `['AWS', 'Google Cloud']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): experience with databricks, including spark\\-based processing and the databricks platform ecosystem. — skills ['Databricks', 'Spark']; satisfied []

### HW & SW Applications Admin (`in-1793acdc8b794922`)

Changed: preferred, fit
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS']` → `[]`
- Fit / decision / AI: `71.55` / `manual_review` / `False` → `72.05` / `manual_review` / `False`

### Principal Software Engineer — AI Native (IT / OT / Cybersecurity) (`in-1815880fa7a6e625`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Kubernetes']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Senior Manager - AI / Automation Architect (`in-192eb5e264bbc0c7`)

Changed: preferred, fit
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Databricks', 'Google Cloud']` → `[]`
- Fit / decision / AI: `71.28` / `manual_review` / `True` → `72.78` / `manual_review` / `True`

### Readiness, Response & Recovery Security AI Developer (`in-1a16ed70cfc67442`)

Changed: required
- Required gaps: `['Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): minimum of 2 years of hands\\-on experience in microsoft azure environments; familiarity with azure data and analytics services is a strong plus — skills ['Azure']; satisfied ['Azure']
- Source (any_of): minimum of 4 years of demonstrated experience in least one data or development layer: python, power bi, power apps/automate, sql, or a comparable stack — skills ['SQL', 'Python', 'Power BI']; satisfied ['SQL', 'Python']
- Source (any_of): you have experience with kql, sentinel workbooks, or similar query/visualization layers in azure — skills ['Azure']; satisfied ['Azure']

### Manager - Financial Planning and Analysis (`in-1b2d73ace8b12a7b`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Google Agentic AI Delivery Senior Engineer (`in-1ba9252775aa7e00`)

Changed: required
- Required gaps: `['AWS', 'Google Cloud', 'BigQuery', 'Terraform']` → `['Google Cloud', 'BigQuery', 'Terraform', 'AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): , helping clients break free from legacy solution mindset and practices to build truly modern, value\\-driven software products on google cloud. — skills ['Google Cloud']; satisfied []
- Source (all_of): a passionate, hands\\-on gcp senior engineer who understands that great software is not just about elegant code, but about solving real problems leveraging the best technology tools available for a client. — skills ['Google Cloud']; satisfied []
- Source (all_of): you are as comfortable building a multi\\-agent workflow on vertex ai as you are testing a solution built by other team members in a compressed timeline, leveraging the various tools and technologies of google cloud. — skills ['Google Cloud']; satisfied []
- Source (all_of): as a gcp agentic ai delivery senior engineer, you will be a technical and product\\-centric engineer in consulting and engineering projects, customizing google cloud agentic solutions for client — skills ['Google Cloud']; satisfied []
- Source (all_of): you will act as a trusted team player, guiding others in the team on how to adopt a product engineering mindset and be the expert on specific google cloud technologies/products. — skills ['Google Cloud']; satisfied []
- Source (all_of): into gcp technology design elements and customized solutions. — skills ['Google Cloud']; satisfied []
- Source (all_of): design, build, test and deploy innovative, agentic\\-first solutions on gcp that are directly tied to the client business — skills ['Google Cloud']; satisfied []
- Source (all_of): hands\\-on development \\& proof\\-of\\-value:** rapidly design, build, and present compelling proof\\-of\\-concept (poc) solutions that bring your google cloud proficiency to workable solutions. — skills ['Google Cloud']; satisfied []
- Source (all_of): this includes hands\\-on software engineering using vertex ai, gemini/agentic ai, bigquery, google data technologies, terraform, and modern ci/cd practices. — skills ['BigQuery', 'Terraform']; satisfied []
- Source (all_of): guide and enable the delivery team on the principles of the product agile operating model and how to structure delivery sprints for continuous delivery using google cloud technologies. — skills ['Google Cloud']; satisfied []
- Source (all_of): minimum of 5 years of experience in a hands\\-on, client\\-facing technology role (e.g., google cloud engineer, product engineer, technology consultant). — skills ['Google Cloud']; satisfied []
- Source (all_of): minimum of 5 years of deep, hands\\-on experience architecting and building solutions on aws/azure/gcp, of which 4 years in gcp. — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (any_of): minimum of 3 years of proven experience with application modernization, call center ai and/or agentic ai solutions leveraging google cloud technologies. — skills ['Google Cloud']; satisfied []
- Source (all_of): technical depth:** multiple google cloud professional certifications (e.g., professional cloud architect, professional machine learning engineer, professional data engineer, genai leader). — skills ['Google Cloud']; satisfied []
- Source (all_of): project experience across the gcp ecosystem, including gke, bigquery, vertex ai, ces, apigee, and other gcp technologies. — skills ['Google Cloud', 'BigQuery']; satisfied []

### Principal Data Engineer (`in-1be09d65090fe1cc`)

Changed: preferred, fit
- Required gaps: `['Spark']` → `['Spark']`
- Preferred gaps: `['Google Cloud']` → `[]`
- Fit / decision / AI: `71.17` / `manual_review` / `True` → `71.67` / `manual_review` / `True`
- Source (all_of): 7\\+ years' experience with java/python/pyspark full stack development — skills ['Python', 'Spark']; satisfied ['Python']

### Software Engineer III - Java Fullstack / AWS (`in-1c0fffd9961cca4d`)

Changed: required, preferred, fit
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `[]` → `['AWS']`
- Fit / decision / AI: `76.54` / `manual_review` / `True` → `82.04` / `manual_review` / `True`
- Source (any_of): experience working on cloud platform (aws/gcp or azure). — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### IAM Architect (Entra ID-Focused) Hybrid in Plano (`in-1d99f91c3b3baf40`)

Changed: required
- Required gaps: `['Terraform']` → `[]`
- Preferred gaps: `['Kubernetes']` → `['Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): 10\\+ years of iam experience with strong emphasis on entra id / azure ad architecture and engineering. — skills ['Azure']; satisfied ['Azure']
- Source (any_of): experience with automation using powershell, microsoft graph api, python, or terraform. — skills ['Python', 'Terraform']; satisfied ['Python']

### Senior Architect, Software Engineering — Gateway Platform (`in-1df263ef60a18bdf`)

Changed: required, preferred, fit
- Required gaps: `['Kafka', 'Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Preferred gaps: `['AWS']` → `[]`
- Fit / decision / AI: `62.76` / `manual_review` / `True` → `66.26` / `manual_review` / `True`
- Source (equivalent): experience with event\\-driven integrations using apache kafka, jms, or equivalent pub/sub frameworks. — skills ['Kafka']; satisfied []
- Source (all_of): professional experience with containerization and orchestration (docker, kubernetes). — skills ['Docker', 'Kubernetes']; satisfied []
- Source (any_of): professional experience with relational databases (postgresql, oracle) and/or nosql data stores. — skills ['PostgreSQL']; satisfied ['PostgreSQL']

### Senior Consultant, FIS Treasury Technology (`in-1e2de48159c2f7aa`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (equivalent): proficiency in data visualization and productivity tools such as powerbi, tableau, or equivalent. — skills ['Power BI', 'Tableau']; satisfied []

### Engineering Manager (Communications Team) (`in-1eef194241c4147e`)

Changed: preferred, fit
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Docker', 'Kubernetes']` → `['Docker']`
- Fit / decision / AI: `75.14` / `manual_review` / `False` → `75.64` / `manual_review` / `False`

### Lead Analyst Data Engineer (`in-1f5c8418605bc555`)

Changed: required, fit, decision
- Required gaps: `['Databricks', 'Spark', 'AWS', 'Redshift', 'Power BI']` → `['AWS', 'Databricks', 'Spark', 'Power BI']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `53.5` / `skip` / `False` → `56.5` / `manual_review` / `False`
- Source (all_of): 7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments. — skills ['AWS']; satisfied []
- Source (any_of): proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions. — skills ['AWS', 'Redshift']; satisfied []
- Source (all_of): extensive experience working with databricks. — skills ['Databricks']; satisfied []
- Source (all_of): strong skills in sql (t\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql. — skills ['SQL', 'Python', 'Spark']; satisfied ['SQL', 'Python']
- Source (any_of): experience with databases: sql server, oracle, postgresql, azure sql, teradata. — skills ['SQL', 'PostgreSQL', 'SQL Server', 'Azure']; satisfied ['SQL', 'PostgreSQL', 'SQL Server', 'Azure']
- Source (all_of): skilled in power bi, git, visual studio code, ssms. — skills ['Power BI']; satisfied []

### Solution Architect - GenAI (`in-2127fb9204606d87`)

Changed: required
- Required gaps: `['Airflow', 'MySQL', 'Databricks', 'Spark', 'Kafka', 'AWS']` → `['Spark', 'Airflow', 'Databricks', 'Kafka', 'MySQL', 'AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): lead the development and integration of machine learning models leveraging scikit\\-learn, xgboost, and spark mllib, optimizing for performance and accuracy across large datasets. — skills ['Spark']; satisfied []
- Source (all_of): define data pipelines and orchestration workflows utilizing apache airflow, kafka, and databricks to enable robust, real\\-time analytics and model deployment. — skills ['Airflow', 'Databricks', 'Kafka']; satisfied []
- Source (all_of): guide the team in implementing data storage and retrieval solutions using mysql, postgresql, and cloud\\-based platforms, ensuring data integrity and scalability. — skills ['PostgreSQL', 'MySQL']; satisfied ['PostgreSQL']
- Source (all_of): python yes 5 — skills ['Python']; satisfied ['Python']
- Source (all_of): kafka,spark, postgresql yes 5 — skills ['PostgreSQL', 'Spark', 'Kafka']; satisfied ['PostgreSQL']
- Source (all_of): scikit\\-learn, pytorch, pandas, numpy, xgboost, spark, apache spark,apache airflow,apache kafka, rabbitmq,postgresql, mysql yes 5 — skills ['Airflow', 'PostgreSQL', 'MySQL', 'Spark', 'Kafka']; satisfied ['PostgreSQL']
- Source (all_of): r, bash, tensorflow, xgboost, lightgbm, mllib,classical ml, deep learning, nlp, time series forecasting, databricks — skills ['Databricks']; satisfied []
- Source (all_of): aws certified machine learning ï¿½ specialty — skills ['AWS']; satisfied []
- Source (all_of): databricks certified machine learning professional (optional but valuable) — skills ['Databricks']; satisfied []

### Cloud Enterprise Lead (`in-21df4b46b6f3bf00`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Terraform']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Sr Staff AI Engineer (AI Advisory, GenAI/AI Agents) (`in-22c81a0391cc4f88`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Snowflake']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): strong hands\\-on experience with python, sql, and modern data engineering practices, including buildable scalable data pipelines, etl/elt workflows, data integration processes, and production\\-grade analytics or ai/ml solutions. — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']

### Senior Application Developer (`in-23497a9afd5c8270`)

Changed: required, fit
- Required gaps: `['MySQL']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `62.69` / `manual_review` / `False` → `65` / `manual_review` / `False`
- Source (any_of): experience with relational databases (sql server, mysql, or similar), including query writing, optimization, and schema design. — skills ['SQL', 'SQL Server', 'MySQL']; satisfied ['SQL', 'SQL Server']

### Cloud Engineer - Cloud Optimization (`in-23c1b2408a4541fa`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Google Cloud']` → `[]`
- Fit / decision / AI: `85` / `manual_review` / `True` → `85` / `manual_review` / `True`
- Source (all_of): python — skills ['Python']; satisfied ['Python']
- Source (all_of): exposure to cloud platforms (azure — skills ['Azure']; satisfied ['Azure']

### Client Onboarding Data Specialist (`in-2515acb6d79ddad9`)

Changed: required
- Required gaps: `['Databricks']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): working knowledge of sql querying — skills ['SQL']; satisfied ['SQL']
- Source (any_of): familiarity with automated data testing frameworks or scripting languages like python or databricks would be a bonus! — skills ['Python', 'Databricks']; satisfied ['Python']

### Asset Management Engineering - Associate Software Engineer (AI Engineering) - Dallas (`in-252af71079fd2a98`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Google Cloud', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Fit / decision / AI: `85` / `manual_review` / `True` → `85` / `manual_review` / `True`
- Source (all_of): proficiency in python and at least one additional programming language (e.g., java, typescript) — skills ['Python']; satisfied ['Python']

### Lead Data Engineer (Enterprise Platforms Technology) (`in-2585466941d17f02`)

Changed: preferred, fit
- Required gaps: `['AWS', 'Google Cloud']` → `['AWS', 'Google Cloud']`
- Preferred gaps: `['Databricks', 'Kafka', 'MySQL', 'Redshift', 'Snowflake', 'Spark']` → `[]`
- Fit / decision / AI: `55.59` / `manual_review` / `True` → `58.59` / `manual_review` / `True`
- Source (all_of): at least 1 year experience with cloud computing (aws, microsoft azure, google cloud) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Senior Full Stack Developer, React & Python (`in-25f503ca0d3f2444`)

Changed: preferred
- Required gaps: `['Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Preferred gaps: `['AWS', 'Google Cloud']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): strong proficiency in python, especially api implementation and restful api development. — skills ['Python']; satisfied ['Python']
- Source (any_of): experience working with sql databases, preferably microsoft sql server or oracle. — skills ['SQL', 'SQL Server']; satisfied ['SQL', 'SQL Server']
- Source (all_of): familiarity with docker, kubernetes, and github actions. — skills ['Docker', 'Kubernetes']; satisfied []

### Staff Software Engineer - Search / AI (`in-285b7f74c01df4c2`)

Changed: required, fit
- Required gaps: `['AWS', 'Google Cloud', 'Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `55.46` / `manual_review` / `True` → `61.46` / `manual_review` / `True`
- Source (any_of): 5\\+ years of experience building enterprise\\-scale cloud\\-native applications (gcp, azure, or aws) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (any_of): 5\\+ years of programming skills in any one of the following programming languages: java, python, kotlin, or go, with an emphasis on backend and api\\-driven development — skills ['Python']; satisfied ['Python']
- Source (all_of): experience with containerization and orchestration (docker, kubernetes) — skills ['Docker', 'Kubernetes']; satisfied []

### Analytics Solutions Associate Senior - DART (`in-28c45d7cba759cd0`)

Changed: required
- Required gaps: `['Snowflake', 'AWS', 'Tableau']` → `['Tableau']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (all_of): design and build reliable elt/etl pipelines in python/sql; implement orchestration, version control, and ci/cd to ensure repeatability and resilience. — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (all_of): create executive\\-ready dashboards and self\\-service data marts (e.g., tableau) with intuitive ux and clear metric definitions. — skills ['Tableau']; satisfied []
- Source (all_of): expert\\-level sql (complex joins, window functions, ctes, performance tuning) and strong python (pandas, numpy; unit testing with pytest; structured logging; packaging). — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (equivalent): proven experience building automated data pipelines and operating in data lake/cloud environments (snowflake; aws services such as s3, glue, lambda; or equivalent). — skills ['Snowflake', 'AWS']; satisfied []
- Source (equivalent): strong data visualization experience (tableau or equivalent), including kpi design, dashboard ux, and audience\\-specific storytelling. — skills ['Tableau']; satisfied []

### Migration & Modernization Technical BD – US Healthcare, WWPS Migrations (`in-28e78d247a152ff0`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`

### Systems Engineer Project Lead Sr Stf – Level 5 (`in-29453c6000be5654`)

Changed: required
- Required gaps: `['Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): proficiency with ms office, project, visio, jira and/or tableau — skills ['Tableau']; satisfied []

### AWS Pyspark Tech Lead (`in-29530de146a2de8b`)

Changed: required
- Required gaps: `['Spark', 'AWS']` → `['AWS', 'Spark']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `71.67` / `manual_review` / `True` → `71.67` / `manual_review` / `True`
- Source (all_of): strong experience in aws glue (etl, studio, catalog) and data pipeline development — skills ['AWS']; satisfied []
- Source (all_of): hands\\-on expertise in apache spark / pyspark optimization — skills ['Spark']; satisfied []
- Source (all_of): proficiency in python, sql, and data modeling concepts — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (all_of): solid understanding of aws devops practices and automation frameworks — skills ['AWS']; satisfied []

### Quality Engineer - Level 2 (`in-2af873f659da81e7`)

Changed: required
- Required gaps: `['Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): tableau or similar data visualization experience — skills ['Tableau']; satisfied []

### Director of Fleet & Tooling Management (Bird Electric) (`in-2e783073d56d03e8`)

Changed: required
- Required gaps: `['Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (equivalent): strong analytical capability with fleet/maintenance systems, telematics, fuel systems, rental systems, tooling systems, microsoft excel/power bi or equivalent reporting tools, and erp/project\\-cost interfaces. — skills ['Power BI']; satisfied []

### Java Full Stack Developer (Senior) (`in-2fbec198465e3aa0`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Google Cloud', 'Kafka', 'Kubernetes']` → `['AWS', 'Docker', 'Google Cloud', 'Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Systems Administrator 3 (`in-301606afc136e538`)

Changed: preferred
- Required gaps: `['Kubernetes']` → `['Kubernetes']`
- Preferred gaps: `['Power BI']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): minimum of 8 years of experience in openshift, kubernetes, linux, and/or systems engineering. — skills ['Kubernetes']; satisfied []
- Source (all_of): strong understanding of kubernetes architecture and concepts. — skills ['Kubernetes']; satisfied []
- Source (all_of): proficiency with scripting languages such as python for automation and system management. — skills ['Python']; satisfied ['Python']

### Specialist - Data Engineering (`in-33bdef2c376004f0`)

Changed: required
- Required gaps: `['Airflow', 'Spark']` → `['Spark', 'Airflow']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `83.14` / `apply_now` / `False` → `83.14` / `apply_now` / `False`
- Source (all_of): unix sql and shell scripting experience is a — skills ['SQL']; satisfied ['SQL']
- Source (all_of): expertise in designing and developing scalable apache spark etl based data processing pipelines — skills ['Spark']; satisfied []
- Source (all_of): expertise in sql querying and complex joins — skills ['SQL']; satisfied ['SQL']
- Source (all_of): implementing comprehensive spark based data validation frameworks transforming large volumes of financial data within the project lifecycle — skills ['Spark']; satisfied []
- Source (all_of): expertise with complex data workflows with apache airflow managing task dependencies slas etc to ensure timely data delivery and corresponding automated validation controls — skills ['Airflow']; satisfied []
- Source (all_of): :** apache spark, big data hadoop ecosystem, python, python for data, sparksql — skills ['Python', 'Spark']; satisfied ['Python']

### Associate, Business Insights (`in-36d9775bb17439ee`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Snowflake', 'dbt']` → `['Power BI']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Sr Software Engineer - Cloud Infrastructure and Devops (`in-3713e3e943a83d2f`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### AI Engineer - SFL Scientific (`in-3778a847e69710fd`)

Changed: required, preferred
- Required gaps: `['Airflow', 'Kafka', 'AWS', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform']` → `['Kafka', 'Docker', 'Kubernetes']`
- Preferred gaps: `[]` → `['AWS']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): 2\\+ years of experience in designing cloud solutions and supporting production projects, including hands\\-on experience with aws services (or azure, gcp equivalents) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (all_of): 2\\+ years of programming experience with linux shell/cli, python, sql, powershell, etc. — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (any_of): 2\\+ years of experience in devops and leveraging ci/cd services: puppet, ansible, chef, airflow, terraform, jenkins — skills ['Airflow', 'Terraform']; satisfied []
- Source (all_of): 2\\+ years of experience with deployment and optimization: kubernetes, docker, nvidia tensorrt/triton, rapids, kubeflow, mlflow, kafka, etc. — skills ['Kafka', 'Docker', 'Kubernetes']; satisfied []

### Lead Generative AI Data Engineer III (`in-37bdade856dd6f8c`)

Changed: preferred
- Required gaps: `['Spark']` → `['Spark']`
- Preferred gaps: `['Docker', 'Kubernetes']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (all_of): 3\\+ years of experience programming in python, pyspark, pytorch, and tensorflow. — skills ['Python', 'Spark']; satisfied ['Python']
- Source (any_of): active certification or advanced certification in python, pyspark, pytorch, and tensorflow. — skills ['Python', 'Spark']; satisfied ['Python']

### Specialist - Data Sciences (`in-380494998d30967b`)

Changed: required, fit
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `72.61` / `manual_review` / `False` → `78.61` / `manual_review` / `False`
- Source (any_of): tooling deep expertise in python langgraphlangchain vector databases and cloudnative ai stacks azure ai aws bedrock or gcp vertex ai — skills ['Python', 'AWS', 'Azure', 'Google Cloud']; satisfied ['Python', 'Azure']

### Learning Technology & Analytics Specialist (`in-398e8695d1ed9380`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `['Power BI']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): demonstrated ability to build and maintain dashboards and reports using tools such as power bi, — skills ['Power BI']; satisfied []
- Source (equivalent): tableau, or equivalent. — skills ['Tableau']; satisfied []

### Staff Data Engineer — AI & Cloud (`in-3b7f7ea361834438`)

Changed: required, fit
- Required gaps: `['Databricks', 'Spark', 'Kafka', 'AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `['Docker', 'Kubernetes']` → `['Docker', 'Kubernetes']`
- Fit / decision / AI: `61.06` / `manual_review` / `True` → `76.06` / `manual_review` / `True`
- Source (any_of): strong expertise in python, sql, scala, or r with a focus on large\\-scale data processing, optimization, and performance tuning. — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (any_of): extensive experience with big data frameworks such as azure databricks, apache spark, kafka, or hadoop for large\\-scale data processing. — skills ['Databricks', 'Spark', 'Kafka', 'Azure']; satisfied ['Azure']
- Source (any_of): deep knowledge of cloud platforms and data services such as azure, aws, or gcp. — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Data Analyst - Supply Chain Data Insights & Analytics (`in-3d6b640137b56962`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (any_of): typically requires an advanced degree in science, technology, engineering or mathematics (stem) and a minimum of two (2\\) years of prior relevant experience in the following areas: at least two years of experience with structured query language (sql) — skills ['SQL']; satisfied ['SQL']
- Source (any_of): working experience using one or more of the following dashboard applications (power bi or tableau) — skills ['Power BI', 'Tableau']; satisfied []

### Systems Engineer Associate (Fleet Analytics) - Early Career (`in-3e691f0c9b7ac746`)

Changed: required
- Required gaps: `['Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): experience in using spreadsheets or databases (ms excel, access, hana, tableau, or — skills ['Tableau']; satisfied []
- Source (all_of): sql/oracle) — skills ['SQL']; satisfied ['SQL']

### Staff Observability Platform Engineer (`in-3f77f6b39e1a0a7e`)

Changed: preferred, fit
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Kafka', 'Kubernetes']` → `[]`
- Fit / decision / AI: `74.2` / `manual_review` / `False` → `75.2` / `manual_review` / `False`

### JAVA Software Development Engineer (`in-3fecd8003f1e49fe`)

Changed: preferred, fit
- Required gaps: `['Kafka']` → `['Kafka']`
- Preferred gaps: `['Docker', 'Kubernetes']` → `[]`
- Fit / decision / AI: `78.2` / `manual_review` / `True` → `79.2` / `manual_review` / `True`
- Source (all_of): 3\\+ years of experience with sql and nosql databases (e.g., oracle, mongodb 5\\.0\\). — skills ['SQL']; satisfied ['SQL']
- Source (all_of): understanding of restful apis, distributed systems, and integration patterns (rabbitmq, kafka) — skills ['Kafka']; satisfied []

### Data Engineer (`in-414f29729894e258`)

Changed: required
- Required gaps: `['Databricks', 'Spark', 'AWS']` → `['Databricks', 'AWS', 'Spark']`
- Preferred gaps: `['Kafka', 'Terraform']` → `['Kafka', 'Terraform']`
- Fit / decision / AI: `77.93` / `manual_review` / `False` → `77.93` / `manual_review` / `False`
- Source (all_of): establish and mature ci/cd pipelines for databricks workloads and supporting infrastructure, improving reliability, repeatability, and compliance of releases. — skills ['Databricks']; satisfied []
- Source (all_of): strong hands\\-on experience with aws data platforms, including designing and operating production systems leveraging databricks on aws. — skills ['Databricks', 'AWS']; satisfied []
- Source (all_of): deep expertise with apache spark, databricks, delta lake, python, and sql, including performance tuning of distributed workloads. — skills ['SQL', 'Python', 'Databricks', 'Spark']; satisfied ['SQL', 'Python']

### Advisor II, DevOps Engineering (`in-41870e0288ffa6c5`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Docker', 'Kubernetes']` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (any_of): experience with sql, nosql, postgresql, or oracle — skills ['SQL', 'PostgreSQL']; satisfied ['SQL', 'PostgreSQL']

### Senior Analytics Engineer (`in-435894c3393cdbf3`)

Changed: required
- Required gaps: `['Airflow', 'Spark', 'BigQuery', 'Kubernetes']` → `['BigQuery', 'Airflow', 'Spark', 'Kubernetes']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `72.64` / `manual_review` / `False` → `72.64` / `manual_review` / `False`
- Source (all_of): 7\\+ years of experience writing expert level sql within database systems such as bigquery, sap hana, teradata — skills ['SQL', 'BigQuery']; satisfied ['SQL']
- Source (any_of): 5\\+ years of experience with python or other object\\-oriented languages in an analytics engineering setting — skills ['Python']; satisfied ['Python']
- Source (all_of): 5\\+ years of experience with data, orchestration, and pipeline engineering services such as airflow, spark, kubernetes, preferably composer / dataproc — skills ['Airflow', 'Spark', 'Kubernetes']; satisfied []

### Sr. Site Reliability Engineer (`in-4365a1b3f66a24d4`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['AWS', 'Kafka', 'Kubernetes', 'MySQL', 'Spark']` → `['AWS', 'Kafka', 'Kubernetes', 'Spark']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Infrastructure Support Engineer (`in-4426224b58c32b6a`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Kubernetes', 'Spark', 'Terraform']` → `['Spark']`
- Fit / decision / AI: `65` / `manual_review` / `False` → `65` / `manual_review` / `False`

### Social Engineering Simulation Senior Analyst (`in-455c6129c3749c69`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `False` → `65` / `manual_review` / `False`
- Source (any_of): experience working with, analyzing, and creating visualizations for structured and unstructured data using tools such as excel, sql, python, power bi, tableau, or similar. — skills ['SQL', 'Python', 'Power BI', 'Tableau']; satisfied ['SQL', 'Python']

### Senior Data Engineer (`in-45738cf915b51235`)

Changed: required, fit
- Required gaps: `['Spark', 'AWS']` → `['AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `79.38` / `manual_review` / `True` → `82.38` / `manual_review` / `True`
- Source (any_of): proven experience as a data engineer or similar role with a focus on big data technologies such as hadoop, spark, hive, and azure data lake. — skills ['Spark', 'Azure']; satisfied ['Azure']
- Source (all_of): strong proficiency in sql (including microsoft sql server and oracle), python, java, bash (unix shell), shell scripting, and vba for automation and analysis tasks. — skills ['SQL', 'Python', 'SQL Server']; satisfied ['SQL', 'Python', 'SQL Server']
- Source (all_of): familiarity with cloud platforms such as aws and azure for deploying large\\-scale data solutions. — skills ['AWS', 'Azure']; satisfied ['Azure']

### Software Engineer (`in-458f0054facd5c01`)

Changed: required, fit
- Required gaps: `['AWS', 'Docker', 'Kubernetes']` → `['AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `80.29` / `manual_review` / `True` → `85` / `manual_review` / `True`
- Source (all_of): working knowledge of aws ecosystem \\& implement cloud\\-native software solutions on aws — skills ['AWS']; satisfied []
- Source (all_of): (oracle, postgresql, dynamodb) — skills ['PostgreSQL']; satisfied ['PostgreSQL']
- Source (all_of): experience with backend data integration (sql such as postgres, and data connection elements) — skills ['SQL', 'PostgreSQL']; satisfied ['SQL', 'PostgreSQL']
- Source (any_of): at least some experience with** **ecs,** **docker,** **fargate****,** **or ec2,** **and** **kubernetes — skills ['Docker', 'Kubernetes']; satisfied []
- Source (all_of): experience aws govcloud and dod/dow srg approved cloud software and aws services — skills ['AWS']; satisfied []

### Lead Information Security Engineer (`in-48bbfa9137327a0f`)

Changed: required
- Required gaps: `['Databricks', 'AWS', 'Google Cloud']` → `['AWS', 'Google Cloud']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): develop and maintain python‑based backend services, data pipelines, and apis to enable security analytics, automation, and ai/ml adoption — skills ['Python']; satisfied ['Python']
- Source (all_of): apply cloud‑native best practices across aws, azure, and gcp to improve reliability, scalability, and cost efficiency — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (any_of): 5\\+ years of experience in a modern programming language (e.g., python, java, c/c\\+\\+, go, or rust) — skills ['Python']; satisfied ['Python']
- Source (any_of): experience working with data platforms, databases, and data processing frameworks (e.g., databricks or similar) — skills ['Databricks']; satisfied []
- Source (any_of): proven expertise building secure, scalable cloud‑native solutions across aws, azure, and/or google cloud — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Principal of People Analytics (`in-48ed92d4c070063f`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Tableau']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Senior AI Pricing Analyst (`in-49534396a2f1afea`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Tableau']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Java Developer (`in-4ac9681ff49c88cc`)

Changed: required, fit
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `78.04` / `manual_review` / `False` → `84.04` / `manual_review` / `False`
- Source (all_of): proficiency working with relational databases (e.g., sql server, postgresql) and strong sql skills for data modeling and querying — skills ['SQL', 'PostgreSQL', 'SQL Server']; satisfied ['SQL', 'PostgreSQL', 'SQL Server']
- Source (any_of): exposure to cloud\\-based application development across platforms such as aws, azure, gcp, or pcf — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Yourgi Software Engineer II (`in-4ca878a5ee5c49c4`)

Changed: required
- Required gaps: `['MySQL', 'AWS']` → `['AWS', 'MySQL']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `66.31` / `manual_review` / `False` → `66.31` / `manual_review` / `False`
- Source (all_of): design and develop services in a serverless aws architecture to maintain modularity, performance, security, development efficiency and enhancements — skills ['AWS']; satisfied []
- Source (all_of): 3\\+ years commercial software development – typescript, javacript, java, c\\#, scala, python, go — skills ['Python']; satisfied ['Python']
- Source (any_of): proficient with agile scrum, azure devops or jira — skills ['Azure']; satisfied ['Azure']
- Source (all_of): skills:* experience writing sql queries and dml for rdms such as mysql — skills ['SQL', 'MySQL']; satisfied ['SQL']

### Healthcare Data Analyst (`in-4cb4087ecae9434d`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): strong working knowledge of sql for data extraction, querying, manipulation, and analysis. — skills ['SQL']; satisfied ['SQL']
- Source (any_of): experience with data visualization and reporting tools such as power bi, tableau, or looker. — skills ['Power BI', 'Tableau']; satisfied []

### Senior Associate, Project Management for Operational Data and Performance (`in-4f584c4b7d3c0f83`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `False` → `65` / `manual_review` / `False`
- Source (any_of): familiarity with databases (like sql) and bi tools (such as tableau, power bi, or sap analytics cloud) is beneficial — skills ['SQL', 'Power BI', 'Tableau']; satisfied ['SQL']
- Source (all_of): familiarity with programming languages (like javascript, python) is beneficial — skills ['Python']; satisfied ['Python']

### Sales Enablement Specialist (contract) (`in-5011c67e3c7045c3`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`

### Americas Tax Technology Group - Solutions Architect - Senior Manager (`in-502ddc25eb06d122`)

Changed: required
- Required gaps: `['Kubernetes']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (all_of): leverages microsoft azure ai foundry capabilities (model selection, agent service, agent framework/sdk, hosted agents, and observability/evaluations) to deliver scalable solutions. — skills ['Azure']; satisfied ['Azure']
- Source (any_of): ensures production operations and reliability:** kubernetes or serverless hosting, reliability engineering, cost/performance tuning, and incident response readiness. — skills ['Kubernetes']; satisfied []

### DevOps Engineer, G&A Solutions Engineering (GSE) (`in-507a688d50818dad`)

Changed: required, preferred
- Required gaps: `['AWS', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform']` → `[]`
- Preferred gaps: `['Kafka']` → `['AWS', 'Google Cloud', 'Kafka']`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): experience creating and implementing ci/cd pipeline with tools such as terraform, pulumi, ansible, or spinnaker toolset — skills ['Terraform']; satisfied []
- Source (any_of): experience implementing applications in private/public cloud infrastructure (aws or gcp) and container technologies, like kubernetes or docker in production environments — skills ['AWS', 'Google Cloud', 'Docker', 'Kubernetes']; satisfied []
- Source (any_of): ability to program in a high\\-level programming languages or scripting, such java, python, shell, or golang — skills ['Python']; satisfied ['Python']

### Senior. Platform Engineer (Onsite) (`in-51a923fbd46593eb`)

Changed: required
- Required gaps: `['AWS', 'Docker', 'Kubernetes', 'Terraform']` → `['AWS']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`
- Source (any_of): experience with infrastructure automation and configuration management tools such as terraform, ansible, and/or chef — skills ['Terraform']; satisfied []
- Source (all_of): hands\\-on experience designing, implementing, and integrating cloud infrastructure solutions, preferably with aws. — skills ['AWS']; satisfied []
- Source (any_of): working knowledge of scripting languages such as python and/or bash used for automation and operational workflows — skills ['Python']; satisfied ['Python']
- Source (all_of): strong aws experience, including architecture, deployment, and security of services such as ec2, eks, s3, cloudwatch, iam, and vpc, with an emphasis on scalability and cost optimization — skills ['AWS']; satisfied []
- Source (any_of): container and platform engineering experience using kubernetes and container runtimes such as docker or podman — skills ['Docker', 'Kubernetes']; satisfied []

### Sr Engineer, Data - Finance Domain (`in-51c6cf515e58363e`)

Changed: required, preferred
- Required gaps: `['dbt', 'Databricks', 'AWS', 'Google Cloud']` → `['dbt', 'Databricks']`
- Preferred gaps: `['Snowflake']` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (all_of): develop and maintain transformation logic and reusable data models using sql, python, databricks, dbt, and related data engineering tools. — skills ['SQL', 'Python', 'dbt', 'Databricks']; satisfied ['SQL', 'Python']
- Source (any_of): 4\\-7 years developing cloud solutions using data series; experience with cloud platforms (amazon web services, azure, or google cloud) (required) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']
- Source (any_of): proven track record in sql, nosql, and/or relational database design and development (required) — skills ['SQL']; satisfied ['SQL']
- Source (any_of): 4\\-7 years advanced knowledge and experience in building sophisticated data pipelines with python, experience in languages such as sql, dax python, java, scala, and/or go (required) — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (any_of): experience developing scalable data models, transformation logic, and curated datasets using sql, python, databricks, or comparable data engineering technologies. — skills ['SQL', 'Python', 'Databricks']; satisfied ['SQL', 'Python']
- Source (all_of): databricks dbrx (required) — skills ['Databricks']; satisfied []
- Source (all_of): dbt (data build tool) framework (required) — skills ['dbt']; satisfied []

### SVP Lead Full Stack Engineer (M&A Technology & AI) (`in-5276d3450ba88e65`)

Changed: required
- Required gaps: `['Kafka', 'AWS', 'Google Cloud', 'Docker', 'Kubernetes']` → `['Kafka', 'Docker', 'Kubernetes', 'AWS', 'Google Cloud']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): demonstrated experience with event\\-driven architectures (e.g., kafka, rabbitmq). — skills ['Kafka']; satisfied []
- Source (all_of): + hands\\-on experience with message brokers and event streaming platforms (e.g., apache kafka, rabbitmq). — skills ['Kafka']; satisfied []
- Source (all_of): + proficiency with relational and nosql databases (e.g., postgresql, mongodb, cassandra) — skills ['PostgreSQL']; satisfied ['PostgreSQL']
- Source (all_of): + experience with containerization technologies (docker) and orchestration (kubernetes). — skills ['Docker', 'Kubernetes']; satisfied []
- Source (all_of): + proficiency with ci/cd pipelines (e.g., jenkins, gitlab ci, azure devops). — skills ['Azure']; satisfied ['Azure']
- Source (all_of): + experience with cloud platforms (e.g., aws, azure, gcp) and their relevant services. — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Senior Full Stack Developer (`in-55920e1408bf3d66`)

Changed: preferred
- Required gaps: `['AWS']` → `['AWS']`
- Preferred gaps: `['Docker', 'Kubernetes']` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): minimum of three (3\\) years of experience with cloud applications development to build /modernize applications and datasets on the aws cloud — skills ['AWS']; satisfied []
- Source (all_of): experience and proficiency in implementing frontend and backend services for cloud\\-native software products and solutions such as python, javascript, django and vue.js. — skills ['Python']; satisfied ['Python']
- Source (all_of): the must\\-have skills include proficiency in python and javascript. — skills ['Python']; satisfied ['Python']

### Finance Analyst II (`in-56b0e99f74a9b5c4`)

Changed: required
- Required gaps: `['Power BI']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (any_of): some exposure to power bi, sap, business objects, and business warehouse or similar systems required. — skills ['Power BI']; satisfied []

### Merchant Services Business Manager - Vice President (`in-5a57d0b15631210a`)

Changed: preferred
- Required gaps: `[]` → `[]`
- Preferred gaps: `['Power BI', 'Tableau']` → `[]`
- Fit / decision / AI: `15` / `skip` / `True` → `15` / `skip` / `True`

### Specialist - Data Sciences (`in-5c8fc653455c136b`)

Changed: required, fit
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `72.61` / `manual_review` / `False` → `78.61` / `manual_review` / `False`
- Source (any_of): tooling deep expertise in python langgraphlangchain vector databases and cloudnative ai stacks azure ai aws bedrock or gcp vertex ai — skills ['Python', 'AWS', 'Azure', 'Google Cloud']; satisfied ['Python', 'Azure']

### Senior Data Analyst - Remote (`in-5cea760be9af8f95`)

Changed: required
- Required gaps: `['Power BI', 'Tableau']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `65` / `manual_review` / `True` → `65` / `manual_review` / `True`
- Source (all_of): sql\\-based automation (stored procedures, scheduling, reusable logic) — skills ['SQL']; satisfied ['SQL']
- Source (all_of): provide guidance and support to junior team members on sql, reporting, and automation concepts — skills ['SQL']; satisfied ['SQL']
- Source (all_of): 5\\+ years of experience querying databases (microsoft sql and oracle) — skills ['SQL']; satisfied ['SQL']
- Source (any_of): 5\\+ years of experience with power bi, tableau, and/or ssrs — skills ['Power BI', 'Tableau']; satisfied []

### Full Stack Technical Lead (`in-5f110061d1f52e32`)

Changed: required, fit
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `64.22` / `manual_review` / `False` → `65` / `manual_review` / `False`
- Source (all_of): strong proficiency in server\\-side programming languages and technologies – c\\#/.net, asp.net core, entity framework, sql, python is a plus. — skills ['SQL', 'Python']; satisfied ['SQL', 'Python']
- Source (any_of): experience designing, building, or supporting cloud\\-based architectures; familiarity with cloud\\-hosted systems (e.g., aws, azure, gcp) is highly desirable. — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Software Engineering Senior Manager Chief Development Office (`in-607128accbafc740`)

Changed: required, preferred, fit
- Required gaps: `['Google Cloud', 'Docker', 'Kubernetes', 'Terraform']` → `['Kubernetes', 'Google Cloud', 'Terraform', 'Docker']`
- Preferred gaps: `['AWS']` → `[]`
- Fit / decision / AI: `58.33` / `manual_review` / `False` → `58.83` / `manual_review` / `False`
- Source (all_of): 6\\+ years of experience with applications that run java, .net, node.js, c, c\\+\\+, kubernetes, saas, commercial off the shelf products from a ci/cd perspective — skills ['Kubernetes']; satisfied []
- Source (all_of): 6\\+ years of experience with software architectures including traditional n\\-tier and containerized kubernetes microservices — skills ['Kubernetes']; satisfied []
- Source (all_of): 5\\+ years of experience with code sign tools like venafi, artifactory, blackduck, checkmarx, threadfix, prisma scans, ibm urban code deploy, harness, azure devops (ado), team foundation server (tfs) — skills ['Azure']; satisfied ['Azure']
- Source (all_of): 3\\+ years of experience on the ci/cd next gen tools like github actions, gitlab, azure pipelines, harness cd, spinnaker, and argo cd — skills ['Azure']; satisfied ['Azure']
- Source (all_of): 2\\+ years of experience in ci/cd pipeline that deploys to a managed kubernetes public cloud environment — skills ['Kubernetes']; satisfied []
- Source (all_of): 3\\+ years of experience with different landing zones for deployments to windows, linux, virtual machines (vm), tanzu application service (tas), tanzu kubernetes grid integrated (tkgi), and public cloud with azure and google cloud environments — skills ['Azure', 'Google Cloud', 'Kubernetes']; satisfied ['Azure']
- Source (any_of): experience with azure, google cloud platform (gcp) or openshift including services like compute, storage, databases, and networking — skills ['Azure', 'Google Cloud']; satisfied ['Azure']
- Source (all_of): knowledge of infrastructure as code (iac) tools such as terraform, ansible — skills ['Terraform']; satisfied []
- Source (all_of): experience in creating and managing docker containers — skills ['Docker']; satisfied []
- Source (all_of): experience with deploying and managing applications on kubernetes clusters — skills ['Kubernetes']; satisfied []

### Technical Lead - AI OPs (`in-6124726592ad6bac`)

Changed: required, fit, decision
- Required gaps: `['AWS', 'Google Cloud']` → `[]`
- Preferred gaps: `['Kafka']` → `['Kafka']`
- Fit / decision / AI: `52.63` / `skip` / `True` → `58.63` / `manual_review` / `True`
- Source (any_of): experience with programming languages \\- python and/or java — skills ['Python']; satisfied ['Python']
- Source (any_of): experience, hands\\-on with cloud platforms (aws, azure, or google cloud) — skills ['AWS', 'Azure', 'Google Cloud']; satisfied ['Azure']

### Staff Full Stack Software Engineer (`in-621dbc468d8ad82e`)

Changed: required
- Required gaps: `['Airflow', 'Spark', 'Kubernetes', 'Terraform']` → `['Airflow', 'Spark']`
- Preferred gaps: `[]` → `[]`
- Fit / decision / AI: `15` / `skip` / `False` → `15` / `skip` / `False`
- Source (all_of): solid hands\\-on experience with microservices development (grpc, rest etc.), object oriented programming system (oops), sql and nosql databases, messaging infrastructure, etc. — skills ['SQL']; satisfied ['SQL']
- Source (any_of): at least 5 years of development and production experience with kubernetes (such as in an on\\-premise or private cloud environment), openshift, or other enterprise\\-grade private cloud platforms, terraform, etc. — skills ['Kubernetes', 'Terraform']; satisfied []
- Source (all_of): you’ll work with cutting\\-edge technologies like trino, spark, airflow, and advanced ai inferencing systems to shape the future of analytics. — skills ['Airflow', 'Spark']; satisfied []

