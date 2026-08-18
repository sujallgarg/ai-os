export type GoalStatusType = 'in_progress' | 'completed' | 'partial_failure' | 'failed' | 'queued' | 'paused';

export type TaskStatusType = 'pending' | 'ready' | 'running' | 'completed' | 'failed' | 'retrying' | 'replanned' | 'waiting_approval' | 'cancelled';

export type AgentStatusType = 'available' | 'busy' | 'offline' | 'error';

export type ApprovalStatusType = 'pending' | 'approved' | 'rejected' | 'expired';

export type MemoryType = 'shared' | 'goal' | 'task' | 'preference' | 'result' | 'private';

export type JobStatusType = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';

export type ActivitySeverity = 'info' | 'success' | 'warning' | 'error';

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export type SupervisorActionType = 'CONTINUE' | 'REPLAN' | 'HANDOFF' | 'ASK_USER' | 'FAIL' | 'COMPLETE';

export interface ExecutionTask {
  id: number;
  goalId?: string;
  description: string;
  agent: string | null;
  action: string;
  tool_name?: string | null;
  parameters: Record<string, any>;
  depends_on: number[];
  priority: number;
  required_capabilities: string[];
  status: TaskStatusType;
  retry_count?: number;
  max_retries?: number;
  output?: any;
  error?: string | null;
  started_at?: string;
  completed_at?: string;
  duration_ms?: number;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  status: GoalStatusType;
  progress: number;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  pending_tasks: number;
  tasks: ExecutionTask[];
  created_at: string;
  updated_at: string;
  completed_at?: string;
  tags: string[];
  supervisor_decision?: {
    action: SupervisorActionType;
    reason: string;
    timestamp: string;
  };
  artifacts?: {
    id: string;
    name: string;
    type: 'file' | 'report' | 'code' | 'url' | 'data';
    url?: string;
    content?: string;
    size?: string;
  }[];
}

export interface AgentProfile {
  id: string;
  name: string;
  role: string;
  description: string;
  capabilities: string[];
  tools: string[];
  priority: number;
  status: AgentStatusType;
  current_task?: string;
  total_executed: number;
  success_rate: number;
  avg_latency_ms: number;
  memory_types: string[];
  avatar_bg?: string;
}

export interface ApprovalRequest {
  id: string;
  agent_id: string;
  agent_name?: string;
  tool_name: string;
  action: string;
  parameters: Record<string, any>;
  reason: string;
  risk_level: RiskLevel;
  status: ApprovalStatusType;
  created_at: string;
  resolved_at?: string;
  resolved_by?: string;
  task_id?: number;
  goal_id?: string;
}

export interface MemoryItem {
  key: string;
  value: any;
  agent_id: string;
  memory_type: MemoryType;
  importance: number; // 1-10
  created_at: string;
  updated_at: string;
  expires_at?: string;
  metadata?: Record<string, any>;
}

export interface ScheduledTask {
  id: string;
  name: string;
  goal_prompt: string;
  cron_or_interval: string;
  run_at: string;
  last_run?: string;
  next_run: string;
  recurring: boolean;
  interval_seconds?: number;
  enabled: boolean;
  target_agent?: string;
  task_data?: Record<string, any>;
}

export interface Job {
  id: string;
  goal: string;
  status: JobStatusType;
  progress: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  result?: any;
  error?: string | null;
  logs: {
    timestamp: string;
    level: 'info' | 'warn' | 'error';
    message: string;
  }[];
}

export interface ActivityEvent {
  id: string;
  timestamp: string;
  agent_id?: string;
  agent_name?: string;
  event_type: 'goal_created' | 'task_started' | 'task_completed' | 'task_failed' | 'retry' | 'replan' | 'approval_required' | 'approval_granted' | 'approval_rejected' | 'memory_write' | 'handoff';
  title: string;
  description: string;
  severity: ActivitySeverity;
  metadata?: Record<string, any>;
  goal_id?: string;
  task_id?: number;
}

export interface SystemMetrics {
  activeGoals: number;
  totalGoalsCompleted: number;
  activeAgents: number;
  totalAgents: number;
  pendingApprovals: number;
  totalTasksExecuted: number;
  successRate: number;
  avgTaskDurationMs: number;
  memoryItemsCount: number;
  scheduledJobsCount: number;
}
