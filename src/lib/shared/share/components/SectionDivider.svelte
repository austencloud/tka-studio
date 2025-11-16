<!-- SectionDivider.svelte - Decorative section divider with label -->
<script lang="ts">
  let {
    label = "",
  }: {
    label?: string;
  } = $props();
</script>

<div class="divider">
  <span>{label}</span>
</div>

<style>
  .divider {
    position: relative;
    text-align: center;
    margin: 12px 0;
  }

  .divider span {
    display: inline-block;
    padding: 0 18px;
    background: rgba(15, 20, 30, 0.96);
    color: rgba(255, 255, 255, 0.45);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    position: relative;
    z-index: 1;
  }

  .divider::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.15) 20%,
      rgba(255, 255, 255, 0.15) 80%,
      transparent 100%
    );
  }
</style>
