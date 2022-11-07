resource "kubernetes_pod" "gmi-netapp" {
  metadata {
    name = "gmi-netapp"
    namespace = "evolved5g"
    labels = {
      app = "gmi-netapp1"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/gmi-netapp:latest"
      name  = "gmi-netapp1"
    }
  }
}

resource "kubernetes_service" "gmi-netapp_service" {
  metadata {
    name = "example-netapp-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.example.metadata.0.labels.app
    }
    port {
      port = 8080
      target_port = 8080
    }
  }
}
