#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { VpcStack } from '../lib/vpc-stack';
import { RdsStack } from '../lib/rds-stack';
import { S3Stack } from '../lib/s3-stack';
import { SecretsStack } from '../lib/secrets-stack';
import { EcsStack } from '../lib/ecs-stack';
import { Route53Stack } from '../lib/route53-stack';
import { EcrStack } from '../lib/ecr-stack';

const app = new cdk.App();

const domainName = 'testtranquilla.com';      // your domain
const hostedZoneId = 'ZoneTranquilla'; // your hosted zone id

const vpcStack = new VpcStack(app, 'VpcStack');
const rdsStack = new RdsStack(app, 'RdsStack', { vpcStack });
const s3Stack = new S3Stack(app, 'S3Stack');
const secretsStack = new SecretsStack(app, 'SecretsStack');
const ecrStack = new EcrStack(app, 'EcrStack');

const ecsStack = new EcsStack(app, 'EcsStack', {
  vpcStack,
  rdsStack,
  s3Stack,
  externalApiKeySecret: secretsStack.externalApiKeySecret,
  frontendRepository: ecrStack.frontendRepository,
  backendRepository: ecrStack.backendRepository,
});

// After ECS stack is created, we have an ALB reference:
// Now create Route53 stack and provide the ALB from ECS stack
new Route53Stack(app, 'Route53Stack', {
  domainName,
  alb: ecsStack.alb,
});

// const route53Stack = new Route53Stack(app, 'Route53Stack', {
//   domainName,
//   hostedZoneId,
//   alb: ecsStack.node.tryFindChild('TranquillaALB') as any
// });
