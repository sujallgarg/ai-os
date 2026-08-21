import {
  Goal,
  ExecutionTask,
  AgentProfile,
  ApprovalRequest,
  MemoryItem,
  ScheduledTask,
  Job,
  ActivityEvent,
  SystemMetrics
} from "./types";

// ============================================================================
// INITIAL SEED DATA
// ============================================================================

export const INITIAL_AGENTS: AgentProfile[] = [
  {
    id: "email",
    name: "Email Agent",
    role: "Communication & Inbox Automation",
    description: "Connects to Gmail API to search, read, triage, draft responses, and manage thread workflows with approval gates.",
    capabilities: ["email.read", "email.search", "email.draft", "email.reply", "email.archive", "email.classify"],
    tools: ["gmail.search", "gmail.read", "gmail.draft", "gmail.send", "gmail.modify", "gmail.labels"],
    priority: 8,
    status: "available",
    current_task: "Triaging client inbox",
    total_executed: 142,
    success_rate: 98.6,
    avg_latency_ms: 840,
    memory_types: ["shared", "goal", "task", "preference", "result"],
    avatar_bg: "bg-blue-500"
  },
  {
    id: "coding",
    name: "Coding Agent",
    role: "Full-Stack Software Engineering",
    description: "Autonomous code generation, refactoring, dependency analysis, terminal execution, Git version control, and bug diagnostics.",
    capabilities: ["code.read", "code.write", "code.modify", "code.test", "code.debug", "git.commit", "git.push"],
    tools: ["filesystem.read", "filesystem.write", "terminal.execute", "git.commit", "git.push", "git.diff"],
    priority: 9,
    status: "busy",
    current_task: "Synthesizing responsive React layout",
    total_executed: 318,
    success_rate: 96.2,
    avg_latency_ms: 2150,
    memory_types: ["shared", "goal", "task", "preference", "result"],
    avatar_bg: "bg-violet-500"
  },
  {
    id: "browser",
    name: "Browser Agent",
    role: "Web Automation & Visual Testing",
    description: "Automates browser navigation via Playwright, web scraping, form filling, visual regression testing, and live web exploration.",
    capabilities: ["browser.open", "browser.search", "browser.click", "browser.type", "browser.extract", "browser.test", "browser.screenshot"],
    tools: ["playwright.open", "playwright.click", "playwright.extract", "playwright.screenshot", "browser.download"],
    priority: 8,
    status: "available",
    current_task: undefined,
    total_executed: 204,
    success_rate: 94.8,
    avg_latency_ms: 1820,
    memory_types: ["shared", "goal", "task", "result"],
    avatar_bg: "bg-emerald-500"
  },
  {
    id: "calendar",
    name: "Calendar Agent",
    role: "Schedule & Time Optimization",
    description: "Manages Google Calendar events, attendee coordination, meeting scheduling conflicts, and reminder triggers.",
    capabilities: ["calendar.read", "calendar.search", "calendar.create", "calendar.update", "calendar.delete"],
    tools: ["google_calendar.events.list", "google_calendar.events.create", "google_calendar.events.delete"],
    priority: 7,
    status: "available",
    current_task: undefined,
    total_executed: 88,
    success_rate: 100,
    avg_latency_ms: 450,
    memory_types: ["shared", "preference", "result"],
    avatar_bg: "bg-amber-500"
  },
  {
    id: "file",
    name: "File & Storage Agent",
    role: "Cloud & Local Storage Operations",
    description: "Handles secure document parsing, PDF analysis, file search, directory sync, and Google Drive cloud integration.",
    capabilities: ["file.read", "file.write", "file.search", "file.move", "file.delete", "file.parse_pdf"],
    tools: ["filesystem.read", "filesystem.write", "google_drive.list", "google_drive.upload", "pdf.extractor"],
    priority: 7,
    status: "available",
    current_task: undefined,
    total_executed: 165,
    success_rate: 97.4,
    avg_latency_ms: 610,
    memory_types: ["shared", "task", "result"],
    avatar_bg: "bg-orange-500"
  },
  {
    id: "supervisor",
    name: "Supervisor Agent",
    role: "Plan Monitoring & Error Recovery",
    description: "Central monitoring agent that validates execution DAG, detects failure loops, initiates replanning, and enforces security handoffs.",
    capabilities: ["supervise.monitor", "supervise.replan", "supervise.handoff", "supervise.evaluate"],
    tools: ["replanner.generate", "recovery.handle_failure", "memory.inspect"],
    priority: 10,
    status: "available",
    current_task: "Monitoring active task execution DAGs",
    total_executed: 540,
    success_rate: 99.8,
    avg_latency_ms: 320,
    memory_types: ["shared", "goal", "task", "preference", "result"],
    avatar_bg: "bg-indigo-600"
  }
];

export const INITIAL_GOALS: Goal[] = [
  {
    id: "goal-101",
    title: "Build and Test SaaS Landing Page for AI OS",
    description: "Create a modern, high-converting product landing page with dynamic interactive components, run visual tests in browser, and prepare git commit.",
    status: "in_progress",
    progress: 60,
    total_tasks: 5,
    completed_tasks: 3,
    failed_tasks: 0,
    pending_tasks: 2,
    created_at: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    tags: ["frontend", "coding", "testing", "browser"],
    supervisor_decision: {
      action: "CONTINUE",
      reason: "All prior dependencies completed successfully. Task 4 currently executing with Coding Agent.",
      timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString()
    },
    artifacts: [
      { id: "art-1", name: "LandingPage.tsx", type: "code", size: "14.2 KB" },
      { id: "art-2", name: "HeroSection_Preview.png", type: "file", size: "1.4 MB" },
      { id: "art-3", name: "lighthouse_report.json", type: "report", size: "8.1 KB" }
    ],
    tasks: [
      {
        id: 1,
        goalId: "goal-101",
        description: "Analyze design requirements and user preferences for brand styling",
        agent: "coding",
        action: "analyze_requirements",
        tool_name: "filesystem.read",
        parameters: { spec_file: "config/brand_spec.json" },
        depends_on: [],
        priority: 9,
        required_capabilities: ["code.read"],
        status: "completed",
        duration_ms: 1200,
        output: { theme: "light", font: "Inter", primaryColor: "#4f46e5" }
      },
      {
        id: 2,
        goalId: "goal-101",
        description: "Scaffold Next.js component hierarchy with Tailwind CSS classes",
        agent: "coding",
        action: "write_code",
        tool_name: "filesystem.write",
        parameters: { target: "components/landing/Hero.tsx" },
        depends_on: [1],
        priority: 9,
        required_capabilities: ["code.write"],
        status: "completed",
        duration_ms: 2450,
        output: { files_created: ["components/landing/Hero.tsx", "components/landing/Features.tsx"] }
      },
      {
        id: 3,
        goalId: "goal-101",
        description: "Fetch live testimonials and product stats from shared memory",
        agent: "file",
        action: "read_data",
        tool_name: "filesystem.read",
        parameters: { memory_key: "marketing.metrics" },
        depends_on: [1],
        priority: 7,
        required_capabilities: ["file.read"],
        status: "completed",
        duration_ms: 650,
        output: { activeUsers: "45,000+", uptime: "99.99%" }
      },
      {
        id: 4,
        goalId: "goal-101",
        description: "Assemble full landing page layout and connect interactive CTA hooks",
        agent: "coding",
        action: "integrate_page",
        tool_name: "filesystem.write",
        parameters: { page_file: "app/landing/page.tsx" },
        depends_on: [2, 3],
        priority: 8,
        required_capabilities: ["code.write", "code.modify"],
        status: "running",
        started_at: new Date(Date.now() - 1000 * 60 * 3).toISOString()
      },
      {
        id: 5,
        goalId: "goal-101",
        description: "Run automated Playwright browser end-to-end and responsive viewport test",
        agent: "browser",
        action: "test_viewport",
        tool_name: "playwright.extract",
        parameters: { url: "http://localhost:3000/landing", viewports: ["desktop", "mobile"] },
        depends_on: [4],
        priority: 8,
        required_capabilities: ["browser.open", "browser.test"],
        status: "pending"
      }
    ]
  },
  {
    id: "goal-102",
    title: "Executive Inbox Triage and Client Proposal Dispatch",
    description: "Scan recent unread emails, extract partnership inquiries, draft tailored commercial proposals, and request user sign-off prior to sending.",
    status: "in_progress",
    progress: 75,
    total_tasks: 4,
    completed_tasks: 2,
    failed_tasks: 0,
    pending_tasks: 2,
    created_at: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    tags: ["email", "automation", "client", "approvals"],
    supervisor_decision: {
      action: "ASK_USER",
      reason: "Task 3 generated an outbound email with high commercial impact. Awaiting human confirmation.",
      timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString()
    },
    artifacts: [
      { id: "art-4", name: "Executive_Summary_Aug18.md", type: "report", size: "3.8 KB" },
      { id: "art-5", name: "Partnership_Proposal_ApexLabs.pdf", type: "file", size: "420 KB" }
    ],
    tasks: [
      {
        id: 11,
        goalId: "goal-102",
        description: "Query Gmail for high-priority unread messages labeled 'Partner/Client'",
        agent: "email",
        action: "search",
        tool_name: "gmail.search",
        parameters: { query: "is:unread label:important" },
        depends_on: [],
        priority: 9,
        required_capabilities: ["email.search", "email.read"],
        status: "completed",
        duration_ms: 910,
        output: { matchedCount: 3, topSender: "partnerships@apexlabs.ai" }
      },
      {
        id: 12,
        goalId: "goal-102",
        description: "Summarize requirement threads and draft proposal in shared memory",
        agent: "email",
        action: "draft_response",
        tool_name: "gmail.draft",
        parameters: { template: "partnership_standard_tier" },
        depends_on: [11],
        priority: 8,
        required_capabilities: ["email.draft"],
        status: "completed",
        duration_ms: 1540,
        output: { draftId: "draft_8829104", recipient: "sarah@apexlabs.ai" }
      },
      {
        id: 13,
        goalId: "goal-102",
        description: "Send approved partnership proposal email to client",
        agent: "email",
        action: "send_email",
        tool_name: "gmail.send",
        parameters: { draftId: "draft_8829104", to: "sarah@apexlabs.ai" },
        depends_on: [12],
        priority: 9,
        required_capabilities: ["email.reply"],
        status: "waiting_approval"
      },
      {
        id: 14,
        goalId: "goal-102",
        description: "Archive processed emails and schedule follow-up check in calendar",
        agent: "calendar",
        action: "schedule_reminder",
        tool_name: "google_calendar.events.create",
        parameters: { title: "Follow up with Apex Labs", date: "2026-08-22" },
        depends_on: [13],
        priority: 6,
        required_capabilities: ["calendar.create"],
        status: "pending"
      }
    ]
  },
  {
    id: "goal-103",
    title: "Autonomous Competitive Intelligence & Pricing Benchmark",
    description: "Crawl 5 competitor product catalogs, extract feature tiers and API price points, analyze unit costs, and output comparative analysis table.",
    status: "completed",
    progress: 100,
    total_tasks: 4,
    completed_tasks: 4,
    failed_tasks: 0,
    pending_tasks: 0,
    created_at: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    tags: ["research", "browser", "data", "report"],
    supervisor_decision: {
      action: "COMPLETE",
      reason: "All 4 research tasks completed with 100% data coverage. Stored in shared memory under 'market.benchmarks'.",
      timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString()
    },
    artifacts: [
      { id: "art-6", name: "Q3_AI_Pricing_Matrix.csv", type: "data", size: "48 KB" },
      { id: "art-7", name: "Competitor_Intelligence_Brief.pdf", type: "report", size: "2.1 MB" }
    ],
    tasks: [
      {
        id: 21,
        goalId: "goal-103",
        description: "Launch headless browser to scrape pricing tiers across top 5 AI agent vendors",
        agent: "browser",
        action: "extract_pricing",
        tool_name: "playwright.extract",
        parameters: { targets: ["cloud-agent.ai", "hyper-os.com", "agent-stack.io"] },
        depends_on: [],
        priority: 8,
        required_capabilities: ["browser.open", "browser.extract"],
        status: "completed",
        duration_ms: 3400,
        output: { rowsExtracted: 18, vendorsCovered: 5 }
      },
      {
        id: 22,
        goalId: "goal-103",
        description: "Normalize token/seat pricing data and compute median price per million tokens",
        agent: "coding",
        action: "process_data",
        tool_name: "filesystem.write",
        parameters: { script: "scripts/pricing_norm.py" },
        depends_on: [21],
        priority: 7,
        required_capabilities: ["code.write", "code.test"],
        status: "completed",
        duration_ms: 1100,
        output: { medianTokenPrice: "$0.0035/1k", averageSeatPrice: "$49/mo" }
      },
      {
        id: 23,
        goalId: "goal-103",
        description: "Store synthesized intelligence benchmarks into shared memory",
        agent: "file",
        action: "write_memory",
        tool_name: "filesystem.write",
        parameters: { key: "market.benchmarks" },
        depends_on: [22],
        priority: 6,
        required_capabilities: ["file.write"],
        status: "completed",
        duration_ms: 480,
        output: { memoryKey: "market.benchmarks", status: "persisted" }
      },
      {
        id: 24,
        goalId: "goal-103",
        description: "Generate executive presentation and markdown summary",
        agent: "coding",
        action: "generate_report",
        tool_name: "filesystem.write",
        parameters: { target: "reports/market_report.md" },
        depends_on: [23],
        priority: 8,
        required_capabilities: ["code.write"],
        status: "completed",
        duration_ms: 1850,
        output: { reportFile: "Competitor_Intelligence_Brief.pdf" }
      }
    ]
  },
  {
    id: "goal-104",
    title: "Database Backup and Cloud Storage Encryption Verification",
    description: "Perform scheduled full backup of persistent memory store, verify AES-256 encryption hashes, and rotate access keys.",
    status: "queued",
    progress: 0,
    total_tasks: 3,
    completed_tasks: 0,
    failed_tasks: 0,
    pending_tasks: 3,
    created_at: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
    tags: ["security", "database", "maintenance"],
    tasks: [
      {
        id: 31,
        goalId: "goal-104",
        description: "Snapshot memory database SQLite tables",
        agent: "file",
        action: "snapshot",
        tool_name: "filesystem.read",
        parameters: { source: "data/memory.db" },
        depends_on: [],
        priority: 7,
        required_capabilities: ["file.read"],
        status: "ready"
      },
      {
        id: 32,
        goalId: "goal-104",
        description: "Encrypt snapshot and push to secure secondary storage",
        agent: "file",
        action: "encrypt_upload",
        tool_name: "google_drive.upload",
        parameters: { destination: "backups/2026-08-18.enc" },
        depends_on: [31],
        priority: 8,
        required_capabilities: ["file.write"],
        status: "pending"
      },
      {
        id: 33,
        goalId: "goal-104",
        description: "Log verification integrity signature in audit trail",
        agent: "supervisor",
        action: "audit_log",
        tool_name: "recovery.handle_failure",
        parameters: { verifySignature: true },
        depends_on: [32],
        priority: 6,
        required_capabilities: ["supervise.monitor"],
        status: "pending"
      }
    ]
  }
];

export const INITIAL_APPROVALS: ApprovalRequest[] = [
  {
    id: "appr-1",
    agent_id: "email",
    agent_name: "Email Agent",
    tool_name: "gmail.send",
    action: "send_email",
    parameters: {
      recipient: "sarah@apexlabs.ai",
      subject: "Partnership Proposal: AI Operating System Deployment",
      body_preview: "Hi Sarah,\n\nFollowing our review of Apex Labs requirements, we have prepared the custom enterprise architecture specification...",
      attachments: ["Partnership_Proposal_ApexLabs.pdf"]
    },
    reason: "Outbound communication to external corporate client with commercial commitment.",
    risk_level: "high",
    status: "pending",
    created_at: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
    task_id: 13,
    goal_id: "goal-102"
  },
  {
    id: "appr-2",
    agent_id: "coding",
    agent_name: "Coding Agent",
    tool_name: "git.push",
    action: "push_to_remote",
    parameters: {
      repository: "sujallgarg/ai-os",
      branch: "main",
      commit_count: 3,
      last_commit_msg: "Deploy dynamic multi-agent task execution visualizer"
    },
    reason: "Modifying production branch repository directly.",
    risk_level: "medium",
    status: "pending",
    created_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
    task_id: 4,
    goal_id: "goal-101"
  },
  {
    id: "appr-3",
    agent_id: "coding",
    agent_name: "Coding Agent",
    tool_name: "terminal.execute",
    action: "system_command",
    parameters: {
      command: "npm run build && docker build -t ai-os-core:latest .",
      environment: "production"
    },
    reason: "Executing root level build and containerization commands.",
    risk_level: "medium",
    status: "approved",
    created_at: new Date(Date.now() - 1000 * 60 * 80).toISOString(),
    resolved_at: new Date(Date.now() - 1000 * 60 * 75).toISOString(),
    resolved_by: "Administrator (Sujal)"
  }
];

export const INITIAL_MEMORIES: MemoryItem[] = [
  {
    key: "user.theme.preference",
    value: "Light theme only with high-contrast slate typography and indigo accents",
    agent_id: "supervisor",
    memory_type: "preference",
    importance: 10,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    metadata: { source: "user_directive", immutable: true }
  },
  {
    key: "client.theme",
    value: "dark",
    agent_id: "email",
    memory_type: "preference",
    importance: 9,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
    metadata: { context: "apexlabs_preferences" }
  },
  {
    key: "system.concurrency_limit",
    value: { maxParallelAgents: 4, taskTimeoutSeconds: 60 },
    agent_id: "supervisor",
    memory_type: "shared",
    importance: 8,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString()
  },
  {
    key: "market.benchmarks",
    value: { medianTokenPrice: "$0.0035/1k", averageSeatPrice: "$49/mo", competitorsSampled: 5 },
    agent_id: "browser",
    memory_type: "result",
    importance: 8,
    created_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    metadata: { goal_id: "goal-103" }
  },
  {
    key: "email.triage.whitelist",
    value: ["@apexlabs.ai", "@deepmind.google.com", "@startup.co"],
    agent_id: "email",
    memory_type: "preference",
    importance: 7,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString()
  },
  {
    key: "github.default_repo",
    value: "sujallgarg/ai-os",
    agent_id: "coding",
    memory_type: "shared",
    importance: 6,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString()
  }
];

export const INITIAL_SCHEDULES: ScheduledTask[] = [
  {
    id: "sched-1",
    name: "Morning Executive Inbox Triage",
    goal_prompt: "Check Gmail for priority client threads, summarize action items, and draft replies",
    cron_or_interval: "0 8 * * 1-5 (Weekdays at 8:00 AM)",
    run_at: new Date(Date.now() + 1000 * 60 * 60 * 11).toISOString(),
    last_run: new Date(Date.now() - 1000 * 60 * 60 * 13).toISOString(),
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 11).toISOString(),
    recurring: true,
    interval_seconds: 86400,
    enabled: true,
    target_agent: "email"
  },
  {
    id: "sched-2",
    name: "Nightly Automated Security & Backup Sync",
    goal_prompt: "Snapshot persistent database tables, test AES-256 hashes, and archive to cloud",
    cron_or_interval: "0 2 * * * (Daily at 2:00 AM)",
    run_at: new Date(Date.now() + 1000 * 60 * 60 * 5).toISOString(),
    last_run: new Date(Date.now() - 1000 * 60 * 60 * 19).toISOString(),
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 5).toISOString(),
    recurring: true,
    interval_seconds: 86400,
    enabled: true,
    target_agent: "file"
  },
  {
    id: "sched-3",
    name: "Weekly Competitor Intelligence Scan",
    goal_prompt: "Crawl top 5 competitor product catalogs and update pricing benchmark memory",
    cron_or_interval: "0 9 * * 1 (Every Monday at 9:00 AM)",
    run_at: new Date(Date.now() + 1000 * 60 * 60 * 120).toISOString(),
    last_run: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 120).toISOString(),
    recurring: true,
    interval_seconds: 604800,
    enabled: true,
    target_agent: "browser"
  }
];

export const INITIAL_JOBS: Job[] = [
  {
    id: "job-801",
    goal: "Build and Test SaaS Landing Page for AI OS",
    status: "running",
    progress: 60,
    created_at: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 24).toISOString(),
    logs: [
      { timestamp: "20:30:12", level: "info", message: "[Planner] Decomposed goal into 5 task execution graph." },
      { timestamp: "20:30:14", level: "info", message: "[Capability Matcher] Assigned tasks to Coding, File, Browser agents." },
      { timestamp: "20:31:02", level: "info", message: "[TaskRunner] Task 1 completed (1200ms)." },
      { timestamp: "20:33:45", level: "info", message: "[TaskRunner] Task 2 completed (2450ms)." },
      { timestamp: "20:34:30", level: "info", message: "[TaskRunner] Task 3 completed (650ms)." },
      { timestamp: "20:36:15", level: "info", message: "[TaskRunner] Task 4 currently executing with Coding Agent." }
    ]
  },
  {
    id: "job-802",
    goal: "Autonomous Competitive Intelligence & Pricing Benchmark",
    status: "completed",
    progress: 100,
    created_at: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 179).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    result: { status: "success", artifactsGenerated: 2, memoryUpdated: true },
    logs: [
      { timestamp: "18:00:00", level: "info", message: "[Supervisor] Started execution plan with 4 tasks." },
      { timestamp: "18:05:40", level: "info", message: "[Browser] Extracted 18 data points across 5 vendor targets." },
      { timestamp: "18:08:12", level: "info", message: "[Coding] Normalized token calculation models." },
      { timestamp: "18:09:00", level: "info", message: "[Memory] Saved benchmarks into shared cluster." },
      { timestamp: "18:10:00", level: "info", message: "[Supervisor] Plan complete. 100% success rate." }
    ]
  },
  {
    id: "job-803",
    goal: "Executive Inbox Triage and Client Proposal Dispatch",
    status: "running",
    progress: 75,
    created_at: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 44).toISOString(),
    logs: [
      { timestamp: "20:10:00", level: "info", message: "[Email] Scanned 12 unread inbox threads." },
      { timestamp: "20:12:30", level: "info", message: "[Email] Generated custom proposal draft for sarah@apexlabs.ai." },
      { timestamp: "20:13:00", level: "warn", message: "[Permissions] gmail.send triggered security policy: ASK_USER." },
      { timestamp: "20:13:02", level: "info", message: "[ApprovalManager] Created approval ticket appr-1. Pausing task 13." }
    ]
  }
];

export const INITIAL_ACTIVITY: ActivityEvent[] = [
  {
    id: "act-1",
    timestamp: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
    agent_id: "coding",
    agent_name: "Coding Agent",
    event_type: "task_started",
    title: "Task #4 Started",
    description: "Integrating hero section CTA hooks and state bindings in page layout.",
    severity: "info",
    goal_id: "goal-101",
    task_id: 4
  },
  {
    id: "act-2",
    timestamp: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
    agent_id: "email",
    agent_name: "Email Agent",
    event_type: "approval_required",
    title: "Human Approval Requested",
    description: "Outbound message to client requires confirmation before dispatch.",
    severity: "warning",
    goal_id: "goal-102",
    task_id: 13
  },
  {
    id: "act-3",
    timestamp: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    agent_id: "file",
    agent_name: "File Agent",
    event_type: "task_completed",
    title: "Task #3 Completed",
    description: "Retrieved client metrics and testimonial records from storage.",
    severity: "success",
    goal_id: "goal-101",
    task_id: 3
  },
  {
    id: "act-4",
    timestamp: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
    agent_id: "supervisor",
    agent_name: "Supervisor Agent",
    event_type: "goal_created",
    title: "Goal Dispatched",
    description: "Decomposed 'Build and Test SaaS Landing Page' into 5 connected tasks.",
    severity: "info",
    goal_id: "goal-101"
  },
  {
    id: "act-5",
    timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    agent_id: "supervisor",
    agent_name: "Supervisor Agent",
    event_type: "task_completed",
    title: "Goal Completed: Market Research",
    description: "Finished competitive intelligence gathering with 100% success.",
    severity: "success",
    goal_id: "goal-103"
  }
];

// ============================================================================
// STORAGE HELPERS (with localStorage support)
// ============================================================================

const STORAGE_KEYS = {
  GOALS: "ai_os_goals_v1",
  AGENTS: "ai_os_agents_v1",
  APPROVALS: "ai_os_approvals_v1",
  MEMORIES: "ai_os_memories_v1",
  SCHEDULES: "ai_os_schedules_v1",
  JOBS: "ai_os_jobs_v1",
  ACTIVITY: "ai_os_activity_v1",
};

function getStored<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : fallback;
  } catch {
    return fallback;
  }
}

function setStored<T>(key: string, value: T): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (err) {
    console.error("Storage error:", err);
  }
}

// ============================================================================
// API CLIENT IMPLEMENTATION
// ============================================================================

export class AIOSClient {
  // Goals
  static getGoals(): Goal[] {
    return getStored(STORAGE_KEYS.GOALS, INITIAL_GOALS);
  }

  static getGoal(id: string): Goal | undefined {
    return this.getGoals().find((g) => g.id === id);
  }

  static createGoal(title: string, description?: string): Goal {
    const goals = this.getGoals();
    const newId = `goal-${Date.now().toString().slice(-4)}`;
    const desc = description || title;

    // Intelligent automated task decomposition logic based on goal content
    const tasks: ExecutionTask[] = [];
    const lower = (title + " " + desc).toLowerCase();

    if (lower.includes("email") || lower.includes("inbox") || lower.includes("gmail")) {
      tasks.push({
        id: 1,
        goalId: newId,
        description: "Search email inbox for relevant threads and attachments",
        agent: "email",
        action: "search",
        tool_name: "gmail.search",
        parameters: { query: title },
        depends_on: [],
        priority: 9,
        required_capabilities: ["email.search", "email.read"],
        status: "ready"
      });
      tasks.push({
        id: 2,
        goalId: newId,
        description: "Synthesize email content and draft appropriate action plan",
        agent: "email",
        action: "draft",
        tool_name: "gmail.draft",
        parameters: { goal: title },
        depends_on: [1],
        priority: 8,
        required_capabilities: ["email.draft"],
        status: "pending"
      });
    }

    if (lower.includes("code") || lower.includes("build") || lower.includes("website") || lower.includes("app") || lower.includes("saas") || lower.includes("frontend") || lower.includes("backend")) {
      const dep = tasks.length > 0 ? [tasks.length] : [];
      tasks.push({
        id: tasks.length + 1,
        goalId: newId,
        description: "Implement code architecture and functional components",
        agent: "coding",
        action: "write_code",
        tool_name: "filesystem.write",
        parameters: { goal: title },
        depends_on: dep,
        priority: 9,
        required_capabilities: ["code.write", "code.test"],
        status: dep.length === 0 ? "ready" : "pending"
      });
    }

    if (lower.includes("test") || lower.includes("browser") || lower.includes("web") || lower.includes("research") || lower.includes("competitor") || lower.includes("website")) {
      const dep = tasks.length > 0 ? [tasks.length] : [];
      tasks.push({
        id: tasks.length + 1,
        goalId: newId,
        description: "Perform browser automation, live navigation, and quality check",
        agent: "browser",
        action: "browser_action",
        tool_name: "playwright.open",
        parameters: { goal: title },
        depends_on: dep,
        priority: 8,
        required_capabilities: ["browser.open", "browser.test"],
        status: dep.length === 0 ? "ready" : "pending"
      });
    }

    if (tasks.length === 0) {
      tasks.push({
        id: 1,
        goalId: newId,
        description: "Decompose objective and coordinate execution strategy",
        agent: "supervisor",
        action: "coordinate",
        tool_name: "replanner.generate",
        parameters: { objective: title },
        depends_on: [],
        priority: 8,
        required_capabilities: ["supervise.monitor"],
        status: "ready"
      });
      tasks.push({
        id: 2,
        goalId: newId,
        description: "Execute primary task action items",
        agent: "coding",
        action: "execute",
        tool_name: "filesystem.write",
        parameters: { goal: title },
        depends_on: [1],
        priority: 7,
        required_capabilities: ["code.write"],
        status: "pending"
      });
    }

    const newGoal: Goal = {
      id: newId,
      title,
      description: desc,
      status: "in_progress",
      progress: 0,
      total_tasks: tasks.length,
      completed_tasks: 0,
      failed_tasks: 0,
      pending_tasks: tasks.length,
      tasks,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      tags: ["autonomous", "multi-agent"],
      supervisor_decision: {
        action: "CONTINUE",
        reason: "Initial plan generated with " + tasks.length + " connected tasks.",
        timestamp: new Date().toISOString()
      },
      artifacts: []
    };

    const updated = [newGoal, ...goals];
    setStored(STORAGE_KEYS.GOALS, updated);

    // Also add to Activity and Jobs
    this.addActivity({
      event_type: "goal_created",
      title: `Goal Dispatched: ${title.slice(0, 30)}...`,
      description: `Created execution DAG with ${tasks.length} tasks across ${new Set(tasks.map((t) => t.agent)).size} agents.`,
      severity: "info",
      goal_id: newId
    });

    this.createJob(title);

    return newGoal;
  }

  static updateGoalTask(goalId: string, taskId: number, updates: Partial<ExecutionTask>): Goal | undefined {
    const goals = this.getGoals();
    const goalIndex = goals.findIndex((g) => g.id === goalId);
    if (goalIndex === -1) return undefined;

    const goal = goals[goalIndex];
    const taskIndex = goal.tasks.findIndex((t) => t.id === taskId);
    if (taskIndex === -1) return undefined;

    goal.tasks[taskIndex] = { ...goal.tasks[taskIndex], ...updates };

    // Recompute goal metrics
    const completed = goal.tasks.filter((t) => t.status === "completed").length;
    const failed = goal.tasks.filter((t) => t.status === "failed").length;
    goal.completed_tasks = completed;
    goal.failed_tasks = failed;
    goal.pending_tasks = goal.total_tasks - completed - failed;
    goal.progress = Math.round((completed / goal.total_tasks) * 100);
    goal.updated_at = new Date().toISOString();

    if (completed === goal.total_tasks) {
      goal.status = "completed";
      goal.completed_at = new Date().toISOString();
      goal.supervisor_decision = {
        action: "COMPLETE",
        reason: "All tasks completed successfully.",
        timestamp: new Date().toISOString()
      };
    } else if (failed > 0 && goal.pending_tasks === 0) {
      goal.status = "partial_failure";
    }

    goals[goalIndex] = goal;
    setStored(STORAGE_KEYS.GOALS, goals);
    return goal;
  }

  // Agents
  static getAgents(): AgentProfile[] {
    return getStored(STORAGE_KEYS.AGENTS, INITIAL_AGENTS);
  }

  static getAgent(id: string): AgentProfile | undefined {
    return this.getAgents().find((a) => a.id === id);
  }

  // Approvals
  static getApprovals(): ApprovalRequest[] {
    return getStored(STORAGE_KEYS.APPROVALS, INITIAL_APPROVALS);
  }

  static approveRequest(id: string, reviewer = "Administrator"): ApprovalRequest | undefined {
    const approvals = this.getApprovals();
    const index = approvals.findIndex((a) => a.id === id);
    if (index === -1) return undefined;

    const req = approvals[index];
    req.status = "approved";
    req.resolved_at = new Date().toISOString();
    req.resolved_by = reviewer;
    approvals[index] = req;
    setStored(STORAGE_KEYS.APPROVALS, approvals);

    // If attached to a task, update task to ready/running
    if (req.goal_id && req.task_id) {
      this.updateGoalTask(req.goal_id, req.task_id, {
        status: "running",
        started_at: new Date().toISOString()
      });
    }

    this.addActivity({
      agent_id: req.agent_id,
      agent_name: req.agent_name,
      event_type: "approval_granted",
      title: `Approval Granted: ${req.action}`,
      description: `Action ${req.tool_name} was approved by ${reviewer}.`,
      severity: "success",
      goal_id: req.goal_id,
      task_id: req.task_id
    });

    return req;
  }

  static rejectRequest(id: string, reviewer = "Administrator"): ApprovalRequest | undefined {
    const approvals = this.getApprovals();
    const index = approvals.findIndex((a) => a.id === id);
    if (index === -1) return undefined;

    const req = approvals[index];
    req.status = "rejected";
    req.resolved_at = new Date().toISOString();
    req.resolved_by = reviewer;
    approvals[index] = req;
    setStored(STORAGE_KEYS.APPROVALS, approvals);

    if (req.goal_id && req.task_id) {
      this.updateGoalTask(req.goal_id, req.task_id, {
        status: "failed",
        error: "Action rejected by security approval policy."
      });
    }

    this.addActivity({
      agent_id: req.agent_id,
      agent_name: req.agent_name,
      event_type: "approval_rejected",
      title: `Approval Denied: ${req.action}`,
      description: `Action ${req.tool_name} was rejected by ${reviewer}.`,
      severity: "error",
      goal_id: req.goal_id,
      task_id: req.task_id
    });

    return req;
  }

  // Memory
  static getMemories(): MemoryItem[] {
    return getStored(STORAGE_KEYS.MEMORIES, INITIAL_MEMORIES);
  }

  static addMemory(item: Omit<MemoryItem, "created_at" | "updated_at">): MemoryItem {
    const memories = this.getMemories();
    const existingIndex = memories.findIndex((m) => m.key === item.key);
    const now = new Date().toISOString();

    const newMemory: MemoryItem = {
      ...item,
      created_at: existingIndex >= 0 ? memories[existingIndex].created_at : now,
      updated_at: now
    };

    if (existingIndex >= 0) {
      memories[existingIndex] = newMemory;
    } else {
      memories.unshift(newMemory);
    }

    setStored(STORAGE_KEYS.MEMORIES, memories);

    this.addActivity({
      agent_id: item.agent_id,
      event_type: "memory_write",
      title: `Memory Stored: ${item.key}`,
      description: `Type: ${item.memory_type}, Importance: ${item.importance}/10`,
      severity: "info"
    });

    return newMemory;
  }

  static forgetMemory(key: string): boolean {
    const memories = this.getMemories();
    const filtered = memories.filter((m) => m.key !== key);
    if (filtered.length === memories.length) return false;
    setStored(STORAGE_KEYS.MEMORIES, filtered);
    return true;
  }

  // Schedules
  static getSchedules(): ScheduledTask[] {
    return getStored(STORAGE_KEYS.SCHEDULES, INITIAL_SCHEDULES);
  }

  static addSchedule(task: Omit<ScheduledTask, "id">): ScheduledTask {
    const schedules = this.getSchedules();
    const newSchedule: ScheduledTask = {
      ...task,
      id: `sched-${Date.now().toString().slice(-4)}`
    };
    schedules.push(newSchedule);
    setStored(STORAGE_KEYS.SCHEDULES, schedules);
    return newSchedule;
  }

  static toggleSchedule(id: string): ScheduledTask | undefined {
    const schedules = this.getSchedules();
    const index = schedules.findIndex((s) => s.id === id);
    if (index === -1) return undefined;

    schedules[index].enabled = !schedules[index].enabled;
    setStored(STORAGE_KEYS.SCHEDULES, schedules);
    return schedules[index];
  }

  static runScheduleNow(id: string): Goal | undefined {
    const schedule = this.getSchedules().find((s) => s.id === id);
    if (!schedule) return undefined;
    return this.createGoal(schedule.name, schedule.goal_prompt);
  }

  // Jobs
  static getJobs(): Job[] {
    return getStored(STORAGE_KEYS.JOBS, INITIAL_JOBS);
  }

  static getJob(id: string): Job | undefined {
    return this.getJobs().find((j) => j.id === id);
  }

  static createJob(goal: string): Job {
    const jobs = this.getJobs();
    const newJob: Job = {
      id: `job-${Date.now().toString().slice(-4)}`,
      goal,
      status: "running",
      progress: 10,
      created_at: new Date().toISOString(),
      started_at: new Date().toISOString(),
      logs: [
        { timestamp: new Date().toLocaleTimeString(), level: "info", message: `[Planner] Initialized autonomous job for '${goal.slice(0, 40)}...'` },
        { timestamp: new Date().toLocaleTimeString(), level: "info", message: "[Supervisor] Validating task dependency graph and security profile." }
      ]
    };
    jobs.unshift(newJob);
    setStored(STORAGE_KEYS.JOBS, jobs);
    return newJob;
  }

  // Activity
  static getActivity(): ActivityEvent[] {
    return getStored(STORAGE_KEYS.ACTIVITY, INITIAL_ACTIVITY);
  }

  static addActivity(event: Omit<ActivityEvent, "id" | "timestamp">): ActivityEvent {
    const activities = this.getActivity();
    const newEvent: ActivityEvent = {
      ...event,
      id: `act-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString()
    };
    activities.unshift(newEvent);
    if (activities.length > 100) activities.pop();
    setStored(STORAGE_KEYS.ACTIVITY, activities);
    return newEvent;
  }

  // Metrics
  static getMetrics(): SystemMetrics {
    const goals = this.getGoals();
    const agents = this.getAgents();
    const approvals = this.getApprovals();
    const memories = this.getMemories();
    const schedules = this.getSchedules();

    const activeGoals = goals.filter((g) => g.status === "in_progress").length;
    const totalGoalsCompleted = goals.filter((g) => g.status === "completed").length;
    const activeAgents = agents.filter((a) => a.status === "busy" || a.status === "available").length;
    const pendingApprovals = approvals.filter((a) => a.status === "pending").length;

    const allTasks = goals.flatMap((g) => g.tasks);
    const completedTasks = allTasks.filter((t) => t.status === "completed").length;
    const successRate = allTasks.length > 0 ? Math.round((completedTasks / allTasks.length) * 100) : 98;

    return {
      activeGoals,
      totalGoalsCompleted,
      activeAgents,
      totalAgents: agents.length,
      pendingApprovals,
      totalTasksExecuted: allTasks.length,
      successRate,
      avgTaskDurationMs: 1420,
      memoryItemsCount: memories.length,
      scheduledJobsCount: schedules.length
    };
  }
}

export const getAgents = () => AIOSClient.getAgents();
export const getApprovals = () => AIOSClient.getApprovals();
export const getJobs = () => AIOSClient.getJobs();
export const createGoal = (goal: string) => AIOSClient.createGoal(goal);
export const getJob = (id: string) => AIOSClient.getJob(id);
export const approveRequest = (id: string) => AIOSClient.approveRequest(id);
export const rejectRequest = (id: string) => AIOSClient.rejectRequest(id);

