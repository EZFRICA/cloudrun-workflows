# cloudrun-workflows
Cloud Run service to execute the workflow
gcloud eventarc triggers create notif-devs \
    --location=us-central1 \
    --destination-run-service=cloudrun-workflows \
    --destination-run-region=us-central1 \
    --event-filters="type=google.cloud.audit.log.v1.written" \
    --event-filters="serviceName=run.googleapis.com" \
    --event-filters="methodName=google.cloud.run.v2.Services.UpdateService" \
    --service-account=event-notif-by-mail@myfreestyle.iam.gserviceaccount.com