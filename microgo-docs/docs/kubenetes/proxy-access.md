# Proxy access

The easiest way to debug a kubenetes pod is to proxy access. 

```
kubectl proxy
```

When proxy access, the kubenetes deploy a static url like `localhost:8001`, then, we access the pod by pod name, for example

```
http://localhost:8001/api/v1/namespaces/default/pods/api-server-deploy-5c476f9477-gx8hw/proxy/
```

We get the pod name by call the `kubectl get pods` command

:::tip

`kube proxy` is a very good command, because it expose all the namespaces without the underlying IPs of the cluster (remember, we investigate the pods in out local machine, while the k8s run in a seperated host - GKE or minikube).

:::