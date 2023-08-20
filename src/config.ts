import * as core from "@actions/core";
import * as fs from "fs";
import mustache from "mustache";
import { Config, PortainerConfig, StackConfig } from "./types";
import error from "./utils";

function parsePortainerConfig(): PortainerConfig {
  return {
    url: new URL(process.env.PORTAINER_URL ?? error("PORTAINER_URL not set")),
    apiKey: process.env.PORTAINER_API_KEY ?? error("PORTAINER_API_KEY not set"),
    endpoint: process.env.APP_ENV ?? error("APP_ENV not set"),
  };
}

function parseStackConfig(): StackConfig {
  if (!process.env.APP_ENV) error("APP_ENV not set");
  const filePath = `docker-compose.${process.env.APP_ENV}.yml.mustache`;
  const repoName = core.getInput("repo-name", { required: true });
  const name = `${repoName}-${process.env.APP_ENV}`;

  const hostnames = JSON.parse(fs.readFileSync("hostnames.json", "utf-8"));
  const hostname = hostnames[process.env.APP_ENV];
  if (!hostname) error(`Hostname for ${process.env.APP_ENV} not found`);

  let file = fs.readFileSync(filePath, "utf-8");

  core.debug(`File before mustache: ${file}`);

  if (filePath.split(".").pop() === "mustache") {
    mustache.escape = JSON.stringify;
    file = mustache.render(file, {
      REPO_NAME: repoName,
      TAG: process.env.APP_ENV,
      HOSTNAME: hostname,
    });
  }

  core.debug(`File after mustache: ${file}`);

  return {
    name,
    file,
  };
}

export function parse(): Config {
  return {
    portainer: parsePortainerConfig(),
    stack: parseStackConfig(),
  };
}
