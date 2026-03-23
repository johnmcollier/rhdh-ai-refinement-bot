# Deployment

OpenShift manifests for the AI refinement bot. These are intended to be onboarded to [rosa-gitops](https://github.com/redhat-ai-dev/rosa-gitops) — apply them manually for one-off deployments or testing.

## Prerequisites

- `oc` CLI logged in to the target cluster
- A target namespace/project created (`oc project <your-namespace>`)
- The container image built and pushed to an accessible registry (see [Building the image](#building-the-image))

## Building the image

```bash
podman build -t <registry>/<org>/refinement-bot:latest .
podman push <registry>/<org>/refinement-bot:latest
```

Update the `image:` field in `deploy/deployment.yaml` to match your registry path before applying.

## Secret

The service requires an OpenShift Secret named `refinement-bot-secret` with the key `openai_api_key`. Create it before deploying:

```bash
oc create secret generic refinement-bot-secret \
  --from-literal=openai_api_key=<your-openai-api-key>
```

## Applying the manifests

```bash
oc apply -f deploy/deployment.yaml
oc apply -f deploy/service.yaml
oc apply -f deploy/route.yaml
```

Or all at once:

```bash
oc apply -f deploy/
```

## Verifying the deployment

```bash
# Check pod status
oc get pods -l app=refinement-bot

# Get the assigned Route hostname
oc get route refinement-bot -o jsonpath='{.spec.host}'

# Hit the health endpoint
curl https://$(oc get route refinement-bot -o jsonpath='{.spec.host}')/health
```
