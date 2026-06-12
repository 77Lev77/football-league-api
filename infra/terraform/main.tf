terraform {
  required_version = ">= 1.5.0"

  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.115"
    }
  }
}

provider "yandex" {
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

resource "yandex_vpc_network" "football_network" {
  name = "football-api-network"
}

resource "yandex_vpc_subnet" "football_subnet" {
  name           = "football-api-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.football_network.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

resource "yandex_compute_instance" "football_api_vm" {
  name        = "football-league-api-vm"
  platform_id = "standard-v1"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8kdq6d0p8sij7h5qe3"
      size     = 15
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.football_subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.ssh_public_key_path)}"
    user-data = <<-EOF
      #cloud-config
      package_update: true
      packages:
        - docker.io
      runcmd:
        - systemctl enable docker
        - systemctl start docker
        - docker pull ${var.docker_image}
        - docker run -d --restart unless-stopped --name football-league-api -p 80:8000 ${var.docker_image}
    EOF
  }
}
