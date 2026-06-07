# Minimal CPU-only ComfyUI image for the text-pipeline integration check.
# No GPU, no models — just enough to register custom nodes and serve the
# /prompt + /history HTTP endpoints.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/comfyui

# Pin to a known-good ComfyUI revision so the build is reproducible.
# Bump as needed.
ARG COMFYUI_REF=master
RUN git clone https://github.com/comfyanonymous/ComfyUI.git . \
    && git checkout "${COMFYUI_REF}"

# CPU-only torch first (avoids pulling the CUDA wheel transitively).
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

EXPOSE 8188

# --cpu avoids GPU init; --listen 0.0.0.0 exposes the server outside the container.
CMD ["python", "main.py", "--cpu", "--listen", "0.0.0.0", "--port", "8188"]
