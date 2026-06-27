# Hardware

You can run small open-weight models on many laptops. The experience depends mostly on model size, available memory, and whether you have GPU acceleration.

## CPU

CPU-only inference works and is the easiest place to start. It is usually slower than GPU inference, but it is enough for testing the stack, exploring prompts, and running smaller models.

Good CPU-first choices:

- `phi3:mini`
- `llama3.1:8b` if your machine has enough memory and you can tolerate slower responses

## GPU

A GPU can make local inference much faster. It also makes larger models more practical. Exact setup depends on your operating system, Docker installation, GPU vendor, and drivers.

For the MVP, keep the first run simple:

1. Start the Docker Compose stack.
2. Pull a small model.
3. Confirm everything works.
4. Add GPU-specific configuration later if you need more speed.

## Memory and Disk

Models can be several gigabytes. Keep extra disk space available for downloads and future experiments.

As a practical rule:

- smaller models are easier to run and cheaper to host
- larger models tend to produce better answers but need more resources
- GPU improves speed more than it changes whether the stack works at all

## Beginner-Friendly Advice

Start small. Confirm the workflow works end to end. Then try larger or more specialized models.

If your machine struggles, use `phi3:mini` first:

```bash
./scripts/pull-model.sh phi3:mini
```
