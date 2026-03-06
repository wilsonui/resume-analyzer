# models/skill_model.py
# Central database for skills, job roles, and NLP reference data

# ─────────────────────────────────────────────
# SKILL DATABASE
# ─────────────────────────────────────────────

SKILLS_DB = {
    "programming_languages": [
        "python", "javascript", "java", "c++", "c#", "c", "typescript",
        "kotlin", "swift", "go", "rust", "ruby", "php", "scala", "r",
        "matlab", "dart", "perl", "haskell", "lua", "groovy", "bash",
        "shell", "powershell", "sql", "pl/sql", "vba"
    ],

    "web_frontend": [
        "html", "css", "react", "angular", "vue", "nextjs", "nuxtjs",
        "svelte", "bootstrap", "tailwind", "jquery", "webpack", "vite",
        "redux", "graphql", "sass", "less", "gatsby", "remix"
    ],

    "web_backend": [
        "node.js", "express", "django", "flask", "fastapi", "spring",
        "spring boot", "laravel", "rails", "asp.net", "nestjs", "fastify",
        "gin", "fiber", "actix", "rocket", "phoenix"
    ],

    "databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "cassandra",
        "elasticsearch", "dynamodb", "firebase", "neo4j", "mariadb",
        "oracle", "mssql", "couchdb", "influxdb", "supabase", "prisma"
    ],

    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "terraform", "ansible", "ci/cd", "git", "github", "gitlab",
        "bitbucket", "linux", "nginx", "apache", "heroku", "vercel",
        "netlify", "cloudflare", "datadog", "grafana", "prometheus"
    ],

    "data_ml": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau",
        "power bi", "data analysis", "data visualization", "statistics",
        "regression", "classification", "clustering", "opencv", "huggingface",
        "transformers", "bert", "gpt", "llm", "langchain", "rag",
        "feature engineering", "model deployment", "mlflow", "airflow"
    ],

    "mobile": [
        "android", "ios", "react native", "flutter", "xamarin",
        "ionic", "cordova", "swift", "kotlin", "expo"
    ],

    "soft_skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "project management",
        "agile", "scrum", "kanban", "collaboration", "presentation",
        "analytical", "creative", "mentoring", "negotiation"
    ],

    "security": [
        "cybersecurity", "penetration testing", "ethical hacking",
        "network security", "cryptography", "owasp", "soc", "siem",
        "firewalls", "vulnerability assessment", "compliance"
    ]
}

# ─────────────────────────────────────────────
# JOB ROLES DATABASE
# ─────────────────────────────────────────────

JOB_ROLES = {
    "Data Analyst": {
        "description": """Analyze large datasets to extract meaningful business insights.
        Work with stakeholders to define KPIs, build dashboards, and create reports.
        Use SQL, Python, and visualization tools to drive data-informed decisions.""",
        "required_skills": [
            "sql", "python", "pandas", "numpy", "excel", "tableau",
            "power bi", "data visualization", "statistics", "matplotlib",
            "data analysis", "reporting", "communication", "problem solving"
        ],
        "nice_to_have": [
            "machine learning", "r", "seaborn", "airflow", "dbt",
            "spark", "bigquery", "snowflake"
        ],
        "keywords": [
            "data analysis", "business intelligence", "kpi", "dashboard",
            "reporting", "insights", "metrics", "data-driven", "sql queries",
            "pivot tables", "data cleaning", "etl"
        ]
    },

    "Machine Learning Engineer": {
        "description": """Design, build, and deploy machine learning models at scale.
        Work on end-to-end ML pipelines, feature engineering, model training and evaluation.
        Deploy models to production and monitor their performance.""",
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "statistics", "sql",
            "model deployment", "docker", "git"
        ],
        "nice_to_have": [
            "mlflow", "airflow", "kubernetes", "spark", "aws", "gcp",
            "transformers", "nlp", "computer vision", "cuda"
        ],
        "keywords": [
            "machine learning", "model training", "feature engineering",
            "hyperparameter tuning", "cross validation", "neural network",
            "model deployment", "a/b testing", "data pipeline", "mlops"
        ]
    },

    "Backend Developer": {
        "description": """Build robust, scalable server-side applications and REST APIs.
        Work with databases, caching, message queues, and microservices.
        Focus on performance, security, and maintainability.""",
        "required_skills": [
            "python", "java", "node.js", "rest api", "sql", "postgresql",
            "mysql", "redis", "docker", "git", "linux", "authentication",
            "microservices"
        ],
        "nice_to_have": [
            "kubernetes", "kafka", "rabbitmq", "aws", "graphql",
            "mongodb", "nginx", "ci/cd", "terraform"
        ],
        "keywords": [
            "rest api", "microservices", "database design", "authentication",
            "authorization", "caching", "performance optimization",
            "scalability", "server-side", "backend", "api development"
        ]
    },

    "Frontend Developer": {
        "description": """Create beautiful, responsive user interfaces for web applications.
        Work with design teams to implement pixel-perfect UI/UX.
        Optimize performance, accessibility, and cross-browser compatibility.""",
        "required_skills": [
            "html", "css", "javascript", "react", "typescript", "git",
            "responsive design", "rest api", "webpack", "accessibility"
        ],
        "nice_to_have": [
            "nextjs", "vue", "angular", "redux", "graphql", "tailwind",
            "figma", "testing", "performance optimization", "seo"
        ],
        "keywords": [
            "ui/ux", "responsive design", "user interface", "component",
            "state management", "cross-browser", "accessibility", "spa",
            "performance", "frontend", "web development"
        ]
    },

    "Full Stack Developer": {
        "description": """Build end-to-end web applications covering both frontend and backend.
        Design databases, create APIs, and craft user interfaces.
        Work across the entire software development lifecycle.""",
        "required_skills": [
            "javascript", "react", "node.js", "python", "sql", "html",
            "css", "rest api", "git", "docker", "postgresql"
        ],
        "nice_to_have": [
            "typescript", "kubernetes", "aws", "mongodb", "graphql",
            "redis", "ci/cd", "microservices", "testing"
        ],
        "keywords": [
            "full stack", "frontend", "backend", "web application",
            "api", "database", "deployment", "devops", "scalable",
            "end-to-end", "agile"
        ]
    },

    "DevOps Engineer": {
        "description": """Build and maintain CI/CD pipelines, infrastructure as code,
        and monitoring systems. Ensure reliability, scalability, and security
        of cloud infrastructure. Bridge the gap between development and operations.""",
        "required_skills": [
            "docker", "kubernetes", "aws", "ci/cd", "terraform", "ansible",
            "linux", "bash", "git", "jenkins", "monitoring", "nginx"
        ],
        "nice_to_have": [
            "azure", "gcp", "helm", "prometheus", "grafana", "elk stack",
            "vault", "istio", "python", "go"
        ],
        "keywords": [
            "devops", "infrastructure", "deployment", "automation",
            "cloud", "container", "orchestration", "reliability",
            "scalability", "monitoring", "incident response", "sre"
        ]
    },

    "AI/NLP Engineer": {
        "description": """Research and implement AI solutions using Large Language Models,
        NLP techniques, and generative AI. Build pipelines for text processing,
        semantic search, and conversational AI applications.""",
        "required_skills": [
            "python", "nlp", "transformers", "pytorch", "tensorflow",
            "bert", "huggingface", "scikit-learn", "pandas", "numpy",
            "langchain", "llm"
        ],
        "nice_to_have": [
            "rag", "vector databases", "fine-tuning", "aws", "docker",
            "fastapi", "elasticsearch", "mlflow", "cuda"
        ],
        "keywords": [
            "natural language processing", "text classification", "named entity recognition",
            "sentiment analysis", "language model", "fine-tuning",
            "prompt engineering", "semantic similarity", "chatbot", "rag"
        ]
    },

    "Cybersecurity Analyst": {
        "description": """Protect organizational assets by monitoring, detecting, and responding
        to security threats. Conduct vulnerability assessments and penetration testing.
        Implement security best practices and compliance frameworks.""",
        "required_skills": [
            "cybersecurity", "network security", "vulnerability assessment",
            "penetration testing", "siem", "firewalls", "owasp",
            "python", "linux", "cryptography"
        ],
        "nice_to_have": [
            "ethical hacking", "incident response", "soc", "compliance",
            "cloud security", "malware analysis", "wireshark", "metasploit"
        ],
        "keywords": [
            "security", "threat detection", "risk assessment", "compliance",
            "incident response", "penetration testing", "vulnerability",
            "security audit", "access control", "encryption"
        ]
    },"Marketing Manager": {
        "description": """Develop and execute marketing strategies to drive brand awareness and growth.
        Manage campaigns, analyze performance metrics, and lead marketing teams.""",
        "required_skills": [
            "marketing strategy", "seo", "sem", "google analytics", "social media",
            "content marketing", "email marketing", "crm", "communication",
            "project management", "data analysis", "leadership"
        ],
        "nice_to_have": [
            "hubspot", "salesforce", "mailchimp", "adobe creative suite",
            "a/b testing", "paid advertising", "copywriting", "branding"
        ],
        "keywords": [
            "campaign management", "brand awareness", "lead generation",
            "digital marketing", "roi", "marketing funnel", "customer acquisition",
            "market research", "content strategy", "kpi"
        ]
    },

    "Financial Analyst": {
        "description": """Analyze financial data to support business decisions.
        Build financial models, forecasts, and reports for stakeholders.""",
        "required_skills": [
            "financial modeling", "excel", "accounting", "budgeting",
            "forecasting", "data analysis", "sql", "reporting",
            "communication", "problem solving", "statistics"
        ],
        "nice_to_have": [
            "python", "tableau", "power bi", "bloomberg", "quickbooks",
            "sap", "valuation", "investment analysis", "risk management"
        ],
        "keywords": [
            "financial analysis", "budget", "forecast", "variance analysis",
            "p&l", "cash flow", "revenue", "financial reporting",
            "investment", "roi", "balance sheet", "income statement"
        ]
    },

    "Human Resources Manager": {
        "description": """Oversee recruitment, employee relations, performance management,
        and HR policies. Foster a positive workplace culture and ensure compliance.""",
        "required_skills": [
            "recruitment", "employee relations", "performance management",
            "hr policies", "onboarding", "communication", "leadership",
            "conflict resolution", "compliance", "training", "payroll"
        ],
        "nice_to_have": [
            "workday", "sap hr", "bamboohr", "adp", "talent management",
            "diversity and inclusion", "compensation", "organizational development"
        ],
        "keywords": [
            "talent acquisition", "employee engagement", "workforce planning",
            "hr strategy", "benefits administration", "succession planning",
            "labor relations", "hr compliance", "culture", "retention"
        ]
    },

    "UI/UX Designer": {
        "description": """Design intuitive, beautiful user interfaces and experiences.
        Conduct user research, create wireframes, prototypes, and work with developers.""",
        "required_skills": [
            "figma", "ui design", "ux design", "wireframing", "prototyping",
            "user research", "usability testing", "adobe xd", "sketch",
            "design systems", "typography", "color theory", "communication"
        ],
        "nice_to_have": [
            "html", "css", "illustrator", "photoshop", "motion design",
            "accessibility", "information architecture", "a/b testing"
        ],
        "keywords": [
            "user experience", "user interface", "wireframe", "prototype",
            "usability", "design thinking", "user journey", "interaction design",
            "responsive design", "visual design", "user research"
        ]
    },

    "Sales Manager": {
        "description": """Lead sales teams to meet revenue targets. Build client relationships,
        develop sales strategies, and manage the full sales pipeline.""",
        "required_skills": [
            "sales strategy", "crm", "salesforce", "negotiation", "communication",
            "leadership", "pipeline management", "forecasting", "client relations",
            "presentation", "problem solving", "time management"
        ],
        "nice_to_have": [
            "hubspot", "zoho", "b2b sales", "b2c sales", "account management",
            "cold calling", "business development", "market analysis"
        ],
        "keywords": [
            "revenue growth", "sales target", "pipeline", "quota",
            "client acquisition", "account management", "business development",
            "sales funnel", "closing deals", "customer retention"
        ]
    },

    "Project Manager": {
        "description": """Plan, execute, and close projects on time and within budget.
        Coordinate cross-functional teams, manage risks, and communicate with stakeholders.""",
        "required_skills": [
            "project management", "agile", "scrum", "stakeholder management",
            "risk management", "budgeting", "communication", "leadership",
            "planning", "jira", "ms project", "problem solving"
        ],
        "nice_to_have": [
            "pmp certification", "prince2", "kanban", "confluence", "trello",
            "resource management", "change management", "six sigma"
        ],
        "keywords": [
            "project planning", "delivery", "milestones", "scope management",
            "resource allocation", "risk mitigation", "cross-functional",
            "stakeholder communication", "budget management", "timeline"
        ]
    },

    "Content Writer": {
        "description": """Create compelling written content for blogs, websites, social media,
        and marketing materials. Research topics and tailor content for target audiences.""",
        "required_skills": [
            "writing", "editing", "seo", "research", "communication",
            "content strategy", "social media", "blogging", "copywriting",
            "grammar", "storytelling", "time management"
        ],
        "nice_to_have": [
            "wordpress", "google analytics", "email marketing", "adobe creative suite",
            "video scripting", "technical writing", "proofreading"
        ],
        "keywords": [
            "content creation", "blog posts", "seo writing", "copywriting",
            "editorial", "audience engagement", "brand voice", "content calendar",
            "social media content", "web content"
        ]
    },

    "Healthcare Professional": {
        "description": """Provide patient care, diagnosis, and treatment in clinical settings.
        Collaborate with medical teams and maintain accurate patient records.""",
        "required_skills": [
            "patient care", "clinical skills", "medical knowledge", "communication",
            "empathy", "teamwork", "documentation", "medical terminology",
            "emergency response", "compliance", "problem solving"
        ],
        "nice_to_have": [
            "ehr systems", "epic", "research", "leadership", "training",
            "public health", "telehealth", "medical coding"
        ],
        "keywords": [
            "patient care", "diagnosis", "treatment", "clinical", "healthcare",
            "medical", "nursing", "therapy", "rehabilitation", "health records",
            "patient outcomes", "evidence-based"
        ]
    },

    "Accountant": {
        "description": """Manage financial records, prepare tax returns, and ensure
        regulatory compliance. Analyze financial statements and support audits.""",
        "required_skills": [
            "accounting", "excel", "quickbooks", "tax preparation", "auditing",
            "financial reporting", "bookkeeping", "compliance", "budgeting",
            "communication", "attention to detail", "gaap"
        ],
        "nice_to_have": [
            "sap", "oracle financials", "xero", "cpa certification",
            "forensic accounting", "payroll", "cost accounting"
        ],
        "keywords": [
            "financial statements", "general ledger", "accounts payable",
            "accounts receivable", "tax", "audit", "reconciliation",
            "journal entries", "balance sheet", "compliance", "gaap"
        ]
    },

    "Graphic Designer": {
        "description": """Create visual content for print and digital media.
        Design logos, marketing materials, social media graphics, and brand identities.""",
        "required_skills": [
            "adobe illustrator", "photoshop", "indesign", "typography",
            "color theory", "branding", "layout design", "creativity",
            "communication", "attention to detail", "figma"
        ],
        "nice_to_have": [
            "after effects", "premiere pro", "3d design", "motion graphics",
            "ux design", "video editing", "print design", "web design"
        ],
        "keywords": [
            "visual design", "branding", "logo design", "print design",
            "digital design", "creative direction", "brand identity",
            "illustration", "layout", "typography", "marketing materials"
        ]
    }
}

# ─────────────────────────────────────────────
# ATS KEYWORDS (universal high-value terms)
# ─────────────────────────────────────────────

ATS_POWER_WORDS = [
    "achieved", "improved", "developed", "led", "managed", "created",
    "designed", "implemented", "optimized", "delivered", "built",
    "launched", "increased", "reduced", "automated", "collaborated",
    "mentored", "architected", "deployed", "engineered", "researched",
    "analyzed", "streamlined", "enhanced", "integrated", "scaled"
]

WEAK_VERBS = [
    "worked", "helped", "assisted", "did", "made", "used", "was",
    "involved", "participated", "tried", "attempted", "went", "got"
]

RESUME_SECTIONS = [
    "experience", "education", "skills", "projects", "certifications",
    "summary", "objective", "achievements", "publications", "awards",
    "contact", "references", "languages", "interests", "volunteer"
]

REQUIRED_SECTIONS = ["experience", "education", "skills"]
