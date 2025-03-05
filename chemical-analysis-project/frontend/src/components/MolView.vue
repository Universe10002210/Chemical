<template>
  <div ref="molContainer"></div>
</template>

<script>
export default {
  props: ['smiles'],
  mounted() {
    // 使用MolView嵌入分子结构
    const iframe = document.createElement('iframe');
    iframe.width = '300';
    iframe.height = '300';
    iframe.src = `https://molview.org/?q=${encodeURIComponent(this.smiles)}`;
    this.$refs.molContainer.appendChild(iframe);
  }
};
</script>