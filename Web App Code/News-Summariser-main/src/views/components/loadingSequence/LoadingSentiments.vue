<template>
  <div class="lds-heart mx-auto"><div></div></div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.lds-heart {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  transform: rotate(45deg);
  transform-origin: 40px 40px;
}
.lds-heart div {
  width: 28px;
  height: 28px;
  background: #dadada;
  animation: lds-heart 1.2s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
}
.lds-heart div:after,
.lds-heart div:before {
  content: " ";
  position: absolute;
  justify-content: center;
  align-items: center;
  display: block;
  width: 28px;
  height: 28px;
  background: #dadada;
}
.lds-heart div:before {
  left: -24px;
  border-radius: 50% 0 0 50%;
}
.lds-heart div:after {
  top: -24px;
  border-radius: 50% 50% 0 0;
}
@keyframes lds-heart {
  0% {
    transform: scale(0.95);
  }
  5% {
    transform: scale(1.1);
  }
  39% {
    transform: scale(0.85);
  }
  45% {
    transform: scale(1);
  }
  60% {
    transform: scale(0.95);
  }
  100% {
    transform: scale(0.9);
  }
}
</style>
