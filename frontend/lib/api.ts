const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export interface Goal {
  job_id: string;
  goal: string;
  status: string;
  progress?: number;
  result?: unknown;
  error?: string | null;
}

export interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  result?: unknown;
  error?: string | null;
}

export interface Agent {
  name: string;
  description: string;
  capabilities: string[];
  tools: string[];
  priority: number;
  status: string;
}

export interface Approval {
  id: string;
  agent_id: string;
  tool_name: string;
  action: string;
  parameters: Record<string, unknown>;
  reason: string;
  status: string;
}

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type":
          "application/json",
        ...(options?.headers || {})
      },
      cache: "no-store"
    }
  );

  if (!response.ok) {

    const message =
      await response.text();

    throw new Error(
      message ||
      `API request failed: ${response.status}`
    );
  }

  return response.json();
}


export async function createGoal(
  goal: string
): Promise<Goal> {

  return request<Goal>(
    "/goals",
    {
      method: "POST",

      body: JSON.stringify({
        goal
      })
    }
  );
}


export async function getJob(
  jobId: string
): Promise<Job> {

  return request<Job>(
    `/jobs/${jobId}`
  );
}


export async function getJobs():
  Promise<Job[]> {

  return request<Job[]>(
    "/jobs"
  );
}


export async function getAgents():
  Promise<Agent[]> {

  return request<Agent[]>(
    "/agents"
  );
}


export async function getApprovals():
  Promise<Approval[]> {

  return request<Approval[]>(
    "/approvals"
  );
}


export async function approveRequest(
  requestId: string
) {

  return request(
    `/approvals/${requestId}/approve`,
    {
      method: "POST"
    }
  );
}


export async function rejectRequest(
  requestId: string
) {

  return request(
    `/approvals/${requestId}/reject`,
    {
      method: "POST"
    }
  );
}