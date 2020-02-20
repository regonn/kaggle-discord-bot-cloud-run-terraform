data "google_container_registry_image" "kaggle_discord_bot" {
  name = "kaggle-discord-bot-for-cloud-run"
  tag = "latest"
}

resource "google_cloud_run_service" "kaggle_discord_bot" {
  name     = "kaggle-discord-bot-service"
  project = var.gcp_project_id
  location = var.gcp_region

  template {
    spec {
      containers {
        image = data.google_container_registry_image.kaggle_discord_bot.image_url
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "cr_invoker_all" {
  service = google_cloud_run_service.kaggle_discord_bot.name
  location = google_cloud_run_service.kaggle_discord_bot.location
  role = "roles/run.invoker"
  member = "allUsers"
}

resource "google_cloud_scheduler_job" "job" {
  name             = "utc0-job"
  description      = "utc0-job"
  schedule         = "0 9 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "320s"

  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_service.kaggle_discord_bot.status[0].url}/post_kaggle_competitions"
  }
}
