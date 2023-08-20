import * as core from "@actions/core";
import axios, { AxiosError } from "axios";
import * as config from "./config";
import { PortainerClient } from "./portainer";
import error from "./utils";

if (!process.env.DOTENV_KEY) error("DOTENV_KEY not set");
require("dotenv-vault-core").config();
async function run() {
  try {
    const cfg = config.parse();

    core.startGroup("Authentication");
    const portainer = new PortainerClient(
      cfg.portainer.url,
      cfg.portainer.apiKey
    );

    core.startGroup("Get current state");
    const endpoints = await portainer.getEndpoints();
    core.debug(`Found Endpoints`);
    let endpoint =
      endpoints.find((item) => item.name === cfg.portainer.endpoint) ??
      error(`Endpoint ${cfg.portainer.endpoint} not found`);
    const stacks = await portainer.getStacks();
    core.debug(`Found Stacks`);

    let stack = stacks.find((item) => item.name === cfg.stack.name);
    core.endGroup();

    if (stack) {
      core.debug(`Attempting to update stack: ${stack}`);

      core.startGroup("Update existing stack");
      core.info(
        `Updating existing stack (NAME: ${stack.name}; ID: ${stack.id}; prune: true)...`
      );
      await portainer.updateStack({
        id: stack.id,
        endpoint: endpoint.id,
        file: cfg.stack.file,
        prune: true,
      });
      core.info("Stack updated.");
      core.endGroup();
    } else {
      core.startGroup("Create new stack");
      core.info("Creating new stack...");
      core.debug(`Attempting to create stack: ${cfg.stack.name}`);
      core.debug(`Stack parsed: ${cfg.stack.file}`);

      try {
        await portainer.createStack({
          endpoint: endpoint.id,
          name: cfg.stack.name,
          file: cfg.stack.file,
        });
      } catch (error) {
        const axiosError = error as AxiosError;
        if (axiosError) {
          core.setFailed(
            `Axios Error: ${JSON.stringify(axiosError.response?.data)}`
          );
        }
      }

      core.info("Stack created.");
      core.endGroup();
    }
  } catch (e) {
    core.setFailed(`Action failed with error: ${e}`);
  }
}

run();
