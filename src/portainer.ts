import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import {
  CreateStackPayload,
  PortainerStack,
  Stack,
  UpdateStackPayload,
} from "./types";

export class PortainerClient {
  private readonly client: AxiosInstance;

  constructor(url: URL, apiKey: string) {
    if (url.pathname !== "/api/") {
      url.pathname = "/api/";
    }

    /**
     * Create axios instance for requests.
     */
    this.client = axios.create({
      baseURL: url.toString(),
    });

    /**
     * Create Axios Interceptor for Authorization header if token is set.
     */
    this.client.interceptors.request.use(
      (config: AxiosRequestConfig): AxiosRequestConfig => {
        config.headers["X-API-Key"] = `Bearer ${apiKey}`;

        return config;
      }
    );
  }

  /**
   * Retrieve all existing endpoints from portainer.
   *
   */
  async getEndpoints(): Promise<Stack[]> {
    const { data }: { data: PortainerStack[] } = await this.client.get(
      "/endpoints"
    );

    return data.map((item) => ({
      id: item.Id,
      name: item.Name,
    }));
  }

  /**
   * Retrieve all existing stacks from portainer.
   *
   */
  async getStacks(): Promise<Stack[]> {
    const { data }: { data: PortainerStack[] } = await this.client.get(
      "/stacks"
    );

    return data.map((item) => ({
      id: item.Id,
      name: item.Name,
    }));
  }

  /**
   * Create new stack and return name and id of it.
   *
   * @param payload {CreateStackPayload} - Payload for the stack to be created.
   */
  async createStack(payload: CreateStackPayload) {
    await this.client.post(
      "/stacks",
      {
        name: payload.name,
        stackFileContent: payload.file,
        env: [
          {
            name: "DOTENV_KEY",
            value: process.env.DOTENV_KEY,
          },
        ],
      },
      {
        params: {
          endpointId: payload.endpoint,
          method: "string",
          type: 1,
        },
      }
    );
  }

  /**
   * Update existing stack with given data.
   *
   * @param payload {UpdateStackPayload} - Payload for the stack to be updated.
   */
  async updateStack(payload: UpdateStackPayload): Promise<Stack> {
    const { data }: { data: PortainerStack } = await this.client.put(
      `/stacks/${payload.id}`,
      {
        stackFileContent: payload.file,
        prune: payload.prune,
        env: [
          {
            name: "DOTENV_KEY",
            value: process.env.DOTENV_KEY,
          },
        ],
      },
      {
        params: {
          endpointId: payload.endpoint,
        },
      }
    );

    return {
      id: data.Id,
      name: data.Name,
    };
  }
}
