
python -m explainaboard_client.upload_benchmark \
      --email YOUR_EMAIL  \
      --api_key YOUR_API_KEY \
      --system_name MODEL_NAME \
      --system_outputs submissions/* \
      --public \
      --benchmark config_gaokao.json \
      --server main
