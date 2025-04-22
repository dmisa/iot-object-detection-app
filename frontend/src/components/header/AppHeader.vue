<template>
    <div class="header">
        <img src="../../assets/logo.svg" alt="Logo" class="logo" />
    </div>
</template>

<script>
export default {
  name: "AppHeader",
  mounted() {
  },
  methods: {
  },
};
</script>

<style scoped>
.header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #111111;
    border-radius: 3rem;
    width: 70%;
    margin: 1rem auto 0 auto;

    @media screen and (min-width: 1024px) {
        width: 90%;
        margin: 1rem auto 0 auto;
    }
}
.logo {
    height: 75px;
    width: auto;
}
</style>