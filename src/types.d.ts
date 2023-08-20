/**
 * Application specific interfaces
 */
export interface Config {
  portainer: PortainerConfig;
  stack: StackConfig;
}

export interface PortainerConfig {
  url: URL;
  apiKey: string;
  endpoint: string;
}

export interface StackConfig {
  name: string;
  file: string;
}

export interface Stack {
  id: number;
  name: string;
}

export interface StackResponse {
  stack: Stack;
  response: string;
}

export interface CreateStackPayload {
  name: string;
  endpoint: number;
  file: string;
}

export interface UpdateStackPayload {
  id: number;
  endpoint: number;
  file: string;
  prune: boolean;
}

/**
 * Portainer specific interfaces
 */
export interface PortainerStack {
  Id: number;
  Name: string;
}
